#!/bin/bash

###############################################################
#运行python程序
#   $1   程序运行脚本完整路径及启动参数
function runPython()
{
    appCmd=$1

    appRunNum=`ps -ef|grep  "$appCmd" |grep -v "grep"|wc -l`
    if [ $appRunNum -gt 0 ]
    then
        echo "close $appRunNum $appCmd" >> $LogFile
        ps -ef|grep  "$appCmd" |grep -v "grep"|awk '{print $2}'|xargs kill -9
    fi

    echo "[`date "+%Y-%m-%d %H:%M:%S" `] python3 $appCmd" >> $LogFile
    python3 $appCmd &>> $LogFile
}

################################################################
#程序从这里开始
WORKDIR=`cd $(dirname $0);pwd -P`
cd $WORKDIR

#设置日志目录和名字
logDir="/data/tradeTip/log/run"
if [ ! -d $logDir ]; then
  mkdir -p $logDir
fi
CurDate=`date "+%Y%m%d"`
LogFile="$logDir/run.log.$CurDate"

runPython "$WORKDIR/indexTip.py"

echo 'run over'