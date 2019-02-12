from html.parser import HTMLParser
import re

PRICE_REGEX = re.compile(r'^[0-9]\d+$')

class MyParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        
        if tag == 'button' and self.mode == 'wanna':
            for attr in attrs:
                if attr[0] == 'aria-label' and 'Wanna Get Away' in attr[1]:
                    self.foundWannaGetAway = True


        if tag == 'li':
            for attr in attrs:
                if attr[0] == 'class' and 'air-booking-select-detail' in attr[1]:
                    self.foundLineItem = True
                    

        if tag == 'div':
            for attr in attrs:
                if attr[0] == 'class' and 'air-operations-time-status' in attr[1] and not self.foundArrivalTime and not self.foundDepartingTime:
                    self.foundArrivalTime = True

    def handle_data(self, data):
        
        if self.foundWannaGetAway and self.mode == 'wanna':
            self.rawFares.append(data)

        if self.foundArrivalTime:
            self.documentData.append(data)

        

    def handle_endtag(self, tag):
        if tag == 'button' and self.foundWannaGetAway and self.mode == 'wanna':
            self.foundWannaGetAway = False

        
        if tag == 'li' and self.foundLineItem:
            self.foundLineItem = False

        if tag == 'div' and self.foundArrivalTime:
            self.foundArrivalTime = False

        

    def findWannaGetAway(self, data):
        self.mode = 'wanna'
        self.foundWannaGetAway = False
        self.rawFares = []
        self.prunedFares = []
        self.feed(data)
        for price in self.rawFares:
            if PRICE_REGEX.match(price):
                self.prunedFares.append(int(price))

        
        self.lowestPrice = self.findLowestPrice(self.prunedFares)
        self.averagePrice = self.findAveragePrice(self.prunedFares)
        self.reset()


    def findLowestPrice(self, array):
        try:
            min = array[0]
            for item in array:
                if item < min:
                    min = item
            
            return min
        except: 
            return "Error"


    def findAveragePrice(self, array):
        try:
            sum = 0
            for item in array:
                sum += item
            
            return sum / len(array)
        except:
            return "Error"


    def parseDocument(self, data):
        self.mode = 'wholeDoc'
        self.foundLineItem = False
        self.foundDepartingTime = False
        self.foundArrivalTime = False
        self.foundDuration = False
        self.foundFares = False
        self.foundBusiness = False
        self.foundAnytime = False
        self.foundWannaGetAway = False

        self.documentData = []

        self.feed(data)

        print(self.documentData)

        self.reset()

    # def determineState(self):
    #     if 