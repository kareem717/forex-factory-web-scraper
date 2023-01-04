from functions import *
from calendar import monthrange
import csv
import datetime

with open("sundays.txt", "r") as file:
    # Iterate over each line in the file
    iteration = 1
    totalInsertedRows = 0
    for date in file:
        year = date[6:]
        print("===========================================================================================================================================================================")
        time_string = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"Starting week of {date.strip()}, at {time_string}......")
        dayNewsData = scrape(f"https://www.forexfactory.com/calendar?week={date}\n")
        time = "" 
        # Open the CSV file in write mode
        with open('file.csv', 'a', newline='') as csvfile:
            # Create a CSV writer object
            writer = csv.writer(csvfile)
            # Write the first, second, and last elements of the list to the CSV file
            insertedRows = 0
            for row in dayNewsData:

                if ":" in row[1]:
                    time = row[1]
                else:
                    row.insert(1, time)
                
                if "USD" in row[2] or "CAD" in row[2] or "ALL" in row[2]:
                    writer.writerow([row[0] + " " + year.strip(), row[1], row[2], row[3], row[-1]])
                    insertedRows += 1
        now = datetime.datetime.now()

        totalInsertedRows += insertedRows
        # Format the current time as a string in the desired format
        time_string = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"Done week of {date.strip()}, at {time_string}! || Total Inserted Row Count: {totalInsertedRows} || Inserted Row Count: {insertedRows} || Iteration Number: {iteration} ")
        iteration+=1
        print("===========================================================================================================================================================================\n\n")