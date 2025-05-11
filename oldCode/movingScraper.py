from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import pytz
import datetime

# initialize WebDriver
driver_path = '/Users/javierzegada/Desktop/chromedriver-mac-arm64/chromedriver'

data = []
# setting up the service object
service = Service(driver_path)



# initialize the WebDriver with the service
driver = webdriver.Chrome(service=service)


# url to stocktwits
url = 'https://stocktwits.com/symbol/QQQ'



driver.get(url)


# wait for the page to load completely
time.sleep(5)

# scroll the page to simulate loading more tweets
scroll_pause_time = 5

# clicking into log in
wait = WebDriverWait(driver, 5)
link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log in to existing account")))

# wait to load
link.click()
time.sleep(5)

# type in Username
username_field = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div[3]/div/div[2]/form/div[1]/input')
username_field.send_keys("brunito123")
time.sleep(2)

# type in Password
password_field = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div[3]/div/div[2]/form/div[2]/input')
password_field.send_keys("hellofive!")
time.sleep(2)

# click sign in
signUp = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div[3]/div/div[2]/form/button')
signUp.click()
time.sleep(3)

# set the target year to stop
target_date = "24"

# initial scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

# keeping going until target year is hit
while True:

    # extracting information
    data_testid = driver.find_elements(By.XPATH, "//div[@data-testid]")
    time.sleep(1)

    try:
        for index, element in enumerate(data_testid):
            
            try:
                # find the div inside this element that contains the message text
                message_div = element.find_element(By.XPATH, ".//div[contains(@class, 'RichTextMessage_body__4qUeP')]")
                
                # extract the username
                username_div = element.find_element(By.XPATH, ".//div[contains(@class, 'flex flex-row justify-between items-center gap-x-2')]")
                username = username_div.text.split("\n")[0]


                # extract the time
                time_element = element.find_element(By.XPATH, ".//time")
                time_value = time_element.get_attribute("datetime")


                # extract the date part of the time_value (before the "T") for year
                message_date = time_value.split("T")[0].split("-")[2]

                # compare with target year
                if message_date == target_date:
                    print(f"Target date {target_date} reached, stopping.")
                    break

                # extract the text
                message_text = message_div.text

                # append to the data list
                data.append([username, message_text, time_value])
                
                print(f"Message {index + 1}: {username} with {message_text} on {time_value}\n\n")

            except:
                print(f"Message {index + 1}: No message text found in this data-testid div.\n")
        
        # scroll to the next page
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")

        # wait for new tweets to load by waiting for an element that changes when the scroll completes
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'RichTextMessage_body__4qUeP')]"))
            )
        except:
            print("Timed out waiting for new content to load.")
            break

        # calculate new scroll height and compare with last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        last_height = new_height
    except Exception as e:
        print(f"Error was {e}")
        df = pd.DataFrame(data, columns=["Username", "Message", "Time"])
        print(df)

# save into a dataframe
df = pd.DataFrame(data, columns=["Username", "Message", "Time"])

# safety check of df
print(df)

# quit driver
driver.quit()

# saving the df
#df.to_csv("./QQQtweets.csv")

