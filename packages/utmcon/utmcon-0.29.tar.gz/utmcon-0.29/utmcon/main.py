import utm
import pandas as pd
import os


class Utm2latlon():

    def __init__(self, file_name, zone_number, zone_letter):
        self.file_name = file_name
        self.zone_number = zone_number
        self.zone_letter = zone_letter
        self.df = pd.read_csv("{}".format(self.file_name))
        self.lat = "latitude"
        self.lon = "longitude"
        self.convert(self.df)

    def convert(self, df_convert):

        df_convert[self.lat] = 0
        df_convert[self.lon] = 0
        for index, row in df_convert.iterrows():
            try:
                easting = row.easting
                northing = row.northing
            except:
                print("Error: File requires \"easting\" and \"northing\" column headings (lower casexxx).")
                break
            utm_lat, utm_lon =\
                utm.to_latlon(easting, northing, self.zone_number, self.zone_letter)
            df_convert.loc[index, self.lat] = utm_lat
            df_convert.loc[index, self.lon] = utm_lon
        self.write_file(df_convert)

    def write_file(self, df_write):
        output_file = self.file_name[:-3] + "_output.csv"
        df_write.to_csv(output_file, index=False)
        print(output_file)


