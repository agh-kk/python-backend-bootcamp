import csv
from pathlib import Path
from typing import List, Dict, Any


# --- Custom Exception (Reuse from Day 5, for quality) ---
class FileProcessingError(Exception):
    """Custom exception for errors during file I/O operations."""

    pass


# 1. Processing Logic
def calculate_totals(data: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Calculates the TotalCost for each record and converts types."""
    processed_data = []
    for row in data:
        try:
            # Convert string inputs to proper types
            quantity = int(row["Quantity"])
            price = float(row["Price"])

            # Create a new dictionary for the processed record
            new_row = {
                "Item": row["Item"],
                "Quantity": quantity,
                "Price": price,
                "TotalCost": round(quantity * price, 2),  # Calculate the new field
            }
            processed_data.append(new_row)
        except (ValueError, KeyError) as e:
            # Quality: Skip bad data, but log the issue instead of crashing
            print(f"Skipping malformed row: {row}. Error: {e}")
            continue
    return processed_data


# 2. File I/O Logic
def process_sales_data(input_filename: str, output_filename: str):
    """Reads data from CSV, processes it, and writes to a new CSV."""

    # Quality: Use pathlib for robust path handling
    input_path = Path(input_filename)
    output_path = Path(output_filename)

    # 2a. Read the input file
    data = []
    try:
        with input_path.open("r", newline="", encoding="utf-8") as infile:
            # csv.DictReader maps column headers to dictionary keys
            reader = csv.DictReader(infile)
            data = list(reader)
    except FileNotFoundError:
        raise FileProcessingError(f"Input file not found: {input_filename}")

    # Process the data
    processed_data = calculate_totals(data)

    # 2b. Write the output file
    if not processed_data:
        print("No valid data to write.")
        return

    # Determine the fieldnames for the output (ensures order)
    fieldnames = list(processed_data[0].keys())

    try:
        # Use 'w' for write. newline='' is necessary for cross-platform CSV handling.
        with output_path.open("w", newline="", encoding="utf-8") as outfile:
            # csv.DictWriter maps dictionaries back to CSV rows
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)

            writer.writeheader()  # Writes the column names
            writer.writerows(processed_data)  # Writes all rows

        print(
            f"\nSUCCESS: Processed {len(data)} records. Output written to {output_filename}"
        )
    except IOError as e:
        raise FileProcessingError(f"Error writing to output file: {e}")


if __name__ == "__main__":
    INPUT_FILE = "input_sales.csv"
    OUTPUT_FILE = "output_sales_summary.csv"

    try:
        process_sales_data(INPUT_FILE, OUTPUT_FILE)
    except FileProcessingError as e:
        print(f"FATAL ERROR: {e}")
