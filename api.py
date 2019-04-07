from flask import Flask, request, make_response
from flask import jsonify
from sqlalchemy import create_engine
from math import cos, asin, sqrt
import re

app = Flask(__name__)


@app.route("/post_location", methods=['POST'])
def function_name1():

    postgre_engine = create_engine(
        "postgresql://{}:{}@localhost:{}/{}".format(
            app.config['DB_USER'], app.config['DB_PASSWORD'], app.config['DB_PORT'], app.config['DB_NAME']
        ))

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
        return make_response( jsonify(error = "Wrong Pincode entered", status="404"), 404)

    if re.match('^.*', str(param.get("address"))):
        pass
    else:
        return make_response( jsonify(error = "Wrong address entered", status="404"), 404)

    if re.match('^.*', str(param.get("city"))):
        pass
    else:
        return make_response( jsonify(error = "Wrong City entered", status="404"), 404)

    if re.match('^$|^\d', str(param.get("accuracy"))):
        pass
    else:
        return make_response( jsonify(error = "Wrong accuracy entered", status="404"), 404)

    if re.match('^[0-9]*$|^[0-9]*\.[0-9]*$', str(param.get("Latitude"))):
        pass
    else:
        return make_response ( jsonify(error = "Wrong Latitude entered", status="404"), 404 )

    if re.match('^[0-9]*$|^[0-9]*\.[0-9]*$', str(param.get("Longitude"))):
        pass
    else:
        return make_response( jsonify(error = "Wrong longitude entered", status="404"), 404)

    cur.execute("select key from CSV")
    pin = cur.fetchall()
    z = []
    for i in range(len(pin)):
        z.append("'"+pin[i][0].strip()+"'")
    if x in z:
        return make_response( jsonify(Response="PIN EXISTS"), 400 )
    else:
        cur.execute(
            '''INSERT INTO CSV(key,place_name,admin_name1,latitude,longitude,accuracy) 
            VALUES ({},{},{},{},{},{})'''.format(x, y, i, a, b, j))
        conn.commit()

    conn.close()
    return make_response( jsonify(Text='Inserted Successfully'), 200 )


@app.route("/get_using_self", methods=['GET'])
def function_name2():
    postgre_engine = create_engine(
        "postgresql://{}:{}@localhost:{}/{}".format(
            app.config['DB_USER'], app.config['DB_PASSWORD'], app.config['DB_PORT'], app.config['DB_NAME']
        ))

    req = request.json
    param = {'Latitude': req.get('Latitude'), 'Longitude': req.get('Longitude'), 'Value': req.get('Value')}
    pin = []
    conn = postgre_engine.raw_connection()

    if re.match('^[0-9]*$|^[0-9]*\.[0-9]*$', str(param.get("Latitude"))):
        pass
    else:
        return make_response(jsonify(error="Wrong latitude entered", status="404"), 404)

    if re.match('^[0-9]*$|^[0-9]*\.[0-9]*$', str(param.get("Longitude"))):
        pass
    else:
        return make_response(jsonify(error="Wrong longitude entered", status="404"), 404)

    if (re.match('^[0-9]*$|^[0-9]*\.[0-9]*$',str(param.get('Value'))) and param.get('Value')!= ''):
        pass
    else:
        return make_response(jsonify(error="Wrong value entered", status="404"),404)

    lat1 = float(param.get('Latitude'))
    lon1 = float(param.get('Longitude'))
    value = float(param.get('Value'))
    cur = conn.cursor()
    cur.execute('select CSV.latitude from CSV')
    lat2 = cur.fetchall()
    cur.execute('select CSV.longitude from CSV')
    lon2 = cur.fetchall()
    for count, i in enumerate(range(len(lat2))):
        try:
            p = 0.017453292519943295
            a = 0.5 - cos((lat2[i][0] - lat1) * p)/2 + cos(lat1 * p) * cos(lat2[i][0] * p) * (1 - cos((lon2[i][0] - lon1) * p)) / 2
            if 12742 * asin(sqrt(a)) <= value:
                cur.execute('select CSV.key from CSV where sno={}'.format(count+1))
                pin.append(cur.fetchall()[0][0].strip())
        except TypeError:
            pass

    return make_response( jsonify(pincode=pin), 200)
    conn.close()


@app.route('/get_using_postgres', methods=['GET'])
def function_name3():

    postgre_engine = create_engine(
        "postgresql://{}:{}@localhost:{}/{}".format(
            app.config['DB_USER'], app.config['DB_PASSWORD'], app.config['DB_PORT'], app.config['DB_NAME']
        ))

    req = request.json
    param = {'Latitude': req.get("Latitude"), 'Longitude': req.get("Longitude"), 'Value': req.get('Value')}
    if re.match('^[0-9]*$|^[0-9]*\.[0-9]*$', str(param.get("Latitude"))):
        pass
    else:
        return make_response(jsonify(error="Wrong latitude entered", status="404"), 404)

    if re.match('^[0-9]*$|^[0-9]*\.[0-9]*$', str(param.get("Longitude"))):
        pass
    else:
        return make_response(jsonify(error="Wrong longitude entered", status="404"), 404)

    if (re.match('^[0-9]*$|^[0-9]*\.[0-9]*$', str(param.get('Value'))) and str(param.get('Value'))!=''):
        pass
    else:
        return make_response(jsonify(error="Wrong value entered"), 404)
    value= float(param.get("Value"))*1000
    conn = postgre_engine.raw_connection()
    cur = conn.cursor()
    cur.execute('CREATE EXTENSION IF NOT EXISTS cube')
    cur.execute('CREATE EXTENSION IF NOT EXISTS earthdistance')
    cur.execute('''select CSV.key from CSV where earth_distance(ll_to_earth({},{}),ll_to_earth(CSV.latitude,CSV.longitude))<={} '''.format(param.get('Latitude'), param.get('Longitude'), value))
    pincode = cur.fetchall()
    return make_response(jsonify(pincode=pincode), 200)
    conn.close()


@app.route("/latitude_longitude", methods=["GET"])
def function_name4():

    postgre_engine = create_engine(
        "postgresql://{}:{}@localhost:{}/{}".format(
            app.config['DB_USER'], app.config['DB_PASSWORD'], app.config['DB_PORT'], app.config['DB_NAME']
        ))

    req = request.json
    param = {'Latitude': req.get("Latitude"), 'Longitude': req.get("Longitude")}
    if re.match('^[0-9]*$|^[0-9]*\.[0-9]*$', str(param.get("Latitude"))):
        pass
    else:
        return make_response(jsonify(error="Wrong latitude entered", status="404"), 404)
    if re.match('^[0-9]*$|^[0-9]*\.[0-9]*$', str(param.get("Longitude"))):
        pass
    else:
        return make_response(jsonify(error="Wrong Longitude entered", status="404"), 404)

    conn = postgre_engine.raw_connection()
    cur = conn.cursor()
    cur.execute(
        "select name from geojson where (min_lat<={0} and max_lat>={0}) and (min_lon<={1} and max_lon>={1})".format(float(param.get('Latitude')), float(param.get('Longitude'))))
    location = cur.fetchall()
    return make_response(jsonify(location=location), 200)
    conn.close()


