#! /bin/bash

show_tree() {
#	sleep 0.5
	local root_dir=$1
	local root_file=$2
	local fond_file
	local level=$3
	local i=$3
	local files=`cat $root_dir/$root_file|grep "include" |awk -F '"' '{print $2}'`
	while((i--))
	do
		echo -e "	\c"
	done
	echo `basename $root_file`
	local file
	for file in $files
	do
			fond_file=`find $root_dir/ |grep $file`
			file=${fond_file#$root_dir}
			show_tree $root_dir $file $((level+1))
	done
}
#echo $(python -c "import os; print os.path.dirname(os.path.realpath('$0'))")
# `readlink -f` won't work on Mac, this hack should work on all systems.
#cd $(python -c "import os; print os.path.dirname(os.path.realpath('$0'))")

root_dir=`dirname $1`
root_file=`basename $1`
show_tree $root_dir $root_file 0
