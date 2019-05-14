from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import random, time, sys, Adafruit_DHT

# A random programmatic shadow client ID.
SHADOW_CLIENT = "myShadowClient"

# The unique hostname that &IoT; generated for 
# this device.
HOST_NAME = "acrf1wh8dkfym-ats.iot.ap-southeast-1.amazonaws.com"

# The relative path to the correct root CA file for &IoT;, 
# which you have already saved onto this device.
ROOT_CA = "Root-CA.pem"

# The relative path to your private key file that 
# &IoT; generated for this device, which you 
# have already saved onto this device.
PRIVATE_KEY = "c3291a1ce4-private.pem.key"

# The relative path to your certificate file that 
# &IoT; generated for this device, which you 
# have already saved onto this device.
CERT_FILE = "c3291a1ce4-certificate.pem.crt.txt"

# A programmatic shadow handler name prefix.
SHADOW_HANDLER = "MyRPi"


# Automatically called whenever the shadow is updated.
def myShadowUpdateCallback(payload, responseStatus, token):
  print()
  print('UPDATE: $aws/things/' + SHADOW_HANDLER + 
    '/shadow/update/#')
  print("payload = " + payload)
  print("responseStatus = " + responseStatus)
  print("token = " + token)

# Create, configure, and connect a shadow client.
myShadowClient = AWSIoTMQTTShadowClient(SHADOW_CLIENT)
myShadowClient.configureEndpoint(HOST_NAME, 8883)
myShadowClient.configureCredentials(ROOT_CA, PRIVATE_KEY,
  CERT_FILE)
myShadowClient.configureConnectDisconnectTimeout(10)
myShadowClient.configureMQTTOperationTimeout(5)
myShadowClient.connect()

# Create a programmatic representation of the shadow.
myDeviceShadow = myShadowClient.createShadowHandlerWithName(
  SHADOW_HANDLER, True)

# Keep generating random test data until this script 
# stops running.
# To stop running this script, press Ctrl+C.
while True:
  # Generate random True or False test data to represent
  # okay or low moisture levels, respectively.
  hum, tem = Adafruit_DHT.read_retry(11, 21)
  humidity = str(hum)
  temperature = str(tem)

#  if hum > 94:
#    moisture = True
#  else:
#    moisture = False

#  if moisture:
#    myDeviceShadow.shadowUpdate(
#      '{"state":{"reported":{"moisture":"okay"}}}',
#      myShadowUpdateCallback, 5)
# else:
  myDeviceShadow.shadowUpdate(
     '{"state":{"reported":{"moisture":"low","humidity":"'+humidity +
     '% ","temperature":"'+ temperature + '*C"}}}',
     myShadowUpdateCallback, 5)

  # Wait for this test value to be added.
  time.sleep(5)
