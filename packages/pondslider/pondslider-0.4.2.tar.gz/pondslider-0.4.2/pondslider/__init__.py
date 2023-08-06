# coding:utf-8 Copy Right Takeyuki UEDA © 2015 -
#
import os
import sys
#import inspect
import traceback
#import subprocess
#import datetime
import importlib
#import logging
#import ConfigParser
import pytoml as toml

# Const
#reboot = 'sudo reboot'

def error_report():
  info=sys.exc_info()
  print (traceback.format_exc(info[0]))

def read(configfilepath):
  if os.path.exists(configfilepath):
    with open(configfilepath, 'rb') as fin:
      config = toml.load(fin)

    if "sensors" in config.keys():
      for sensor in config["sensors"]:
        if "handler" in sensor.keys():
          # road sensor_handler.
          sensor_handler = importlib.import_module(sensor["handler"])
          try:
            red_values = sensor_handler.read()
            print(red_values)
          except:
            error_report()
            continue

          if "values" in sensor.keys():
            values = sensor["values"]
            for value in values:
              if "name" in value.keys():
                if value["name"] in red_values.keys():
                  if "handlers" in value.keys():
                    for handler in value["handlers"]:
                      try:
                        value_handler = importlib.import_module(handler)
                        value_handler.handle(sensor_handler, value["name"], red_values[value["name"]])
                      except:
                        error_report()
                        continue
                  if "terminator" in value.keys():
                    if value["terminator"]:
                      try:
                        terminator_handler = importlib.import_module(value["terminator"])
                        print ("call value handler")
                        terminator_handler.terminate(sensor_handler, value["name"], red_values[value["name"]])
                      except:
                        error_report()
                        continue

def read2(sensor_handlers, value_handlers, terminators):
  if not sensor_handlers is None:
    for s in sensor_handlers:
      # road sensor_handler.
      sensor_handler = importlib.import_module(s)
      try:
        red_values = sensor_handler.read()
        print(red_values)
      except:
        error_report()
        continue

      for name, value in red_values.items():
        if not value_handlers is None:
          for v in value_handlers:
            try:
              value_handler = importlib.import_module(v)
              value_handler.handle(sensor_handler, name, value)
            except:
              error_report()
              continue
        if not terminators is None:
          for v in terminators:
            try:
              terminator = importlib.import_module(v)
              terminator.terminate(sensor_handler, name, value)
            except:
              error_report()
              continue
