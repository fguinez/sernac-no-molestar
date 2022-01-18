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


def charging_companies():
    print("Cargando compañías...", end='', flush=True)


def charging_login():
    print("Cargando login...", end='', flush=True)

def charging_block():
    print("Cargando pestaña de bloqueo...", end='', flush=True)

def OK():
    cprint("OK", 'green')


def total_companies(num, filename):
    print(
        f"Se bloquearán un total de {num} compañías,\nobtenidas desde {filename}"
    )

def waiting_auto_login():
    print("Iniciando sesión...", end='', flush=True)

def waiting_manual_login():
    cprint("Esperando a que rellenes tus datos...", 'green', attrs=['bold', 'reverse'], end='', flush=True)

def input_telephone():
    cprint(" Número de teléfono (+56912345678):", 'green', attrs=['bold', 'reverse'], end=' ', flush=True)

def incorrect_telephone():
    print("Número incorrecto, intenta nuevamente.")

def blocking():
    print("\nBloqueando compañías...\n")

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
