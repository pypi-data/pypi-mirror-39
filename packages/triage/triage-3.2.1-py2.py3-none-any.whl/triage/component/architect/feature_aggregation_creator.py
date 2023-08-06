import logging

from triage.component.collate import (
    Aggregate,
    Categorical,
    Compare,
    SpacetimeAggregation,
)


class FeatureAggregationCreator(object):
    def __init__(
        self, db_engine, features_schema_name, replace=True, feature_start_time=None
    ):
        """Generates aggregate features using collate

        Args:
            db_engine (sqlalchemy.db.engine)
            features_schema_name (string) Name of schema where feature
                tables should be written to
            replace (boolean, optional) Whether or not existing features
                should be replaced
            feature_start_time (string/datetime, optional) point in time before which
                should not be included in features
        """
        self.db_engine = db_engine
        self.features_schema_name = features_schema_name
        self.categorical_cache = {}
        self.feature_start_time = feature_start_time
        self.entity_id_column = "entity_id"

    def _compute_choices(self, choice_query):
        if choice_query not in self.categorical_cache:
            with self.db_engine.begin() as conn:
                self.categorical_cache[choice_query] = [
                    row[0] for row in conn.execute(choice_query)
                ]

            logging.info(
                "Computed list of categoricals: %s for choice query: %s",
                self.categorical_cache[choice_query],
                choice_query,
            )

        return self.categorical_cache[choice_query]

    def _build_choices(self, categorical):
        logging.info(
            "Building categorical choices for column %s, metrics %s",
            categorical["column"],
            categorical["metrics"],
        )
        if "choices" in categorical:
            logging.info("Found list of configured choices: %s", categorical["choices"])
            return categorical["choices"]
        else:
            return self._compute_choices(categorical["choice_query"])

    def _build_categoricals(self, categorical_config, impute_rules):
        # TODO: only include null flag where necessary
        return [
            Categorical(
                col=categorical["column"],
                choices=self._build_choices(categorical),
                function=categorical["metrics"],
                impute_rules=dict(
                    impute_rules,
                    coltype="categorical",
                    **categorical.get("imputation", {})
                ),
                include_null=True,
            )
            for categorical in categorical_config
        ]

    def _build_array_categoricals(self, categorical_config, impute_rules):
        # TODO: only include null flag where necessary
        return [
            Compare(
                col=categorical["column"],
                op="@>",
                choices={
                    choice: "array['{}'::varchar]".format(choice)
                    for choice in self._build_choices(categorical)
                },
                function=categorical["metrics"],
                impute_rules=dict(
                    impute_rules,
                    coltype="array_categorical",
                    **categorical.get("imputation", {})
                ),
                op_in_name=False,
                quote_choices=False,
                include_null=True,
            )
            for categorical in categorical_config
        ]

    def _aggregation(self, aggregation_config, feature_dates, state_table):
        logging.info(
            "Building collate.SpacetimeAggregation for config %s and as_of_dates %s",
            aggregation_config,
            feature_dates,
        )

        # read top-level imputation rules from the aggregation config; we'll allow
        # these to be overridden by imputation rules at the individual feature
        # level as those get parsed as well
        agimp = aggregation_config.get("aggregates_imputation", {})
        catimp = aggregation_config.get("categoricals_imputation", {})
        arrcatimp = aggregation_config.get("array_categoricals_imputation", {})

        aggregates = [
            Aggregate(
                aggregate["quantity"],
                aggregate["metrics"],
                dict(agimp, coltype="aggregate", **aggregate.get("imputation", {})),
            )
            for aggregate in aggregation_config.get("aggregates", [])
        ]
        logging.info("Found %s quantity aggregates", len(aggregates))
        categoricals = self._build_categoricals(
            aggregation_config.get("categoricals", []), catimp
        )
        logging.info("Found %s categorical aggregates", len(categoricals))
        array_categoricals = self._build_array_categoricals(
            aggregation_config.get("array_categoricals", []), arrcatimp
        )
        logging.info("Found %s array categorical aggregates", len(array_categoricals))
        return SpacetimeAggregation(
            aggregates + categoricals + array_categoricals,
            from_obj=aggregation_config["from_obj"],
            intervals=aggregation_config["intervals"],
            groups=aggregation_config["groups"],
            dates=feature_dates,
            state_table=state_table,
            state_group=self.entity_id_column,
            date_column=aggregation_config["knowledge_date_column"],
            output_date_column="as_of_date",
            input_min_date=self.feature_start_time,
            schema=self.features_schema_name,
            prefix=aggregation_config["prefix"],
        )

    def aggregations(self, feature_aggregation_config, feature_dates, state_table):
        """Creates collate.SpacetimeAggregations from the given arguments

        Args:
            feature_aggregation_config (list) all values, except for feature
                date, necessary to instantiate a collate.SpacetimeAggregation
            feature_dates (list) dates to generate features as of
            state_table (string) schema.table_name for state table with all entity/date pairs

        Returns: (list) collate.SpacetimeAggregations
        """
        return [
            self._aggregation(aggregation_config, feature_dates, state_table)
            for aggregation_config in feature_aggregation_config
        ]
