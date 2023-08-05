import schedule
import time
import json
import os
import sys

from .x import joke
from .AtlasI2C import AtlasI2C

storage_path = "/var/www/dist/logs/ph.json"
run = True

ph = AtlasI2C()   # creates the I2C port object, specify the address or bus if necessary
ph.set_i2c_address(99)

pump = AtlasI2C()   # creates the I2C port object, specify the address or bus if necessary
pump.set_i2c_address(103)

def PHLong():
  data = None
  if os.path.exists(storage_path):
    with open(storage_path,'r') as f:
      try:
        data = json.load(f)
        print('loaded that: ',data)
      except Exception as e:
        print("got %s on json.load()" % e)

  if data is None:
    print('Create new dataset')
    data = [ ]

  xTime = time.strftime("%Y-%m-%d %H:%M:%S")
  xVal = ph.query("R")

  data.append({'time': xTime, 'value': xVal})
  
  with open(storage_path, 'w') as outfile:
    json.dump(data, outfile)

def PHShort():
  xTime = time.strftime("%Y-%m-%d %H:%M:%S")
  xVal = ph.query("R")
  print("%s: pH %s" % (xTime, xVal))


def main():
  
  schedule.every(1).seconds.do(PHShort)
  schedule.every(1).minutes.do(PHLong)
  schedule.every().day.at("23:55").do(sys.exit)
  
  try:
    while run:
      schedule.run_pending()
      time.sleep(1)
  except KeyboardInterrupt:     # catches the ctrl-c command, which breaks the loop above
    print("Continuous polling stopped")

if __name__ == '__main__':
  main()




