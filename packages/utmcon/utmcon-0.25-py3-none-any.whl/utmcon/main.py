import utm
import pandas as pd


def to_ll():
    file_name = input("File name? ")
    zone_number = int(input("UTM zone number? "))
    zone_letter = input("UTM zone? ")

    print(file_name)

    df = pd.read_csv("{}".format(file_name))

    lat = "latitude"
    lon = "longitude"
    df[lat] = 0
    df[lon] = 0


    for index, row in df.iterrows():
        easting = row.easting
        northing = row.northing
        df.loc[index, lat], df.loc[index, lon] = \
        utm.to_latlon(easting, northing, zone_number, zone_letter)

    df.to_csv(file_name + "_output.csv", index=False)


