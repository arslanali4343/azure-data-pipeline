import csv
import json
import random
from datetime import datetime
from azure.eventhub import EventHubProducerClient, EventData
import time

# Replace with your connection string and event hub name
CONNECTION_STR = "Your_Connection_String"
EVENTHUB_NAME = "Your_Event"


producer = EventHubProducerClient.from_connection_string(conn_str=CONNECTION_STR, eventhub_name=EVENTHUB_NAME)

# File path for CSV
csv_file = '2024-10-08 1_45pm.csv'  # Replace with your actual CSV file path

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

        count = 0
        while True:
            # Send CSV Data
            try:
                row = next(reader)
                csv_data = ','.join(row)  # Convert list to a comma-separated string
                send_to_event_hub(csv_data, "CSV Data")
            except StopIteration:
                print("All CSV data sent.")
                break

            # Send Live Data
            live_data = generate_data()
            live_data_str = json.dumps(live_data)  # Convert live data to JSON string
            send_to_event_hub(live_data_str, "Live Data")

            count += 1
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
