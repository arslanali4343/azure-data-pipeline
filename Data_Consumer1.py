import json
import pyodbc
from azure.eventhub import EventHubConsumerClient

# Replace with your connection string and event hub name
CONNECTION_STR = "Your_COnnection_String"
EVENTHUB_NAME = "Your_Event_Name"
CONSUMER_GROUP = "$Default"

# SQL Database connection details
SERVER = "datapipeline-server1.database.windows.net"
DATABASE = "DataPipelineDB1"
USER = "Your_UserName"
PASSWORD = "Your_Password"

# Function to handle CSV data insertion into the database
def handle_csv_data(data):
    print(f"Processing CSV data: {data}")
    try:
        print("Attempting to connect to the database...")
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USER};PWD={PASSWORD}'
        )
        print("Database connection successful.")
        cursor = conn.cursor()

        # Assuming the CSV data is already split into columns
        columns = data.split(',')  # Split by comma since CSV is comma-separated
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
        print("Attempting to connect to the database...")
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USER};PWD={PASSWORD}'
        )
        print("Database connection successful.")
        cursor = conn.cursor()

        # Insert live data into the database
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
    
    # Determine if the data is CSV or live JSON
    if data_type == "CSV":
        handle_csv_data(data)
    elif data_type == "Live":
        try:
            json_data = json.loads(data)  # Try to parse as JSON (for live data)
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
        print("Consuming CSV data...")
        data_type = "CSV"
    elif choice == '2':
        print("Consuming live generated data...")
        data_type = "Live"
    elif choice == '3':
        print("Consuming both CSV and live data alternately...")
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
