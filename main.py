import typer
import pandas as pd
import logging
from pathlib import Path

app = typer.Typer()

# Create logs folder if it doesn't exist
Path("logs").mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def load_file(file_path: str, sheet_name: str = "Sheet1"):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File '{file_path}' not found.")

    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)

    elif path.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(path, sheet_name=sheet_name)

    else:
        raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")
    
@app.command()
def read(file_path: str):
    """
    Read a dataset and display its basic information.
    """
    try:
        df = load_file(file_path)

        print("\nDataset Shape:")
        print(df.shape)

        print("\nColumn Names:")
        print(df.columns.tolist())

        print("\nData Types:")
        print(df.dtypes)
        logging.info(f"READ command executed successfully on {file_path}")

    except Exception as e:
        logging.error(f"READ command failed: {e}")
        print(f"Error: {e}")

@app.command()
def head(file_path: str, n: int = 5):
    """
    Display the first N rows of the dataset.
    """
    try:
        df = load_file(file_path)

        print(f"\nFirst {n} rows of the dataset:\n")
        print(df.head(n))
        logging.info(f"HEAD command executed on {file_path} | Rows={n}")

    except Exception as e:
        logging.error(f"HEAD command failed: {e}")
        print(f"Error: {e}")

@app.command()
def columns(file_path: str, show_types: bool = False):
    """
    Display all column names.
    Use --show-types to display data types as well.
    """
    try:
        df = load_file(file_path)

        if show_types:
            print("\nColumns with Data Types:\n")
            for col in df.columns:
                print(f"{col} --> {df[col].dtype}")
        else:
            print("\nColumn Names:\n")
            for i, col in enumerate(df.columns, start=1):
                print(f"{i}. {col}")
        logging.info(f"COLUMNS command executed on {file_path}")

    except Exception as e:
        logging.error(f"COLUMNS command failed: {e}")
        print(f"Error: {e}")

@app.command()
def rename_columns(
    file_path: str,
    old: str = typer.Option(..., "--old", help="Old column name"),
    new: str = typer.Option(..., "--new", help="New column name")
):
    """
    Rename a column in the dataset.
    """
    try:
        df = load_file(file_path)

        if old not in df.columns:
            print(f"Column '{old}' not found.")
            return

        df.rename(columns={old: new}, inplace=True)

        print("\nColumn renamed successfully!\n")
        print(df.columns.tolist())
        logging.info(f"RENAME command executed on {file_path}")

    except Exception as e:
        logging.error(f"RENAME COLUMNS command failed: {e}")
        print(f"Error: {e}")

@app.command()
def drop_null(
    file_path: str,
    method: str = typer.Option(
        "drop",
        "--method",
        help="Choose 'drop' or 'fill'"
    )
):
    """
    Remove or fill missing values.
    """
    try:
        df = load_file(file_path)

        print(f"\nMissing values before:\n")
        print(df.isnull().sum())

        if method.lower() == "drop":
            df = df.dropna()

        elif method.lower() == "fill":

            for col in df.columns:

                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].median())

                else:
                    mode = df[col].mode()

                    if not mode.empty:
                        df[col] = df[col].fillna(mode[0])

        else:
            print("Invalid method. Use 'drop' or 'fill'.")
            return

        print("\nMissing values after:\n")
        print(df.isnull().sum())
        logging.info(f"DROP-NULL command executed on {file_path} | Method={method}")

    except Exception as e:
        logging.error(f"DROP-NULL command failed: {e}")
        print(f"Error: {e}")

@app.command()
def clean(file_path: str):
    """
    Perform complete data cleaning.
    """
    try:
        df = load_file(file_path)

        # Clean column names
        df.columns = df.columns.str.strip()

        # Clean text columns
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].astype(str).str.strip()

        # Remove duplicates
        before = len(df)
        df = df.drop_duplicates()
        duplicates_removed = before - len(df)

        # Fill missing values
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].median())
            else:
                mode = df[col].mode()
                if not mode.empty:
                    df[col] = df[col].fillna(mode[0])

        # Format date columns
        for col in df.columns:
            if "date" in col.lower():
                df[col] = pd.to_datetime(df[col], errors="coerce")
                df[col] = df[col].dt.strftime("%Y-%m-%d")

        print("\nDataset cleaned successfully!")
        print(f"Duplicates Removed: {duplicates_removed}")

        print("\nMissing Values After Cleaning:")
        print(df.isnull().sum())
        logging.info(f"CLEAN command executed on {file_path}")

    except Exception as e:
        logging.error(f"CLEAN command failed: {e}")
        print(f"Error: {e}")

@app.command()
def filter(
    file_path: str,
    column: str = typer.Option(..., "--column", help="Column name"),
    value: str = typer.Option(..., "--value", help="Value to filter")
):
    """
    Filter rows based on a column value.
    """
    try:
        df = load_file(file_path)

        # Check if column exists
        if column not in df.columns:
            print(f"Error: Column '{column}' not found.")
            return

        # Filter rows (case-insensitive)
        filtered_df = df[
            df[column].astype(str).str.lower()
            == value.lower()
        ]

        if filtered_df.empty:
            print("\nNo matching records found.")
        else:
            print("\nFiltered Data:\n")
            print(filtered_df)

            print(f"\nTotal Records Found: {len(filtered_df)}")
        logging.info(
    f"FILTER command | File={file_path} | Column={column} | Value={value}"
)

    except Exception as e:
        logging.error(f"FILTER command failed: {e}")
        print(f"Error: {e}")

@app.command()
def summarize(file_path: str):
    """
    Display a summary of the dataset.
    """
    try:
        df = load_file(file_path)

        print("\n========== DATASET SUMMARY ==========\n")

        # Shape
        print(f"Total Rows    : {df.shape[0]}")
        print(f"Total Columns : {df.shape[1]}")

        # Missing Values
        print("\nMissing Values:")
        print(df.isnull().sum())

        # Duplicate Rows
        print(f"\nDuplicate Rows: {df.duplicated().sum()}")

        # Data Types
        print("\nData Types:")
        print(df.dtypes)

        # Statistical Summary
        print("\nStatistical Summary:")
        print(df.describe(include="all"))
        print("\nMemory Usage:")
        print(f"{df.memory_usage(deep=True).sum()} bytes")
        logging.info(f"SUMMARIZE command executed on {file_path}")

    except Exception as e:
        logging.error(f"SUMMARIZE command failed: {e}")
        print(f"Error: {e}")

@app.command()
def merge(
    file1: str,
    file2: str,
    key: str = typer.Option(..., "--key", help="Common column to merge on"),
    how: str = typer.Option(
        "inner",
        "--how",
        help="Merge type: inner, left, right, outer"
    )
):
    """
    Merge two datasets using a common key.
    """
    try:
        df1 = load_file(file1)
        df2 = load_file(file2)

        # Check if key exists
        if key not in df1.columns:
            print(f"Error: '{key}' not found in first dataset.")
            return

        if key not in df2.columns:
            print(f"Error: '{key}' not found in second dataset.")
            return

        merged_df = pd.merge(df1, df2, on=key, how=how)

        print("\nDatasets merged successfully!")

        print(f"\nMerged Shape: {merged_df.shape}")

        print("\nFirst 5 Rows:\n")
        print(merged_df.head())
        logging.info(
    f"MERGE command | {file1} + {file2} | Key={key} | Type={how}"
)

    except Exception as e:
        logging.error(f"MERGE command failed: {e}")
        print(f"Error: {e}")

@app.command()
def export(
    file_path: str,
    output: str = typer.Option(..., "--output", help="Output file path"),
):
    """
    Export the dataset to CSV or Excel.
    """
    try:
        df = load_file(file_path)

        output_path = Path(output)

        # Create output folder if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if output_path.suffix.lower() == ".csv":
            df.to_csv(output_path, index=False)

        elif output_path.suffix.lower() in [".xlsx", ".xls"]:
            df.to_excel(output_path, index=False)

        else:
            print("Unsupported file format. Use .csv or .xlsx")
            return

        print("\nDataset exported successfully!")
        print(f"Saved to: {output_path}")
        logging.info(
    f"EXPORT command | {file_path} -> {output}"
)

    except Exception as e:
        logging.error(f"EXPORT command failed: {e}")
        print(f"Error: {e}")
if __name__ == "__main__":
    app()