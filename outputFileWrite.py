import xlsxwriter
from datetime import datetime
import pandas as pd
from WebdriverOperations import MatchSummary

class writeToExcel():
    def __init__(self, match):

        self.matchDate=match.getMatchDate()
        self.matchReferee=match.getmatchReferee()
        self.TeamA=match.getTeamA()
        self.TeamB=match.getTeamB()
        self.matchCompetition=match.getmatchCompetition()
        self.rowScore=match.getrowScore()
        self.PenXg=match.getPenXg()
        self.rowPenXg=match.getrowPenXg()
        self.rowManager=match.getrowManager()
        self.rowCaptain=match.getrowCaptain()
        self.rowPosession=match.getrowPosession()
        self.rowPasses=match.getrowPasses()
        self.rowShots=match.getrowShots()
        self.rowFormation=match.getrowFormation()
        self.PlayerListA=match.getPlayerListA()
        self.PlayerListB=match.getPlayerListB()
        self.list_PlayerNamesA=match.getlist_PlayerNamesA()
        self.list_NumbersA=match.getlist_NumbersA()
        self.list_NationalityA=match.getlist_NationalityA()
        self.list_PositionA=match.getlist_PositionA()
        self.list_AgeA=match.getlist_AgeA()
        self.list_MinutesA=match.getlist_MinutesA()
        self.list_GoalsA=match.getlist_GoalsA()
        self.list_AssistsA=match.getlist_AssistsA()
        self.list_PkA=match.getlist_PkA()
        self.list_PKattA=match.getlist_PKattA()
        self.list_ShotsA=match.getlist_ShotsA()
        self.list_ShotsOnTargetA=match.getlist_ShotsOnTargetA()
        self.list_YellowCardsA=match.getlist_YellowCardsA()
        self.list_RedCardsA=match.getlist_RedCardsA()
        self.list_TouchesA=match.getlist_TouchesA()
        self.list_PressA=match.getlist_PressA()
        self.list_TacklesA=match.getlist_TacklesA()
        self.list_InterceptionsA=match.getlist_InterceptionsA()
        self.list_BlocksA=match.getlist_BlocksA()
        self.list_PlayerNamesB=match.getlist_PlayerNamesB()
        self.list_NumbersB =match.getlist_NumbersB ()
        self.list_NationalityB=match.getlist_NationalityB()
        self.list_PositionB=match.getlist_PositionB()
        self.list_AgeB=match.getlist_AgeB()
        self.list_MinutesB=match.getlist_MinutesB()
        self.list_GoalsB=match.getlist_GoalsB()
        self.list_AssistsB=match.getlist_AssistsB()
        self.list_PkB=match.getlist_PkB()
        self.list_PKattB = match.getlist_PKattB()
        self.list_ShotsB=match.getlist_ShotsB()
        self.list_ShotsOnTargetB=match.getlist_ShotsOnTargetB()
        self.list_YellowCardsB=match.getlist_YellowCardsB()
        self.list_RedCardsB=match.getlist_RedCardsB()
        self.list_TouchesB=match.getlist_TouchesB()
        self.list_PressB=match.getlist_PressB()
        self.list_TacklesB=match.getlist_TacklesB()
        self.list_InterceptionsB=match.getlist_InterceptionsB()
        self.list_BlocksB=match.getlist_BlocksB()




    def FormatAndExport(self):
        filepath = '{0}-{1}-{2}.xlsx'.format(self.matchDate, self.TeamA, self.TeamB)
        workbook = xlsxwriter.Workbook(filepath)
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 1})
        worksheet.write('A1', "Date", bold)
        date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})
        date_formatted = datetime.strptime(self.matchDate, "%Y-%m-%d")
        worksheet.write_datetime('B1', date_formatted, date_format)
        worksheet.write('A2', 'Competition', bold)
        worksheet.write('B2', self.matchCompetition)
        worksheet.write('A3', 'Referee', bold)
        worksheet.write('B3', self.matchReferee)
        worksheet.write('B4', self.TeamA, bold)
        worksheet.write('C4', self.TeamB, bold)
        worksheet.write('B5', self.rowScore[1])
        worksheet.write('C5', self.rowScore[2])
        worksheet.write('A6', self.PenXg, bold)
        worksheet.write('B6', self.rowPenXg[1])
        worksheet.write('C6', self.rowPenXg[2])
        worksheet.write('A7', "Manager", bold)
        worksheet.write('B7', self.rowManager[1])
        worksheet.write('C7', self.rowManager[2])
        worksheet.write('A8', 'Captain', bold)
        worksheet.write('B8', self.rowCaptain[1])
        worksheet.write('C8', self.rowCaptain[2])
        worksheet.write('A10', 'Posession', bold)
        worksheet.write('B10', self.rowPosession[1])
        worksheet.write('C10', self.rowPosession[2])
        worksheet.write('A11', 'Passing', bold)
        worksheet.write('B11', self.rowPasses[1])
        worksheet.write('C11', self.rowPasses[2])
        worksheet.write('A12', 'Shots', bold)
        worksheet.write('B12', self.rowShots[1])
        worksheet.write('C12', self.rowShots[2])
        worksheet.write('A14', 'Formations', bold)
        worksheet.write('B14', self.rowFormation[1])
        worksheet.write('C14', self.rowFormation[2])

        worksheet.set_column('A:A', 12)
        worksheet.set_column('B:B', 22)
        worksheet.set_column('C:C', 22)

        row = 15
        col = 1
        i = 0
        worksheet.write(row, col - 1, "Starting XI")
        for player in self.PlayerListA:
            i += 1
            worksheet.write(row, col, player)
            row += 1

            if (i == 11):
                worksheet.write(row, col, '')
                row += 1
                worksheet.write(row, col - 1, "Bench")
        row = 15
        col = 2

        j = 0
        for player in self.PlayerListB:
            j += 1
            worksheet.write(row, col, player)
            row += 1

            if (j == 11):
                worksheet.write(row, col, '')
                row += 1

        columnList = ['Name', '#', 'Nation', 'POS', 'Age', 'MinutesPlayed', 'Goals', 'Assists', 'PK', 'PKatt', \
                      'Shots', 'ShotsOnTarget', 'YellowCards', 'RedCards', 'Touches', 'Pressures', 'Tackles', \
                      'Interceptions', 'Blocks']
        dfA = pd.DataFrame(data=list(zip(self.list_PlayerNamesA, self.list_NumbersA, self.list_NationalityA, \
                                         self.list_PositionA, self.list_AgeA, self.list_MinutesA, self.list_GoalsA,\
                                         self.list_AssistsA, self.list_PkA, self.list_PKattA, self.list_ShotsA, \
                                         self.list_ShotsOnTargetA, self.list_YellowCardsA, self.list_RedCardsA, \
                                         self.list_TouchesA,   self.list_PressA, self.list_TacklesA, \
                                         self.list_InterceptionsA, self.list_BlocksA)), columns=columnList)

        dfB = pd.DataFrame(data=list(zip(self.list_PlayerNamesB, self.list_NumbersB, self.list_NationalityB, \
                                         self.list_PositionB, self.list_AgeB, self.list_MinutesB, self.list_GoalsB,\
                                         self.list_AssistsB, self.list_PkB, self.list_PKattB, self.list_ShotsB, \
                                         self.list_ShotsOnTargetB, self.list_YellowCardsB, self.list_RedCardsB, \
                                         self.list_TouchesB,   self.list_PressB, self.list_TacklesB, \
                                         self.list_InterceptionsB, self.list_BlocksB)), columns=columnList)
        writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
        writer.book = workbook
        dfA.to_excel(writer, sheet_name='{0} Stats'.format(self.TeamA), index=False)
        dfB.to_excel(writer, sheet_name='{0} Stats'.format(self.TeamB), index=False)

        worksheetA = writer.sheets['{0} Stats'.format(self.TeamA)]
        worksheetA.set_column('A:A', 21)

        worksheetB = writer.sheets['{0} Stats'.format(self.TeamB)]
        worksheetB.set_column('A:A', 21)

        writer.save()
        writer.close()
        workbook.close()

