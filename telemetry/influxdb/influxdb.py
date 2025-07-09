import logging
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Setup logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# InfluxDB client setup
influxdb_token = "C1sco12345!"
influxdb_org = "lab"
influxdb_bucket = "vrf"
influxdb_url = "http://198.18.140.3:8086"

client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Variable to be pushed
variable_name = "test_variable"
variable_value = 42

try:
    # Create a point and write it to the InfluxDB bucket
    point = Point("simple_measurement")\
        .tag("variable", variable_name)\
        .field("value", variable_value)\
        .time(time.time_ns(), WritePrecision.NS)
    
    write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=point)
    logging.info(f"Successfully pushed {variable_name} with value {variable_value} to InfluxDB.")
except Exception as e:
    logging.error(f"Failed to push data to InfluxDB: {e}")
