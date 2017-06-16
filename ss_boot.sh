# !/bin/sh
function send_img()
{
	local _imagName=$1
	local _partition=$2
	#       adb wait-for-device
	#       adb reboot bootloader
	echo $_imagName:$_partition
	fastboot flash $_partition $_imagName
	#       fastboot reboot
}

function send_one()
{
	local filename="boot.img"
	local partition="boot"
	if [ "$1" != "" ]
	then
		case $1 in
			boot)
				filename="boot.img"
				partition="boot"
				;;
			sys)
				filename="system.img"
				partition="system"
				;;
			lk)
				filename="emmc_appsboot.mbn"
				partition="aboot"
				;;
			re)
				filename="recovery.img"
				partition="recovery"
				;;
			user)
				filename="userdata.img"
				partition="userdata"
				;;
			*)
				filename="boot.img"
				partition="boot"
				exit
				;;
		esac
	fi
	send_img $OUT/$filename $partition

}
function main()
{
	local args
	adb reboot bootloader
	if [ $? -ne 0 ]
	then
		adb wait-for-device
		adb reboot bootloader
	fi
	for args in $@
	do
		echo $args
		send_one $args
	done
	fastboot reboot

}
if [ $# -lt 1 ]
then
	echo usage:`basename $0` boot lk re sys
	exit
fi
ret=$(main $@)
echo $ret
