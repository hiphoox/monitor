#!/bin/bash
PATH=$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games
HOME=/home/hernando/sistema/alarma
PID=""

function get_pid {
   PID=`ps ax |grep centinela |grep bin| awk '{print $1}'`
}

function quiet {
   (
      echo "# Silenciando alarma..."
      rm $HOME/activaAlarma
      echo "# Hecho ."; sleep 1
   ) |
   zenity --progress --pulsate
}


function stop {
   (
      echo "# Deteniendo alarma..."
      get_pid
      until [ -z $PID ]; do
         kill $PID; sleep 1
         get_pid
      done
      echo "# Alarma detenida."; sleep 1
   ) |
   zenity --progress --pulsate
}


function start {
   (
      echo "# Iniciando alarma..."
      get_pid
      cd /home/hernando/sistema/alarma	
      nohup ./centinela.sh >> log & 
      while [ -z $PID ]; do
         get_pid; sleep 1
      done
      get_pid;
      echo "# Alarma corriendo. PID = " $PID
   ) |
   zenity --progress --pulsate
}

get_pid
if [ -z  $PID ]; then
   ans=$(zenity --list \
      --text "Alarma no iniciada. Que desea hacer?" \
      --radiolist \
      --column "" --column "Accion" \
      TRUE "Iniciar alarma")

   case $ans in
      "Iniciar alarma")
         start
      ;;
      *)
   esac

else
   ans=$(zenity --list \
      --text "La alarma esta corriendo con el PID=$PID. Que desea hacer?" \
      --radiolist \
      --column "" --column "Accion" \
      TRUE "Callar alarma" \
      FALSE "Reiniciar alarma" \
      FALSE "Detener alarma")

   case $ans in
      "Callar alarma")
	quiet
      ;;
      "Reiniciar alarma")
         stop
         start
      ;;
      "Detener alarma")
         stop
      ;;
      *)
   esac

fi
exit 0 

