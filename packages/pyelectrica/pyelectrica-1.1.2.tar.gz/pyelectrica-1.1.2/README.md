> Se omiten signos ortograficos intensionalmente para evitar problemas de visualizacion en la pagina del modulo en PyPI.

# PyElectrica
MODULO PyElectrica, UTIL PARA RESOLVER PROBLEMAS ESPECIFICOS DE LA INGENIERIA ELECTRICA RELATIVOS A LOS CIRCUITOS Y MAQUINAS ELECTRICAS

## INSTALACION
```bash
> pip install pyelectrica
```
## ACTUALIZACION
```bash
> pip install -U pyelectrica
```
## MANUAL DE USO
Desde el interprete de Python se importa la funcion a utilizar segun el tipo de problemas que se quiera resolver.
```bash
>>> from pyelectrica import "nombre de la funcion"
```
### Ejemplo
Calcular el valor de la corriente utilizando la ley de Ohm, y considerando que se tiene un voltaje de 12V (V=12)
y una resistencia de 2 Ohms (R=2).
```bash
>>> from pyelectrica import leyOhm
```
```bash
>>> leyOhm(V=12, I='?', R=2)
```
```bash
I = 6.0 A
```
```bash
>>>
```
## FUNCIONES INCLUIDAS EN LA VERSION 1.1.2 EL MODULO PyElectrica

### Para analisis de Circuitos Electricos

* leyOhm

* bode

* bodeNb

* escalon

* vNodos

* vNodosV

* iLazos

* iLazosV

* c_1orden

### Para el analisis de Maquinas electricas

* mLineal_CD

* compCA_GenSinc

* par_vel

## GENERAR INFORMACION DE AYUDA DE LA FUNCION IMPORTADA
Basta con llamar en el interprete de Python la funcion "help()" y la función importada del modulo PyElectrica,
utilizando la siguiente sintaxis: help("nombre de la funcion").

Ejemplo:
```bash
>>> help(leyOhm)
```

