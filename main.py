# Code performing basic functionalities of web scraping and extraction
# Later version will include GUIs


import pandas as pd
import numpy as np
from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

## Information on Computer, League, Team, Years, Competition
ComputerUsername= "hsnsh"
league = "Premier League"
team= "Chelsea"    # Note, may want to scrape for exact name here later
Year= "2019-2020"
Competition="" # Dropdown menu with multiple selections
df=pd.DataFrame()

# Edit with your chrome driver executable location
path_chromedriver = r'C:\Users\{0}\OneDrive\Documents\chromedriver_win32\chromedriver.exe'.format(ComputerUsername)
driver = webdriver.Chrome(executable_path=path_chromedriver)

driver.get('https://fbref.com/en/squads/cff3d9bb/{0}/{1}-Stats'.format(Year, team))
a=driver.find_elements_by_xpath('//table[@class="stats_table sortable min_width now_sortable sticky_table eq1 re1 le1" and @id = "matchlogs_for"]//tbody//tr//th//a[@href]')

links=[]
for elem in a:
    links.append(elem.get_attribute("href"))

x=0
for link in links:
    x+=1
    driver.get(link)
    if x>2:
        break
#driver.findElement(by.xpath("//a[@href='/docs/configuration']")).click();

driver.get("https://fbref.com/en/matches/4a69dd20/Liverpool-Chelsea-August-14-2019-UEFA-Super-Cup")

rowDate=["Date",driver.find_element_by_xpath('//span[@class="venuetime"]').get_attribute("data-venue-date"),""]
objectDate={"Date",driver.find_element_by_xpath('//span[@class="venuetime"]').get_attribute("data-venue-date"),""}
rowCompetition = ["Competition", driver.find_element_by_xpath('//div[@class="scorebox_meta"]//div[2]//a').get_attribute('text'),""]
rowReferee = ["Referee", driver.find_element_by_xpath('//div[@class="scorebox_meta"]//div[7]//small//span[1]').text,""]

TeamA=driver.find_element_by_xpath('//div[@class="scorebox"]//div[1]//div//strong//a').get_attribute('text')
TeamB=driver.find_element_by_xpath('//div[@class="scorebox"]//div[2]//div//strong//a').get_attribute('text')
rowTeams=["",TeamA,TeamB]

rowScore=["", driver.find_element_by_xpath('//div[@class="scorebox"]//div[1]//div[@class="scores"]//div[1]').text,\
          driver.find_element_by_xpath('//div[@class="scorebox"]//div[2]//div[@class="scores"]//div[1]').text]

PenXg=driver.find_element_by_xpath('//div[@class="scorebox"]//div[@class="scores"]//div[2]').get_attribute('class')
if (PenXg == "score_pen"):
    PenXg="Penalties"
elif PenXg ==  "score_xg":
    PenXg = "xg"
else: PenXg = "Other"
rowPenXg =[PenXg,driver.find_element_by_xpath('//div[@class="scorebox"]//div[1]//div[@class="scores"]//div[2]').text,\
           driver.find_element_by_xpath('//div[@class="scorebox"]//div[2]//div[@class="scores"]//div[2]').text]

rowManager=["Manager",driver.find_element_by_xpath('//div[@class="scorebox"]//div[1]//div[4]').text.replace("Manager: ",''),\
            driver.find_element_by_xpath('//div[@class="scorebox"]//div[2]//div[4]').text.replace("Manager: ",'')]
rowCaptain=["Captain",driver.find_element_by_xpath('//div[@class="scorebox"]//div[1]//div[5]').text.replace("Captain: ",''),\
            driver.find_element_by_xpath('//div[@class="scorebox"]//div[2]//div[5]').text.replace("Captain: ",'')]
rowEmpty=['']

rowFormation=["Formations",driver.find_element_by_xpath('//div[@class="lineup" and @id="a"]//th[@colspan="2"]').text,\
              driver.find_element_by_xpath('//div[@class="lineup" and @id="b"]//th[@colspan="2"]').text]
#df=pd.concat(rowDate,rowCompetition,rowReferee,rowTeams,rowScore,rowPenXg,rowManager,rowCaptain,rowEmpty)



