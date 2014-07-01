#!/bin/bash

while getopts i: option
do
	case "${option}"
	in
		i) FILE=${OPTARG};;
	esac
done

\date 
\cd $FILE
for dir in $(\ls "$FILE") 
do
	if [ -d "$FILE/$dir" ]
	then
		\cd "$FILE/$dir"
		\echo $PWD
		#python /home/burbs/Workspaces/Python_spyder/Single_Contig_Annotation/Master_Glue.py -r $FILE/$dir/$dir.gbk -p $FILE/$dir/$dir.prod -f $FILE/$dir/$dir.fa -o $FILE/$dir/$dir.out
		python /home/burbs/Workspaces/Python_spyder/Single_Contig_Annotation/Master_Glue.py -r $FILE/$dir.gbk -p $FILE/$dir.prod -f $FILE/$dir.fa -o $FILE/$dir.out
		\echo 
		\cd ..
	fi
done

\mkdir Output
\find . -name "*.out" -exec mv -t ./Output/ {} \+
