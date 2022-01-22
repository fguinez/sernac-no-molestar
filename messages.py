from audioop import reverse
from attr import attr
from termcolor import cprint


def welcome():
    print(
        """
——————————————————————————————————————————————————
——————————————————————————————————————————————————
——————————————————————————————————————————————————
           ___          ___          ___          
          /  /\        /__/\        /__/\         
         /  /::\       \  \:\      |  |::\        
        /  /:/\:\       \  \:\     |  |:|:\       
       /  /:/~/::\  _____\__\:\  __|__|:|\:\      
      /__/:/ /:/\:\/__/::::::::\/__/::::| \:\\     
      \  \:\/:/__\/\  \:\~~\~~\/\  \:\~~\__\/     
       \  \::/      \  \:\  ~~~  \  \:\           
        \  \:\       \  \:\       \  \:\          
         \  \:\       \  \:\       \  \:\         
          \__\/        \__\/        \__\/         
                                                  
——————————————————————————————————————————————————
———————————————— Auto No Molestar ————————————————
——————————————————————————————————————————————————

    Herramienta anti-spam que bloquea de forma    
    automática las llamadas spam de empresas
    chilenas.

    ANM no tiene ninguna relación con el
    Servicio Nacional del Consumidor, 
    utilizando información pública obtenida
    por medio de la herramienta NoMolestar
    proporcionada por Sernac.

    AMN es una iniciativa de código abierto,
    puedes aportar en:
    www.github.com/fguinez/sernac-no-molestar

——————————————————————————————————————————————————
——————————————————————————————————————————————————
——————————————————————————————————————————————————
""")


def charging_drivers():
    print("Buscando drivers...", end='', flush=True)


def charging_companies(filename):
    print(f"Cargando compañías desde '{filename}'...", end='', flush=True)


def charging_login():
    print("Cargando login...", end='', flush=True)

def charging_block():
    print("Cargando pestaña de bloqueo...", end='', flush=True)

def OK():
    cprint("OK", 'green')


def total_companies(num):
    print(
        f"Se bloquearán un total de {num} compañías"
    )

def waiting_auto_login():
    print("Iniciando sesión...", end='', flush=True)

def waiting_manual_login():
    cprint("Esperando a que rellene sus datos...", 'green', attrs=['bold', 'reverse'], end=' ', flush=True)

def input_telephone():
    cprint("Ingrese su número de teléfono (+56912345678):".center(50), 'green', attrs=['bold', 'reverse'])
    cprint(" > ", 'green', attrs=['bold', 'reverse'], end=' ', flush=True)

def incorrect_telephone():
    print("Número incorrecto, intente nuevamente.".rjust(50))

def blocking():
    print("\nBloqueando compañías...\n")
    cprint("No interactue con el navegador para evitar errores", attrs=['reverse'])
    print()

def block_company(company, i, total):
    cprint(f"{i}. Bloqueado: ", attrs=['bold'], end='')
    print(company.ljust(11))
    cprint(f"({i}/{total})", end='\r', attrs=['reverse'])

def success():
    print('\n')
    cprint("¡Compañías bloqueadas con éxito!".center(50), 'green', attrs=['bold'])

def end():
    print("""
——————————————————————————————————————————————————
——————————————————————————————————————————————————
——————————————————————————————————————————————————
""")

def error_companies_not_found(companies_filename):
    cprint("\nERROR:", 'red', attrs=['bold', 'reverse'], end=' ')
    cprint(f"Archivo '{companies_filename}' no encontrado.", 'red', attrs=['bold'])
    cprint(f"{' '*6} Debes añadir un archivo '{companies_filename}' en el directorio", 'red', attrs=['bold'])
    cprint(f"{' '*6} para continuar. Si no sabes cómo, revisa:", 'red', attrs=['bold'])
    cprint(f"{' '*6} github.com/fguinez/sernac-no-molestar/wiki/empresas.txt\n", 'red', attrs=['underline'])
    
    