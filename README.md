# Bill Generator

A Python-based bill generator application featuring a Tkinter GUI, SQLite database integration, and PDF export capabilities. Designed for efficient bill creation and management.

## Features

- **User-Friendly GUI**: Intuitive Tkinter interface for easy bill generation
- **Database Storage**: SQLite database for persistent data storage
- **Database Management GUI**: Dedicated interface for viewing, editing, and managing database records
- **PDF Export**: Generate professional PDF bills
- **Modular Design**: Clean code structure following Python best practices

## Requirements

- Python 3.8 or higher
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository and navigate to the project directory.

2. Create a virtual environment and activate it:

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   ```

3. Install dependencies and the package in editable mode:

   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

## Usage

Run the GUI application:

```bash
bill-generator
# or
python -m bill_generator.app_main
```

### Database GUI

To access the database management interface for viewing, editing, and managing records:

```bash
python -m bill_generator.db_main
```

## Database

The application uses an SQLite database stored at `data/data.db`. The database schema and initial setup are handled by scripts in the `data/scripts/` directory. Use the Database GUI to directly view, edit, and manage database records.

## Project Structure

- `src/bill_generator/`: Main application code
- `data/`: Database and related scripts
- `requirements.txt`: Python dependencies

## Contributing

Contributions are welcome! Please ensure code follows the project's style and includes appropriate tests.

## License

This project is licensed under the MIT License.