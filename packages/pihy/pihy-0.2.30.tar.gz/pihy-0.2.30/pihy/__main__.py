import time
import json
import os

from .x import joke
from .AtlasI2C import AtlasI2C

storage_path = "/var/www/dist/logs/ph.json"

def main():
  ph = AtlasI2C()   # creates the I2C port object, specify the address or bus if necessary
  ph.set_i2c_address(99)
  
  pump = AtlasI2C()   # creates the I2C port object, specify the address or bus if necessary
  pump.set_i2c_address(103)
  
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

  try:
    while True:
      xTime = time.strftime("%Y-%m-%d %H:%M:%S")
      xVal = ph.query("R")

      print("%s: pH %s" % (xTime, xVal))
      data.append({'time': xTime, 'value': xVal})
      
      with open(storage_path, 'w') as outfile:
        json.dump(data, outfile)
      
      time.sleep(60)

  except KeyboardInterrupt:     # catches the ctrl-c command, which breaks the loop above
    print("Continuous polling stopped")

if __name__ == '__main__':
  main()




