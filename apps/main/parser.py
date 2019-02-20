from html.parser import HTMLParser
import re

PRICE_REGEX = re.compile(r'^[0-9]\d+$')

class MyParser(HTMLParser):

    def myInit(self):
        self.foundWannaGetAway = False
        self.foundLineItem = False
        self.foundDepartingTime = False
        self.foundArrivalTime = False
        self.foundDuration = False
        self.foundBusiness = False
        self.foundAnytime = False
        self.documentData = {}
        self.flightNum = 0
        self.rawFares = []

    def handle_starttag(self, tag, attrs):
        
        if tag == 'button':
            for attr in attrs:
                if attr[0] == 'aria-label':
                    if 'Wanna Get Away fare' in attr[1]:
                        self.foundWannaGetAway = True
                        if self.mode == 'wholeDoc':
                            self.documentData[self.flightNum].append('Wanna Get Away fare')

                    if 'Business Select fare' in attr[1]:
                        if self.mode == 'wholeDoc':
                            self.documentData[self.flightNum].append('Business Select fare')
                        self.foundBusiness = True
                    
                    if 'Anytime fare' in attr[1]:
                        if self.mode == 'wholeDoc':
                            self.documentData[self.flightNum].append('Anytime fare')
                        self.foundAnytime = True


        if tag == 'li':
            for attr in attrs:
                if attr[0] == 'class' and 'air-booking-select-detail' in attr[1]:
                    self.foundLineItem = True
                    self.documentData[self.flightNum] = []

        if tag == 'div':
            for attr in attrs:
                if attr[0] == 'class' and 'air-operations-time-status' in attr[1] and not self.foundArrivalTime and not self.foundDepartingTime:
                    self.foundArrivalTime = True

                elif attr[0] == 'class' and 'flight-stops--duration' in attr[1]:
                    self.foundDuration = True


    def handle_data(self, data):
        if self.foundWannaGetAway:
            if self.mode == 'wanna':
                self.rawFares.append(data)

            elif self.mode == 'wholeDoc' and PRICE_REGEX.match(data):
                self.documentData[self.flightNum].append(data)


        if self.foundBusiness and self.mode == 'wholeDoc' and PRICE_REGEX.match(data):
            self.documentData[self.flightNum].append(data)


        if self.foundAnytime and self.mode == 'wholeDoc' and PRICE_REGEX.match(data):
            self.documentData[self.flightNum].append(data)
        
        if self.foundArrivalTime and self.mode == 'wholeDoc':
            self.documentData[self.flightNum].append(data)

        if self.foundDuration and self.mode == 'wholeDoc':
            self.documentData[self.flightNum].append(data)


    def handle_endtag(self, tag):
        if tag == 'button':
            if self.foundWannaGetAway:
                self.foundWannaGetAway = False

            elif self.foundBusiness:
                self.foundBusiness = False
            
            elif self.foundAnytime:
                self.foundAnytime = False

        if tag == 'li' and self.foundLineItem:
            self.foundLineItem = False
            self.flightNum += 1

        if tag == 'div' and self.foundArrivalTime:
            self.foundArrivalTime = False

        if tag == 'div' and self.foundDuration:
            self.foundDuration = False
            

    def findWannaGetAway(self, data):
        self.mode = 'wanna'
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



    def processWholeDocument(self, data):
        self.mode = 'wholeDoc'

        self.feed(data)
        return self.cleanFlightData()

    def cleanFlightData(self):
        flights = []
        # print(self.documentData)
        for flightNum in self.documentData:
            flights.append({})

            flights[flightNum]['stops'] = -1
            flights[flightNum]['business'] = -1
            flights[flightNum]['anytime'] = -1
            flights[flightNum]['wanna'] = -1

            for idx in range(len(self.documentData[flightNum])):
                data = self.documentData[flightNum][idx]

                if 'Departs' in data:
                    flights[flightNum]['departs'] = self.documentData[flightNum][idx + 1] + self.documentData[flightNum][idx + 2]

                if 'Arrives' in data:
                    flights[flightNum]['arrives'] = self.documentData[flightNum][idx + 1] + self.documentData[flightNum][idx + 2]

                if 'Duration' in data:
                    flights[flightNum]['duration'] = self.documentData[flightNum][idx + 1]
                
                if 'stop' in data:
                    flights[flightNum]['stops'] = self.documentData[flightNum][idx][0]

                if 'Business' in data:
                    flights[flightNum]['business'] = self.documentData[flightNum][idx + 1]

                if 'Anytime' in data:
                    flights[flightNum]['anytime'] = self.documentData[flightNum][idx + 1] 

                if 'Wanna' in data:
                    flights[flightNum]['wanna'] = self.documentData[flightNum][idx + 1]
             
        return flights