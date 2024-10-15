import os
import datetime


def list_files_in_date_range(directory, start_date, end_date):
    # Convert start_date and end_date strings to datetime objects
    start_datetime = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    end_datetime = datetime.datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

    # List to store files within the date range
    files_in_range = []

    # Iterate through files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):
            # Get the file's creation time
            creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
            
            # Check if the file was created within the specified date range
            if start_datetime <= creation_time <= end_datetime:
                files_in_range.append(filename)

    return files_in_range


if __name__ == "__main__":
    directory_path = "data"
    user_input = input("Unload Sample? (y/n): ")
    if user_input == 'n':
        print("OK")
    else:
        input_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        start_date = "2024-01-15 00:00:00"
        end_date = input_time

        files = list_files_in_date_range(directory_path, start_date, end_date)

        print(f"Files created between {start_date} and {end_date}:")

        for file in files:
            print(file)