from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
import time
import winsound
from decouple import config

driver = webdriver.Chrome('..\..\Downloads\chromedriver_win32\chromedriver')
driver.get("https://www.ea.com/fr-fr/fifa/ultimate-team/web-app/")

# LOGIN

# Click on button Connection after waiting to be clickable
login = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Login"]/div/div/button[1]')))
login.click()

# Put the email into the email input
email = driver.find_element_by_id("email")
email.send_keys(config("EMAIL_EA"))

# Put the password into the password input
pwd = driver.find_element_by_id("password")
pwd.send_keys(config("PWD_EA"))

# Click on the Login button
driver.find_element_by_id("btnLogin").click()

# Click on the Send Verification Code button
driver.find_element_by_id("btnSendCode").click()

# MARKET

# Wait for home page transfer button to be located
WebDriverWait(driver, 90).until(EC.visibility_of_element_located((By.XPATH, '/html/body/main/section/nav/button[3]')))
time.sleep(5)

# Wait for loader to be invisible
WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.ID, 'futweb-loader')))
time.sleep(5)

# Click on transfer button
driver.find_element_by_xpath("/html/body/main/section/nav/button[3]").click()
time.sleep(5)

# Click on transfer market button
driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/div[2]").click()
time.sleep(1)

# SEARCH FILTER

time.sleep(1)
# Click on country dropdown button
driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[6]/div/div").click()
time.sleep(1)

# Click on italian button to get only italian players
driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[6]/div/ul/li[8]").click()
time.sleep(1)

# Set the max offer price to make benefits on sell
offer = driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[2]/div[3]/div[2]/input")
offer.send_keys(config("ITALIAN_PRICE_BUY"))
time.sleep(1)

# Click search button
driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[2]/button[2]").click()

# Variable to check the number of offers made
p = 0

# Infinite loop to buy and sell endlessly
while 42:    

    # SEARCH RESULTS

    # loop on a page 20 players max per page
    time.sleep(2)
    for i in range(20):
        time.sleep(1)

        # Select player after waiting to be clickable
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[1]/div/ul/li[" + str(i + 1) + "]")))
        element.click()

        # Check if the price input is located and break the for loop to change page if timeout
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div/input')))
        except TimeoutException:
            print("Timeout Exception")
            break

        # Check if the price input is located and enabled
        if driver.find_elements(By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div/input") and driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div/input").is_enabled():

            # Get price input value
            price = driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div/input").get_attribute('value')

            # Remove space (eg: 1 200 => 1200)
            price = price.replace("\u202f", "")

            # Check if the price is lower or equal to the max offer price to make benefits on sell
            if int(price) <= int(config("ITALIAN_PRICE_BUY")):

                # if it is then click on price input to select the previous value
                element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div/input')))
                element.click()
                time.sleep(1)

                # Put our max offer price into the input
                buy_price = driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div/input")

                # Error check if the element is not interactable (player was buy between the price check and now)
                try:
                    buy_price.send_keys(config("ITALIAN_PRICE_BUY"))
                except ElementNotInteractableException:
                    break
                time.sleep(1)

                # Double check the entered input price is lower or equal to the max offer price
                price = driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div/input").get_attribute('value')
                price = price.replace("\u202f", "")
                if int(price) <= int(config("ITALIAN_PRICE_BUY")):

                    # Check if the make offer button is clickable
                    try:
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[1]")))
                    except TimeoutException:
                        print("Timeout Exception")
                        break

                    # Click on the make offer button
                    element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[1]")))
                    element.click()

                    # Increment by one the number of offers
                    p = p + 1
        # If the number of offers is equal to the number we want to stop buying (maximum 50 offers)
        if p == 10:
            break
    
    # Go to next page if the for loop end
    element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/section[1]/div/div/button[2]')))
    element.click()

    # If the number of offers is equal to the number we want to stop buying, let's sell our players
    if p == 10:

        # Check if loader is invisible
        WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]')))
        time.sleep(1)

        # Go back and check if loader is invisble twice
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[1]/button[1]')))
        element.click()
        WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]')))
        time.sleep(1)
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[1]/button[1]')))
        element.click()
        WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]')))
        time.sleep(1)

        # Click on current offers
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/div[4]')))
        element.click()

        # loop while there is active offers
        while driver.find_elements(By.XPATH, "/html/body/main/section/section/div[2]/div/div/div/section[1]/ul/li[1]"):
            time.sleep(2)
        
        # Check if there is expired items 
        if driver.find_elements(By.XPATH, "/html/body/main/section/section/div[2]/div/div/div/section[4]/ul/li[1]"):

            # Click on delete button to delete expired items
            element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/div/section[4]/header/button')))
            element.click()
        time.sleep(1)

        # Check if loader is invisible
        WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]')))

        # loop while there is win items
        while driver.find_elements(By.XPATH, "/html/body/main/section/section/div[2]/div/div/div/section[3]/ul/li[1]"):

            # Check if loader is invisible
            WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]')))

            # Check if element is attached to DOM (rare error)
            while 42:
                try:
                    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/div/section[3]/ul/li[1]')))
                except StaleElementReferenceException:
                    print("Stale Exception")
                    continue
                break

            # Click on the first element of the win items list
            element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/div/section[3]/ul/li[1]')))
            element.click()
            time.sleep(1)

            # Click on the add to sell button
            element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[1]/button')))
            element.click()
            time.sleep(1)

            # Click on the min price input
            element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/input')))
            element.click()
            time.sleep(3)

            # Put min sell price
            min_price = driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/input")
            min_price.send_keys(config("ITALIAN_PRICE_MIN_SELL"))
            time.sleep(2)

            # Click on the max price input
            element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[2]/div[3]/div[2]/input')))
            element.click()
            time.sleep(3)

            # Put max sell price
            min_price = driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[2]/div[3]/div[2]/input")
            min_price.send_keys(config("ITALIAN_PRICE_MAX_SELL"))
            time.sleep(3)

            # Click on the sell button
            element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[2]/button')))
            element.click()
            time.sleep(1)
        
        # Reset offers to zero
        p = 0

        # Check if loader is invisible
        WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]')))
        time.sleep(1)

        # Click on transfer button in menu
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/nav/button[3]')))
        element.click()

        # Check if loader is invisible
        WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]')))
        time.sleep(1)

        # Click on our active transfers
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/div[3]')))
        element.click()

        # Check if loader is invisible
        WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]')))
        time.sleep(1)

        # Check if there is selled player
        if driver.find_elements(By.XPATH, "/html/body/main/section/section/div[2]/div/div/div/section[1]/ul/li[1]"):

            # Click on remove selled player
            element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/div/section[1]/header/button')))
            element.click()

        # Check if loader is invisible
        WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]')))
        time.sleep(1)

        # Go back to transfer menu
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/nav/button[3]')))
        element.click()

        # Check if loader is invisible
        WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]')))
        time.sleep(1)

        # Click on the transfer maket
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/div[2]')))
        element.click()

        # Check if loader is invisible
        WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]')))
        time.sleep(1)

        # Search again
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div[2]/div/div[2]/button[2]')))
        element.click()


