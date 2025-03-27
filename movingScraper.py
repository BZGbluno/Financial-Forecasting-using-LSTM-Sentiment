from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import pytz
import datetime

# Initialize WebDriver (replace with the actual path to your chromedriver)
driver_path = '/Users/javierzegada/Desktop/chromedriver-mac-arm64/chromedriver'

data = []
# Set up the Service object
service = Service(driver_path)



#Initialize the WebDriver with the service
driver = webdriver.Chrome(service=service)


# Open the URL
url = 'https://stocktwits.com/symbol/QQQ'



driver.get(url)


# Wait for the page to load completely (adjust time as needed)
time.sleep(5)

# Scroll the page to simulate loading more tweets
scroll_pause_time = 5  # Time to pause to allow tweets to load


wait = WebDriverWait(driver, 5)  # Wait up to 10 seconds
link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log in to existing account")))

link.click()
time.sleep(5)

# Type in Username
username_field = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div[3]/div/div[2]/form/div[1]/input')
username_field.send_keys("brunito123")
time.sleep(2)

# Type in Password
password_field = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div[3]/div/div[2]/form/div[2]/input')
password_field.send_keys("hellofive!")
time.sleep(2)

# Click sign in
signUp = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div[3]/div/div[2]/form/button')
signUp.click()
time.sleep(3)


target_date = "23"

# Initial scroll height
last_height = driver.execute_script("return document.body.scrollHeight")


while True:

    # Extracting Information
    data_testid = driver.find_elements(By.XPATH, "//div[@data-testid]")
    time.sleep(1)

    try:
        for index, element in enumerate(data_testid):
            
            try:
                # Find the div inside this element that contains the message text
                message_div = element.find_element(By.XPATH, ".//div[contains(@class, 'RichTextMessage_body__4qUeP')]")
                
                # Extract the username (inside the 'flex flex-row justify-between items-center gap-x-2' div)
                username_div = element.find_element(By.XPATH, ".//div[contains(@class, 'flex flex-row justify-between items-center gap-x-2')]")
                username = username_div.text.split("\n")[0]


                # Extract the time (from <time datetime="...">)
                time_element = element.find_element(By.XPATH, ".//time")
                time_value = time_element.get_attribute("datetime")


                # Extract the date part of the time_value (before the "T")
                message_date = time_value.split("T")[0].split("-")[2]

                # Compare with target date
                if message_date == target_date:
                    print(f"Target date {target_date} reached, stopping.")
                    break

                # Extract the text
                message_text = message_div.text

                # Append to the data list
                data.append([username, message_text, time_value])
                
                print(f"Message {index + 1}: {username} with {message_text} on {time_value}\n\n")

            except:
                print(f"Message {index + 1}: No message text found in this data-testid div.\n")
        

        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollBy(0, 1500);")

        # Wait for new tweets to load by waiting for an element that changes when the scroll completes
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'RichTextMessage_body__4qUeP')]"))
            )
        except:
            print("Timed out waiting for new content to load.")
            break

        # Calculate new scroll height and compare with last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        last_height = new_height
    except Exception as e:
        print(f"Error was {e}")
        df = pd.DataFrame(data, columns=["Username", "Message", "Time"])
        print(df)


df = pd.DataFrame(data, columns=["Username", "Message", "Time"])
print(df)
time.sleep(1000)
driver.quit()

