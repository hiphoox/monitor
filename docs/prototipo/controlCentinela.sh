#!/bin/bash

PID=""
HOME=/home/hernando/sistema/alarma

function get_pid {
   PID=`ps ax |grep centinela |grep bin| awk '{print $1}'`
}

function stop {
   get_pid
   if [ -z $PID ]; then
      echo -n "La alarma no esta corriendo."
      exit 1
   else
      echo  "Deteniendo la alarma..."
      kill $PID
      sleep 1
      echo  ".. Hecho."
   fi
}


function start {
   get_pid
   if [ -z $PID ]; then
      echo  -n "Iniciando alarma..."
      cd $HOME  
      nohup ./centinela.sh >> log & 
      get_pid
      echo  "..Hecho. PID=$PID"
   else
      echo "La alarma ya estaba nicializada y corriendo, PID=$PID"
   fi
}

function restart {
   echo  "Reiniciando alarma.."
   get_pid
   if [ -z $PID ]; then
      start
   else
      stop
      start
   fi
}

function quiet {
   get_pid
   if [ -z $PID ]; then
      echo "La alarma no esta corriendo."
      exit 1
   else
      if [ -f $HOME/activaAlarma ];
      then
        echo -n  "Callando la alarma..." 
	rm $HOME/activaAlarma 
      echo  ".. Hecho."
      else
        echo "La alarma no esta sonando.."
      fi
      sleep 1
   fi
}


function status {
   get_pid
   if [ -z  $PID ]; then
      echo "La alarma no esta corriendo."
      exit 1
   else
      echo "La alarma esta corriendo, PID=$PID"
   fi
}

case "$1" in
   start)
      start
   ;;
   stop)
      stop
   ;;
   restart)
      restart
   ;;
   status)
      status
   ;;
   quiet)
     quiet 
   ;;

   *)
      echo "Usage: sudo $0 {start|stop|restart|status|quiet}"
esac 
