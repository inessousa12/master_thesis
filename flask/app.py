import os
import json
import mysql.connector
import datetime, time
from flask import Flask
from flask import jsonify

app = Flask(__name__)

def datetime_converter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

@app.route('/', methods=['GET'])
def hello_world():
  return 'Hello, Docker!'

@app.route("/api/<sensor_name>/<variable>/<begin_date>/<period>/raw_measurements", methods=['GET'])
def get_raw_measurements(sensor_name, variable, begin_date, period):
    try:
        conn = mysql.connector.connect(
                        host="mysql",
                        port=3306,
                        user="aquamon",
                        password="password",
                        database="aquamon")

        cursor = conn.cursor(buffered=True)
        timestamp = int(time.mktime(datetime.datetime.strptime(begin_date,"%d-%m-%Y").timetuple()))
        period = int(period) * 24 * 60 * 60 * 1000 + timestamp
        
        if variable == "temp":
            variable = "Water Temperature"

        query = "SELECT * FROM `measurement` WHERE `station_id` = (SELECT `id` FROM `station` WHERE `name`= '" + sensor_name + \
            "') AND `metric_name` = '" + variable + "' AND `timestamp` BETWEEN FROM_UNIXTIME(" + str(timestamp) + ") AND FROM_UNIXTIME(" + str(period) + ");"
        
        cursor.execute(query)
        conn.commit()
        
        result = cursor.fetchall()
        
        results = []
        for elem in result:
            results.append({"value": elem[3], "time": datetime_converter(elem[-1]), "sensor": sensor_name, "metric": elem[2]})
        return json.dumps({'results': results}, indent = 2)
    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route("/api/<sensor_name>/<variable>/<begin_date>/<period>/corrected_measurements", methods=['GET'])
def get_corrected_measurements(sensor_name, variable, begin_date, period):
    try:
        conn = mysql.connector.connect(
                        host="mysql",
                        port=3306,
                        user="aquamon",
                        password="password",
                        database="aquamon")

        cursor = conn.cursor(buffered=True)
        timestamp = int(time.mktime(datetime.datetime.strptime(begin_date,"%d-%m-%Y").timetuple()))
        period = int(period) * 24 * 60 * 60 * 1000 + timestamp
        
        if variable == "temp":
            variable = "Water Temperature"

        query = "SELECT * FROM `measurement` WHERE `station_id` = (SELECT `id` FROM `station` WHERE `name`= '" + sensor_name + \
            "') AND `metric_name` = '" + variable + "' AND `timestamp` BETWEEN FROM_UNIXTIME(" + str(timestamp) + ") AND FROM_UNIXTIME(" + str(period) + ");"
        
        cursor.execute(query)
        conn.commit()
        
        result = cursor.fetchall()
        
        results = []
        for elem in result:
            results.append({"value": elem[4], "time": datetime_converter(elem[-1]), "sensor": sensor_name, "metric": elem[2]})
        return json.dumps({'results': results}, indent = 2)
    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route("/api/<sensor_name>/<variable>/<begin_date>/<period>/quality", methods=['GET'])
def get_quality(sensor_name, variable, begin_date, period):
    try:
        conn = mysql.connector.connect(
                        host="mysql",
                        port=3306,
                        user="aquamon",
                        password="password",
                        database="aquamon")

        cursor = conn.cursor(buffered=True)
        timestamp = int(time.mktime(datetime.datetime.strptime(begin_date,"%d-%m-%Y").timetuple()))
        period = int(period) * 24 * 60 * 60 * 1000 + timestamp
        
        if variable == "temp":
            variable = "Water Temperature"

        query = "SELECT * FROM `measurement` WHERE `station_id` = (SELECT `id` FROM `station` WHERE `name`= '" + sensor_name + \
            "') AND `metric_name` = '" + variable + "' AND `timestamp` BETWEEN FROM_UNIXTIME(" + str(timestamp) + ") AND FROM_UNIXTIME(" + str(period) + ");"
        
        cursor.execute(query)
        conn.commit()
        
        result = cursor.fetchall()
        
        count = 0
        quality = 0
        
        results = []
        for elem in result:
            count += 1
            quality += elem[5]
        return json.dumps({'quality_mean': quality/count}, indent = 2)
    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route("/api/<sensor_name>/<variable>/<begin_date>/<period>/outliers", methods=['GET'])
def get_outliers(sensor_name, variable, begin_date, period):
    try:
        conn = mysql.connector.connect(
                        host="mysql",
                        port=3306,
                        user="aquamon",
                        password="password",
                        database="aquamon")

        cursor = conn.cursor(buffered=True)
        timestamp = int(time.mktime(datetime.datetime.strptime(begin_date,"%d-%m-%Y").timetuple()))
        period = int(period) * 24 * 60 * 60 * 1000 + timestamp
        
        if variable == "temp":
            variable = "Water Temperature"

        query = "SELECT * FROM `measurement` WHERE `station_id` = (SELECT `id` FROM `station` WHERE `name`= '" + sensor_name + \
            "') AND `metric_name` = '" + variable + "' AND `timestamp` BETWEEN FROM_UNIXTIME(" + str(timestamp) + ") AND FROM_UNIXTIME(" + str(period) + ") AND `failure_type` = 'outlier';"
        
        cursor.execute(query)
        conn.commit()
        
        result = cursor.fetchall()
        
        results = []
        for elem in result:
            results.append({"value": elem[3], "time": datetime_converter(elem[-1]), "sensor": sensor_name, "metric": elem[2]})
        return json.dumps({'outliers': results}, indent = 2)
    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route("/api/<sensor_name>/<variable>/<begin_date>/<period>/omissions", methods=['GET'])
def get_omissions(sensor_name, variable, begin_date, period):
    try:
        conn = mysql.connector.connect(
                        host="mysql",
                        port=3306,
                        user="aquamon",
                        password="password",
                        database="aquamon")

        cursor = conn.cursor(buffered=True)
        timestamp = int(time.mktime(datetime.datetime.strptime(begin_date,"%d-%m-%Y").timetuple()))
        period = int(period) * 24 * 60 * 60 * 1000 + timestamp
        
        if variable == "temp":
            variable = "Water Temperature"

        query = "SELECT * FROM `measurement` WHERE `station_id` = (SELECT `id` FROM `station` WHERE `name`= '" + sensor_name + \
            "') AND `metric_name` = '" + variable + "' AND `timestamp` BETWEEN FROM_UNIXTIME(" + str(timestamp) + ") AND FROM_UNIXTIME(" + str(period) + ") AND `failure_type` = 'omission';"
        
        cursor.execute(query)
        conn.commit()
        
        result = cursor.fetchall()
        
        results = []
        for elem in result:
            results.append({"value": elem[3], "time": datetime_converter(elem[-1]), "sensor": sensor_name, "metric": elem[2]})
        return json.dumps({'omissions': results}, indent = 2)
    except Exception as e:
        return json.dumps({'error':str(e)})

@app.route("/api/<sensor_name>/<variable>/<begin_date>/<period>/anomalies", methods=['GET'])
def get_all_anomalies(sensor_name, variable, begin_date, period):
    try:
        conn = mysql.connector.connect(
                        host="mysql",
                        port=3306,
                        user="aquamon",
                        password="password",
                        database="aquamon")

        cursor = conn.cursor(buffered=True)
        timestamp = int(time.mktime(datetime.datetime.strptime(begin_date,"%d-%m-%Y").timetuple()))
        period = int(period) * 24 * 60 * 60 * 1000 + timestamp
        
        if variable == "temp":
            variable = "Water Temperature"

        query = "SELECT * FROM `measurement` WHERE `station_id` = (SELECT `id` FROM `station` WHERE `name`= '" + sensor_name + \
            "') AND `metric_name` = '" + variable + "' AND `timestamp` BETWEEN FROM_UNIXTIME(" + str(timestamp) + ") AND FROM_UNIXTIME(" + str(period) + ") AND (`failure_type` = 'outlier' OR `failure_type` = 'omission');"
        
        cursor.execute(query)
        conn.commit()
        
        result = cursor.fetchall()
        
        results = []
        for elem in result:
            results.append({"value": elem[3], "time": datetime_converter(elem[-1]), "sensor": sensor_name, "metric": elem[2], "anomaly_type": elem[7]})
        return json.dumps({'anomalies': results}, indent = 2)
    except Exception as e:
        return json.dumps({'error':str(e)})



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)  