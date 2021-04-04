import constants
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd


class initializeWebDriver():
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=constants.path_chromedriver)

    def setDriver(self):
        driver = self.driver
        return driver


class GetLinks(initializeWebDriver):
    # driver=webdriver.Chrome(executable_path=constants.path_chromedriver)

    def __init__(self, year, team, driver):
        self.year = year
        self.team = team
        self.driver = driver
        self.driver.get('https://fbref.com/en/squads/cff3d9bb/{0}/{1}-Stats'.format(year, team))

    def obtainLinks(self):
        driver = self.driver
        a = driver.find_elements_by_xpath('//table[@id = "matchlogs_for"]//tbody//tr//th//a[@href]')

        links = []
        for elem in a:
            links.append(elem.get_attribute("href"))  # Get links of all matches
        return links


class MatchSummary:  # call this for every match
    def __init__(self, link, driver):
        self.link = link
        self.driver = driver
        self.driver.get(link)


    def setInfo(self):
        driver = self.driver
        self.matchDate = driver.find_element_by_xpath('//span[@class="venuetime"]').get_attribute("data-venue-date")
        self.matchCompetition = driver.find_element_by_xpath('//div[@class="scorebox_meta"]//div[2]//a').get_attribute(
            'text')
        self.matchReferee = driver.find_element_by_xpath('//div[@class="scorebox_meta"]//div[7]//small//span[1]').text

        self.TeamA = driver.find_element_by_xpath('//div[@class="scorebox"]//div[1]//div//strong//a').get_attribute('text')
        self.TeamB = driver.find_element_by_xpath('//div[@class="scorebox"]//div[2]//div//strong//a').get_attribute('text')

        self.rowScore = ["",
                    driver.find_element_by_xpath('//div[@class="scorebox"]//div[1]//div[@class="scores"]//div[1]').text, \
                    driver.find_element_by_xpath('//div[@class="scorebox"]//div[2]//div[@class="scores"]//div[1]').text]

        try:
            driver.find_element_by_xpath('//div[@class="scorebox"]//div[@class="scores"]//div[2]').click()
            self.PenXg = driver.find_element_by_xpath(
                '//div[@class="scorebox"]//div[@class="scores"]//div[2]').get_attribute('class')
            if (self.PenXg == "score_pen"):
                self.PenXg = "Penalties"
            elif self.PenXg == "score_xg":
                self.PenXg = "xg"
            else:
                self.PenXg = "Other"
            self.rowPenXg = [self.PenXg,
                        driver.find_element_by_xpath(
                            '//div[@class="scorebox"]//div[1]//div[@class="scores"]//div[2]').text, \
                        driver.find_element_by_xpath(
                            '//div[@class="scorebox"]//div[2]//div[@class="scores"]//div[2]').text]

        except NoSuchElementException:
            print('Xg for {0} not found'.format('{0}-{1}-{2}'.format(self.matchDate, self.TeamA, self.TeamB)))
            self.rowPenXg = ["xg", "", ""]

        self.rowManager = ["Manager",
                      driver.find_element_by_xpath(
                          '//div[@class="scorebox"]//div[1]//div[@class="datapoint"][1]').text.replace("Manager: ", ''), \
                      driver.find_element_by_xpath(
                          '//div[@class="scorebox"]//div[2]//div[@class="datapoint"][1]').text.replace("Manager: ", '')]

        self.rowCaptain = ["Captain", driver.find_element_by_xpath(
            '//div[@class="scorebox"]//div[1]//div[@class="datapoint"][2]').text.replace("Captain: ", ''), \
                      driver.find_element_by_xpath(
                          '//div[@class="scorebox"]//div[2]//div[@class="datapoint"][2]').text.replace("Captain: ", '')]
        self.rowEmpty = ['']
        self.rowFormation = ["Formations",
                        driver.find_element_by_xpath('//div[@class="lineup" and @id="a"]//th[@colspan="2"]').text, \
                        driver.find_element_by_xpath('//div[@class="lineup" and @id="b"]//th[@colspan="2"]').text]

        self.LineupsA = driver.find_elements_by_xpath('//div[@class="lineup" and @id="a"]//table//tbody//tr//a')
        self.LineupsB = driver.find_elements_by_xpath('//div[@class="lineup" and @id="b"]//table//tbody//tr//a')
        self.PlayerListA = []
        self.PlayerListB = []

        for player in self.LineupsA:
            self.PlayerListA.append(player.get_attribute('text'))

        for player in self.LineupsB:
            self.PlayerListB.append(player.get_attribute('text'))

        self.rowPosession = ["Posession",
                        driver.find_element_by_xpath('//div[@id="team_stats"]//tbody//tr[3]//td[1]//div//div[1]').text, \
                        driver.find_element_by_xpath('//div[@id="team_stats"]//tbody//tr[3]//td[2]//div//div[1]').text]
        self.rowPasses = ["Passing Accuracy",
                     driver.find_element_by_xpath('//div[@id="team_stats"]//tbody//tr[5]//td[1]//div//div[1]').text, \
                     driver.find_element_by_xpath('//div[@id="team_stats"]//tbody//tr[5]//td[2]//div//div[1]').text]
        self.rowShots = ["Shots on Target",
                    driver.find_element_by_xpath('//div[@id="team_stats"]//tbody//tr[7]//td[1]//div//div[1]').text, \
                    driver.find_element_by_xpath('//div[@id="team_stats"]//tbody//tr[7]//td[2]//div//div[1]').text]

        self.PlayerNamesA = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//th//a')
        self.PlayerNamesB = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//th//a')
        self.list_PlayerNamesA = []
        self.list_PlayerNamesB = []

        self.NumbersA = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[1]')
        self.NumbersB = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[1]')
        self.list_NumbersA = []
        self.list_NumbersB = []

        self.NationalityA = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[2]//a')  # note: get last 3 characters only
        self.NationalityB = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[2]//a')  # note: get last 3 characters only
        self.list_NationalityA = []
        self.list_NationalityB = []

        self.PositionA = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[3]')
        self.PositionB = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[3]')
        self.list_PositionA = []
        self.list_PositionB = []

        self.AgeA = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[4]')
        self.AgeB = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[4]')
        self.list_AgeA = []
        self.list_AgeB = []

        self.MinutesA = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[5]')
        self.MinutesB = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[5]')
        self.list_MinutesA = []
        self.list_MinutesB = []

        self.GoalsA = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[6]')
        self.GoalsB = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[6]')
        self.list_GoalsA = []
        self.list_GoalsB = []

        self.AssistsA = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[7]')
        self.AssistsB = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[7]')
        self.list_AssistsA = []
        self.list_AssistsB = []

        self.PkA = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[8]')
        self.PkB = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[8]')
        self.list_PkA = []
        self.list_PkB = []

        self.PKattA = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[9]')
        self.PKattB = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[9]')
        self.list_PKattA = []
        self.list_PKattB = []

        self.ShotsA = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[10]')
        self.ShotsB = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[10]')
        self.list_ShotsA = []
        self.list_ShotsB = []

        self.ShotsOnTargetA = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[11]')
        self.ShotsOnTargetB = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[11]')
        self.list_ShotsOnTargetA = []
        self.list_ShotsOnTargetB = []

        self.YellowCardsA = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[12]')
        self.YellowCardsB = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[12]')
        self.list_YellowCardsA = []
        self.list_YellowCardsB = []

        self.RedCardsA = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[13]')
        self.RedCardsB = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[13]')
        self.list_RedCardsA = []
        self.list_RedCardsB = []

        self.TouchesA = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[14]')
        self.TouchesB = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[14]')
        self.list_TouchesA = []
        self.list_TouchesB = []

        self.PressuresA = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[15]')
        self.PressuresB = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[15]')
        self.list_PressA = []
        self.list_PressB = []

        self.TacklesA = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[16]')
        self.TacklesB = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[16]')
        self.list_TacklesA = []
        self.list_TacklesB = []

        self.InterceptionsA = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[17]')
        self.InterceptionsB = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[17]')
        self.list_InterceptionsA = []
        self.list_InterceptionsB = []

        self.BlocksA = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][1]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[18]')
        self.BlocksB = driver.find_elements_by_xpath \
                (
                '//div[contains(@id,"all_player_stats")][2]//div[contains(@id,"div_stats")]//table[contains(@id,"stats") and contains(@id,"summary")]//tbody//td[18]')
        self.list_BlocksA = []
        self.list_BlocksB = []

        for player in range(len(self.PlayerNamesA)):
            self.list_PlayerNamesA.append(self.PlayerNamesA[player].text)
            self.list_NumbersA.append(self.NumbersA[player].text)
            self. list_NationalityA.append(self.NationalityA[player].text[-3:])  # only last 3 characters
            self.list_PositionA.append(self.PositionA[player].text)
            self.list_AgeA.append(self.AgeA[player].text)
            self.list_MinutesA.append(self.MinutesA[player].text)
            self.list_GoalsA.append(self.GoalsA[player].text)
            self.list_AssistsA.append(self.AssistsA[player].text)
            self.list_PkA.append(self.PkA[player].text)
            self.list_PKattA.append(self.PKattA[player].text)
            self.list_ShotsA.append(self.ShotsA[player].text)
            self.list_ShotsOnTargetA.append(self.ShotsOnTargetA[player].text)
            self.list_YellowCardsA.append(self.YellowCardsA[player].text)
            self.list_RedCardsA.append(self.RedCardsA[player].text)
            self.list_TouchesA.append(self.TouchesA[player].text)
            self.list_PressA.append(self.PressuresA[player].text)
            self.list_TacklesA.append(self.TacklesA[player].text)
            self.list_InterceptionsA.append(self.InterceptionsA[player].text)
            self.list_BlocksA.append(self.BlocksA[player].text)

        for player in range(len(self.PlayerNamesB)):
            self.list_PlayerNamesB.append(self.PlayerNamesB[player].text)
            self.list_NumbersB.append(self.NumbersB[player].text)
            self.list_NationalityB.append(self.NationalityB[player].text[-3:])  # only last 3 characters
            self.list_PositionB.append(self.PositionB[player].text)
            self.list_AgeB.append(self.AgeB[player].text)
            self.list_MinutesB.append(self.MinutesB[player].text)
            self.list_GoalsB.append(self.GoalsB[player].text)
            self.list_AssistsB.append(self.AssistsB[player].text)
            self.list_PkB.append(self.PkB[player].text)
            self.list_PKattB.append(self.PKattB[player].text)
            self.list_ShotsB.append(self.ShotsB[player].text)
            self.list_ShotsOnTargetB.append(self.ShotsOnTargetB[player].text)
            self.list_YellowCardsB.append(self.YellowCardsB[player].text)
            self.list_RedCardsB.append(self.RedCardsB[player].text)
            self.list_TouchesB.append(self.TouchesB[player].text)
            self.list_PressB.append(self.PressuresB[player].text)
            self.list_TacklesB.append(self.TacklesB[player].text)
            self.list_InterceptionsB.append(self.InterceptionsB[player].text)
            self.list_BlocksB.append(self.BlocksB[player].text)

    def getMatchDate(self):
        return self.matchDate

    def getTeamA(self):
        return self.TeamA

    def getTeamB(self):
        return self.TeamB

    def getmatchCompetition(self):
        return self.matchCompetition

    def getmatchReferee(self):
        return self.matchReferee

    def getrowScore(self):
        return self.rowScore

    def getPenXg(self):
        return self.PenXg

    def getrowPenXg(self):
        return self.rowPenXg

    def getrowManager(self):
        return self.rowManager

    def getrowCaptain(self):
        return self.rowCaptain

    def getrowPosession(self):
        return self.rowPosession

    def getrowPasses(self):
        return self.rowPasses

    def getrowShots(self):
        return self.rowShots

    def getrowFormation(self):
        return self.rowFormation

    def getPlayerListA(self):
        return self.PlayerListA

    def getPlayerListB(self):
        return self.PlayerListB

    def getlist_PlayerNamesA(self):
        return self.list_PlayerNamesA

    def getlist_NumbersA(self):
        return self.list_NumbersA\

    def getlist_NationalityA(self):
        return self.list_NationalityA

    def getlist_PositionA(self):
        return self.list_PositionA

    def getlist_AgeA(self):
        return self.list_AgeA

    def getlist_MinutesA(self):
        return self.list_MinutesA

    def getlist_GoalsA(self):
        return self.list_GoalsA

    def getlist_AssistsA(self):
        return self.list_AssistsA

    def getlist_PkA(self):
        return self.list_PkA

    def getlist_PKattA(self):
        return self.list_PKattA

    def getlist_ShotsA(self):
        return self.list_ShotsA

    def getlist_ShotsOnTargetA(self):
        return self.list_ShotsOnTargetA

    def getlist_YellowCardsA(self):
        return self.list_YellowCardsA

    def getlist_RedCardsA(self):
        return self.list_RedCardsA

    def getlist_TouchesA(self):
        return self.list_TouchesA
    def getlist_PressA(self):
        return self.list_PressA

    def getlist_TacklesA(self):
        return self.list_TacklesA

    def getlist_InterceptionsA(self):
        return self.list_InterceptionsA

    def getlist_BlocksA(self):
        return self.list_BlocksA

    def getlist_PlayerNamesB(self):
       return self.list_PlayerNamesB

    def getlist_NumbersB(self):
       return self.list_NumbersB

    def getlist_NationalityB(self):
       return self.list_NationalityB

    def getlist_PositionB(self):
       return self.list_PositionB

    def getlist_AgeB(self):
       return self.list_AgeB

    def getlist_MinutesB(self):
       return self.list_MinutesB

    def getlist_GoalsB(self):
       return self.list_GoalsB

    def getlist_AssistsB(self):
       return self.list_AssistsB

    def getlist_PkB(self):
       return self.list_PkB

    def getlist_PKattB(self):
       return self.list_PKattB

    def getlist_ShotsB(self):
        return self.list_ShotsB

    def getlist_ShotsOnTargetB(self):
       return self.list_ShotsOnTargetB

    def getlist_YellowCardsB(self):
       return self.list_YellowCardsB

    def getlist_RedCardsB(self):
       return self.list_RedCardsB

    def getlist_TouchesB(self):
       return self.list_TouchesB

    def getlist_PressB(self):
       return self.list_PressB

    def getlist_TacklesB(self):
       return self.list_TacklesB

    def getlist_InterceptionsB(self):
       return self.list_InterceptionsB

    def getlist_BlocksB(self):
       return self.list_BlocksB
