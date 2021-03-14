# Code performing basic functionalities of web scraping and extraction
# Later version will include GUIs

from selenium import webdriver
import xlsxwriter
from datetime import datetime
import pandas as pd
from selenium.common.exceptions import NoSuchElementException


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
    links.append(elem.get_attribute("href")) # Get links of all matches

x=0
for link in links: # to iterate through all links of matches
    x+=1 # We're only getting the data for a few matches now
    driver.get(link)

    matchDate = driver.find_element_by_xpath('//span[@class="venuetime"]').get_attribute("data-venue-date")
    matchCompetition = driver.find_element_by_xpath('//div[@class="scorebox_meta"]//div[2]//a').get_attribute('text')
    matchReferee = driver.find_element_by_xpath('//div[@class="scorebox_meta"]//div[7]//small//span[1]').text

    TeamA = driver.find_element_by_xpath('//div[@class="scorebox"]//div[1]//div//strong//a').get_attribute('text')
    TeamB = driver.find_element_by_xpath('//div[@class="scorebox"]//div[2]//div//strong//a').get_attribute('text')

    rowScore = ["", driver.find_element_by_xpath('//div[@class="scorebox"]//div[1]//div[@class="scores"]//div[1]').text, \
                driver.find_element_by_xpath('//div[@class="scorebox"]//div[2]//div[@class="scores"]//div[1]').text]

    try:
        driver.find_element_by_xpath('//div[@class="scorebox"]//div[@class="scores"]//div[2]').click()
        PenXg = driver.find_element_by_xpath('//div[@class="scorebox"]//div[@class="scores"]//div[2]').get_attribute('class')
        if (PenXg == "score_pen"):
            PenXg = "Penalties"
        elif PenXg == "score_xg":
            PenXg = "xg"
        else:
            PenXg = "Other"
        rowPenXg = [PenXg,
                    driver.find_element_by_xpath('//div[@class="scorebox"]//div[1]//div[@class="scores"]//div[2]').text, \
                    driver.find_element_by_xpath('//div[@class="scorebox"]//div[2]//div[@class="scores"]//div[2]').text]

    except NoSuchElementException:
        print('Xg for {0} not found'.format('{0}-{1}-{2}'.format(matchDate, TeamA, TeamB)))
        rowPenXg=["xg","",""]

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

    filepath='{0}-{1}-{2}.xlsx'.format(matchDate, TeamA, TeamB)
    workbook = xlsxwriter.Workbook(filepath)
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

    worksheet.set_column('A:A', 12)
    worksheet.set_column('B:B', 22)
    worksheet.set_column('C:C', 22)

    row = 15
    col = 1
    i=0
    worksheet.write(row, col - 1, "Starting XI")
    for player in PlayerListA:
        i+=1
        worksheet.write(row, col, player)
        row += 1

        if (i==11):
            worksheet.write(row,col,'')
            row += 1
            worksheet.write(row,col-1, "Bench")
    row = 15
    col = 2

    j=0
    for player in PlayerListB:
        j += 1
        worksheet.write(row, col, player)
        row += 1

        if (j == 11):
            worksheet.write(row, col, '')
            row += 1

    PlayerNamesA = driver.find_elements_by_xpath\
        ('//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//th//a')
    PlayerNamesB = driver.find_elements_by_xpath\
        ('//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//th//a')
    list_PlayerNamesA=[]
    list_PlayerNamesB=[]

    NumbersA=driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[1]')
    NumbersB= driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[1]')
    list_NumbersA=[]
    list_NumbersB=[]

    NationalityA= driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[2]//a') #note: get last 3 characters only
    NationalityB = driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[2]//a')  # note: get last 3 characters only
    list_NationalityA=[]
    list_NationalityB=[]

    PositionA= driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[3]')
    PositionB= driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[3]')
    list_PositionA=[]
    list_PositionB=[]


    AgeA= driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[4]')
    AgeB= driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[4]')
    list_AgeA=[]
    list_AgeB=[]

    MinutesA= driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[5]')
    MinutesB = driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[5]')
    list_MinutesA=[]
    list_MinutesB=[]

    GoalsA= driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[6]')
    GoalsB= driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[6]')
    list_GoalsA=[]
    list_GoalsB=[]

    AssistsA=driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[7]')
    AssistsB=driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[7]')
    list_AssistsA=[]
    list_AssistsB=[]

    PkA=driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[8]')
    PkB=driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[8]')
    list_PkA=[]
    list_PkB=[]

    PKattA=driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[9]')
    PKattB=driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[9]')
    list_PKattA=[]
    list_PKattB=[]

    ShotsA=driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[10]')
    ShotsB=driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[10]')
    list_ShotsA=[]
    list_ShotsB=[]

    ShotsOnTargetA= driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[11]')
    ShotsOnTargetB= driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[11]')
    list_ShotsOnTargetA=[]
    list_ShotsOnTargetB=[]

    YellowCardsA=driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[12]')
    YellowCardsB=driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[12]')
    list_YellowCardsA=[]
    list_YellowCardsB=[]

    RedCardsA=driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[13]')
    RedCardsB=driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[13]')
    list_RedCardsA=[]
    list_RedCardsB=[]

    TouchesA=driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[14]')
    TouchesB=driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[14]')
    list_TouchesA=[]
    list_TouchesB=[]

    PressuresA=driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[15]')
    PressuresB=driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[15]')
    list_PressA=[]
    list_PressB=[]

    TacklesA=driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[16]')
    TacklesB=driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[16]')
    list_TacklesA=[]
    list_TacklesB=[]

    InterceptionsA=driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[17]')
    InterceptionsB=driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[17]')
    list_InterceptionsA=[]
    list_InterceptionsB=[]

    BlocksA=driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[18]')
    BlocksB=driver.find_elements_by_xpath \
        ('//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[18]')
    list_BlocksA=[]
    list_BlocksB=[]

    for player in range(len(PlayerNamesA)):
        list_PlayerNamesA.append(PlayerNamesA[player].text)
        list_NumbersA.append(NumbersA[player].text)
        list_NationalityA.append(NationalityA[player].text[-3:]) #only last 3 characters
        list_PositionA.append(PositionA[player].text)
        list_AgeA.append(AgeA[player].text)
        list_MinutesA.append(MinutesA[player].text)
        list_GoalsA.append(GoalsA[player].text)
        list_AssistsA.append(AssistsA[player].text)
        list_PkA.append(PkA[player].text)
        list_PKattA.append(PKattA[player].text)
        list_ShotsA.append(ShotsA[player].text)
        list_ShotsOnTargetA.append(ShotsOnTargetA[player].text)
        list_YellowCardsA.append(YellowCardsA[player].text)
        list_RedCardsA.append(RedCardsA[player].text)
        list_TouchesA.append(TouchesA[player].text)
        list_PressA.append(PressuresA[player].text)
        list_TacklesA.append(TacklesA[player].text)
        list_InterceptionsA.append(InterceptionsA[player].text)
        list_BlocksA.append(BlocksA[player].text)

    for player in range(len(PlayerNamesB)):
        list_PlayerNamesB.append(PlayerNamesB[player].text)
        list_NumbersB.append(NumbersB[player].text)
        list_NationalityB.append(NationalityB[player].text[-3:]) #only last 3 characters
        list_PositionB.append(PositionB[player].text)
        list_AgeB.append(AgeB[player].text)
        list_MinutesB.append(MinutesB[player].text)
        list_GoalsB.append(GoalsB[player].text)
        list_AssistsB.append(AssistsB[player].text)
        list_PkB.append(PkB[player].text)
        list_PKattB.append(PKattB[player].text)
        list_ShotsB.append(ShotsB[player].text)
        list_ShotsOnTargetB.append(ShotsOnTargetB[player].text)
        list_YellowCardsB.append(YellowCardsB[player].text)
        list_RedCardsB.append(RedCardsB[player].text)
        list_TouchesB.append(TouchesB[player].text)
        list_PressB.append(PressuresB[player].text)
        list_TacklesB.append(TacklesB[player].text)
        list_InterceptionsB.append(InterceptionsB[player].text)
        list_BlocksB.append(BlocksB[player].text)

    columnList=['Name', '#','Nation' ,'POS','Age','MinutesPlayed','Goals','Assists','PK','PKatt',\
                'Shots','ShotsOnTarget','YellowCards','RedCards','Touches','Pressures','Tackles',\
                'Interceptions','Blocks']
    dfA=pd.DataFrame(data=list(zip(list_PlayerNamesA,list_NumbersA,list_NationalityA,list_PositionA,list_AgeA, \
                                  list_MinutesA, list_GoalsA,list_AssistsA, list_PkA,list_PKattA ,list_ShotsA, \
                                  list_ShotsOnTargetA, list_YellowCardsA, list_RedCardsA, list_TouchesA,list_PressA, \
                                  list_TacklesA, list_InterceptionsA, list_BlocksA)),columns=columnList)

    dfB=pd.DataFrame(data=list(zip(list_PlayerNamesB,list_NumbersB,list_NationalityB,list_PositionB,list_AgeB, \
                                  list_MinutesB, list_GoalsB,list_AssistsB, list_PkB,list_PKattB ,list_ShotsB, \
                                  list_ShotsOnTargetB, list_YellowCardsB, list_RedCardsB, list_TouchesB,list_PressB, \
                                  list_TacklesB, list_InterceptionsB, list_BlocksB)),columns=columnList)


    writer=pd.ExcelWriter(filepath,engine='xlsxwriter')
    writer.book=workbook
    dfA.to_excel(writer,sheet_name='{0} Stats'.format(TeamA),index=False)
    dfB.to_excel(writer,sheet_name='{0} Stats'.format(TeamB),index=False)

    worksheetA=writer.sheets['{0} Stats'.format(TeamA)]
    worksheetA.set_column('A:A',21)

    worksheetB=writer.sheets['{0} Stats'.format(TeamB)]
    worksheetB.set_column('A:A',21)

    writer.save()
    writer.close()
    workbook.close()


    if x > 20:  #specify number of matches you want to extract here: testing purposes
        break



