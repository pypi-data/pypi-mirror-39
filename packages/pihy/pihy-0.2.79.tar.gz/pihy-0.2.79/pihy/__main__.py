import schedule
import time
import json
import os
import sys

from .x import joke
from .AtlasI2C import AtlasI2C

storage_path_ph_long = "/var/www/raspberry_reactjs/logs/ph"
storage_path_ph_short = "/var/www/raspberry_reactjs/logs/ph_short"
storage_path_pump = "/var/www/raspberry_reactjs/logs/pump"
storage_path_pump_run = "/var/www/raspberry_reactjs/logs/pump_run"

run = True
runPump = 0

ph = AtlasI2C()   # creates the I2C port object, specify the address or bus if necessary
ph.set_i2c_address(99)
ph.set_is_sensor(True)

pump = AtlasI2C()   # creates the I2C port object, specify the address or bus if necessary
pump.set_i2c_address(103)
pump.set_is_sensor(False)

def Log(storage, xVal, limit=-9):
  storage_today = storage + time.strftime("%Y-%m-%d") + ".json"
  storage_web = storage + ".json"
  
  data = None
  if os.path.exists(storage_today):
    with open(storage_today,'r') as f:
      try:
        data = json.load(f)
      except Exception as e:
        print("got %s on json.load()" % e)

  if data is None:
    print('Create new dataset')
    data = [ ]

  xTime = time.strftime("%Y-%m-%d %H:%M:%S")
  data.append({'time': xTime, 'value': xVal})

  if(limit>0):
    data = data[-limit:]

  with open(storage_today, 'w') as outfile:
    json.dump(data, outfile)
  
  with open(storage_web, 'w') as outfile:
    json.dump(data, outfile)

  return xTime

def PHLong():
  global runPump
  xVal = ph.query("R")

  if xVal > 6.0:
    runPump = runPump + 1
  elif runPump and xVal < 5.9:
    runPump = 0

  Log(storage_path_ph_long, xVal)
  Log(storage_path_pump_run, runPump)

def PHShort():
  xVal = ph.query("R")
  xTime = Log(storage_path_ph_short, xVal, 720)

  print("%s: pH %s" % (xTime, xVal))

def PumpLong():
  data = None
  print("PUMP VALUE: %s" % runPump)
  
  if runPump > 2:
    print("PUMP IT!!")
    phVal = ph.query("R")
    if phVal>6.5:
      pumpVal = 5
    elif phVal>6.25:
      pumpVal = 5
    elif phVal>6.1:
      pumpVal = 2
    elif phVal>6.0:
      pumpVal = 1
    else:
      pumpVal = 0.5

    print("PUMPING: %s" % pumpVal)

    print(pump.query("D,"+str(pumpVal)))

    Log(storage_path_pump,pumpVal)
    
def Goodbye():
  global run
  print("Goodbye")
  run = False


def main():
  print("Hello")
  
  schedule.every(5).seconds.do(PHShort)
  schedule.every(1).minutes.do(PHLong)
  schedule.every(30).minutes.do(PumpLong)
  schedule.every().day.at("23:55").do(Goodbye)
  
  try:
    while run:
      schedule.run_pending()
      time.sleep(1)
  except KeyboardInterrupt:     # catches the ctrl-c command, which breaks the loop above
    print("Continuous polling stopped")

if __name__ == '__main__':
  main()




