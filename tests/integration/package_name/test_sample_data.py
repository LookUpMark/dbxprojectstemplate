"""Integration test: sample data functions against a live Spark session."""

from package_name import sample_data


def test_find_all_sample_data(spark):
    results = sample_data.find_all_sample_data(spark)
    assert results.count() > 5
