from influxdb_client import InfluxDBClient, Point, WritePrecision

# InfluxDB client setup
influxdb_token = "C1sco12345!"  # Authentication token for InfluxDB
influxdb_org = "lab"            # Organization name in InfluxDB
influxdb_bucket = "vrf"         # Bucket name where data will be stored
influxdb_url = "http://198.18.140.3:8086"  # URL of the InfluxDB server

# Create an InfluxDB client instance
client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)

# Create a write API instance with synchronous write option
write_api = client.write_api(write_options=WritePrecision.NS)

# Variable to be pushed to InfluxDB
variable_name = "test_variable"  # Name of the variable (tag)
variable_value = 42              # Value of the variable (field)

# Create a point and write it to the InfluxDB bucket
point = Point("simple_measurement")\
    .tag("variable", variable_name)\
    .field("value", variable_value)\
    .time(time.time_ns(), WritePrecision.NS)  # Create a data point

write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=point)  # Write the data point to InfluxDB







