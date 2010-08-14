#!/bin/bash
PATH=$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games

#mailx -s "ALARMA DE ROBO" hernando@sigma.iimas.unam.mx < /home/hernando/sistema/alarma/resultadoAlarma 
contador=0
while [ $contador -lt 111360 ] 
do
	if [  -f activaAlarma ]
	then
        	playsound alarm.wav

		awk  -F"\t" '{ if(!($1==$2||!$3))  {system("espeak -vesp-mx \"" $5 "\"");  }  }' resultadoGeneral

		#espeak -vesp-mx "atención, posible robo, edificio antigüo iimas, primer piso, oficina 119"
        	echo alarma: $contador
	else
		exit
	fi
let contador+=1
done
rm activaAlarma
