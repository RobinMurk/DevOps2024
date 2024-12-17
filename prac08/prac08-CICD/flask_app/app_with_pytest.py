#Flask imports
from flask import Flask, render_template, send_file, make_response, url_for
from flask import Response 

# Influx
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.exceptions import InfluxDBError

#Pandas 
import pandas as pd
from dateutil import tz


import io
import random
import os

# Read the data 
STUD_INFLUX_HOST_ADD=os.getenv('STUD_INFLUX_HOST_ADD')
STUD_INFLUX_ORG=os.getenv('STUD_INFLUX_ORG')
STUD_INFLUX_TOKEN=os.getenv('STUD_INFLUX_TOKEN')

err_msg = ""
df = pd.DataFrame()
client = None
query = ""

def test_initialization():
    initialize()
    global client
    global query
    assert client != None
    assert query != ""

def test_get_data():
    global client
    global query
    df = get_data(client, query)
    assert df.empty == False

def test_convert_time():
    global df
    df = convert_time(df)
    assert df.empty == False




def is_df_empty(df):
    return df.empty

def forward_data_to_html(df):
    if is_df_empty(df):
        # return render_template('home.html', table=err_msg)
        return render_template('404.html', error=err_msg)
    else:        
        return render_template('home.html', table=df.to_html(index = False) )

def convert_time(df):
    global err_msg
    if is_df_empty(df): 
        # df is empty
        if not err_msg:
            err_msg = "_______No data to found__________Try changing the duration."
        return df
    else:
        # df is not empty
        df['_start'] = df['_start'].dt.tz_convert(tz='Europe/Tallinn')
        df['_stop'] = df['_stop'].dt.tz_convert(tz='Europe/Tallinn')
        df['_time'] = df['_time'].dt.tz_convert(tz='Europe/Tallinn')
        return df

def get_data(client, data_query):
    """
    Get the data from remote DB
    Returns:
        The data in dataframe if connection and token authentication are successful, False otherwise
    """
    global err_msg
    global df

    try:
        # Attempt a query to get data        
        df = client.query_api().query_data_frame(org=STUD_INFLUX_ORG, query=data_query)       
    except InfluxDBError as e:
        err_msg = err_msg + f"\n\nInfluxDB Error:******* {e}"
    except Exception as e:
        # print(f"An error occurred: {e}")
        err_msg = err_msg + f"\n\nAn error occurred::******* {e}"
    return df


   
def initialize():    
    global client
    global query
    client = InfluxDBClient(url=STUD_INFLUX_HOST_ADD, token=STUD_INFLUX_TOKEN, org=STUD_INFLUX_ORG, debug=True)
    query= '''
        from(bucket: "weather_data") 
        |> range(start:-60d, stop: now())
        |> filter(fn: (r) => r._measurement == "weather")
        |> filter(fn: (r) => r._field == "temp")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'''

    return client, query # this statement is not needed


# Create a flask app
app = Flask(__name__)

# main route
@app.route('/')
@app.route('/pandas', methods=("POST", "GET"))
def GK():
    # return render_template('home.html',
                        #    PageTitle = "weather",table=[df.to_html(classes='data', index = False)], titles=df.columns.values)
    return forward_data_to_html(df)

if __name__ == '__main__':
    # global client
    # global query
    # global df
    initialize()
    get_data(client, query)
    df = convert_time(df)
    app.run(debug = True,host='0.0.0.0',port=5000)

