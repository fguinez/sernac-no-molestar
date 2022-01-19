# sernac-no-molestar

Bloquea automáticamente las principales empresas de spam chilenas

## Instrucciones

Para utilizar esta herramienta, debes:

1. Tener [Google Chrome](https://www.google.com/chrome/) instalado.
2. Tener Python 3 instalado. Puedes comprobar si lo tienes siguiente [este tutorial](https://es.wikihow.com/revisar-la-versi%C3%B3n-de-Python-en-una-PC-o-Mac). En caso de que no lo tengas instalado, puedes descargarlo [aquí](https://www.python.org/downloads/).
3. Registrarte como consumidor en [este](https://www.sernac.cl/app/consumidor/index.php?a=registro&utm_source=CONSUMIDORES&utm_medium=BOTONWEB&utm_campaign=REGISTRO%20PORTAL%20CONSUMIDOR) formulario del Sernac. Esto te dará acceso a la herramienta anti spam No Molestar (más información [aquí](https://www.sernac.cl/portal/617/w3-propertyvalue-518.html)).
4. Clonar este repositorio en tu equipo. Si no sabes como, revisa [este tutorial](https://docs.github.com/es/repositories/creating-and-managing-repositories/cloning-a-repository).
5. Instalar las librerías de Python a utilizar con el comando:

```
pip install -r requirements.txt
```

6. Detallar las empresas a bloquear en un archivo llamado `empresas.txt` ubicado en la carpeta raíz del repositorio. El repositorio ya viene con un archivo con empresas por defecto, pero puede que quieras modificarlo añadiendo o quitando elementos.
7. Opcional: Añadir tus datos en un archivo `data.txt` que contenga:

```
RUT=[Tu RUT en formato 123456780]
CLAVE_UNICA=[Tu clave unica]
TELEFONO=[Tu número de celular en formato +56912345678]
```

Este paso tiene la única finalidad de que la ejecución sea totalmente automática. Si no agregas alguno de estos datos, de todas formas el programa te los pedirá durante la ejecución.

Este programa no recolecta información de ningún tipo. Sin embargo, para tu seguridad y tranquilidad, tienes la opción de añadir información parcial en `data.txt`. Por ejemplo, puedes añadir solo tu rut y número de teléfono (omitiendo clave única), para así luego ingresar tu clave única directamente en la página del Sernac cuando el programa te lo indique.

8. Finalmente, puedes ejecutar el programa con el comando:

```
python main.py
```
