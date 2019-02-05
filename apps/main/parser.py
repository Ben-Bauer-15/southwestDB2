from html.parser import HTMLParser
import re

PRICE_REGEX = re.compile(r'^[0-9]+.+[0-9]+ Dollars+$')

class MyParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        
        if tag == 'button':
            for attr in attrs:
                if attr[0] == 'aria-label' and 'Wanna Get Away' in attr[1]:
                    self.foundWannaGetAway = True

    def handle_data(self, data):
        if self.foundWannaGetAway:
            self.rawFares.append(data)

    def handle_endtag(self, tag):
        if tag == 'button' and self.foundWannaGetAway:
            self.foundWannaGetAway = False

    

    def findWannaGetAway(self, data):
        self.foundWannaGetAway = False
        self.rawFares = []
        self.prunedFares = []
        self.feed(data)
        for price in self.rawFares:
            if PRICE_REGEX.match(price):
                index = 0
                for i in range(len(price)):
                    if price[i] == '.':
                        index = i

                self.prunedFares.append(int(price[0:index]))
        
        self.lowestPrice = self.findLowestPrice(self.prunedFares)
        self.averagePrice = self.findAveragePrice(self.prunedFares)


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

