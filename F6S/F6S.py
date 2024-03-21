from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException

search_word = input("Enter a search word: ")
url = f'https://www.f6s.com/search?q={search_word}'

driver = webdriver.Firefox()

driver.implicitly_wait(50)

# empty lists to store scraped data
names = []
services = []
descriptions = []
locations = []
links = []
companies = []
linkedin_link = []
twitter_link = []
facebook_link = []


driver.get(url)
time.sleep(5)  

# Scroll down to load results
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)  

# people section to display results
people_section = driver.find_element(By.CSS_SELECTOR, "#searchFilters > li:nth-child(3) > a")
people_section.click()
time.sleep(10)

# range of desired results
start_search = int(input("Enter the desired start search result: "))
search_results = int(input("Enter the limit of search results: "))

# scrape data from the results page
for i in range(start_search, search_results + 1):
    result_selector = f"#csSearchResultsList > div:nth-child({i}) > div:nth-child(2) > div.t.b18 > a"
    result_element = driver.find_element(By.CSS_SELECTOR, result_selector)
    result_element.click()
    time.sleep(5)

    # data from the result page
    try:
        name = driver.find_element(By.CSS_SELECTOR, "#__layout > div > main > div > div:nth-child(1) > div.header-main > div > div.profile-data > div.profile-heading > h1").text
    except NoSuchElementException:
        name = None
    try:
        service = driver.find_element(By.CSS_SELECTOR, "#__layout > div > main > div > div:nth-child(1) > div.header-main > div > div.profile-data > div.member-badges.member-badges > span:nth-child(1) > span").text
    except NoSuchElementException:
        service = None
    try:
        description = driver.find_element(By.CSS_SELECTOR, "#__layout > div > main > div > div:nth-child(1) > div.header-main > div > div.profile-data > p").text
    except NoSuchElementException:
        description = None
    try:
        location = driver.find_element(By.CSS_SELECTOR, "#about > div.centered-content.g8.overview-line").text
    except NoSuchElementException:
        location = None
    try:
        link = driver.find_element(By.CSS_SELECTOR, "#about > div.links.centered-content.overview-line.member-links > div > a").get_attribute("href")
    except NoSuchElementException:
        link = None
    try:
        company = driver.find_element(By.CSS_SELECTOR, "#investments > div > div > a").text
    except NoSuchElementException:
        company = None
    try:
        linkedin = driver.find_element(By.CSS_SELECTOR, "#about > div.links.centered-content.overview-line.member-links > a:nth-child(2)").get_attribute("href")
    except NoSuchElementException:
        linkedin= None

    try:
        twitter= driver.find_element(By.CSS_SELECTOR, "#about > div.links.centered-content.overview-line.member-links > a").get_attribute("href")
    except NoSuchElementException:  
        twitter= None

    try:
        facebook= driver.find_element(By.CSS_SELECTOR, "#about > div.links.centered-content.overview-line.member-links > a:nth-child(3)").get_attribute("href")
    except NoSuchElementException:
        facebook= None


    # Append the scraped data to the lists
    names.append(name)
    services.append(service)
    descriptions.append(description)
    locations.append(location)
    links.append(link)
    companies.append(company)
    linkedin_link.append(linkedin)
    twitter_link.append(twitter)
    facebook_link.append(facebook)


    # back to the search results page
    driver.back()
    people_section = driver.find_element(By.CSS_SELECTOR, "#searchFilters > li:nth-child(3) > a")
    people_section.click()
    time.sleep(10)

# DataFrame
result_df = pd.DataFrame({
    "Name": names,
    "Service": services,
    "Description": descriptions,
    "Company": companies,
    "Location": locations,
    "Link": links,
    "twitter": twitter_link,
    "linkedin": linkedin_link,
    "facebook": facebook_link
})

# Print the DataFrame
print(result_df)

# Save data to a CSV and xlsx file
result_df.to_csv('f6s.csv', index=False)
print("Data saved to CSV file")
result_df.to_excel('f6s.xlsx', index=False)
print("Data saved to xlsx file")

# Close
driver.quit()
