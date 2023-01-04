import numpy as np
import csv
from functions import *

while True:
    # Get user input
    start_year = int(input("Enter start year for scraping (data before 2007 does not exist):\n"))
    end_year = int(input("Enter the end year for scraping (up to 2024):\n"))
    try:
        if start_year < 2007:
            # Invalid input handling
            print("\nUser Error: Please enter a start date equal to or after 2007! Try again.\n")
            continue
        elif end_year > 2024:
            # Invalid input handling
            print("\nUser Error: Please enter a start date equal to or before 2024! Try again.\n")
            continue
        elif start_year > end_year:
            # Invalid input handling
            print("\nUser Error: The start year has to be lesser than the end year! Try again.\n")
            continue
        else:
            # Get date range
            dates = first_days_of_month(start_year,end_year)

            with open('news_event_data.csv', 'a', newline='') as outcsv:
                # Add header to output CSV file 
                writer = csv.writer(outcsv)
                writer.writerow(["Date", "Time", "Currency, Expected Impact Class, News Event Title, Actual Impact, Forcasted Impact, Previous Impact"])
                
                for date in np.nditer(dates):
                    # Write each sub-array of `news-events` to the output csv file
                    news_events = np.array(scrape(f"https://www.forexfactory.com/calendar?month={date}"))
                    np.savetxt(outcsv, news_events, delimiter=",", fmt="%s",)
            break
    # Invalid input handling
    except ValueError:
        print("Please enter integer values")