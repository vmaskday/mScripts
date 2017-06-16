#!/bin/sh
cat > fastboot_all.sh <<EOF
#!/bin/sh
function die()
{
	 if [ \$? != 0 ]
	 then
		 exit -1
	 fi
}
EOF
echo adb wait-for-device  >> fastboot_all.sh 
echo adb reboot bootloader >> fastboot_all.sh
echo sleep 1  >> fastboot_all.sh
cat partition.xml |grep label |awk -F '"' '{ if ($12 > 0) { print "fastboot flash " $2 " " $12 "\n die"} }' >> fastboot_all.sh
cat rawprogram0.xml|awk -F '"' '{ if ($6 > 0) { print "fastboot flash " $8 " " $6 "\ndie"} }' >> fastboot_all.sh
