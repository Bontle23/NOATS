"""
python code to send data from the senors to read the data from the senors and send it to the server 
Author: Bontle Mere
"""
#import the required libraries 
import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import digitalio
import adafruit_rfm9x
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008  


#set up spi for the rfm module to connect to tiny lora
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(board.CE1)
irq = digitalio.DigitalInOut(board.D7)
rst = digitalio.DigitalInOut(board.D4)

#set up the temperature sensor device for tiny lora
temp_addr = bytearray([0x26, 0x01, 0x18, 0x92])
# network key from the things network console
temp_netw_key = bytearray([0x4E, 0xF8, 0x21, 0xA4, 0x11, 0x98, 0xA8, 0x5D, 0x51, 0x2D, 0x2A, 0xD3, 0x0C, 0xCA, 0x91, 0xB7])
# application key from the things network console 
temp_app_key = bytearray([0x22, 0xD5, 0xC3, 0x29, 0xE9, 0x06, 0x77, 0xD9, 0x22, 0xBB, 0x28, 0xA6, 0x0B, 0x55, 0xB0, 0x62])
#configure the moisture sensor for the things network
temp_ttn_config = TTN(temp_addr, temp_netw_key, temp_app_key, country = "EU")
# create a tiny loar object for the temperature sensor
temp_lora = TinyLoRa(spi, cs, irq, rst, temp_ttn_config, channel = 0)

# set up the moisture sensor device for tiny lora
moisture_addr = bytearray([0x26, 0x01, 0x15, 0xA9])
# network key from the things network console
moisture_netw_key = bytearray([0xD9, 0x56, 0xFE, 0x3B, 0xDB, 0x76, 0x78, 0x4D, 0xBA, 0x28, 0x1E, 0x5D, 0x89, 0xE2, 0x11, 0xD4])
# application key from the things network console
moisture_app_key = bytearray([0xB2, 0x26, 0xDE, 0x4B, 0xB5, 0x99, 0xF7, 0x7D, 0xDD, 0xE1, 0xCD, 0x0B, 0x6C, 0x9D, 0xF2, 0x0E])
# configure the moisture sensor for the things network 
moisture_ttn_config = TTN(moisture_addr, moisture_netw_key, moisture_app_key, country = "EU")
# create a tiny loar object for the temperature sensor
moisture_lora = TinyLoRa(spi, cs, irq, rst, moisture_ttn_config, channel = 0)


#Configure SPI for the mcp3008 ADC 
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


def temperature(channel):
    """"function to read the temperature from the sensor"""
    """channel: channel number of the mcp3008 adc to read from
       return the temperature 
    """
    volts = ((mcp.read_adc(channel))*(3.3))/1024
    temperature = round(volts/(0.01), 2)
    return temperature 

def moisture(channel):
    """function to read the moisture from the sensor"""
    """channel: channel number of the mcp3008 adc to read from
       return the moisture as a percentage
    """
    read = mcp.read_adc(channel)
    moisture_percent = ((read/100)/(3.5))*100
    return moisture_percent

while True:  
    #read the temperature and transmit the data via the gateway        
    temp = bytearray( str(temperature(0)), "utf-8")
    temp_lora.send_data(temp, len(temp), temp_lora.frame_counter)
    temp_lora.frame_counter += 1
    print("sent")

    #read the soil moisture and transmit the data via the gateway
    print(moisture(1))
    moist = bytearray( str(moisture(1)), "utf-8")
    moisture_lora.send_data(moist, len(moist), moisture_lora.frame_counter )
    moisture_lora.frame_counter += 1
    time.sleep(0.1)		
	
