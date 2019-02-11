def readFile():
    airports = []
    with open('./apps/main/files/airportCodes.txt') as f:
        content = f.readlines()

    for item in content:
        airports.append(item[: len(item) - 1])

    combinations = []

    for i in range(len(airports) - 1):
        for j in range(i + 1, len(airports)):
            combinations.append((airports[i], airports[j]))

    