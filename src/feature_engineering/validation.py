from great_expectations.core import ExpectationSuite, ExpectationConfiguration

def build_expectation_suite(expec_name) -> ExpectationSuite:

    expectation_suite_energy_consumption = ExpectationSuite(
        expectation_suite_name=expec_name
    )

    # Columns.
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_table_columns_to_match_ordered_list",
            kwargs={
                "column_list": [
                    "datetime_utc",
                    "area",
                    "consumer_type",
                    "energy_consumption",
                ]
            },
        )
    )
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_table_column_count_to_equal", kwargs={"value": 4}
        )
    )

    # Datetime UTC
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_not_be_null",
            kwargs={"column": "datetime_utc"},
        )
    )

    # Area
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_distinct_values_to_be_in_set",
            kwargs={"column": "area", "value_set": (0, 1, 2)},
        )
    )
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_of_type",
            kwargs={"column": "area", "type_": "int8"},
        )
    )

    # Consumer type
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_distinct_values_to_be_in_set",
            kwargs={
                "column": "consumer_type",
                "value_set": (
                    111,
                    112,
                    119,
                    121,
                    122,
                    123,
                    130,
                    211,
                    212,
                    215,
                    220,
                    310,
                    320,
                    330,
                    340,
                    350,
                    360,
                    370,
                    381,
                    382,
                    390,
                    410,
                    421,
                    422,
                    431,
                    432,
                    433,
                    441,
                    442,
                    443,
                    444,
                    445,
                    446,
                    447,
                    450,
                    461,
                    462,
                    999,
                ),
            },
        )
    )
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_of_type",
            kwargs={"column": "consumer_type", "type_": "int32"},
        )
    )

    # Energy consumption
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_min_to_be_between",
            kwargs={
                "column": "energy_consumption",
                "min_value": 0,
                "strict_min": False,
            },
        )
    )
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_of_type",
            kwargs={"column": "energy_consumption", "type_": "float64"},
        )
    )
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_not_be_null",
            kwargs={"column": "energy_consumption"},
        )
    )

    return expectation_suite_energy_consumption

def build_expectation_feature_1(expec_name) -> ExpectationSuite:
    expectation_suite_energy_consumption = ExpectationSuite(
        expectation_suite_name=expec_name
    )

    # Columns.
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_table_columns_to_match_ordered_list",
            kwargs={
                "column_list": [
                    "datetime_utc",
                    "area",
                    "consumer_type",
                    "energy_consumption",
                    "hour",
                    "avg_energy_per_area",
                    "total_energy_per_consumer_type"
                ]
            },
        )
    )
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_table_column_count_to_equal", kwargs={"value": 7}
        )
    )

    # Datetime UTC
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_not_be_null",
            kwargs={"column": "datetime_utc"},
        )
    )

    # Area
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_distinct_values_to_be_in_set",
            kwargs={"column": "area", "value_set": (0, 1, 2)},
        )
    )
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_of_type",
            kwargs={"column": "area", "type_": "int8"},
        )
    )

    # Consumer type
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_distinct_values_to_be_in_set",
            kwargs={
                "column": "consumer_type",
                "value_set": (
                    111,
                    112,
                    119,
                    121,
                    122,
                    123,
                    130,
                    211,
                    212,
                    215,
                    220,
                    310,
                    320,
                    330,
                    340,
                    350,
                    360,
                    370,
                    381,
                    382,
                    390,
                    410,
                    421,
                    422,
                    431,
                    432,
                    433,
                    441,
                    442,
                    443,
                    444,
                    445,
                    446,
                    447,
                    450,
                    461,
                    462,
                    999,
                ),
            },
        )
    )
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_of_type",
            kwargs={"column": "consumer_type", "type_": "int32"},
        )
    )

    # Energy consumption
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_min_to_be_between",
            kwargs={
                "column": "energy_consumption",
                "min_value": 0,
                "strict_min": False,
            },
        )
    )
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_of_type",
            kwargs={"column": "energy_consumption", "type_": "float64"},
        )
    )
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_not_be_null",
            kwargs={"column": "energy_consumption"},
        )
    )

    # Hour
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_min_to_be_between",
            kwargs={
                "column": "hour",
                "min_value": 0,
                "strict_min": True,
            },
        )
    )
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_max_to_be_between",
            kwargs={
                "column": "hour",
                "max_value": 23,
                "strict_max": True,
            },
        )
    )

    # Average Energy per Area
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_min_to_be_between",
            kwargs={
                "column": "avg_energy_per_area",
                "min_value": 0,
                "strict_min": False,
            },
        )
    )
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_of_type",
            kwargs={"column": "avg_energy_per_area", "type_": "float64"},
        )
    )
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_not_be_null",
            kwargs={"column": "avg_energy_per_area"},
        )
    )

    # Total Energy per Consumer Type
    # expectation_suite_energy_consumption.add_expectation(
    #     ExpectationConfiguration(
    #         expectation_type="expect_column_min_to_be_between",
    #         kwargs={
    #             "column": "total_energy_per_consumer_type",
    #             "min_value": 0,
    #             "strict_min": False,
    #         },
    #     )
    # )
    # expectation_suite_energy_consumption.add_expectation(
    #     ExpectationConfiguration(
    #         expectation_type="expect_column_values_to_be_of_type",
    #         kwargs={"column": "total_energy_per_consumer_type", "type_": "float64"},
    #     )
    # )
    # expectation_suite_energy_consumption.add_expectation(
    #     ExpectationConfiguration(
    #         expectation_type="expect_column_values_to_not_be_null",
    #         kwargs={"column": "total_energy_per_consumer_type"},
    #     )
    # )

    return expectation_suite_energy_consumption