#Flask imports
from flask import Flask, render_template, send_file, make_response, url_for
from flask import Response, request

# Influx
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.warnings import MissingPivotFunction

#Pandas 
import pandas as pd
import datetime
import warnings
import io
import random
import os

# Read the data 
INFLUX_HOST_ADD=os.getenv('INFLUX_HOST_ADD','http://172.17.91.7:8086')
INFLUX_ORG=os.getenv('INFLUX_ORG','UT')
INFLUX_TOKEN=os.getenv('INFLUX_TOKEN','YYmgQ7vp6l2dzJOB-oP8SoijWdpxQpvq8LpQI1cM1YRKnO6KnggeTmPm9PXuPmastJ_S3_m_zoEk1Ff2nDubuA==')

#Connect to Influxdb database server

_db_client = InfluxDBClient(url=INFLUX_HOST_ADD, token=INFLUX_TOKEN, org=INFLUX_ORG, debug=True)

# The following query retrieve the temp data of Tartu City for previous 60minutes
# Database name=weather_data
# Measurement name=weather

try:
    query= '''
            from(bucket: "weather_data")
            |> range(start: 2024-09-01T17:47:00Z, stop: now())
            |> filter(fn: (r) => r._measurement == "weather")
            |> filter(fn: (r) => r._field == "temp")'''
    result = _db_client.query_api().query_data_frame(org=INFLUX_ORG, query=query)
    df=result[result.columns[4:]]

    today = datetime.date.today()
    data = (df['_time'].dt.date == today)
    today_data = df[data]
    minTemp = today_data['_value'].min()
    maxTemp = today_data['_value'].max()
except:
    print("error getting data")
# Create a flask app
app = Flask(__name__)

# main route
@app.route('/')
@app.route('/pandas', methods=("POST", "GET"))
def GK():
    ip = request.host.split(':')[0]
    name = "Robin Mürk"
    return render_template('home.html',
                           PageTitle = "weather",table=[df.to_html(classes='data', index = False)], titles=df.columns.values,minTemp=minTemp, maxTemp=maxTemp, ip=ip, name=name)

if __name__ == '__main__':
    app.run(debug = True,host='0.0.0.0',port=5000)

