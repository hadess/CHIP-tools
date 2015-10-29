#!/usr/bin/env python

import io
import sys
import serial
import re
import time

#------------------------------------------------------------------
def answer_prompt(sio,prompt_to_wait_for,answer_to_write,send_cr=True):
#------------------------------------------------------------------
  sio.flush()
  prompt_found = False
  data = ''
  #if send_cr:
    #sio.write(unicode('\n'))

  d='something'
  while not len(d)==0:
    d = sio.read(2000);
    data += d
    time.sleep(1)
#    print '-' * 50
#    print ' %d bytes read' % (len(data))
#    print '-' * 50

  #print data

  line=''
  while not prompt_found:
    d = sio.read(100);
    data += d
#    print '-' * 50
#    print ' %d bytes read' % (len(data))
#    print '-' * 50
#    print data
#    print '-' * 50
    if len(data.split())>0:
      line=data.split()[-1]
#    print "matching [%s] against [%s]" % (line,prompt_to_wait_for)
    if(re.match(prompt_to_wait_for,line,re.M)):
        sio.write(unicode(answer_to_write+'\n'))
#        print '-' * 50
#        print ' detected [%s] ' % prompt_to_wait_for
#        print '-' * 50
        prompt_found = True
    else:
        if send_cr:
          sio.write(unicode('\n'))
    sio.flush()
    #sys.stdin.readline()

#------------------------------------------------------------------
def scanfor(sio,regexp_to_scan_for,answer_to_write):
#------------------------------------------------------------------
  prompt_found = False
  data = ''
  while not prompt_found:
    data += sio.read(100);
#    print '-' * 50
#    print ' %d bytes read' % (len(data))
#    print '-' * 50
#    print data
    if re.search(regexp_to_scan_for,data):
#        print '-' * 50
#        print ' detected [%s] ' % regexp_to_scan_for
#        print '-' * 50
        sio.write(unicode(answer_to_write+'\n'))
        prompt_found = True
    sio.flush()
  return data


#------------------------------------------------------------------
def main():
#------------------------------------------------------------------

  if( len(sys.argv)>1 ):
    serial_port=sys.argv[1]
  else:
    serial_port='/dev/ttyACM0';

  #print 'reading from %s:' % serial_port

  ser = serial.Serial(serial_port,115200, timeout=1);
  sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))

  #login

  print "login...",
  sys.stdout.flush()
  answer_prompt(sio,'.*login:','chip',True)
  print "OK\npassword...",
  sys.stdout.flush()
  answer_prompt(sio,'.*Password:','chip',False)
  print "OK\npoweroff...",
  sys.stdout.flush()
  answer_prompt(sio,'.*[\$#]','sudo poweroff')
  answer_prompt(sio,'.*:','chip')
  time.sleep(2)
  print "OK\n",
  #d=scanfor(sio,r'.*### [^#]+ ###.*','poweroff')
#  if re.search(r'.*### ALL TESTS PASSED ###.*',d):
#    print "---> TESTS PASSED"
#    ser.close();
#    return 0 
    
  ser.close();
  
#  print "---> TESTS FAILED"
  return 0



#------------------------------------------------------------------
if __name__ == "__main__":
#------------------------------------------------------------------
  exit( main() )
