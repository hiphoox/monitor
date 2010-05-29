#!/bin/bash
PATH=$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games

#uso: sudo ./centinela.sh
	
###inicializacion, no borra estadoAlarma pues este ultimo es un indicador
rm estadoActual estadoAnterior resultadoGeneral estadoAlerta activaAlarma

#inicializa archivos de mapa, si apuntan a los adecuados no pasa nada
cp ./mapa/estructuraZona.html ./mapa/zona.html
cp ./mapa/estructuraLlave.html  ./mapa/llave.html
#inicializa la alarma de los clientes 
cp ./mapa/estructuraAlarmaOFF.html ./mapa/alarma.html

### este contador verifica cuantas veces continuas ha sido detectado un estado de alerta
contadorEstado=0;
contadorAlarma=0;
volumenOriginal=0;
volumenAlarma=64; #de 0 a 64

### conteo maximo de veces continuas de estados de alerta para activar la alarma  
conteoActivacion=12;



###cuerpo principal
while true 
do

	###obtiene informacion actualizada del switch
	#wget  --http-user=admin --http-passwd=rcrd09   -O switch.html  -o  ./log.html http://192.168.66.3/dev01/mimic/mimic.rhtm

	###la filtra y adecua
	#grep -o -e "tpc" -e "tpe"  -e "bpc" -e "bpe" switch.html | sed -e s/tpc/1/ -e s/tpe/0/ -e s/bpc/1/ -e s/bpe/0/  > estadoActual 
	snmpwalk -v 2c -c iimas 132.248.51.194 IF-MIB::ifOperStatus | head -24 | grep -o -e "up" -e "down" | sed -e s/up/1/ -e s/down/0/ > estadoActual
	
	###si no existe este archivo es que se esta inicializando apenas
	if [ -f estadoAnterior ]; 
	then 		 
		###si el estado anterior no es igual al actual activa estadoAlerta
        	paste estadoActual estadoAnterior permisos > resultadoGeneral; 
        	######awk  -F"\t" '{ if(!($1==$2||!$3))  system("touch estadoAlerta")  }' resultadoGeneral
	 	#si estado anterio><actual y esta habilitado, lanza alerta(12), si no solo pasa el estado que tiene, 
		#si el resultado es mayor que 10 esta habilitado , 10 desenchufado, 11 enchufado 
		#si el resultado es menor de 10 esta deshabilitado, 0 desenchufado, 1 enchufado 
		#En el Javascript de la pagina debera asignarse manualmente a cada renglon un frame, 
		#y asi cambiar su color dependiendo del estado	
		awk  -F"\t" '{ if(!($1==$2||!$3))  {system("touch estadoAlerta"); print "c"$3""2;} else print "c"$3$1  }' resultadoGeneral > resultadoWeb
	
	        date
	else 
        	echo "Inicializando..." 	
	fi

	#######determina alarma
	###si hay estadoAlerta aumenta el contador		
	if [ -f estadoAlerta ];
	then 
		let contadorEstado+=1
		rm estadoAlerta 
		echo `date` Estado alerta $contadorEstado
		# reportar las alertas como archivos
 		cp resultadoGeneral ./alarmas/`date | tr " " "_"`_alerta_`echo $contadorEstado`

        	###si han pasado 3 estados de alerta continuos lanza alarma
        	if [  $contadorEstado -eq $conteoActivacion ]
        	then
                	contadorEstado=0
			alarmaActual=contadorAlarma	
                	cp estadoActual estadoAnterior #si no se hiciera esto seguiria sonando hasta reconectar la maquina
                	cp resultadoGeneral ./alarmas/`date | tr " " "_"`_alarma_`echo $contadorAlarma`
			alarmaActual=contadorAlarma
			let contadorAlarma+=1
			#12 es alerta, 13 es alarma  	
			tr "12" "13" < resultadoWeb > resultadoWeb1
			mv resultadoWeb1 resultadoWeb
			#actualiza paginas de mapas
			sed s/llave./llaveC6./ ./mapa/llave.html > ./mapa/llave.html.temporal
			cp  ./mapa/llave.html.temporal  ./mapa/llave.html
			sed s/C6.gif/C6Rec.jpg/ ./mapa/zona.html  > ./mapa/zona.html.temporal
			cp ./mapa/zona.html.temporal ./mapa/zona.html
			cp ./mapa/estructuraAlarmaON.html ./mapa/alarma.html
			touch activaAlarma
			chmod 777 activaAlarma		
	        fi

	###si no es que ya no fueron continuos, contadorEstado a cero y se resetean los estados del switch 
	else
		contadorEstado=0
		cp estadoActual estadoAnterior
	fi	

        #######visualiza resultados
        ####genera pagina, el archivo codigosColores contiene el color de fondo que se pondra de acuerdo al codigo en resultadoWeb
	#aqui hay que tener cuidado que no se generen los codigos usados cnn  en el archivo codigosColores o en estructuraPasillo.html 	
        for i in `cat resultadoWeb`
        do
                #echo $i
                color=`cat codigosColores | cut -f1,2 |grep $i | cut  -f2`
                echo $color
        done  > coloresConector
        #coloresConector contiene los colores  de fondo para cada conector en ese orden

        awk '{print "color"$2}' permisos > usuarioConector
        #usuarioConector  contiene los usuarios en el orden que corresponde por cada conector

        paste coloresConector usuarioConector > coloresUsuario
        #coloresUsuario contiene los usuarios y sus colores de estado

        #para cada usuario en coloresUsuario sustituira su codigo de color en la pagina pasillo.html para su visualizacion
        cp estructuraPasillo.html pasillo.html.temporal

        awk '{system("sed s/" $2"/" $1"/ pasillo.html.temporal > pasillo.html.temporal1" ); system("mv  pasillo.html.temporal1 pasillo.html.temporal"); }' coloresUsuario

	#aniade un timestamp con el momento de la ultima actualizacion del archivo web
	#sed s/"horaFecha"/"`date`"/ pasillo.html.temporal  > pasillo.html.temporal1
	timeStamp=`ls -l --full-time /var/www/pasillo.html | cut -d" " -f6-7|cut -d"." -f1`
	sed s/"horaFecha"/"`echo $timeStamp`"/ pasillo.html.temporal  > pasillo.html.temporal1

        cp pasillo.html.temporal1 pasillo.html

	########finalmente si se activa el alarma debe sonar el altavoz
              if [  -f activaAlarma ]
              then
              	volumenOriginal=amixer get Master |grep Mono:| cut -d" " -f5
              	#aumenta el volumen
              	amixer set Master front $volumenAlarma

		./alarma.sh 

	      	#restaura el volumen
              	amixer set Master front volumenOriginal
		#reinicializa archivos de mapa, si apuntan a los adecuados no pasa nada
		cp ./mapa/estructuraZona.html ./mapa/zona.html
		cp ./mapa/estructuraLlave.html  ./mapa/llave.html
		#termina alarma en clientes
		cp ./mapa/estructuraAlarmaOFF.html ./mapa/alarma.html
              fi
######## espera n segundos entre consultas
sleep 3	
done
