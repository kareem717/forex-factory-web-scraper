from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from calendar import monthrange
import datetime
import datetime
import datetime
from datetime import date, timedelta

def allsundays(year):
   d = date(year, 1, 1)                    # January 1st
   d += timedelta(days = 6 - d.weekday())  # First Sunday
   while d.year == year:
      yield d
      d += timedelta(days = 7)

def convert_date(date_str: str) -> str:
    # Parse the input string as a date object
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    # Extract the month and day from the date object
    month = date.strftime("%b")  # abbreviated month name
    day = date.strftime("%d")
    # Return the formatted string
    return f"{month.lower()}{day}.{date.year}"

with open('firstdays.txt', 'a') as f:
    for x in range(2007,2024):
        for d in allsundays(x):
        # The rest of the code stays the same
            f.write(f"{convert_date(str(d))}\n")

def scrape(html):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    try:
        driver.get(html)
        row_datas = []
        # Get the table
        table = driver.find_element(By.CLASS_NAME, "calendar__table")
        # Iterate over each table row
        
        current_day = ""
        for row in table.find_elements(By.TAG_NAME, "tr"):
            if "calendar__row calendar__row--day-breaker" in row.get_attribute("class"):
                current_day = row.get_attribute("textContent")[4:]
            # list comprehension to get each cell's data and filter out empty cells
            row_data = list(filter(None, [td.text for td in row.find_elements(By.TAG_NAME, "td") if not "\n" in td.text]))
            
            high_impact_elements = [td for td in row.find_elements(By.CLASS_NAME, "calendar__impact--high")]
            medium_impact_elements = [td for td in row.find_elements(By.CLASS_NAME, "calendar__impact--medium")]
            row_impact = high_impact_elements + medium_impact_elements
            if row_data == [] or row_impact == []:
                continue
            if len(medium_impact_elements):
                row_datas.append([current_day.strip()] + row_data + ["MED"])
            else:
                row_datas.append([current_day.strip()] + row_data + ["HIGH"])

        return row_datas
    except Exception as e:
        return e
    finally:
        driver.quit()



    


