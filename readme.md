# Real-Time Data Streaming Implementation on Azure

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Project Overview](#project-overview)
- [Architecture Diagram](#architecture-diagram)
- [Setup Instructions](#setup-instructions)
  - [Azure Setup](#azure-setup)
    - [1. Create a Resource Group](#1-create-a-resource-group)
    - [2. Create an Event Hubs Namespace and Event Hub](#2-create-an-event-hubs-namespace-and-event-hub)
    - [3. Get the Event Hub Connection String](#3-get-the-event-hub-connection-string)
    - [4. Create an Azure SQL Database](#4-create-an-azure-sql-database)
    - [5. Configure the SQL Database Firewall](#5-configure-the-sql-database-firewall)
  - [Local Machine Setup](#local-machine-setup)
    - [1. Install Python and Required Libraries](#1-install-python-and-required-libraries)
    - [2. Clone the Repository](#2-clone-the-repository)
    - [3. Update Configuration Files](#3-update-configuration-files)
- [Running the Project](#running-the-project)
  - [1. Running the Data Producer](#1-running-the-data-producer)
  - [2. Running the Data Consumer](#2-running-the-data-consumer)
  - [3. Verifying Data in SQL Database](#3-verifying-data-in-sql-database)
- [Code Files](#code-files)
  - [data_producer.py](#data_producerpy)
  - [data_consumer.py](#data_consumerpy)
  - [schema_creator.py](#schema_creatorpy)
- [Conclusion](#conclusion)
- [Acknowledgments](#acknowledgments)

---

## Introduction

This project demonstrates how to build a data pipeline using Azure services. It covers data production, ingestion, storage, processing, and visualization using Azure Event Hubs, Azure SQL Database, and Python.

## Prerequisites

- An **Azure account** with sufficient permissions.
- **Python 3.x** installed on your local machine.
- Basic knowledge of Python programming.
- Familiarity with Azure services (Event Hubs, SQL Database).
- **SQL Server Management Studio (SSMS)** or **Azure Data Studio** (optional, for verifying data).

## Project Overview

The data pipeline consists of the following components:

1. **Data Producer**: A Python script that generates data (both from a CSV file and live generated data) and sends it to Azure Event Hubs.

2. **Message Queue**: Azure Event Hubs acts as a message queue to ingest and process streaming data.

3. **Serverless SQL Database**: An Azure SQL Database (serverless tier) to store the data consumed from Event Hubs.

4. **Data Consumer**: A Python script that reads data from Event Hubs and inserts it into the SQL Database.

5. **Schema Creator**: A Python script to generate SQL table schemas based on the data structure.

## Architecture Diagram

![Architecture Diagram](images/architecture_diagram.png)

*(Include an image named `architecture_diagram.png` in the `images` directory of your repository.)*

## Setup Instructions

### Azure Setup

#### 1. Create a Resource Group

1. Log into the [Azure Portal](https://portal.azure.com/).
2. Search for **Resource Groups** in the search bar.
3. Click **Create**.
4. Enter the following details:
   - **Subscription**: Select your subscription.
   - **Resource group**: `DataPipelineRG`
   - **Region**: Choose a region close to you (e.g., `East US`).
5. Click **Review + create** and then **Create**.

#### 2. Create an Event Hubs Namespace and Event Hub

1. In the Azure Portal, search for **Event Hubs**.
2. Click **Create**.
3. Fill in the following details:
   - **Subscription**: Your subscription.
   - **Resource group**: `DataPipelineRG`.
   - **Namespace name**: A unique name (e.g., `datapipeline-namespace`).
   - **Location**: Same as your resource group.
   - **Pricing tier**: **Basic**.
4. Click **Review + create** and then **Create**.
5. After the namespace is created, navigate to it.
6. Under **Entities**, select **Event Hubs**.
7. Click **+ Event Hub** to create a new Event Hub.
8. Enter the **Name**: `samplehub`.
9. Click **Create**.

#### 3. Get the Event Hub Connection String

1. In your Event Hubs namespace, go to **Shared access policies** under **Settings**.
2. Click on **RootManageSharedAccessKey**.
3. Copy the **Connection string–primary key**.

#### 4. Create an Azure SQL Database

1. In the Azure Portal, search for **Azure SQL**.
2. Click **Create** under **SQL databases**.
3. Fill in the following details:
   - **Subscription**: Your subscription.
   - **Resource group**: `DataPipelineRG`.
   - **Database name**: `DataPipelineDB`.
   - **Server**: Click **Create new** and fill in:
     - **Server name**: A unique name (e.g., `datapipeline-server`).
     - **Server admin login**: `sqladmin`.
     - **Password**: A strong password (e.g., `YourStrongPassword123`)
     - **Location**: Same as your resource group.
   - **Compute + storage**: Click **Configure database** and select:
     - **Service tier**: **General Purpose**
     - **Compute tier**: **Serverless**
     - **Autoscaling**: Set the min and max vCores as desired.
     - **Auto-pause delay**: Set to **1 hour** to minimize costs.
   - Click **Apply**.
4. Click **Review + create** and then **Create**.

#### 5. Configure the SQL Database Firewall

1. Navigate to your SQL server (e.g., `datapipeline-server`).
2. Under **Security**, click on **Networking**.
3. Under **Firewall rules**, click **Add your client IPv4 address** to allow your local machine to connect.
4. Click **Save**.

### Local Machine Setup

#### 1. Install Python and Required Libraries

1. **Python 3.x**:
   - Download and install from [python.org](https://www.python.org/downloads/).
2. **Azure Event Hubs SDK**:
   - Open a terminal or command prompt.
   - Install using pip:
     ```bash
     pip install azure-eventhub
     ```
3. **pyodbc** (for SQL Server connectivity):
   ```bash
   pip install pyodbc
   ```
4. **ODBC Driver for SQL Server**:
   - **Windows**: Download and install the [ODBC Driver for SQL Server](https://www.microsoft.com/en-us/download/details.aspx?id=56567).
   - **Mac/Linux**: Follow instructions [here](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server).

#### 2. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/azure-data-pipeline.git
```

*(Replace `https://github.com/yourusername/azure-data-pipeline.git` with the actual URL of your repository.)*

#### 3. Update Configuration Files

Navigate to the cloned repository and update the configuration placeholders in the code files.

- **Replace placeholders** like `<YOUR_CONNECTION_STRING>`, `<YOUR_EVENT_HUB_NAME>`, `<YOUR_SERVER_NAME>`, `<YOUR_DATABASE_NAME>`, `<YOUR_USERNAME>`, and `<YOUR_PASSWORD>` with your actual values.

---

## Running the Project

### 1. Running the Data Producer

The data producer script generates data and sends it to Azure Event Hubs.

#### Steps:

1. **Ensure the CSV File is Available**:

   - Place your CSV file (e.g., `data.csv`) in the same directory as `data_producer.py`.
   - If using a different file name or path, update the `csv_file` variable in `data_producer.py`.

2. **Run the Script**:

   ```bash
   python data_producer.py
   ```

3. **Select the Data Source**:

   - When prompted, enter:
     - `1` to send **CSV Data**.
     - `2` to send **Live Generated Data**.
     - `3` to send **Both CSV and Live Data Alternately**.

### 2. Running the Data Consumer

The data consumer script reads data from Azure Event Hubs and inserts it into the Azure SQL Database.

#### Steps:

1. **Run the Script**:

   ```bash
   python data_consumer.py
   ```

2. **Select the Data Type to Consume**:

   - When prompted, enter:
     - `1` to consume **CSV Data**.
     - `2` to consume **Live Generated Data**.
     - `3` to consume **Both CSV and Live Data**.

### 3. Verifying Data in SQL Database

You can verify that data has been inserted into your Azure SQL Database.

#### Using SQL Server Management Studio (SSMS):

1. **Connect to the SQL Server**:

   - **Server name**: `<YOUR_SERVER_NAME>.database.windows.net`
   - **Authentication**: SQL Server Authentication
   - **Login**: `<YOUR_USERNAME>`
   - **Password**: `<YOUR_PASSWORD>`

2. **Run a Query**:

   - Open a new query window.
   - Execute:
     ```sql
     SELECT * FROM GeneratedCSVTable;
     SELECT * FROM GeneratedLiveTable;
     ```

---

## Code Files

### data_producer.py

```python
import csv
import json
import random
from datetime import datetime
from azure.eventhub import EventHubProducerClient, EventData
import time

# Replace with your connection string and event hub name
CONNECTION_STR = "<YOUR_EVENT_HUB_CONNECTION_STRING>"
EVENTHUB_NAME = "<YOUR_EVENT_HUB_NAME>"

producer = EventHubProducerClient.from_connection_string(
    conn_str=CONNECTION_STR,
    eventhub_name=EVENTHUB_NAME
)

# File path for CSV
csv_file = 'data.csv'  # Replace with your actual CSV file path

# Function to send data to Event Hub
def send_to_event_hub(data, data_type):
    event_data = EventData(data)
    with producer:
        producer.send_batch([event_data])
    print(f"Sent {data_type}: {data}")

# Function to generate live data
def generate_data():
    data = {
        "id": random.randint(1, 10),
        "value": random.uniform(10.0, 100.0),
        "timestamp": datetime.now().isoformat()
    }
    return data

# Function to send live data
def send_live_data(max_messages=10):
    count = 0
    while count < max_messages:
        live_data = generate_data()
        live_data_str = json.dumps(live_data)  # Convert live data to JSON string
        send_to_event_hub(live_data_str, "Live Data")
        count += 1
        time.sleep(5)  # Send live data every 5 seconds

# Function to send CSV data
def send_csv_data():
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            csv_data = ','.join(row)  # Convert list to a comma-separated string
            send_to_event_hub(csv_data, "CSV Data")

# Function to send both CSV and live data alternately
def send_both_data():
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        while True:
            try:
                # Send CSV Data
                row = next(reader)
                csv_data = ','.join(row)
                send_to_event_hub(csv_data, "CSV Data")
            except StopIteration:
                print("All CSV data sent.")
                break

            # Send Live Data
            live_data = generate_data()
            live_data_str = json.dumps(live_data)
            send_to_event_hub(live_data_str, "Live Data")
            time.sleep(5)  # Send every 5 seconds

# Main program: ask the user for the data source option
def main():
    print("Choose the data source to send to Event Hubs:")
    print("1: CSV Data")
    print("2: Live Generated Data")
    print("3: Both CSV and Live Data Alternately")

    choice = input("Enter your choice (1, 2, or 3): ")

    if choice == '1':
        print("Sending CSV data...")
        send_csv_data()
    elif choice == '2':
        print("Sending live generated data...")
        send_live_data()
    elif choice == '3':
        print("Sending both CSV and live generated data alternately...")
        send_both_data()
    else:
        print("Invalid choice. Please run the program again and select 1, 2, or 3.")

if __name__ == "__main__":
    main()
```

### data_consumer.py

```python
import json
import pyodbc
from azure.eventhub import EventHubConsumerClient

# Replace with your connection string and event hub name
CONNECTION_STR = "<YOUR_EVENT_HUB_CONNECTION_STRING>"
EVENTHUB_NAME = "<YOUR_EVENT_HUB_NAME>"
CONSUMER_GROUP = "$Default"

# SQL Database connection details
SERVER = "<YOUR_SERVER_NAME>.database.windows.net"
DATABASE = "<YOUR_DATABASE_NAME>"
USER = "<YOUR_USERNAME>"
PASSWORD = "<YOUR_PASSWORD>"

# Function to handle CSV data insertion into the database
def handle_csv_data(data):
    print(f"Processing CSV data: {data}")
    try:
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USER};PWD={PASSWORD}'
        )
        cursor = conn.cursor()

        # Assuming the CSV data is comma-separated
        columns = data.split(',')
        cursor.execute(
            "INSERT INTO GeneratedCSVTable (FULL_DATE, AMOUNT, LOANS) VALUES (?, ?, ?)",
            columns[0], columns[1], columns[2]
        )
        conn.commit()
        cursor.close()
        conn.close()
        print("CSV data successfully inserted into the database.")
    except Exception as e:
        print(f"Error inserting CSV data into the database: {e}")

# Function to handle live data insertion into the database
def handle_live_data(data):
    print(f"Processing live data: {data}")
    try:
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USER};PWD={PASSWORD}'
        )
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO GeneratedLiveTable (id, value, timestamp) VALUES (?, ?, ?)",
            data["id"],
            data["value"],
            data["timestamp"]
        )
        conn.commit()
        cursor.close()
        conn.close()
        print("Live data successfully inserted into the database.")
    except Exception as e:
        print(f"Error inserting live data into the database: {e}")

# Main function to handle incoming events
def on_event(partition_context, event, data_type):
    data = event.body_as_str()

    if data_type == "CSV":
        handle_csv_data(data)
    elif data_type == "Live":
        try:
            json_data = json.loads(data)
            handle_live_data(json_data)
        except json.JSONDecodeError:
            print("Received data is not valid JSON for live data.")

    partition_context.update_checkpoint(event)

# Event Hub client setup
try:
    client = EventHubConsumerClient.from_connection_string(
        CONNECTION_STR,
        CONSUMER_GROUP,
        eventhub_name=EVENTHUB_NAME
    )
    print("Event Hub client created successfully.")
except Exception as e:
    print(f"Error creating Event Hub client: {e}")

# Main function to start receiving events based on user selection
def main():
    print("Choose the data type to consume from Event Hubs:")
    print("1: CSV Data")
    print("2: Live Generated Data")
    print("3: Both CSV and Live Data")

    choice = input("Enter your choice (1, 2, or 3): ")

    if choice == '1':
        data_type = "CSV"
    elif choice == '2':
        data_type = "Live"
    elif choice == '3':
        data_type = "Both"
    else:
        print("Invalid choice. Please restart and select 1, 2, or 3.")
        return

    # Start receiving events from Event Hubs
    try:
        if client:
            with client:
                print(f"Starting to receive {data_type} events from Event Hub...")
                client.receive(
                    on_event=lambda partition_context, event: on_event(partition_context, event, data_type),
                    starting_position="-1"  # "-1" starts from the beginning of the stream
                )
    except KeyboardInterrupt:
        print("Receiving interrupted by user.")
    except Exception as e:
        print(f"Error during event receiving: {e}")

if __name__ == "__main__":
    main()
```

### schema_creator.py

```python
import csv
import json

# File path for CSV
csv_file = 'data.csv'  # Replace with your actual CSV file path

# Function to generate SQL schema for CSV data
def generate_sql_schema_csv(csv_file, table_name="GeneratedCSVTable"):
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
def generate_sql_schema_live(data_example, table_name="GeneratedLiveTable"):
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
```

---

## Conclusion

By following this guide, you have set up a complete data pipeline using Azure services. You can now generate data, send it through Event Hubs, store it in an Azure SQL Database, and consume it using Python scripts.

## Acknowledgments

- **Azure Documentation**: For detailed guides on using Azure services.
- **Python Community**: For developing libraries like `azure-eventhub` and `pyodbc`.
- **Microsoft**: For providing tools like SSMS and Azure services.

---

**Disclaimer**: Ensure that all sensitive information such as passwords and connection strings are kept secure. Do not share them publicly or commit them to public repositories.

---

I hope this detailed `README.md` file meets your requirements. Remember to replace all placeholders with your actual configuration details and to include the necessary images in the `images` directory.

If you need further assistance or have additional requests, feel free to ask!
