#!/bin/sh

LCD=0x3e
NETWORK=wlan0

LANG=
#IP=`/sbin/ifconfig $NETWORK | grep "inet addr:" | cut -f2 -d : | cut -f1 -d " "`
IP=`/bin/hostname -I | cut -f1 -d' '`

echo "IP: $IP"

ip_char_at(){
  ch=`echo -n $IP | od -An -tx1 | cut -d " " -f$1`
  if [ -z $ch ]; then
    echo 0x20
  else
    echo 0x$ch
  fi
}

IP1=`ip_char_at 2`
IP2=`ip_char_at 3`
IP3=`ip_char_at 4`
IP4=`ip_char_at 5`
IP5=`ip_char_at 6`
IP6=`ip_char_at 7`
IP7=`ip_char_at 8`
IP8=`ip_char_at 9`
IP9=`ip_char_at 10`
IP10=`ip_char_at 11`
IP11=`ip_char_at 12`
IP12=`ip_char_at 13`
IP13=`ip_char_at 14`
IP14=`ip_char_at 15`
IP15=`ip_char_at 16`

sudo i2cset -y 1 $LCD 0x00 0x38 0x39 0x14 0x70 0x56 0x6c i
sudo i2cset -y 1 $LCD 0x00 0x38 0x0c 0x01 i
sudo i2cset -y 1 $LCD 0x40 $IP1 $IP2 $IP3 $IP4 $IP5 $IP6 $IP7 $IP8 i
sudo i2cset -y 1 $LCD 0x00 0xc0 i
sudo i2cset -y 1 $LCD 0x40 $IP9 $IP10 $IP11 $IP12 $IP13 $IP14 $IP15 i