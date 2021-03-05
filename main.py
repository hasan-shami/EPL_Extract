# Code performing basic functionalities of web scraping and extraction
# Later version will include GUIs


import pandas as pd
import numpy as np
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

## Information on Computer, League, Team, Years, Competition
ComputerUsername= "hsnsh"
league = "Premier League"
team= "Chelsea"    # Note, may want to scrape for exact name here later
Year= "2019-2020"
Competition="" # Dropdown menu with multiple selections



# Edit with your chrome driver executable location
path_chromedriver = r'C:\Users\{0}\Documents\chromedriver-win32\chromedriver.exe'.format(ComputerUsername)
driver = webdriver.Chrome(executable_path=path_chromedriver)

driver.get('https://fbref.com/en/squads/cff3d9bb/{0}/{1}-Stats'.format(Year, team))





