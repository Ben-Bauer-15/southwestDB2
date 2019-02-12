from html.parser import HTMLParser
import re

PRICE_REGEX = re.compile(r'^[0-9]\d+$')

class MyParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        
        if tag == 'button':
            for attr in attrs:
                if attr[0] == 'aria-label':
                    if 'Wanna Get Away fare' in attr[1]:
                        self.foundWannaGetAway = True

                        if self.mode == 'wholeDoc':
                            self.documentData[self.flightNum].append('Wanna Get Away fare')
                
                    elif 'Business Select fare' in attr[1]:
                        self.foundBusiness = True
                        self.documentData[self.flightNum].append('Business Select fare')

                    elif 'Anytime fare' in attr[1]:
                        self.foundAnytime = True
                        self.documentData[self.flightNum].append('Anytime fare')


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

            else:
                if PRICE_REGEX.match(data):
                    self.documentData[self.flightNum].append(data)
        

        if self.foundBusiness or self.foundAnytime:
            if PRICE_REGEX.match(data):
                self.documentData[self.flightNum].append(data)

        if self.foundArrivalTime:
            self.documentData[self.flightNum].append(data)

        if self.foundDuration:
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
        self.flightNum = 0

        self.documentData = {}

        self.feed(data)

        return self.cleanFlightData()

        self.reset()


    def cleanFlightData(self):
        flights = []
        for flightNum in self.documentData:
            flights.append({})

            for idx in range(len(self.documentData[flightNum])):
                data = self.documentData[flightNum][idx]

                flights[flightNum]['stops'] = -1
                flights[flightNum]['businessSelect'] = -1
                flights[flightNum]['anytime'] = -1
                flights[flightNum]['wanna'] = -1

                print(data)
                if 'Departs' in data:
                    flights[flightNum]['departs'] = self.documentData[flightNum][idx + 1] + self.documentData[flightNum][idx + 2]

                elif 'Arrives' in data:
                    flights[flightNum]['arrives'] = self.documentData[flightNum][idx + 1] + self.documentData[flightNum][idx + 2]

                elif 'Duration' in data:
                    flights[flightNum]['duration'] = self.documentData[flightNum][idx + 1]
                
                elif 'stop' in data:
                    flights[flightNum]['stops'] = self.documentData[flightNum][idx][0   ]

                elif 'Business' in data:
                    flights[flightNum]['business'] = self.documentData[flightNum][idx + 1]

                elif 'Anytime' in data:
                    flights[flightNum]['anytime'] = self.documentData[flightNum][idx + 1] 

                elif 'Wanna' in data:
                    flights[flightNum]['wanna'] = self.documentData[flightNum][idx + 1]

        return flights