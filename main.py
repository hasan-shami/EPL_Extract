# Code performing basic functionalities of web scraping and extraction
# Later version will include GUIs


from selenium import webdriver
import xlsxwriter
from datetime import datetime
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

## Information on Computer, League, Team, Years, Competition
ComputerUsername= "hsnsh"
league = "Premier League"
team= "Chelsea"    # Note, may want to scrape for exact name here later
Year= "2019-2020"
Competition="" # Dropdown menu with multiple selections, when GUI is implemented

# Edit with your chrome driver executable location
path_chromedriver = r'C:\Users\{0}\OneDrive\Documents\chromedriver_win32\chromedriver.exe'.format(ComputerUsername)
driver = webdriver.Chrome(executable_path=path_chromedriver)

driver.get('https://fbref.com/en/squads/cff3d9bb/{0}/{1}-Stats'.format(Year, team))
a=driver.find_elements_by_xpath('//table[@class="stats_table sortable min_width now_sortable sticky_table eq1 re1 le1" and @id = "matchlogs_for"]//tbody//tr//th//a[@href]')


links=[]
for elem in a:
    links.append(elem.get_attribute("href"))

x=0
for link in links: #to iterate through all links of matches
    x+=1 # We're only getting the data for a few matches now
    driver.get(link)

    matchDate = driver.find_element_by_xpath('//span[@class="venuetime"]').get_attribute("data-venue-date")
    matchCompetition = driver.find_element_by_xpath('//div[@class="scorebox_meta"]//div[2]//a').get_attribute('text')
    matchReferee = driver.find_element_by_xpath('//div[@class="scorebox_meta"]//div[7]//small//span[1]').text

    TeamA = driver.find_element_by_xpath('//div[@class="scorebox"]//div[1]//div//strong//a').get_attribute('text')
    TeamB = driver.find_element_by_xpath('//div[@class="scorebox"]//div[2]//div//strong//a').get_attribute('text')

    rowScore = ["", driver.find_element_by_xpath('//div[@class="scorebox"]//div[1]//div[@class="scores"]//div[1]').text, \
                driver.find_element_by_xpath('//div[@class="scorebox"]//div[2]//div[@class="scores"]//div[1]').text]

    PenXg = driver.find_element_by_xpath('//div[@class="scorebox"]//div[@class="scores"]//div[2]').get_attribute(
        'class')
    if (PenXg == "score_pen"):
        PenXg = "Penalties"
    elif PenXg == "score_xg":
        PenXg = "xg"
    else:
        PenXg = "Other"

    rowPenXg = [PenXg,
                driver.find_element_by_xpath('//div[@class="scorebox"]//div[1]//div[@class="scores"]//div[2]').text, \
                driver.find_element_by_xpath('//div[@class="scorebox"]//div[2]//div[@class="scores"]//div[2]').text]

    rowManager = ["Manager",
                  driver.find_element_by_xpath('//div[@class="scorebox"]//div[1]//div[@class="datapoint"][1]').text.replace("Manager: ",''), \
                  driver.find_element_by_xpath('//div[@class="scorebox"]//div[2]//div[@class="datapoint"][1]').text.replace("Manager: ",'')]

    rowCaptain = ["Captain",driver.find_element_by_xpath('//div[@class="scorebox"]//div[1]//div[@class="datapoint"][2]').text.replace("Captain: ",''), \
                  driver.find_element_by_xpath('//div[@class="scorebox"]//div[2]//div[@class="datapoint"][2]').text.replace("Captain: ",'')]
    rowEmpty = ['']
    rowFormation = ["Formations",driver.find_element_by_xpath('//div[@class="lineup" and @id="a"]//th[@colspan="2"]').text, \
                    driver.find_element_by_xpath('//div[@class="lineup" and @id="b"]//th[@colspan="2"]').text]

    LineupsA = driver.find_elements_by_xpath('//div[@class="lineup" and @id="a"]//table//tbody//tr//a')
    LineupsB = driver.find_elements_by_xpath('//div[@class="lineup" and @id="b"]//table//tbody//tr//a')
    PlayerListA = []
    PlayerListB = []

    for player in LineupsA:
        PlayerListA.append(player.get_attribute('text'))

    for player in LineupsB:
        PlayerListB.append(player.get_attribute('text'))

    rowPosession = ["Posession",
                    driver.find_element_by_xpath('//div[@id="team_stats"]//tbody//tr[3]//td[1]//div//div[1]').text, \
                    driver.find_element_by_xpath('//div[@id="team_stats"]//tbody//tr[3]//td[2]//div//div[1]').text]
    rowPasses = ["Passing Accuracy",
                 driver.find_element_by_xpath('//div[@id="team_stats"]//tbody//tr[5]//td[1]//div//div[1]').text, \
                 driver.find_element_by_xpath('//div[@id="team_stats"]//tbody//tr[5]//td[2]//div//div[1]').text]
    rowShots = ["Shots on Target",
                driver.find_element_by_xpath('//div[@id="team_stats"]//tbody//tr[7]//td[1]//div//div[1]').text, \
                driver.find_element_by_xpath('//div[@id="team_stats"]//tbody//tr[7]//td[2]//div//div[1]').text]

    workbook = xlsxwriter.Workbook('{0}-{1}-{2}.xlsx'.format(matchDate, TeamA, TeamB))
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': 1})
    worksheet.write('A1', "Date", bold)
    date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})
    date_formatted = datetime.strptime(matchDate, "%Y-%m-%d")
    worksheet.write_datetime('B1', date_formatted, date_format)
    worksheet.write('A2', 'Competition', bold)
    worksheet.write('B2', matchCompetition)
    worksheet.write('A3', 'Referee', bold)
    worksheet.write('B3', matchReferee)
    worksheet.write('B4', TeamA, bold)
    worksheet.write('C4', TeamB, bold)
    worksheet.write('B5', rowScore[1])
    worksheet.write('C5', rowScore[2])
    worksheet.write('A6', PenXg, bold)
    worksheet.write('B6', rowPenXg[1])
    worksheet.write('C6', rowPenXg[2])
    worksheet.write('A7', "Manager", bold)
    worksheet.write('B7', rowManager[1])
    worksheet.write('C7', rowManager[2])
    worksheet.write('A8', 'Captain', bold)
    worksheet.write('B8', rowCaptain[1])
    worksheet.write('C8', rowCaptain[2])
    worksheet.write('A10', 'Posession', bold)
    worksheet.write('B10', rowPosession[1])
    worksheet.write('C10', rowPosession[2])
    worksheet.write('A11', 'Passing', bold)
    worksheet.write('B11', rowPasses[1])
    worksheet.write('C11', rowPasses[2])
    worksheet.write('A12', 'Shots', bold)
    worksheet.write('B12', rowShots[1])
    worksheet.write('C12', rowShots[2])
    worksheet.write('A14', 'Formations', bold)
    worksheet.write('B14', rowFormation[1])
    worksheet.write('C14', rowFormation[2])

    row = 15
    col = 1
    for player in PlayerListA:
        worksheet.write(row, col, player)
        row += 1
    row = 15
    col = 2
    for player in PlayerListB:
        worksheet.write(row, col, player)
        row += 1

    workbook.close()
    if x>4:
        break





