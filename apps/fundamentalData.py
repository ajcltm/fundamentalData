parentPath='c:/Users/ajcltm/PycharmProjects/fundamentalData'
import sys
sys.path.append(parentPath)
import consolidatedData
import nonConsolidatedData

class FundamentalData:

    def __init__(self, receptNo):
        self.cfd = consolidatedData.ConsolidatedData(receptNo)
        self.ncfd = nonConsolidatedData.NonConsolidatedData(receptNo)
        self.blackBox = ""

        self.consolidatedData = self.get_consolidatedData()
        self.nonConsolidatedData = self.get_nonConsolidatedData()
        self.consolidatedHtml = self.get_consolidatedHtml()
        self.nonConsolidatedHtml = self.get_nonConsolidatedHtml()

    def get_consolidatedData(self):

        data = self.cfd.get_data()
        self.blackBox += self.cfd.blackBox

        return data

    def get_nonConsolidatedData(self):

        data = self.ncfd.get_data()
        self.blackBox += self.ncfd.blackBox

        return data

    def get_consolidatedHtml(self):
        html = self.cfd.get_html(record=False)

        return html

    def get_nonConsolidatedHtml(self):
        html = self.ncfd.get_html(record=False)

        return html

    def print_blackBox(self):
        print(self.blackBox)


