import csv
import json

# File path for CSV
csv_file = r'D:\My Projects\Panding Tasks\Azure Kafka\2024-10-08 1_45pm.csv'  # Replace with your actual CSV file path

# Function to generate SQL schema for CSV data
def generate_sql_schema_csv(csv_file, table_name="CSVTable"):
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Read the header row (column names)

    # Create SQL CREATE TABLE statement dynamically
    sql_columns = []
    for header in headers:
        sql_columns.append(f'"{header}" VARCHAR(255)')  # Assuming all columns are VARCHAR for simplicity

    sql_create_table = f'CREATE TABLE {table_name} (\n' + ',\n'.join(sql_columns) + '\n);'
    
    return sql_create_table

# Function to generate SQL schema for live generated data
def generate_sql_schema_live(data_example, table_name="LiveTable"):
    # Extract column names (keys) from live data dictionary
    sql_columns = []
    for key in data_example.keys():
        sql_columns.append(f'"{key}" VARCHAR(255)')  # Assuming all columns are VARCHAR for simplicity

    sql_create_table = f'CREATE TABLE {table_name} (\n' + ',\n'.join(sql_columns) + '\n);'
    
    return sql_create_table

# Example of live generated data
def generate_data():
    data = {
        "id": 1,
        "value": 99.99,
        "timestamp": "2024-10-19T12:34:56.789123"
    }
    return data

# Main program to generate schemas for both CSV and live data
def main():
    # Generate SQL schema for CSV data
    csv_sql_schema = generate_sql_schema_csv(csv_file, "GeneratedCSVTable")
    print("SQL Schema for CSV Data:")
    print(csv_sql_schema)

    # Generate SQL schema for live generated data
    live_data_example = generate_data()
    live_sql_schema = generate_sql_schema_live(live_data_example, "GeneratedLiveTable")
    print("\nSQL Schema for Live Data:")
    print(live_sql_schema)

if __name__ == "__main__":
    main()
