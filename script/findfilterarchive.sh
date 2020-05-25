#!/bin/bash

function usage() {
cat << _EOT_
Usage:
  $0 [-a] [-b] [-f filename] arg1 ...

Description:
  hogehogehoge

Options:
  -a    aaaaaaaaaa
  -b    bbbbbbbbbb
  -f    ffffffffff
_EOT_
exit 1
}

# 
if [ "$OPTIND" = 1 ]; then
    while getopts abf:h OPT
    do
	case $OPT in
	    a)
		FLAG_A="on"
		echo "FLAG_A is $FLAG_A"
		;;
	    b)
		FLAG_B="on"
		echo "FLAG_B is $FLAG_B" 
		;;
	    f)
		ARG_F=$OPTARG
		echo "ARG_F is $ARG_F"
		;;
	    h)
		echo "help"
		usage
		;;
	    \?)
		echo "Try to enter the h option." 1>&2
		;;
	esac
    done
else
    echo "No installed getopts-command." 1>&2
    exit 1
    fi

MODELNAME=${1,,}

GPSTIME=$2
if [ ${#2} -ne 10 ];then
    GPSTIME=`gpstime $2 | tail -n1 | awk -F'[:]' '{print int($2)}'`
fi
# main
PREFIX=/opt/rtcds/kamioka/k1/chans/filter_archive/$MODELNAME/
if test -d ${PREFIX}
then
ls $PREFIX\
    | awk -v GPS=$GPSTIME -v PF=$PREFIX -F'[_.]' '$2>GPS && NF==3 {print PF$0}' \
    | head -n1
else
    echo "nothing"
fi
# if test "${FILE}" = "" 
# then
#     echo "nothing"
# else
#     echo ${FILE}
# fi

