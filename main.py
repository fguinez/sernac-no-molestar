#from twill.commands import go, fv, submit, find, showlinks, save_html, redirect_output, reset_output
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
from time import sleep



class NoMolestar:
    def __init__(self, companies_filename='empresas.txt'):
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)
        self.config = dotenv_values("data.txt")
        self.rut = self.search_config('RUT')
        self.clave_unica = self.search_config('CLAVE_UNICA')
        self.telephone = self.search_config('TELEFONO')
        del self.config
        self.companies = self.read_companies(companies_filename)

    def search_config(self, key):
        if key in self.config.keys():
            return self.config[key].strip()
        return None

    @staticmethod
    def read_companies(companies_filename):
        companies = set()
        with open(companies_filename, 'r') as file:
            for line in file.readlines():
                line = line.strip() 
                if line and not line.startswith("#"): 
                    companies.add(line)
        return companies


    def start(self):
        print("Cargando...")
        self.login()
        self.input_telephone()
        print("Cargando...")
        self.block()
        print("Compañías bloqueadas con éxito!")
        self.driver.quit()

    def login(self):
        self.driver.get('https://www.sernac.cl/app/consumidor/claveunica.php')
        if not (self.rut and self.clave_unica):
            print("Esperando a que inicies sesión...")
        if self.rut:
            self.driver.find_element(By.NAME, 'run').send_keys(self.rut)
        if self.clave_unica:
            self.driver.find_element(By.NAME, 'password').send_keys(self.clave_unica)
        if self.rut and self.clave_unica:
            self.driver.find_element(By.ID, 'login-submit').click()
        del self.clave_unica
        # Espera hasta que logra iniciar sesión
        WebDriverWait(self.driver, 60*10).until(EC.title_contains("Portal del Consumidor"))
        print("Sesión iniciada correctamente!")

    def input_telephone(self, text="Número de teléfono (+56912345678): "):
        if not self.telephone:
            self.telephone = input(text)
        while not self.check_telephone():
            print("Número incorrecto, intenta nuevamente.")
            self.telephone = input(text)
        return self.telephone

    def check_telephone(self):
        if self.telephone[:3] != "+56":
            return False
        if len(self.telephone) != 12:
            return False
        if not self.telephone[1:].isnumeric():
            return False
        return True

    def block(self):
        mqs_button = self.driver.find_element(By.XPATH, '/html/body/div[3]/nav/ul/li[5]/a')
        mqs_url = mqs_button.get_attribute('href').strip('/')
        session_key = mqs_url.split('?p=')[-1]
        self.session_key = session_key
        no_molestar_url = f"https://www.sernac.cl/no-molestar/solicitudes?p={session_key}"
        self.driver.get(no_molestar_url)
        cards = self.driver.find_elements(By.XPATH, '/html/body/div/div[4]/div/div/div/div[1]/div[3]/div')
        for card in cards:
            if card.find_element(By.TAG_NAME, 'button').get_attribute('textContent').strip() == self.telephone:
                aria_controls = card.find_element(By.TAG_NAME, 'button').get_attribute('aria-controls')
                request_number = aria_controls.strip().split('-')[-1]
                return self._block_telephone_already_added(request_number)
        return self._block_new_telephone()


    def _block_telephone_already_added(self, request_number):
        # Redirige al formulario
        block_url = f"https://www.sernac.cl/no-molestar/solicitudes/{request_number}/agregar_empresa_telefono?p={self.session_key}"
        self.driver.get(block_url)
        # Guarda elementos recurrentes
        company_selector   = self.driver.find_element(By.ID, 'select2-empresas-container')
        add_company_button = self.driver.find_element(By.CLASS_NAME, 'agrega_canal')
        # Recorre compañías
        for company in self.companies:
            # Despliega búsqueda de compañías
            company_selector.click()
            # Ingresa compañía
            search_companies = self.driver.find_element(By.CLASS_NAME, 'select2-search__field')
            search_companies.send_keys(company)
            # Espera que carguen las opciones
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'select2-results__option--highlighted')))
            # Selecciona la primera opción
            self.driver.find_element(By.CLASS_NAME, 'select2-results__option--highlighted').click()
            # Añade la compañía seleccionada
            add_company_button.click()
            print("Añadido:", company)
        # Agrega compañías
        self.driver.find_element(By.XPATH, '/html/body/div/form/div/div/div[3]/button').click()


    def _block_new_telephone(self):
        # Redirige al formulario
        block_url = f"https://www.sernac.cl/no-molestar/solicitudes/new?p={self.session_key}"
        self.driver.get(block_url)
        # Ingresa número de teléfono
        self.driver.find_element(By.ID, 'telefono-sub')
        self.driver.find_element(By.ID, 'ingresar-bloqueo').click()
        # Guarda elementos recurrentes
        company_selector   = self.driver.find_element(By.ID, 'select2-empresas-container')
        add_company_button = self.driver.find_element(By.ID, 'ingresar-empresa')
        for company in self.companies:
            # Despliega búsqueda de compañías
            company_selector.click()
            # Ingresa compañía
            search_companies = self.driver.find_element(By.CLASS_NAME, 'select2-search__field')
            search_companies.send_keys(company)
            # Espera que carguen las opciones
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'select2-results__option--highlighted')))
            # Selecciona la primera opción
            self.driver.find_element(By.CLASS_NAME, 'select2-results__option--highlighted').click()
            # Añade la compañía seleccionada
            add_company_button.click()
            print("Añadido:", company)
        # Agrega compañías
        self.driver.find_element(By.ID, 'fake-continuar').click()
        self.driver.find_element(By.ID, 'finalizar').click()



if __name__ == "__main__":
    no_molestar = NoMolestar()
    no_molestar.start()
