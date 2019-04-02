import json
import psycopg2
import csv


class Table:

    def __init__(self):
        self.name = []
        self.Type = []
        self.Parent = []
        self.geometry_type = []
        self.coordinates = []

    def create_csv(self):
        self.cur.execute('''CREATE TABLE CSV (sno BIGSERIAL PRIMARY KEY, key CHAR(12) UNIQUE NOT NULL, place_name CHAR(30) NOT NULL
                                         ,admin_name1 CHAR(30) NOT NULL,latitude REAL CHECK(latitude>=0 and latitude<=90)
                                         ,longitude REAL CHECK(longitude>=0 and longitude<=180),accuracy INT DEFAULT NULL )''')

    def insert_csv(self):
        with open(r"Files Used\CSV.csv", 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                gg = lambda x: "'" + x[0:] + "'"
                ff = lambda y: 'NULL' if y == '' else y
                x = gg(row['key'])
                y = gg(row['place_name'])
                i = gg(row['admin_name1'])
                j = ff(row['accuracy'])
                a = ff(row['latitude'])
                b = ff(row['longitude'])
                self.cur.execute('''INSERT INTO CSV(key,place_name,admin_name1,latitude,longitude,accuracy) 
                VALUES ({},{},{},{},{},{})'''.format(x, y, i, a, b, j))

    def geojson(self):
        with open('Files Used/map.geojson.txt') as json_file:
            data = json.load(json_file)
            x = data['features']
            for i in range(len(x)):
                self.name.append(x[i]['properties']['name'])
                self.Type.append(x[i]['properties']['type'])
                self.Parent.append(x[i]['properties']['parent'])
                self.geometry_type.append(x[i]['geometry']['type'])
                self.coordinates.append(x[i]['geometry']['coordinates'])

    def create_geojson(self):
        self.cur.execute('''CREATE TABLE geojson (name CHAR(30) PRIMARY KEY, Type CHAR(30) NOT NULL
                                         ,Parent CHAR(30) NOT NULL,geometry_type CHAR(30)
                                         ,coordinates varchar(10000) NOT NULL,min_lat DECIMAL CHECK(min_lat>=0 and min_lat<=90),
                                         max_lat DECIMAL CHECK(max_lat>=8.4 and max_lat<=37.6),min_lon DECIMAL CHECK(min_lon>=0 and min_lon<=180),
                                         max_lon DECIMAL CHECK(max_lon>=68.7 and max_lon<=97.25))''')

    def insert_geojson(self):
        for i in range(len(self.coordinates)):
            gg = lambda x: "'" + x[0:] + "'"
            lat = []
            lon = []

            for y in range(len(self.coordinates[i][0])):
                lat.append(self.coordinates[i][0][y][1])
                lon.append(self.coordinates[i][0][y][0])
            self.min_lat = min(lat)
            self.max_lat = max(lat)
            self.min_long = min(lon)
            self.max_long = max(lon)
            self.output1 = gg(self.name[i])
            self.output2 = gg(self.Type[i])
            self.output3 = gg(self.Parent[i])
            self.output4 = gg(self.geometry_type[i])
            self.output5 = gg(str(self.coordinates[i][0]))
            self.cur.execute(
                '''INSERT INTO geojson(name,Type,Parent,geometry_type,coordinates,min_lat,max_lat,min_lon,max_lon) VALUES ({},{},{},{},{},{},{},{},{})'''.format(
                    self.output1, self.output2, self.output3, self.output4, self.output5, self.min_lat, self.max_lat, self.min_long, self.max_long))


def main():
    obj = Table()
    obj.conn = psycopg2.connect(database='mydb', user='sanjay', password='mclarenf1!@#', host='127.0.0.1', port='5432')
    obj.cur = obj.conn.cursor()
    obj.create_csv()
    obj.insert_csv()
    obj.geojson()
    obj.create_geojson()
    obj.insert_geojson()
    obj.conn.commit()
    obj.conn.close()
    print("Values entered Successfully")


if __name__ == "__main__":
    main()
