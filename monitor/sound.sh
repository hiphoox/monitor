#!/bin/bash

contador=0
while [ $contador -lt 360000 ] 
do
  afplay ./monitor/media/monitor/sound/alarm.wav
  let contador+=1
done
