# NOATS
Networked Open source Agricultural Things Specification

Bill of Materials
1. Seeed Studio soil moisture sensor
2. DS18B20 digital temperature sensor
3. MCP3008 ADC
4. Raspberry Pi 2B
5. Raspberry Pi 3
6. HopeRF RFM95W LoRa Module x2
7. Antenna x2

A list of libbraries used in this project:
1. Python 3 and Pip3: required to install the subsequent libraries
2. Mysql server: for storage of sensor data in a database
3. Mysql connector python: for inserting sensor data in the database
      - pip3 install mysql-connector-python
4. Adafruit circuitpython rfm9x: for testing the rfm lora module
      - pip3 install adafruit-circuitpython-rfm9x
5. Adafruit circuitpython tinylora: for creating and managing devices on The Things Network 
      - pip3 install adafruit-circuitpython-tinylora
6. MQTT Python client: for accessing sensor data via the things network API
      - pip3 install paho-mqtt

**SAMPLE OUTPUT RESULTS

1. A sample of the output of the gateway when it is receiving packets from the nodes is shown on the image titled "terminal_output.png".
2. After successfully registering devices, your TTN console should look something like that on the image titled "registered_devices.png".
3. A sample of the output of the terminal after successfully executing the API code is shown in the image titled "API_output.png".
4. Individual soil moisture and soil temperature consoles are shown on the images titled "soil_moisture_console.png" and "temperature_console.png" respectively
5. A sample output of a sensor sending data to TTN is shown in the image titled "soil_moisture_data.png'
6. The metadata provided by TTN giving information about the packets sent is shown in the image titled "moisture_metadata.png".
7. The soil moisture and soil temperature graphs generated in Grafan are shown in images titled "grafana_soil_moisture.png" and "grafana_soil_temperature.png" respectively. 

**Step-by-step approach to creating the NOATS based Wireless Sensor Network

**Acquire the materials listed in the BOM above.

**Set up gateway

1. Connect antenna to the LoRa module pin labelled "ANT".
2. Connect the LoRa module to the Raspberry Pi 3.
3. In the "gatewaytwo" folder, open the global_conf.json file to ensure the pin numbers set correspond with the physical ones.
4. Execute the "single_chan_pkt_fwd" code in the "gateway.zip" file .
5. A sample of the output of the gateway when it is receiving packets from the nodes is shown on the image titled "terminal_output.png".


**Node

1. Connect the soil moisture sensor to the ADC
2. The ADC uses SPI to communicate with the MCU, connect the pins accordingly with the Raspberry Pi 2B SPI connections.
3. The DS18B20 uses 1-wire interface to communicate with the MCU, connect it to the designated 1-wire pin on the Raspberry Pi.
4. Connect the antenna onto the LoRa module on the pin labelled "ANT".
5. When the antenna is fully secure, connect the LoRa module to the Raspberry Pi (make use of the datasheets to make sure to connect to the correct pins).
6. Execute the code in "send_sensor_data.py"

**If not registered with the The Things Network, register at https://thethingsnetwork.org to register devices and a gateway.

1. After successfully registering devices, your TTN console should look something like that on the image titled "registered_devices.png".
2. Individual soil moisture and soil temperature consoles are shown on the images titled "soil_moisture_console.png" and "temperature_console.png" respectively.

**To extract data from The Things Network, use TTN API and send to database.

1. Execute the code "collect_data.py" found in the repo.
2. A sample of the output of the terminal after successfully executing the API code is shown in the image titled "API_output.png".

**Using MySQL

The following instructions are executed on the mysql shell in a Linux-based machine. 
See: https://support.rackspace.com/how-to/installing-mysql-server-on-ubuntu/

**Create a database and tables for each sensor*

create schema Bontle_database;
use Bontle_database;
create table temperature(time_stamp datetime primary key, temperature double, snr double, rssi double);
create table soil_moisture(time_stamp datetime primary key, moisture double, snr double, rssi double);

**create new user to have access to the database, this is needed so that the pi can insert data into the database*

create user 'newuser'@'localhost' identified by 'password';
grant all privileges on Bontle_database.* to 'user'@ip_addresss with grant option; 

**Displaying sensor data on Grafana

1. Navigate to http://grafana.com
2. Select MySQL as a datasource
3. Enter credentials created in the database creation section above
4. When connected, the sensor tables will appear. Select the one(s) required and voila! You can now monitor your sensor data in real time. Congratulations.
