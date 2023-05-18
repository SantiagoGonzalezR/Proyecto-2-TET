# Proyecto 2 TET
Proyecto 2 de aula, realizado por Pablo Maya Villegas, Mariana Vasquez Esobar y Santiago Gonzalez Rodriguez

## Descripcion del proyecto
Auto scaling de AWS creado a mano usando Python Boto3, con un sistema de monitoreo implementado en NodeJS con gRPC

## Prerrequisitos para correr el codigo
Instalar las siguientes librerias en la maquina que va a correr los monitores S y ASG:

Python3
Boto3 para python
Node
gRPC para NodeJS
dotenv para NodeJS

Instalar las siguientes para el monitor C

Python3
gRPC para python

## Desarrollo
La creacion de este proyecto nos tomo mucho tiempo, tuvimos problemas a la hora de realizarlo porque uno de los 2 fines de semana no teniamos ningun dia libre para trabajarle.

El mayor reto fue la implementacion correcta del SDK de AWS para poder crear y borrar las instancias usando las IPs en vez de las IDs de cada instancia, manejamos JSONs para el registro de maquinas con su contador para borrado el borrado de estas y un sistema de impresion de consola que nos indica cuantas maquinas estan conectadas brindando informacion junto a la informacion que es mandada.

## Video de demostracion.
Este video es por si no ejecuta el codigo a la hora de la exposicion, funciona con el mismo codigo que esta montado en el github.
https://youtu.be/XU4SAxQitBo

## Referencias
https://docs.aws.amazon.com/code-library/latest/ug/python_3_ec2_code_examples.html
