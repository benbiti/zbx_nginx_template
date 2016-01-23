#!/usr/bin/python

import re, struct, sys, os.path

# Nginx log file path
nginx_log_file_path = '/appsdata1/log/nginx/access.log'

# Temp file, with log file cursor position
seek_file = '/tmp/nginx_log_stat'

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

total_rps = 0
res_code = {}

nf = open(nginx_log_file_path, 'r')

new_seek = seek = read_seek(seek_file)
# if new log file, don't do seek
if os.path.getsize(nginx_log_file_path) > seek:
    nf.seek(seek)

line = nf.readline()
while line:

   new_seek = nf.tell()
   total_rps += 1
   code = re.match(r'(.*)"\s(\d*)\s', line).group(2)
   if code in res_code:
       res_code[code] += 1
   else:
       res_code[code] = 1

   line = nf.readline()

if total_rps != 0:
    write_seek(seek_file, str(new_seek))

nf.close()

if total_rps == 0:
    print 0
else :
    try:
        code_200 = res_code['200']
    except:
        code_200 = 0

    try:
        code_204 = res_code['204']
    except:
        code_204 = 0

    try:
        print (code_204 + code_200)*1.0/total_rps
    except:
        print 0/total_rps

