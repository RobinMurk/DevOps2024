import connexion
import six

from swagger_server.models.bodytemplate import Bodytemplate  # noqa: E501
from swagger_server.models.temperature import Temperature  # noqa: E501
from swagger_server import util


#add imports
import os
import json
import pandas
import datetime
import requests


from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.exceptions import InfluxDBError


#Get influxdb env variables
def get_vars():
    # Read the data
    STUD_INFLUX_HOST_ADD=os.getenv('STUD_INFLUX_HOST_ADD')
    STUD_INFLUX_ORG=os.getenv('STUD_INFLUX_ORG')
    STUD_INFLUX_TOKEN=os.getenv('STUD_INFLUX_TOKEN')
    return (STUD_INFLUX_HOST_ADD,STUD_INFLUX_ORG,STUD_INFLUX_TOKEN)

# Create Influxdb client
def getclient():
    # Read the data
    STUD_INFLUX_HOST_ADD,STUD_INFLUX_ORG,STUD_INFLUX_TOKEN = get_vars()
    dbclinet = InfluxDBClient(url=STUD_INFLUX_HOST_ADD, token=STUD_INFLUX_TOKEN, org=STUD_INFLUX_ORG, debug=False)
    return dbclinet


def getavg(date):
    _db_client = getclient()
    STUD_INFLUX_HOST_ADD,STUD_INFLUX_ORG,STUD_INFLUX_TOKEN = get_vars()
    query ='''
  from(bucket: "weather_data")
  |> range(start:'''+date+'''T00:00:00.000Z , stop: now())
  |> filter(fn: (r) => r["_measurement"] == "weather")
  |> filter(fn: (r) => r["_field"] == "temp")
  |> aggregateWindow(every: 24h, fn: mean, createEmpty: false)
  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'''
    print(query)
    result = _db_client.query_api().query_data_frame(org=STUD_INFLUX_ORG, query=query)
    return result


def add_measurement(body):
    _db_client = getclient()
    data = body

    date = data["tags"]["date"]
    station = data["tags"]["station"]

    # Get avg temp data for the
    df = getavg(date)
    field = data["field"]
    print(df)
    value=df.loc[0, 'temp']
    current_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    point1 = Point("weather_stat").field(field,value).tag("station",station).tag("date",date).time(current_time)
    try:
        response=_db_client.write_api().write("weather_data", record = [point1],data_frame_measurement_name='weather_stat')
        data = {"Success message": "Successfully created"}
        status = 200
    except Exception as e:
            data = {"Error message": str(e)}
            status = 400
    if connexion.request.is_json:
        body = Bodytemplate.from_dict(connexion.request.get_json())  # noqa: E501
    return data, status


def delete_temp_bytimeframe(timeframe):  # noqa: E501
    start = timeframe
    stop = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ" )
    stop = (stop+datetime.timedelta(days=+1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    STUD_INFLUX_HOST_ADD,STUD_INFLUX_ORG,STUD_INFLUX_TOKEN = get_vars()
    _db_client= getclient()
    try:
        result =_db_client.delete_api().delete(start, stop, predicate='_measurement="weather" AND station="Tartu" ', bucket='weather_data', org=STUD_INFLUX_ORG)
        print(start,stop,result)
        data = {"Success message": "Successfully deleted"}
        status = 200
    except Exception as e:
            data = {"Error message": str(e)}
            status = 400
    return data, status

def get_temp_bytimeframe(timeframe):  # noqa: E501
    query=""

    #Get the db client
    _db_client = getclient()
    #Get the env variables
    STUD_INFLUX_HOST_ADD,STUD_INFLUX_ORG,STUD_INFLUX_TOKEN = get_vars()
    # Build the query
    try:
        if timeframe == '1hr':
            query = '''from(bucket:"weather_data")
                    |> range(start: -1h,stop: now())
           	        |> filter(fn: (r) => r["_measurement"] == "weather")
                    |> filter(fn: (r) => r["_field"] == "temp")
                    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'''
        elif timeframe == '6hr':
            query = '''from(bucket:"weather_data")
                    |> range(start: -6h,stop: now())
                    |> filter(fn: (r) => r["_measurement"] == "weather")
                    |> filter(fn: (r) => r["_field"] == "temp")
                    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'''
        elif timeframe == '1day':
            query = '''from(bucket:"weather_data")
                    |> range(start: -1d,stop: now())
                    |> filter(fn: (r) => r["_measurement"] == "weather")
                    |> filter(fn: (r) => r["_field"] == "temp")
                    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'''
        elif timeframe == '1week':
            query = '''from(bucket:"weather_data")
                    |> range(start: -7d,stop: now())
                    |> filter(fn: (r) => r["_measurement"] == "weather")
                    |> filter(fn: (r) => r["_field"] == "temp")
                    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'''
        else :
            return {"Error Message": "Invalid timeframe"}, 400
        
        # retrieve the temp records from influxdb    
        df  = _db_client.query_api().query_data_frame(org=STUD_INFLUX_ORG, query=query)

        # Handle exceptions and report the output
        if not df.empty:
            df = df.drop(columns=['result', 'table','_start','_stop'])
            data = df.to_json(orient="records")
            data = json.loads(data)
            status = 200
        else :
            status = 400
            data = {"Error Message": "It seems, I am unable to get any data. The dataframe is empty"}, 400
    except Exception as e:
            data = {"Error message": str(e)}
            status = 404
    return data, status


def update_avg_temperature(body):  # noqa: E501
    _db_client = getclient()
    data = body
    print(data)
    date = data["tags"]["date"]
    station = data["tags"]["station"]
    df = getavg(date)
    field = data["field"]
    print(df)
    value=df.loc[0, 'temp']
    start = date+"T00:00:00Z"
#   stop = str(datetime.date.today())+"T00:00:00Z"
#   stop = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ" )
    stop = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    _db_client = getclient()
    STUD_INFLUX_HOST_ADD,STUD_INFLUX_ORG,STUD_INFLUX_TOKEN = get_vars()
    try:
        result =_db_client.delete_api().delete(start, stop, predicate='_measurement="weather_stat" AND date="'+date+'"', bucket='weather_data', org=STUD_INFLUX_ORG)
        print(start,stop,result)
    except Exception as e:
            print(e)

    current_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    point1 = Point("weather_stat").field(field,value).tag("station",station).tag("date",date).time(current_time)
    try:
        response=_db_client.write_api().write("weather_data", record = [point1],data_frame_measurement_name='weather_stat')
        data = {"Success message": "Successfully created"}
        status = 200
    except Exception as e:
            data = {"Error message": str(e)}
            status = 400
    if connexion.request.is_json:
        body = Bodytemplate.from_dict(connexion.request.get_json())  # noqa: E501
    return data, status