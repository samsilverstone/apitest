from flask import Flask, request, render_template
from sqlalchemy import create_engine
from math import cos, asin, sqrt

app = Flask(__name__)


postgre_engine = create_engine("postgresql://sanjay:mclarenf1!@#@localhost:5432/mydb")


@app.route("/post_location/", methods=['POST'])
def function_name1():
    req = request.json
    param = {"Latitude": req.get("Latitude"), "Longitude": req.get("Longitude"), "pin": req.get("pin"), "address": req.get("address"), "city": req.get("city"), "accuracy": req.get("accuracy")}
    conn = postgre_engine.raw_connection()
    cur = conn.cursor()
    gg = lambda x: "'" + x[0:] + "'"
    ff = lambda y: 'NULL' if y == '' else y
    x = gg(str(param.get("pin")))
    y = gg(str(param.get("address")))
    i = gg(str(param.get("city")))
    j = ff(param.get("accuracy"))
    a = ff(param.get("Latitude"))
    b = ff(param.get("Longitude"))
    cur.execute("select key from CSV")
    pin = cur.fetchall()
    z = []
    for i in range(len(pin)):
        z.append("'"+pin[i][0].strip()+"'")
    if x in z:
        return 'Pin exists'
    else:
        cur.execute(
            '''INSERT INTO CSV(key,place_name,admin_name1,latitude,longitude,accuracy) 
            VALUES ({},{},{},{},{},{})'''.format(x, y, i, a, b, j))
        conn.commit()
        return 'Inserted Successfully'

    conn.close()


@app.route("/get_using_self", methods=['GET'])
def function_name2():
    req = request.json
    param = {'Lat': req.get('Latitude'), 'Long':req.get('Longitude')}
    pin = []
    conn = postgre_engine.raw_connection()
    lat1 = param.get('Lat')
    lon1 = param.get('Long')
    cur = conn.cursor()
    cur.execute('select CSV.latitude from CSV')
    lat2 = cur.fetchall()
    cur.execute('select CSV.longitude from CSV')
    lon2 = cur.fetchall()
    for count, i in enumerate(range(len(lat2))):
        try:
            p = 0.017453292519943295
            a = 0.5 - cos((lat2[i][0] - lat1) * p)/2 + cos(lat1 * p) * cos(lat2[i][0] * p) * (1 - cos((lon2[i][0] - lon1) * p)) / 2
            if 12742 * asin(sqrt(a)) <= 5:
                cur.execute('select CSV.key from CSV where sno={}'.format(count+1))
                pin.append(cur.fetchall()[0][0].strip())
        except TypeError:
            pass
    print(pin)
    return render_template('Index3.html', leng=len(pin), pincode=pin)
    conn.close()


@app.route('/get_using_postgres', methods=['GET'])
def function_name3():
    req = request.json
    param = {'Lat': req.get("Latitude"), 'Long': req.get("Longitude")}
    conn = postgre_engine.raw_connection()
    cur = conn.cursor()
    cur.execute('CREATE EXTENSION IF NOT EXISTS cube')
    cur.execute('CREATE EXTENSION IF NOT EXISTS earthdistance')
    cur.execute('''select CSV.key from CSV where earth_distance(ll_to_earth({},{}),ll_to_earth(CSV.latitude,CSV.longitude))<=5000 '''.format(param.get('Lat'), param.get('Long')))
    pincode = cur.fetchall()
    print(pincode)
    return render_template('Index.html', len=len(pincode), pincode=pincode)
    conn.close()


@app.route("/latitude_longitude", methods=["GET"])
def function_name4():
    req = request.json
    param = {'Lat': req.get("Latitude"), 'Long': req.get("Longitude")}
    conn = postgre_engine.raw_connection()
    cur = conn.cursor()
    cur.execute(
        "select name from geojson where (min_lat<={0} and max_lat>={0}) and (min_lon<={1} and max_lon>={1})".format(param.get('Lat'), param.get('Long')))
    location = cur.fetchall()
    return render_template('Index2.html', leng=len(location), location=location)
    conn.close()


if __name__ == "__main__":
    app.run()
