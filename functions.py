from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
from datetime import datetime

def scrape(html):
    try:
        # Create a new instance of a headless chrome driver.
        driver = webdriver.Chrome()
        # Get the HTML of the webpage that is passed to the function.
        driver.get(html)
        
        # Use bs4 to parse the HTML content
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all rows
        rows = soup.find_all("tr", class_=["calendar__row--grey", "calendar__row--day-breaker"])

        # News events output array
        output = []

        # Get row details
        time = ""
        date = ""
        for row in rows:
            if "calendar__row--day-breaker" in row['class']:
                date = f"{row.find('span', class_='').get_text()} {html[-4:]}"
            elif not "calendar__row--day-breaker" in row['class']:
                # Store news event time
                news_event_time = row.find_all('td', class_="calendar__cell calendar__time time")[0].get_text().strip()
                if news_event_time:
                    time = news_event_time

                # Store currency affected by the news event
                news_event_currency = row.find_all('td', class_="calendar__cell calendar__currency currency")[0].get_text().strip()

                # Store news event title
                news_event_title = row.find_all('span', class_="calendar__event-title")[0].get_text()
                
                # Store impact class of news event
                news_event_class = row.find('span', class_=['low', 'medium', 'high', 'calendar__event-title'])['class'][0].title()
                if news_event_class == 'Calendar__Event-Title': 
                    news_event_class = 'Bank Holiday Impact'
                
                # Store `Actual` value of news event
                news_actual_value = row.find('td', class_="calendar__cell calendar__actual actual").get_text()
                
                # Store `Forecast` value of news event
                news_forecast_value = row.find('td', class_="calendar__cell calendar__forecast forecast").get_text()
                
                # Store `Previous` value of news event
                news_previous_value = row.find('td', class_="calendar__cell calendar__previous previous").get_text()
                
                output.append([date, time, news_event_currency, news_event_class, news_event_title, news_actual_value, news_forecast_value, news_previous_value])
        return output
    except Exception as e:
        return e
    finally:
        driver.quit()


def first_days_of_month(start_year, end_year):
    years, months = np.meshgrid(np.arange(start_year, end_year+1), np.arange(1, 13))
    dates = np.vstack([years.ravel(), months.ravel()]).T
    dates = sorted(dates, key=lambda x: x[0])  # sort by year
    return np.array([datetime(year, month, 1).strftime("%b%d.%Y") for year, month in dates])


