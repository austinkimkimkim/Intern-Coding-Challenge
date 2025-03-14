import math
import json
import csv

# Load data from the json and csv files
def loadData():
    with open("SensorData1.csv") as file:
        sensor1Data = csv.DictReader(file)
        sensor1Data = [line for line in sensor1Data]
    with open("SensorData2.json") as file:
        sensor2Data = json.load(file)

    return sensor1Data, sensor2Data

# Calculate the distance between two points using the haversine formula
def haversine(lat1, Lon1, lat2, Lon2):
    # Distance between latitude and longitude
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (Lon2 - Lon1) * math.pi / 180.0
    lat1 = lat1 * math.pi / 180.0
    lat2 = lat2 * math.pi / 180.0

    #haversine formula
    a = (pow(math.sin(dLat / 2), 2) + pow(math.sin(dLon / 2), 2) * math.cos(lat1) * math.cos(lat2))
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))

    # Return distance in meters
    return rad * c * 1000

# Detect which sensor readings are within 100 meters of each other
def correlate(sensor1Data, sensor2Data):
    # Dictionary to store the correlated data
    correlatedData = {}
    
    # Loop through every sensor reading from sensor 1 and compare it to every sensor reading from sensor 2
    for s1 in sensor1Data:
        id1 = s1['id']
        lat1 = float(s1['latitude'])
        lon1 = float(s1['longitude'])

        for s2 in sensor2Data:
            id2 = s2['id']
            lat2 = float(s2['latitude'])
            lon2 = float(s2['longitude'])

            distance = haversine(lat1, lon1, lat2, lon2)
            if distance <= 100:
                correlatedData[id1] = id2
    return correlatedData

# Output the results in a json file
def output(results):
    with open("CorrelatedData.json", "w") as file:
        json.dump(results, file, indent=4)



if __name__ == "__main__":
    sensor1Data, sensor2Data = loadData()
    correlatedData = correlate(sensor1Data, sensor2Data)
    output(correlatedData)

