import streamlit as st
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import csv
import os
from pathlib import Path


#from selenium.webdriver.chrome.service import Service as ChromiumService
#from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType





from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)

file_path = os.getcwd()
try:
    os.mkdir(os.path.join(file_path, f"Files"))
except:
    pass


def create_file():
    f = open(f'./Files/prod_img.csv', 'w', newline='')
    header = ["Product Name", "Image"]
    writer = csv.writer(f)
    writer.writerow(header)
    f.close()

def add_to_file(data):
    f = open(f'./Files/prod_img.csv', 'a', newline='')
    writer = csv.writer(f)
    writer.writerow(data)
    f.close()


create_file()

cwd = os.getcwd() # Current Path

files = [f for f in os.listdir('.') if os.path.isfile(f)]


#import stat
#stt = os.stat("./chromedriver")
#os.chmod("./chromedriver", stt.st_mode | stat.S_IEXEC)

#PATH = "./chromedriver"
options = wd.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-features=NetworkService")
options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-features=VizDisplayCompositor")
st.title("Image Web Scrapper")
items = st.text_area("Enter product values:")
errs = []
if st.button("Get data"):
    items = items.split("\n")
    for item in items:
        
        st.write(item)
        driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
        #driver = wd.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get("https://images.google.com/")
        search_bar = driver.find_element(By.NAME, "q")
        search_bar.clear()
        search_bar.send_keys(item)
        try:
            search_bar.send_keys(Keys.ENTER)
        except:
            pass
        sleep(2)
        cnt = 0
        while True:
            src_stri = "//div[@data-ri=" + str(cnt) + "]"
            try:
                driver.find_element(By.XPATH, src_stri).click()
            except:
                errs.append(item)
            sleep(5)
            try:
                req = driver.find_element(By.XPATH, "//img[@class='n3VNCb KAlRDb']")
            except:
                req = driver.find_element(By.XPATH, "//*[@id='Sva75c']/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img")
            final = req.get_attribute("src")
            if "https://" in final:
                break
            else:
                cnt += 1
        add_to_file([item, final])
        st.write(final)
        driver.quit()
        
        
    st.balloons()
    st.download_button("Download File", open("./Files/prod_img.csv", "r"), file_name = "Products_file.csv", mime = "text/csv")
    if len(errs) > 0:
        st.error("Un successful Searches list as follows")
        st.text(errs)
    
    st.stop()
