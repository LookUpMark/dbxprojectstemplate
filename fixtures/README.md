# fixtures/

Sample datasets for unit tests (`tests/`).

## Conventions

- Synthetic or public data only: **never** real or sensitive data.
- Small: fixtures must keep tests fast (a few rows of CSV/JSON/Parquet
  is enough).
- Name files explicitly after the test that uses them
  (e.g. `sample_rows.csv` for `tests/test_sample_data.py`).
- If larger datasets are needed, generate them on the fly in tests with
  libraries like `faker` or factory functions instead of committing binaries.
