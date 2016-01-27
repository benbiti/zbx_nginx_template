#!/usr/bin/python

import struct, sys, os.path
from sqlalchemy import *



def read_seek(file):
    if os.path.isfile(file):
        f = open(file, 'r')
        try:
            result = int(f.readline())
            f.close()
            return result
        except:
            return 0
    else:
        return 0

def write_seek(file, value):
    f = open(file, 'w')
    f.write(value)
    f.close()


def check_alarms(clz, level):

  # Temp file, with log file cursor position
  seek_file = "/tmp/" + clz + "stat"
  seek = read_seek(seek_file)
  new_seek = 0
  failed_count = 0
  engine = create_engine('postgresql://rds.cn-north-1.amazonaws.com.cn')
  db = engine.connect()
  results = db.execute("select max(id) pos, count(id) failed_count from job_todo where clz='" + clz + "' and status='FAILED' and id >" + str(seek) )

  for row in results:
    if row['pos']:
        new_seek = row['pos']
    failed_count = row['failed_count']
  db.close()

  if  new_seek != 0:
      write_seek(seek_file, str(new_seek))

  return failed_count

if __name__ == "__main__":
    print check_alarms(sys.argv[1] , sys.argv[2])

