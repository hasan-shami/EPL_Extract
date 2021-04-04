from selenium import webdriver



import constants
from WebdriverOperations import initializeWebDriver, GetLinks, MatchSummary
from outputFileWrite import writeToExcel

driver=initializeWebDriver()
driver=driver.setDriver()
x=GetLinks(constants.Year,constants.team,driver)
links=x.obtainLinks()

x=0
for link in links:
    x+=1
    match=MatchSummary(link,driver)
    match.setInfo()
    output=writeToExcel(match)
    output.FormatAndExport()
    if x>10:
        break



