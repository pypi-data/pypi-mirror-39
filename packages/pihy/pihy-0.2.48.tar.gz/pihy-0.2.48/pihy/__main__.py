import schedule
import time
import json
import os
import sys

from .x import joke
from .AtlasI2C import AtlasI2C

storage_path = "/var/www/dist/logs/ph.json"
run = True
runPump = 0

ph = AtlasI2C()   # creates the I2C port object, specify the address or bus if necessary
ph.set_i2c_address(99)
ph.set_is_sensor(True)

pump = AtlasI2C()   # creates the I2C port object, specify the address or bus if necessary
pump.set_i2c_address(103)
pump.set_is_sensor(False)

def PHLong():
  global runPump
  data = None
  if os.path.exists(storage_path):
    with open(storage_path,'r') as f:
      try:
        data = json.load(f)
      except Exception as e:
        print("got %s on json.load()" % e)

  if data is None:
    print('Create new dataset')
    data = [ ]

  xTime = time.strftime("%Y-%m-%d %H:%M:%S")
  xVal = ph.query("R")

  if xVal > 6.0:
    runPump = runPump + 1
  elif runPump and xVal < 5.75:
    runPump = 0

  data.append({'time': xTime, 'value': xVal})
  
  with open(storage_path, 'w') as outfile:
    json.dump(data, outfile)

def PHShort():
  xTime = time.strftime("%Y-%m-%d %H:%M:%S")
  xVal = ph.query("R")
  print("%s: pH %s" % (xTime, xVal))

def PumpLong():
  print("PUMP VALUE: %s" % runPump)
  if runPump > 2:
    print("PUMP IT!!")
    print(pump.query("D,2"))

def Goodbye():
  global run
  print("Goodbye")
  run = False


def main():
  
  schedule.every(1).seconds.do(PHShort)
  schedule.every(1).minutes.do(PHLong)
  schedule.every(1).minutes.do(PumpLong)
  schedule.every().day.at("23:55").do(Goodbye)
  
  try:
    while run:
      schedule.run_pending()
      time.sleep(1)
  except KeyboardInterrupt:     # catches the ctrl-c command, which breaks the loop above
    print("Continuous polling stopped")

if __name__ == '__main__':
  main()




