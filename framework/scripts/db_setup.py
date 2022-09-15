import mysql.connector
import datetime, time


def insert_station(message):
    """
    Inserts a station into the database.

    Args:
        message (json): json with station information
    """
    cnx = mysql.connector.connect(
                        host="mysql",
                        port=3306,
                        user="aquamon",
                        password="password",
                        database="aquamon")
    cursor = cnx.cursor()

    sql = "INSERT INTO `station` (`name`, `latitude`, `longitude`) SELECT * FROM (SELECT '" + \
            message["sensor_id"] + "', " + str(message["latitude"]) + ", " + str(message["longitude"]) + ") AS tmp WHERE NOT EXISTS (" + \
            "SELECT `name` FROM `station` WHERE `name` = '" + message["sensor_id"] + "');"

    cursor.execute(sql)

    cnx.commit()

    cursor.close()
    cnx.close()

def insert_data(message):
    """
    Inserts data into MySQL database

    Args:
        message (json): json with the parameters to insert the measurement into MySQL
    """
    cnx = mysql.connector.connect(
                        host="mysql",
                        port=3306,
                        user="aquamon",
                        password="password",
                        database="aquamon",
                        auth_plugin='mysql_native_password')
    cursor = cnx.cursor()

    cursor.execute("SELECT `id` FROM `station` WHERE `name` = '" + message["sensor"] + "';")
    sensor_id = cursor.fetchall()

    if message["type"] == "temp":
        metric = "Water Temperature"
    else:
        metric = message["type"]
        
    sql = "INSERT INTO `metric` (`name`) SELECT * FROM (SELECT '" + \
        metric + "') AS tmp WHERE NOT EXISTS (" + \
        "SELECT `name` FROM `metric` WHERE `name` = '" + metric + "');"

    cursor.execute(sql)

    cnx.commit()

    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    sql = ("INSERT INTO `measurement` (`station_id`, `metric_name`, `raw_value`, `corrected_value`, `quality`, `failure`, `failure_type`, `timestamp`) " + \
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);")

    if str(message["failure"]) == False:
        failure = 0
    else:
        failure = 1

    if message["true_value"] == None:
        cursor.execute(sql, (str(sensor_id[0][0]), metric, None, str(message["value"]), str(message["quality"]), failure, message["failure_type"], timestamp))
    else:
        cursor.execute(sql, (str(sensor_id[0][0]), metric, str(message["true_value"]), str(message["value"]), str(message["quality"]), failure, message["failure_type"], timestamp))

    # sql = ("INSERT INTO `measurement` (`station_id`, `metric_name`, `raw_value`, `corrected_value`, `quality`, `failure`, `failure_type`, `timestamp`) " + \
    #         "VALUES (" + str(sensor_id[0][0]) + ", '" + metric + "', " + str(message["true_value"]) + ", " + str(message["value"]) + \
    #         ", " + str(message["quality"]) + ", " + str(message["failure"]) + ", '" + message["failure_type"] + "', '" + timestamp + "');")

    # cursor.execute(sql)

    cnx.commit()

    cursor.close()
    cnx.close()
