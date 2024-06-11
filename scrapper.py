from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

START_URL="https://exoplanets.nasa.gov/exoplanet-catalog/"

browser=webdriver.Chrome()
browser.get(START_URL)

time.sleep(2)

planets_data=[]

def scrape():
    for i in range(0,2):
        print(f'scrapping page{i+1}')

        soup=BeautifulSoup(browser.page_source,'html.parser')
        
        for planet in soup.find_all('div', class_='hds-content-item'):
            planet_info=[]

            planet_info.append(planet.find('h3',class_='heading-22').text.strip())

            information_to_extract=["Light-Years From Earth", "Planet Mass", "Stellar Magnitude", "Discovery Date"]
            
            for info_name in information_to_extract:
                try:
                    # Extract other planet information
                    planet_info.append(planet.select_one(f'span:-soup-contains("{info_name}")')
                                       .find_next_sibling('span').text.strip())
                except:
                    planet_info.append('Unknown')  # Handling cases where information is not found

            link='https://science.nasa.gov'+planet.find('a')['href']

            planet_info.append(link)

            planets_data.append(planet_info)

        try:
            time.sleep(2)
            next_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, 
                    "//button[@class='next page-numbers']")))
            browser.execute_script('arguements[0].scrollIntoView();',next_button)
            time.sleep(2)
            next_button.click()
            
        except:
            print(f'error occured while navigating to next page')
            break

scrape()

# Define Header for DataFrame
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink"]

print(planets_data)
# Create pandas DataFrame from the extracted data
planet_df_1 = pd.DataFrame(planets_data, columns=headers)

# Convert DataFrame to CSV and save to file
planet_df_1.to_csv('updated_scraped_data.csv', index=True, index_label="id")  # Saving the DataFrame as a CSV file
