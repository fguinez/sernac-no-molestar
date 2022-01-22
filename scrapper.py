from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import messages
import os


class NoMolestar:
    def __init__(self, results_filename='resultados.txt', searches_filename='busquedas.txt',
                 companies_filename='empresas-search.txt', data_filename='data.txt', folder='scrap'):
        messages.charging_drivers()
        self.service = Service(ChromeDriverManager(log_level=0).install())
        self.driver = webdriver.Chrome(service=self.service)
        messages.OK()
        self.config = dotenv_values(data_filename)
        self.rut = self.search_config('RUT')
        self.clave_unica = self.search_config('CLAVE_UNICA')
        del self.config
        os.makedirs(folder, exist_ok=True)
        self.results_filename = f"{folder}/{results_filename}"
        self.searches_filename = f"{folder}/{searches_filename}"
        self.companies_filename = f"{folder}/{companies_filename}"
        messages.files_report(self.results_filename,
                              self.searches_filename, self.companies_filename)
        self.companies = self.read_companies()
        self.searches = self.read_searches()
        #######################################################################
        # Este diccionario podría ser de ayuda para iterar entre posibles
        # combinaciones. Su uso es opcional y puedes modificarlo a gusto.
        self.chars = {
            'nums': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            'vcls': ['a', 'e', 'i', 'o', 'u'],
            'cons': ['q', 'w', 'r', 't', 'y', 'p', 's', 'd', 'f',
                     'g', 'h', 'j', 'k', 'l', 'ñ', 'z', 'x', 'c', 'v', 'b', 'n', 'm'],
            'con1': ['b', 'c', 'd', 'f', 'g', 'j', 'k', 'p', 't', 'w', 'z'],
            'con2': ['h', 'l', 'r']
        }
        #######################################################################
        messages.previous_activity_report(self.n_companies, len(self.searches))
        self.analyze_search_WasCalled = False

    @property
    def n_companies(self):
        return len(self.companies)

    def search_config(self, key):
        if key in self.config.keys():
            return self.config[key].strip()
        return None

    def read_companies(self):
        # Crear el archivo self.companies_filename en caso de que no exista
        open(self.companies_filename, 'a').close()
        # Lee las compañías previas
        with open(self.companies_filename, 'r') as file:
            companies = set(line.strip() for line in file.readlines())
        return companies

    def read_searches(self):
        # Crear el archivo self.searches_filename en caso de que no exista
        open(self.searches_filename, 'a').close()
        # Lee las búsquedas previas
        with open(self.searches_filename, 'r') as file:
            searchs = set(line[:3] for line in file.readlines())
        return searchs

    def write_results(self, companies, search):
        with open(self.results_filename, 'a') as file:
            file.write(f"# {search}\n")
            for company in companies:
                file.write(company + '\n')
            file.write('\n')

    def write_companies(self):
        with open(self.companies_filename, 'w') as file:
            for company in self.companies:
                file.write(company + '\n')

    def start(self):
        self.login()
        self.find_session_key()
        self.scrap()
        self.driver.quit()
        messages.end()

    def login(self):
        messages.charging_login()
        self.driver.get('https://www.sernac.cl/app/consumidor/claveunica.php')
        messages.OK()
        if not (self.rut and self.clave_unica):
            messages.waiting_manual_login()
        if self.rut:
            self.driver.find_element(By.NAME, 'run').send_keys(self.rut)
        if self.clave_unica:
            self.driver.find_element(
                By.NAME, 'password').send_keys(self.clave_unica)
        if self.rut and self.clave_unica:
            messages.waiting_auto_login()
            self.driver.find_element(By.ID, 'login-submit').click()
        del self.clave_unica
        # Espera hasta que logra iniciar sesión
        WebDriverWait(self.driver, 60 *
                      10).until(EC.title_contains("Portal del Consumidor"))
        messages.OK()

    def input_telephone(self):
        if not self.telephone:
            messages.input_telephone()
            self.telephone = input()
        while not self.check_telephone():
            messages.incorrect_telephone()
            messages.input_telephone()
            self.telephone = input()
        return self.telephone

    def check_telephone(self):
        if self.telephone[:3] != "+56":
            return False
        if len(self.telephone) != 12:
            return False
        if not self.telephone[1:].isnumeric():
            return False
        return True

    def find_session_key(self):
        mqs_button = self.driver.find_element(
            By.XPATH, '/html/body/div[3]/nav/ul/li[5]/a')
        mqs_url = mqs_button.get_attribute('href').strip('/')
        session_key = mqs_url.split('?p=')[-1]
        self.session_key = session_key

    def scrap(self):
        # Redirige al formulario
        block_url = f"https://www.sernac.cl/no-molestar/solicitudes/new?p={self.session_key}"
        self.driver.get(block_url)
        messages.OK()
        # Despliega búsqueda de compañías
        company_selector = self.driver.find_element(
            By.ID, 'select2-empresas-container')
        company_selector.click()
        messages.blocking()
        # Guarda campo de ingreso de texto
        self.search_companies = self.driver.find_element(
            By.CLASS_NAME, 'select2-search__field')
        # Recorre compañías
        #######################################################################
        # Ejemplo 1: [consonante][vocal][consonante]
        #            Este ejemplo analiza todas las búsquedas compuestas por
        #            una consonante, seguida de una vocal, seguida de una
        #            consonante.
        #
        # for c1 in self.chars['cons']:
        #    for c2 in self.chars['vcls']:
        #        for c3 in self.chars['cons']:
        #            search = f"{c1}{c2}{c3}"
        #            self.analyze_search(search)
        #######################################################################
        # Ejemplo 2: Búsquedas mixtas
        #            Este ejemplo realiza una serie de búsquedas mixtas sin
        #            relación entre sí por medio de diversos llamados al método
        #            analyze_search.
        #
        #self.analyze_search(" - ")
        # self.analyze_search("universidad")
        # self.analyze_search("hos")
        #######################################################################
        #######################################################################
        # < INICIO DEL ESPACIO DE EDICICIÓN>
        #
        # Edita libremente este espacio con llamados al método analyze_search
        # Puedes guiarte por los ejemplos de más arriba si así lo deseas.
        #
        # < TÉRMINO DEL ESPACIO DE EDICICIÓN>
        #######################################################################
        #######################################################################
        if not self.analyze_search_WasCalled:
            messages.warning_dont_call_analyze_search()
        self.write_companies()
        messages.saved_companies(self.n_companies)

    def analyze_search(self, search):
        '''
        Recibe un string y analiza
        '''
        self.analyze_search_WasCalled = True
        # Comprueba si la sección no ha sido analizada
        if search in self.searches:
            return
        # Limpia el campo de ingreso
        self.search_companies.clear()
        # Ingresa compañía
        self.search_companies.send_keys(search)
        # Espera que carguen las opciones
        try:
            WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located(
                (By.CLASS_NAME, 'loading-data')))
        except TimeoutException:
            print("ERROR: Ha pasado mucho tiempo cargando resultados.")
            print("       Detenido en la sección:", search)
            self.write_companies()
            print(f"companies: {self.n_companies}")
            self.driver.quit()
            exit()
        # Selecciona las opciones
        companies_search = self.driver.find_elements(
            By.CLASS_NAME, 'select2-results__option')
        if len(companies_search) == 1:
            if companies_search[0].text == 'Sin resultados':
                return
        companies = set(company.text for company in companies_search)
        search_log = f"{search}: {len(companies)}"
        print(search_log)
        with open(self.searches_filename, 'a') as file:
            file.write(search_log + '\n')
        self.companies = self.companies.union(companies)
        self.write_results(companies, search)


if __name__ == "__main__":
    messages.welcome()
    messages.welcome_scrapper()
    no_molestar = NoMolestar()
    no_molestar.start()
