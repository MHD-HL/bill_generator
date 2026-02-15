# Bill Generator (Sunway Solar)

Simple invoice generator with a Tkinter GUI, SQLite DB, and PDF export.

## Quick start

1. Create a virtual environment and activate it.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

2. Install dependencies and the package in editable mode:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .
```

3. Run the GUI:

```bash
bill-generator
# or
python -m bill_generator.app_main
```

## Tests

Run tests with:

```bash
pytest
```

## Notes

- Database file is under `Data/sunway.db`.
- Package follows the `src/` layout; code is in `src/bill_generator`.