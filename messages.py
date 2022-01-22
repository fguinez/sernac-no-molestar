from audioop import reverse
from attr import attr
from termcolor import cprint


# main.py


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
    
    

# scrapper.py

def welcome_scrapper():
    cprint("Asistente de scrapping".center(50), attrs=['reverse'])
    print("""
    Estás ejecutando el módulo de scrapping de   
    ANM, el cual está diseñado para ayudarte a   
    formar tus propias listas de empresas para   
    bloquear.

    Si lo que deseas es bloquear una lista ya    
    preparada de empresas, cierra este módulo    
    precionando Ctrl+C y ejecuta:
                 python main.py                 

    Para utilizar correctamente este módulo,
    es necesario editar previamente el código
    de 'scrapper.py' en el espacio comentado
    dentro del método 'scrap'.
""")
    cprint(" ".center(50), attrs=['reverse'])
    print()

def files_report(results_filename, searches_filename, companies_filename):
    cprint("\nReporte de archivos:", attrs=['bold'])
    print("- Se omitirán las búsquedas previas presentes en:")
    cprint(f"    {searches_filename}", 'blue')
    print("- Las búsquedas realizadas se añadirán al final de:")
    cprint(f"    {searches_filename}", 'blue')
    print("- Los resultados se añadirán al final de:")
    cprint(f"    {results_filename}", 'blue')
    print("- La lista de empresas considerará las presentes\n  previamente en:")
    cprint(f"    {companies_filename}", 'blue')
    print("- Al final de la ejecución, se escribirá toda la\n  lista de empresas encontradas en:")
    cprint(f"    {companies_filename}", 'blue')

def previous_activity_report(n_companies, n_searches):
    cprint("\nReporte de actividad previa:", attrs=['bold'])
    print(f"- Compañías previas: {n_companies}")
    print(f"- Búsquedas previas: {n_searches}")
    print()

def looking():
    print("\nBuscando compañías...\n")
    cprint("No interactue con el navegador para evitar errores", attrs=['reverse'])
    print()

def warning_dont_call_analyze_search():
    cprint("\nADVERTENCIA:", 'yellow', attrs=['bold', 'reverse'], end=' ')
    cprint(f"Para utilizar correctamente este", 'yellow', attrs=['bold'])
    cprint(
        """             módulo, es necesario editar de forma
             previa el código de 'scrapper.py' en
             el espacio comentado dentro del método
             'scrap'.
            
             Esta advertencia aparece cuando no
             realizas ningún llamado al método
             analyze_search.
        """,
        'yellow',
        attrs=['bold']
    )

def error_TimeoutException_charging_results(search):
    cprint("\nERROR:", 'red', attrs=['bold', 'reverse'], end=' ')
    cprint("Ha pasado mucho tiempo cargando resultados.", 'red', attrs=['bold'])
    cprint(f"       Detenido en la búsqueda: {search}", 'red', attrs=['bold'])

def report_end(n_companies, n_new_companies, n_new_searches):
    cprint("\nReporte final:", attrs=['bold'])
    print(f"- Compañias guardadas: {n_companies} ({n_new_companies} nuevas)")
    print(f"- Nuevas búsquedas: {n_new_searches}")