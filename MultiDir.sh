#!/bin/bash
if [ $# -ne 0 ]; then
	while getopts i: option
	do
		case "${option}"
		in
			i) FILE="${OPTARG}";;
		esac
	done
	\date 
	\cd "$FILE"
	for dir in $(\ls "$FILE") 
	do
		if [ $dir = "Output" ]; then
		:
		elif [ -d "$FILE"/"$dir" ]
		then
			\cd "$FILE"/"$dir"
			\echo $PWD
			python /home/adam/Workspaces/Python_Spyder/Annotation/Master_Glue.py -r "$FILE"/"$dir"/"$dir.gbk" -p "$FILE"/"$dir"/"$dir.prod" -f "$FILE"/"$dir"/"$dir.fa" -o "$FILE"/"$dir"/"$dir.out"
			\echo 
			\cd ..
		fi
	done
	\cd "$FILE"
	\mkdir Output
	\find . -name "*.out" -exec mv -t ./Output/ {} \+
else
	\echo "Please provide an input directory."
fi
