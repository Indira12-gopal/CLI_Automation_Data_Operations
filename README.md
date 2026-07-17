# CLI Automation Data Operations

A Python Command-Line Interface (CLI) tool for performing common data processing operations on CSV and Excel files. This project was developed as part of an internship project to automate data cleaning, transformation, summarization, merging, and exporting of datasets.

---

## Features

- Read CSV and Excel files
- Display first N rows of a dataset
- View all column names and data types
- Rename dataset columns
- Remove or fill missing values
- Clean datasets (remove duplicates, trim spaces, format dates)
- Filter rows based on conditions
- Generate dataset summary
- Merge two datasets using a common key
- Export datasets to CSV or Excel
- Action Audit Logging

---

## Technologies Used

- Python 3.x
- Pandas
- Typer
- OpenPyXL
- Logging Module

---

## Project Structure

```
CLI_Automation_Data_Operations/
│
├── data/
├── output/
├── logs/
│   └── app.log
├── main.py
├── README.md
├── requirements.txt
├── commands.txt
└── .gitignore
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/yourusername/CLI_Automation_Data_Operations.git
```

Move into the project directory

```bash
cd CLI_Automation_Data_Operations
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

### Read Dataset

```bash
python main.py read data/sample.csv
```

### Display First Rows

```bash
python main.py head data/sample.csv --n 5
```

### Show Columns

```bash
python main.py columns data/sample.csv
```

### Rename Column

```bash
python main.py rename-columns data/sample.csv --old Name --new Employee_Name
```

### Remove Missing Values

```bash
python main.py drop-null data/sample.csv --method drop
```

### Fill Missing Values

```bash
python main.py drop-null data/sample.csv --method fill
```

### Clean Dataset

```bash
python main.py clean data/sample.csv
```

### Filter Dataset

```bash
python main.py filter data/sample.csv --column Category --value Cement
```

### Dataset Summary

```bash
python main.py summarize data/sample.csv
```

### Merge Datasets

```bash
python main.py merge data/file1.csv data/file2.csv --key Purchase_ID
```

### Export Dataset

```bash
python main.py export data/sample.csv --output output/final.csv
```

---

## Logging

Every command executed is recorded in:

```
logs/app.log
```

The log contains:

- Command name
- File used
- Date and time
- Success or failure status

---

## Future Improvements

- Automatic data type detection
- Data visualization
- Cleaning score
- Command chaining
- Intelligent missing value suggestions

---

## Author

**Indira Bhattacharjee**

Internship Project – CLI Automation Data Operations