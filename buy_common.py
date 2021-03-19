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
from decouple import config

driver = webdriver.Chrome('chromedriver')
driver.get("https://www.ea.com/fr-fr/fifa/ultimate-team/web-app/")

# LOGIN

login = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Login"]/div/div/button[1]')))
login.click()
email = driver.find_element_by_id("email")
email.send_keys(config("EMAIL_EA"))
pwd = driver.find_element_by_id("password")
pwd.send_keys(config("PWD_EA"))
driver.find_element_by_id("btnLogin").click()
driver.find_element_by_id("btnSendCode").click()

# MARKET
time.sleep(60)
driver.find_element_by_xpath("/html/body/main/section/nav/button[3]").click()
time.sleep(5)
driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/div[2]").click()
time.sleep(1)
# SEARCH FILTER
time.sleep(1)
driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div/div").click()
time.sleep(1)
driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div/ul/li[4]").click()
time.sleep(1)
driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[3]/div/div").click()
time.sleep(1)
driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[3]/div/ul/li[2]").click()
time.sleep(1)
offer = driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[2]/div[3]/div[2]/input")
offer.send_keys(config("COMMON_PRICE_BUY"))
time.sleep(1)
driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[2]/button[2]").click()

p = 0
while 42:    

    # SEARCH RESULTS
    time.sleep(2)
    for i in range(20):
        time.sleep(1)
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[1]/div/ul/li[" + str(i + 1) + "]")))
        element.click()
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div/input')))
        except TimeoutException:
            print("Timeout Exception")
            break
        if driver.find_elements(By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div/input") and driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div/input").is_enabled():
            price = driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div/input").get_attribute('value')
            price = price.replace("\u202f", "")
            if int(price) <= int(config("COMMON_PRICE_BUY")):
                element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div/input')))
                element.click()
                time.sleep(1)
                buy_price = driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div/input")
                try:
                    buy_price.send_keys(config("COMMON_PRICE_BUY"))
                except ElementNotInteractableException:
                    break
                time.sleep(1)
                price = driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div/input").get_attribute('value')
                price = price.replace("\u202f", "")
                if int(price) <= int(config("COMMON_PRICE_BUY")):
                    try:
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[1]")))
                    except TimeoutException:
                        print("Timeout Exception")
                        break
                element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[1]")))
                element.click()
                p = p + 1
        if p == 30:
            break
    element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/section[1]/div/div/button[2]')))
    element.click()
    if p == 30:
        WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]')))
        time.sleep(1)
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[1]/button[1]')))
        element.click()
        WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]')))
        time.sleep(1)
        WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]')))
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[1]/button[1]')))
        element.click()
        WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]')))
        time.sleep(1)
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/div[4]')))
        element.click()
        while driver.find_elements(By.XPATH, "/html/body/main/section/section/div[2]/div/div/div/section[1]/ul/li[1]"):
            time.sleep(2)
        if driver.find_elements(By.XPATH, "/html/body/main/section/section/div[2]/div/div/div/section[4]/ul/li[1]"):
            element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/div/section[4]/header/button')))
            element.click()
        time.sleep(1)
        WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]')))
        while driver.find_elements(By.XPATH, "/html/body/main/section/section/div[2]/div/div/div/section[3]/ul/li[1]"):
            WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]')))
            while 42:
                try:
                    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/div/section[3]/ul/li[1]')))
                except StaleElementReferenceException:
                    print("Stale Exception")
                    continue
                break
            element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/div/section[3]/ul/li[1]')))
            element.click()
            time.sleep(1)
            element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[1]/button')))
            element.click()
            time.sleep(1)
            element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/input')))
            element.click()
            time.sleep(3)
            min_price = driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/input")
            min_price.send_keys(config("COMMON_PRICE_MIN_SELL"))
            time.sleep(2)
            element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[2]/div[3]/div[2]/input')))
            element.click()
            time.sleep(3)
            min_price = driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[2]/div[3]/div[2]/input")
            min_price.send_keys(config("COMMON_PRICE_MAX_SELL"))
            time.sleep(3)
            element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[2]/button')))
            element.click()
            time.sleep(1)
        p = 0
        WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]')))
        time.sleep(1)
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/nav/button[3]')))
        element.click()
        WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]')))
        time.sleep(1)
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/div[3]')))
        element.click()
        WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]')))
        time.sleep(1)
        if driver.find_elements(By.XPATH, "/html/body/main/section/section/div[2]/div/div/div/section[1]/ul/li[1]"):
            while 42:
                try:
                    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/div/section[1]/header/button')))
                except StaleElementReferenceException:
                    print("Stale Exception")
                    continue
                break
            element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/div/section[1]/header/button')))
            element.click()
        WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]')))
        time.sleep(1)
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/nav/button[3]')))
        element.click()
        WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]')))
        time.sleep(1)
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div/div[2]')))
        element.click()
        WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[4]')))
        time.sleep(1)
        element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/section/div[2]/div/div[2]/div/div[2]/button[2]')))
        element.click()


