from selenium import webdriver
from time import sleep # To prevent overwhelming the server between connections
from collections import Counter # Keep track of our term counts
from nltk.corpus import stopwords # Filter out stopwords, such as 'the', 'or', 'and'
import pandas as pd # For converting results to a dataframe and bar chart plots
from selenium.webdriver.common import action_chains, keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import pickle
import re
import csv
import json
import os.path
import warnings
import pandas as pd
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

def init_driver():
    ''' Initialize chrome driver'''

    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    #chrome_options.add_argument('--user-data-dir=C:\\Users\\\\AppData\\Local\\Google\\Chrome\\User Data')
    ##chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--start-maximized")
    #browser = webdriver.Chrome(driver, chrome_options=chrome_options)
    browser = webdriver.Chrome(chrome_options=chrome_options)
    #browser = webdriver.Chrome()

    return browser

website = "https://www.glassdoor.com/index.htm"

browser = init_driver()
browser.get(website)

linkData = pd.read_json('linkDataAll.json')
final_jobDict = {}

for index, row in linkData.iterrows():
    try:
        job_id = row['job_id']
        link = row['link']
        sleep(1)
        browser.get(link)
        sleep(1)
        final_jobDict[job_id] = [job_id]
        final_jobDict[job_id].append(link)
        job_description = browser.find_element_by_xpath('//*[@id="JobDescriptionContainer"]/div/div').text           
        final_jobDict[job_id].append(job_description)
    except Exception as e:
        job_description = ''
        final_jobDict[job_id].append(job_description)
        print('this is error message for job_id:  ', job_id, type(e),e)
        continue


finalDF = pd.DataFrame(list(final_jobDict.values()), columns=['job_id', 'link', 'job_description'])
finalDF.to_json('fullDataAll.json')
    

browser.close()
    