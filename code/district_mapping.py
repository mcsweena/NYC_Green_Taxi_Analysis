import numpy as np
import pandas as pd
import json
import matplotlib.path as mplPath
from tqdm import tqdm
from shapely.geometry import shape, Point


def check_polygon(polygon, point):

    path = mplPath.Path(polygon)

    inside = path.contains_point(point)

    return inside

def find_ed(data, latitude, longitude):
    point = ([longitude, latitude])

    for feature in data['features']:

        polygon = np.array(feature['geometry']['coordinates'][0])
        if len(polygon) == 1:
            polygon = polygon[0]
            inside = check_polygon(polygon, point)
        elif len(polygon) <= 10:
            for i in range(len(polygon)):
                subpolygon = polygon[i]
                inside = check_polygon(subpolygon, point)
                if inside == 1:
                    break
        else:
            inside = check_polygon(polygon, point)

        if inside == 1:
            return feature['properties']['NAME_TAG']

    return None


def find_neighbourhood(data, row):
    # construct point based on lon/lat returned by geocoder
    print(row[1]['Pickup_latitude'])
    print(row[1]['Pickup_longitude'])

    """
    point = Point(row['Pickup_latitude'], row['Pickup_longitude'])

    # check each polygon to see if it contains the point
    for feature in data['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            print('Found containing polygon:', feature)

    """

def main():
    with open('geojsons/boroughs.geojson') as f:
        data = json.load(f)

        for k, v in data.items():
            print(k)

        print("\n")

    df = pd.read_csv('../data/augmented_data/2015_Green_Taxi_Trip_Data_100_lines.csv', encoding='latin1', index_col=0)

    for row in df.iterrows():
        find_neighbourhood(data, row)

    """
    df = pd.read_csv('../data/augmented_data/2015_Green_Taxi_Trip_Data_100_lines.csv', encoding='latin1', index_col=0)
    tqdm.pandas(desc="Progress")

    df['Pickup_borough'] = df.progress_apply(lambda row: find_neighbourhood(data, row),
                                             axis=1)
    print(df)

    df['Pickup_borough'] = df.progress_apply(lambda row: find_ed(data, row['Pickup_latitude'], row['Pickup_longitude']), axis=1)

    df.to_csv('../data/processed_data/2015_Green_Taxi_Trip_Data_100_lines.csv')
    """

if __name__ == '__main__':
    main()
