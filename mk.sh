start_time=`date +%s`
MYOUT=test_out
kernel_out=$MYOUT/KERNEL_OBJ
if [ ! -d $kernel_out ] 
then
	mkdir -p $kernel_out
fi
make O=$MYOUT/KERNEL_OBJ ARCH=arm64 CROSS_COMPILE=aarch64-linux-android- mirageplus01a_msm_defconfig
make O=$MYOUT/KERNEL_OBJ ARCH=arm64 CROSS_COMPILE=aarch64-linux-android- -j8
dtbTool -o $MYOUT/dt.img -s 2048 -p $kernel_out/scripts/dtc/ $kernel_out/arch/arm64/boot/dts/
acp -fp $kernel_out/arch/arm64/boot/Image $MYOUT/Image
mkbootfs $MYOUT/root | minigzip > $MYOUT/ramdisk.img
mkbootimg  --kernel $MYOUT/Image --ramdisk $MYOUT/ramdisk.img --cmdline "console=ttyHSL0,115200,n8 androidboot.console=ttyHSL0 androidboot.hardware=qcom msm_rtb.filter=0x237 ehci-hcd.park=3 androidboot.bootdevice=7824900.sdhci lpm_levels.sleep_disabled=1 earlyprintk" --base 0x80000000 --pagesize 2048 --dt $MYOUT/dt.img  --output $MYOUT/boot.img
end_time=`date +%s`
echo =========$(expr $end_time - $start_time)s========
