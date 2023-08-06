import utm
import pandas as pd


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
            except:
                print("There's no \"easting\" column.")
            try:
                northing = row.northing
            except:
                print("There's no \"northing\" column.")
            utm_lat, utm_lon =\
                utm.to_latlon(easting, northing, self.zone_number, self.zone_letter)
            df_convert.loc[index, self.lat] = utm_lat
            df_convert.loc[index, self.lon] = utm_lon
        self.write_file(df_convert)

    def write_file(self, df_write):
        df_write.to_csv(self.file_name + "_output.csv", index=False)


