#!/bin/bash
#usar: cambiaPermisos  nombre bandera(0|1) 
#./cambiaPermisos.sh  0 Sigma 

echo "Content-type: text/html; charset=iso-8859-1"
echo

eval `./proccgi.sh $*`
nuevaBandera=$FORM_bandera
nombre=$FORM_nombre

#obtiene el campo que se va a cambiar
campo=`grep $nombre permisos` 

#obtiene el valor actual de la bandera de activacion de la alarma
bandera=`echo $campo | cut -d " " -f1`
nuevaBandera=$FORM_bandera
echo  Usuario: $nombre 

#Verifica si se quiere consultar o cambiar un estado
if [ ! -n "$nuevaBandera" ]
then   #consulta estado actual
        #echo "valor actual"
	echo	"<br>"
        echo    -e "<FORM action=\"http://corleone.iimas.unam.mx/cgi-bin/cambiaPermisos$nombre?nombre=$nombre\" method=\"post\">"
        echo    "    <P>"
        echo    -e "    <input type=\"hidden\" name=\"nombre\" value=\"$nombre\">"
	if [ $bandera -eq 1 ] 
	then	
        	echo    -e "    <INPUT type=\"radio\" name=\"bandera\" value=\"1\"checked > Activo<BR>"
        	echo    -e "    <INPUT type=\"radio\" name=\"bandera\" value=\"0\" > Inactiva<BR>"
	else
		echo    -e "    <INPUT type=\"radio\" name=\"bandera\" value=\"1\"> Activo<BR>"
		echo    -e "    <INPUT type=\"radio\" name=\"bandera\" value=\"0\" checked> Inactiva<BR>"
        fi
	echo    "<br>"
        echo    -e "    <INPUT type=\"submit\" value=\"OK\"> <INPUT type=\"reset\" value=\"Limpiar\">"
        echo    "    </P>"
        echo    " </FORM>"

else	#cambia el estado actual si la bandera es diferente 
	if [ $bandera -eq $nuevaBandera ]
	then
		echo "El estado actual es igual al que se desea cambiar." 
		echo "No se realizan cambios."
	else
		awk ' BEGIN {FS = "\t"}; {if($2==nombre) print nuevaBandera "\t" $2 "\t" $3; else print  $1 "\t" $2 "\t" $3; }' nuevaBandera=$nuevaBandera nombre=$nombre permisos > /tmp/permisos.tmp
		cp /tmp/permisos.tmp permisos
 		#cat permisos
		echo "Actualizado."
	fi
fi
