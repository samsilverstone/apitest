from flask import Flask, request, render_template
from sqlalchemy import create_engine
from math import cos, asin, sqrt
import re

app = Flask(__name__)


postgre_engine = create_engine("postgresql://postgres:@localhost:5432/mydb")


@app.route("/post_location", methods=['POST'])
def function_name1():
    req = request.json
    param = {"Latitude": req.get("Latitude"), "Longitude": req.get("Longitude"), "pin": req.get("pin"), "address": req.get("address"), "city": req.get("city"), "accuracy": req.get("accuracy")}
    conn = postgre_engine.raw_connection()
    cur = conn.cursor()
    gg = lambda var1: "'" + var1[0:] + "'"
    ff = lambda var2: 'NULL' if var2 == '' else "'"+var2+"'"
    x = gg(str(param.get("pin")))
    y = gg(str(param.get("address")))
    i = gg(str(param.get("city")))
    j = ff(str(param.get("accuracy")))
    a = gg(str(param.get("Latitude")))
    b = gg(str(param.get("Longitude")))

    if re.match('^IN/[1-9][0-9][0-9][0-9][0-9][0-9]', param.get("pin")):
        pass
    else:
        return 'Incorrect Value for Pin'
    if re.match('^.*', str(param.get("address"))):
        pass
    else:
        return 'Address should be a string'
    if re.match('^.*', str(param.get("city"))):
        pass
    else:
        return 'City should be a string'
    if re.match('^$|^[0-9]$]', str(param.get("accuracy"))):
        pass
    else:
        return 'Incorrect Accuracy'
    if re.match('^\d+\.'+'[0-9]'*(len(param.get("Latitude"))-3), str(param.get("Latitude"))):
        pass
    else:
        return'Incorrect format for Latitude'
    if re.match('^\d+\.'+'[0-9]'*(len(param.get("Longitude"))-3), str(param.get("Longitude"))):
        pass
    else:
        return 'Incorrect format for Longitude'

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

    conn.close()
    return 'Inserted Successfully'


@app.route("/get_using_self", methods=['GET'])
def function_name2():
    req = request.json
    param = {'Latitude': req.get('Latitude'), 'Longitude': req.get('Longitude')}
    pin = []
    conn = postgre_engine.raw_connection()
    lat1 = float(param.get('Latitude'))
    lon1 = float(param.get('Longitude'))
    if re.match('^\d+\.'+'[0-9]'*(len(param.get("Latitude"))-3), str(param.get("Latitude"))):
        pass
    else:
        return'Incorrect format for Latitude'
    if re.match('^\d+\.'+'[0-9]'*(len(str(param.get("Longitude")))-3), str(param.get("Longitude"))):
        pass
    else:
        return 'Incorrect format for Longitude'
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
    return render_template('Index3.html', leng=len(pin), pincode=pin)
    conn.close()


@app.route('/get_using_postgres', methods=['GET'])
def function_name3():
    req = request.json
    param = {'Latitude': req.get("Latitude"), 'Longitude': req.get("Longitude")}
    if re.match('^\d+\.'+'[0-9]'*(len(str(param.get("Latitude")))-3), str(param.get("Latitude"))):
        pass
    else:
        return'Incorrect format for Latitude'
    if re.match('^\d+\.'+'[0-9]'*(len(str(param.get("Longitude")))-3), str(param.get("Longitude"))):
        pass
    else:
        return 'Incorrect format for Longitude'
    conn = postgre_engine.raw_connection()
    cur = conn.cursor()
    cur.execute('CREATE EXTENSION IF NOT EXISTS cube')
    cur.execute('CREATE EXTENSION IF NOT EXISTS earthdistance')
    cur.execute('''select CSV.key from CSV where earth_distance(ll_to_earth({},{}),ll_to_earth(CSV.latitude,CSV.longitude))<=5000 '''.format(param.get('Latitude'), param.get('Longitude')))
    pincode = cur.fetchall()
    return render_template('Index.html', len=len(pincode), pincode=pincode)
    conn.close()


@app.route("/latitude_longitude", methods=["GET"])
def function_name4():
    req = request.json
    param = {'Latitude': req.get("Latitude"), 'Longitude': req.get("Longitude")}
    if re.match('^\d+\.'+'[0-9]'*(len(str(param.get("Latitude")))-3), str(param.get("Latitude"))):
        pass
    else:
        return'Incorrect format for Latitude'
    if re.match('^\d+\.'+'[0-9]'*(len(str(param.get("Longitude")))-3), str(param.get("Longitude"))):
        pass
    else:
        return 'Incorrect format for Longitude'
    conn = postgre_engine.raw_connection()
    cur = conn.cursor()
    cur.execute(
        "select name from geojson where (min_lat<={0} and max_lat>={0}) and (min_lon<={1} and max_lon>={1})".format(float(param.get('Latitude')), float(param.get('Longitude'))))
    location = cur.fetchall()
    return render_template('Index2.html', leng=len(location), location=location)
    conn.close()


if __name__ == "__main__":
    app.run(debug=True)
