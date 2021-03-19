from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
from decouple import config

driver = webdriver.Chrome('chromedriver')
driver.get("https://www.ea.com/fr-fr/fifa/ultimate-team/web-app/")

# LOGIN

login = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Login"]/div/div/button[1]')))
login.click()
email = driver.find_element_by_id("email")
email.send_keys(config("EMAIL_EA"))
time.sleep(2)
pwd = driver.find_element_by_id("password")
pwd.send_keys(config("PWD_EA"))
time.sleep(2)
driver.find_element_by_id("btnLogin").click()
time.sleep(2)
driver.find_element_by_id("btnSendCode").click()

# MARKET
time.sleep(60)
driver.find_element_by_xpath("/html/body/main/section/nav/button[3]").click()
time.sleep(5)
driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/div[2]").click()
time.sleep(2)
# SEARCH FILTER
time.sleep(2)
player = driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[1]/div/div[1]/input")
player.send_keys(config("PLAYER_NAME"))
time.sleep(1)
driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[1]/div/div[2]/ul/button").click()
time.sleep(2)
driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div/div").click()
time.sleep(2)
driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div/ul/li[4]").click()
time.sleep(2)
driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[3]/div/div").click()
time.sleep(2)
driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[3]/div/ul/li[3]").click()
time.sleep(2)
driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[2]/button[2]").click()

p = 0
while 42:    

    # SEARCH RESULTS
    time.sleep(2)
    for i in range(20):
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section[1]/div/ul/li[" + str(i + 1) + "]").click()
        if driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div/input").is_enabled() and driver.find_elements(By.XPATH, "/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div/input"):
            price = driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div/input").get_attribute('value')
            np = price.replace("\u202f", "")
            print(np)
            if int(np) <= int(config("PLAYER_PRICE_BUY")):
                driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div/input").click()
                time.sleep(1)
                buy_price = driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/div/input")
                buy_price.send_keys(config("PLAYER_PRICE_BUY"))
                time.sleep(1)
                driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section[2]/div/div/div[2]/div[2]/button[1]").click()
                p = p + 1
        if p == 5:
            break
    driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section[1]/div/div/button[2]").click()
    if p == 5:
        driver.find_element_by_xpath("/html/body/main/section/section/div[1]/button[1]").click()
        driver.find_element_by_xpath("/html/body/main/section/section/div[1]/button[1]").click()
        driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/div[4]").click()
        while driver.find_elements(By.XPATH, "/html/body/main/section/section/div[2]/div/div/div/section[1]/ul/li[1]"):
            time.sleep(5)
        driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/div/section[4]/header/button").click()
        time.sleep(5)
        while driver.find_elements(By.XPATH, "/html/body/main/section/section/div[2]/div/div/div/section[3]/ul/li[1]"):
            driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/div/section[3]/ul/li[1]").click()
            time.sleep(2)
            driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[1]/button").click()
            time.sleep(2)
            driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/input").click()
            time.sleep(2)
            min_price = driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/input")
            min_price.send_keys(config("PLAYER_PRICE_MIN_SELL"))
            driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[2]/div[3]/div[2]/input").click()
            time.sleep(2)
            min_price = driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[2]/div[3]/div[2]/input")
            min_price.send_keys(config("PLAYER_PRICE_MAX_SELL"))
            driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/section/div/div/div[2]/div[2]/div[2]/button").click()
            time.sleep(2)
        p = 0
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/main/section/nav/button[3]").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div/div[2]").click()
        time.sleep(1)
        time.sleep(2)
        player = driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[1]/div/div[1]/input")
        player.send_keys(config("PLAYER_NAME"))
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[1]/div/div[2]/ul/button").click()
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div/div").click()
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div/ul/li[4]").click()
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[3]/div/div").click()
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[1]/div[1]/div[3]/div/ul/li[3]").click()
        time.sleep(2)
        driver.find_element_by_xpath("/html/body/main/section/section/div[2]/div/div[2]/div/div[2]/button[2]").click()

