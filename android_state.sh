#!/bin/sh
function unlock_screen()
{
	local ret_m=$(display_power_state)
	ret_m=${ret_m::-1}
	if [ "v$ret_m" == "vOFF" ]
	then
		adb -s $serial_number  shell input keyevent POWER
	fi
	sleep 0.5
	adb -s $serial_number  shell input swipe 600 800 600 100
}

function is_screen_locked()
{
	adb -s $serial_number shell dumpsys window policy|grep isStatusBarKeyguard|awk -F '=' '{print $3}'
}
function display_power_state()
{
	adb -s $serial_number shell dumpsys power |grep "Display Power"|awk -F '=' '{print $2}'
}

if [ $# -lt 2 ]
then
	echo usage:`basename $0` serial_number file_prefix
	exit
fi

serial_number=$1
file_prefix=$2
unlock_screen
