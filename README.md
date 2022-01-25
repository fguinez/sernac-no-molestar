# AutoNoMolestar

Bloquea automáticamente las principales empresas de spam chilenas

## Instrucciones

Para utilizar esta herramienta, debes:

1. Tener [Google Chrome](https://www.google.com/chrome/) instalado.
2. Tener Python 3 instalado. Puedes comprobar si lo tienes siguiendo [este tutorial](https://es.wikihow.com/revisar-la-versi%C3%B3n-de-Python-en-una-PC-o-Mac). En caso de que no lo tengas instalado, puedes descargarlo [aquí](https://www.python.org/downloads/).
3. Registrarte como consumidor en [este](https://www.sernac.cl/app/consumidor/index.php?a=registro&utm_source=CONSUMIDORES&utm_medium=BOTONWEB&utm_campaign=REGISTRO%20PORTAL%20CONSUMIDOR) formulario del Sernac. Esto te dará acceso a la herramienta anti spam No Molestar (más información [aquí](https://www.sernac.cl/portal/617/w3-propertyvalue-518.html)).
4. Clonar este repositorio en tu equipo. Si no sabes como, revisa [este tutorial](https://docs.github.com/es/repositories/creating-and-managing-repositories/cloning-a-repository).
5. Instalar las librerías de Python a utilizar con el comando:

```
pip install -r requirements.txt
```

6. Detallar las empresas a bloquear en un archivo llamado `empresas.txt` o `empresas-[LoQueSea].txt` ubicado en la carpeta raíz del repositorio. El repositorio ya viene con un archivo con empresas por defecto, pero puede que quieras modificarlo añadiendo o quitando elementos. Puedes encontrar más sobre el funcionamiento de este archivo en [esta página](https://github.com/fguinez/sernac-no-molestar/wiki/empresas.txt) de la wiki.

7. _Opcional:_ Para automatizar completamente el proceso, puedes añadir tus datos como rut, clave única o teléfono en un archivo `data.txt`. Puedes encontrar más sobre el funcionamiento y estructura de este archivo en [esta página](https://github.com/fguinez/sernac-no-molestar/wiki/data.txt) de la wiki.

8. Finalmente, puedes ejecutar el programa con el comando:

   ```
   python main.py
   ```
