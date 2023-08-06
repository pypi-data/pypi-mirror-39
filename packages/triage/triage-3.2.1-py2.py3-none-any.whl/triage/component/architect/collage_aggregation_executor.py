import logging
from collections import OrderedDict
import sqlalchemy


class CollateAggregationExecutor(object):
    def generate_all_table_tasks(self, aggregations, task_type):
        """Generates SQL commands for creating, populating, and indexing
        feature group tables

        Args:
            aggregations (list) collate.SpacetimeAggregation objects
            type (str) either 'aggregation' or 'imputation'

        Returns: (dict) keys are group table names, values are themselves dicts,
            each with keys for different stages of table creation (prepare, inserts, finalize)
            and with values being lists of SQL commands
        """

        logging.debug("---------------------")

        # pick the method to use for generating tasks depending on whether we're
        # building the aggregations or imputations
        if task_type == "aggregation":
            task_generator = self._generate_agg_table_tasks_for
            logging.debug("---------FEATURE GENERATION------------")
        elif task_type == "imputation":
            task_generator = self._generate_imp_table_tasks_for
            logging.debug("---------FEATURE IMPUTATION------------")
        else:
            raise ValueError("Table task type must be aggregation or imputation")

        logging.debug("---------------------")

        table_tasks = OrderedDict()
        for aggregation in aggregations:
            table_tasks.update(task_generator(aggregation))
        logging.info("Created %s tables", len(table_tasks.keys()))
        return table_tasks

    def create_all_tables(self, feature_aggregations):
        """Create all feature tables.

        First builds the aggregation tables, and then performs
        imputation on any null values, (requiring a two-step process to
        determine which columns contain nulls after the initial
        aggregation tables are built).

        Args:
            feature_aggregation_config (list) all values, except for
                feature date, necessary to instantiate a
                `collate.SpacetimeAggregation`
            feature_dates (list) dates to generate features as of
            state_table (string) schema.table_name for state table with
                all entity/date pairs

        Returns: (list) table names

        """
        # first, generate and run table tasks for aggregations
        table_tasks_aggregate = self.generate_all_table_tasks(
            feature_aggregations, task_type="aggregation"
        )
        self.process_table_tasks(table_tasks_aggregate)

        # second, perform the imputations (this will query the tables
        # constructed above to identify features containing nulls)
        table_tasks_impute = self.generate_all_table_tasks(feature_aggregations, task_type="imputation")
        impute_keys = self.process_table_tasks(table_tasks_impute)

        # double-check that the imputation worked and no nulls remain
        # in the data:
        nullcols = []
        with self.db_engine.begin() as conn:
            for agg in feature_aggregations:
                results = conn.execute(agg.find_nulls(imputed=True))
                null_counts = results.first().items()
                nullcols += [col for (col, val) in null_counts if val > 0]

        if len(nullcols) > 0:
            raise ValueError(
                "Imputation failed for {} columns. Null values remain in: {}".format(
                    len(nullcols), nullcols
                )
            )

        return impute_keys

    def process_table_task(self, task):
        self.run_commands(task.get("prepare", []))
        self.run_commands(task.get("inserts", []))
        self.run_commands(task.get("finalize", []))

    def process_table_tasks(self, table_tasks):
        for table_name, task in table_tasks.items():
            logging.info("Running feature table queries for %s", table_name)
            self.process_table_task(task)
        return table_tasks.keys()

    def _explain_selects(self, aggregations):
        with self.db_engine.begin() as conn:
            for aggregation in aggregations:
                for selectlist in aggregation.get_selects().values():
                    for select in selectlist:
                        query = "explain " + str(select)
                        results = list(conn.execute(query))
                        logging.debug(str(select))
                        logging.debug(results)

    def _clean_table_name(self, table_name):
        # remove the schema and quotes from the name
        return table_name.split(".")[1].replace('"', "")

    def _table_exists(self, table_name):
        try:
            with self.db_engine.begin() as conn:
                conn.execute(
                    "select 1 from {}.{} limit 1".format(
                        self.features_schema_name, table_name
                    )
                ).first()
        except sqlalchemy.exc.ProgrammingError:
            return False
        else:
            return True

    def run_commands(self, command_list):
        with self.db_engine.begin() as conn:
            for command in command_list:
                logging.debug("Executing feature generation query: %s", command)
                conn.execute(command)

    def _aggregation_index_query(self, aggregation, imputed=False):
        return "CREATE INDEX ON {} ({}, {})".format(
            aggregation.get_table_name(imputed=imputed),
            self.entity_id_column,
            aggregation.output_date_column,
        )

    def _aggregation_index_columns(self, aggregation):
        return sorted(
            [group for group in aggregation.groups.keys()]
            + [aggregation.output_date_column]
        )

    def index_column_lookup(self, aggregations, imputed=True):
        return dict(
            (
                self._clean_table_name(aggregation.get_table_name(imputed=imputed)),
                self._aggregation_index_columns(aggregation),
            )
            for aggregation in aggregations
        )

    def _generate_agg_table_tasks_for(self, aggregation):
        """Generates SQL commands for preparing, populating, and finalizing
        each feature group table in the given aggregation

        Args:
            aggregation (collate.SpacetimeAggregation)

        Returns: (dict) of structure {
            'prepare': list of commands to prepare table for population
            'inserts': list of commands to populate table
            'finalize': list of commands to finalize table after population
        }
        """
        create_schema = aggregation.get_create_schema()
        creates = aggregation.get_creates()
        drops = aggregation.get_drops()
        indexes = aggregation.get_indexes()
        inserts = aggregation.get_inserts()

        if create_schema is not None:
            with self.db_engine.begin() as conn:
                conn.execute(create_schema)

        table_tasks = OrderedDict()
        for group in aggregation.groups:
            group_table = self._clean_table_name(
                aggregation.get_table_name(group=group)
            )
            imputed_table = self._clean_table_name(
                aggregation.get_table_name(imputed=True)
            )
            if self.replace or (
                not self._table_exists(group_table)
                and not self._table_exists(imputed_table)
            ):
                table_tasks[group_table] = {
                    "prepare": [drops[group], creates[group]],
                    "inserts": inserts[group],
                    "finalize": [indexes[group]],
                }
                logging.info("Created table tasks for %s", group_table)
            else:
                logging.info("Skipping feature table creation for %s", group_table)
                table_tasks[group_table] = {}
        logging.info("Created table tasks for aggregation")
        if self.replace or (
            not self._table_exists(self._clean_table_name(aggregation.get_table_name()))
            and not self._table_exists(
                self._clean_table_name(aggregation.get_table_name(imputed=True))
            )
        ):
            table_tasks[self._clean_table_name(aggregation.get_table_name())] = {
                "prepare": [aggregation.get_drop(), aggregation.get_create()],
                "inserts": [],
                "finalize": [self._aggregation_index_query(aggregation)],
            }
        else:
            table_tasks[self._clean_table_name(aggregation.get_table_name())] = {}

        return table_tasks

    def _generate_imp_table_tasks_for(self, aggregation, drop_preagg=True):
        """Generate SQL statements for preparing, populating, and
        finalizing imputations, for each feature group table in the
        given aggregation.

        Requires the existance of the underlying feature and aggregation
        tables defined in `_generate_agg_table_tasks_for()`.

        Args:
            aggregation (collate.SpacetimeAggregation)
            drop_preagg: boolean to specify dropping pre-imputation
                tables

        Returns: (dict) of structure {
                'prepare': list of commands to prepare table for population
                'inserts': list of commands to populate table
                'finalize': list of commands to finalize table after population
            }

        """
        table_tasks = OrderedDict()
        imp_tbl_name = self._clean_table_name(aggregation.get_table_name(imputed=True))

        if not self.replace and self._table_exists(imp_tbl_name):
            logging.info("Skipping imputation table creation for %s", imp_tbl_name)
            table_tasks[imp_tbl_name] = {}
            return table_tasks

        if not aggregation.state_table:
            logging.warning(
                "No state table defined in aggregation, cannot create imputation table for %s",
                imp_tbl_name,
            )
            table_tasks[imp_tbl_name] = {}
            return table_tasks

        if not table_exists(aggregation.state_table, self.db_engine):
            logging.warning(
                "State table %s does not exist, cannot create imputation table for %s",
                aggregation.state_table,
                imp_tbl_name,
            )
            table_tasks[imp_tbl_name] = {}
            return table_tasks

        # excute query to find columns with null values and create lists of columns
        # that do and do not need imputation when creating the imputation table
        with self.db_engine.begin() as conn:
            results = conn.execute(aggregation.find_nulls())
            null_counts = results.first().items()
        impute_cols = [col for (col, val) in null_counts if val > 0]
        nonimpute_cols = [col for (col, val) in null_counts if val == 0]

        # table tasks for imputed aggregation table, most of the work is done here
        # by collate's get_impute_create()
        table_tasks[imp_tbl_name] = {
            "prepare": [
                aggregation.get_drop(imputed=True),
                aggregation.get_impute_create(
                    impute_cols=impute_cols, nonimpute_cols=nonimpute_cols
                ),
            ],
            "inserts": [],
            "finalize": [self._aggregation_index_query(aggregation, imputed=True)],
        }
        logging.info("Created table tasks for imputation: %s", imp_tbl_name)

        # do some cleanup:
        # drop the group-level and aggregation tables, just leaving the
        # imputation table if drop_preagg=True
        if drop_preagg:
            drops = aggregation.get_drops()
            table_tasks[imp_tbl_name]["finalize"] += list(drops.values()) + [
                aggregation.get_drop()
            ]
            logging.info("Added drop table cleanup tasks: %s", imp_tbl_name)

        return table_tasks
