if [ $# -ge 1 ] ;then
	files=`echo $1|sed 's/out.*system/system/g'`
else
	files=`cat Install.txt |sed 's/Install.*system/system/g'`
fi
for f in $files 
do
	echo /$f
	adb push $OUT/$f /$f
done
