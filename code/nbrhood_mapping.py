from heapq import heappush, heappop
import pandas as pd
import matplotlib.path as mplPath
import numpy as np


def test_point(lat, long, zones):
    heap = []

    for zone, points in zones.items():
        centroid_lat = np.mean([i[0][1] for i in points])
        centroid_long = np.mean([i[0][0] for i in points])

        a = centroid_lat - lat
        b = centroid_long - long

        distance = np.sqrt((a ** 2) + (b ** 2))
        heappush(heap, (distance, zone))

    for i in range(len(zones)):
        closest_zone = heappop(heap)

        path = []
        for i in range(len(zones[closest_zone[1]])):
            path.extend(zones[closest_zone[1]][i])
        path.extend(zones[closest_zone[1]][0])

        path = np.array(path)

        bbPath = mplPath.Path(path)

        if bbPath.contains_point(([long, lat])) == 1:
            return closest_zone[1]

    return "XX00"

def main():
    # Columns to read into memory
    green_names = ['pickup_datetime', 'dropoff_datetime', 'Pickup_longitude',
                   'Pickup_latitude', 'Dropoff_longitude', 'Dropoff_latitude',
                   'Passenger_count','Trip_distance','Fare_amount','Tip_amount',
                   'Total_amount', 'Payment_type', 'Trip_type']

    # Import geographic lat/long boundaries for each neighbourhood
    df = pd.read_csv('geographic.csv')

    # Import data
    green_cabs = pd.read_csv('../data/interim/2015_Green_Taxi_Trip_Data_11262015.csv',
                             usecols=green_names)

    # Stop/Start points
    start = 0
    #stop = 49815
    stop = 10

    zones = {}

    #Output filename
    output_filename = '../data/processed/zones_data_11262015.csv'


    # process geographic.csv file into usable zone lists
    for i, nbrhood in enumerate(df):
        boundary = df[nbrhood].as_matrix().reshape(int(df[nbrhood].size / 2),2)
        boundary = boundary[~np.isnan(boundary)]
        bd = []
        for j in range(int(len(boundary) / 2)):
            k = [[boundary[j*2], boundary[j*2 + 1]]]
            bd.append(k)
        zones[nbrhood] = bd

    # Process dataframe
    for row in range(start, stop):
        pu_time, do_time = green_cabs.ix[row, :].values[0], green_cabs.ix[row,
                                                           :].values[1]
        pu_lat, pu_long = green_cabs.ix[row,:].values[3], green_cabs.ix[row,
                                                          :].values[2]
        do_lat, do_long = green_cabs.ix[row, :].values[5], green_cabs.ix[row,
                                                           :].values[4]
        pass_count = green_cabs.ix[row, :].values[6]
        trip_distance = green_cabs.ix[row, :].values[7]
        fare_amount = green_cabs.ix[row, :].values[8]
        tip_amount = green_cabs.ix[row, :].values[9]
        total_amount = green_cabs.ix[row, :].values[10]
        payment_type = green_cabs.ix[row, :].values[11]
        trip_type = green_cabs.ix[row, :].values[12]

        # Write processed data to new datafile
        with open(output_filename, "a") as file:
            file.write(pu_time + ',' + do_time + ',' + test_point(pu_lat, pu_long, zones) + ','
                       + test_point(do_lat, do_long, zones) + ',' +str(pass_count) + ','
                       + str(trip_distance) + ',' + str(fare_amount) + ','
                       + str(tip_amount) + ',' + str(total_amount) + ','
                       + str(payment_type) + ',' + str(trip_type) + '\n')


if __name__ == '__main__':
    main()