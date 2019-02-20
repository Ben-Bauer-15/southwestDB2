from datetime import *
import calendar


class SearchGenerator():
    def __init__(self):
        self.now = datetime.now()
        self.month = self.now.month
        self.day = self.now.day
        self.year = self.now.year
        self.cal = calendar.Calendar()
        self.readAirportsFile()
        self.maxFutureBookingMonth(self.month)
        self.possibleBookingDates = []
        self.populateBookingCalendar(self.year)
        self.populateBookingCalendar(self.year + 1)


    def readAirportsFile(self):
        self.airports = []
        with open('./apps/main/files/airportCodes.txt') as f:
            content = f.readlines()

        for item in content:  
            self.airports.append(item[: len(item) - 1])


        #this list contains all possible origin -> destination airport combinations
        self.combinations = []

        for i in range(len(self.airports) - 1):
            for j in range(i + 1, len(self.airports)):
                self.combinations.append([self.airports[i], self.airports[j]])


    def maxFutureBookingMonth(self, monthNumber):
        if monthNumber + 7 > 12:
            difference = 12 - monthNumber
            self.maxFuture = 7 - difference
        else:
            self.maxFuture = monthNumber + 7


    def isValidDate(self, month, day, year):
        # is the year param our current year?
        if year == self.year:
            
            # is the month param our current month?
            if month == self.month:

                # is the day param gt or equal to our current day?
                if day >= self.day:
                    return True


            # is the month param in the future (but not too far in the future)?
            elif month >= self.month and month <= self.maxFuture:
                return True
        

        # the year param is in the future
        elif year > self.year:

            if self.month > 5 and month <= self.maxFuture:
                return True

        return False 



    def populateBookingCalendar(self, yearParam):
        year = self.cal.yeardatescalendar(yearParam)
        for monthRow in year:
            for month in monthRow:
                for week in month:
                    for day in week:
                        validDate = self.isValidDate(day.month, day.day, yearParam)
                        dateStr = self.makePaddedDate(day.day, day.month, yearParam)
                        
                        if dateStr not in self.possibleBookingDates and validDate:
                            self.possibleBookingDates.append(dateStr)


    def makePaddedDate(self, day, month, year):
        dayStr = str(day)
        monthStr = str(month)

        if len(dayStr) < 2:
            dayStr = '0' + dayStr

        if len(monthStr) < 2:
            monthStr = '0' + monthStr
        
        return str(year) + '-' + monthStr + '-' + dayStr



    def generateSearches(self):
        self.searches = []

        for i in range(len(self.combinations)):
            self.searches.append([self.combinations[i]])
            self.searches[i].append([])
            for j in range(len(self.possibleBookingDates)):
                self.searches[i][1].append(self.possibleBookingDates[j])


        return self.searches