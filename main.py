from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import messages
import os
import sys


class NoMolestar:
    def __init__(self, companies_filename='empresas.txt'):
        messages.charging_drivers()
        self.service = Service(ChromeDriverManager(log_level=0).install())
        self.driver = webdriver.Chrome(service=self.service)
        messages.OK()
        self.config = dotenv_values("data.txt")
        self.rut = self.search_config('RUT')
        self.clave_unica = self.search_config('CLAVE_UNICA')
        self.telephone = self.search_config('TELEFONO')
        del self.config
        messages.charging_companies()
        self.companies = self.read_companies(companies_filename)
        messages.OK()
        messages.total_companies(self.n_companies, companies_filename)

    @property
    def n_companies(self):
        return len(self.companies)

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
        self.login()
        self.input_telephone()
        self.block()
        messages.success()
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

    def block(self):
        mqs_button = self.driver.find_element(
            By.XPATH, '/html/body/div[3]/nav/ul/li[5]/a')
        mqs_url = mqs_button.get_attribute('href').strip('/')
        session_key = mqs_url.split('?p=')[-1]
        self.session_key = session_key
        no_molestar_url = f"https://www.sernac.cl/no-molestar/solicitudes?p={session_key}"
        messages.charging_block()
        self.driver.get(no_molestar_url)
        cards = self.driver.find_elements(
            By.XPATH, '/html/body/div/div[4]/div/div/div/div[1]/div[3]/div')
        for card in cards:
            if card.find_element(By.TAG_NAME, 'button').get_attribute('textContent').strip() == self.telephone:
                aria_controls = card.find_element(
                    By.TAG_NAME, 'button').get_attribute('aria-controls')
                request_number = aria_controls.strip().split('-')[-1]
                return self._block_telephone_already_added(request_number)
        return self._block_new_telephone()

    def _block_telephone_already_added(self, request_number):
        # Redirige al formulario
        block_url = f"https://www.sernac.cl/no-molestar/solicitudes/{request_number}/agregar_empresa_telefono?p={self.session_key}"
        self.driver.get(block_url)
        messages.OK()
        # Guarda elementos recurrentes
        company_selector = self.driver.find_element(
            By.ID, 'select2-empresas-container')
        add_company_button = self.driver.find_element(
            By.CLASS_NAME, 'agrega_canal')
        messages.blocking()
        # Recorre compañías
        for i, company in enumerate(self.companies):
            # Despliega búsqueda de compañías
            company_selector.click()
            # Ingresa compañía
            search_companies = self.driver.find_element(
                By.CLASS_NAME, 'select2-search__field')
            search_companies.send_keys(company)
            # Espera que carguen las opciones
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'select2-results__option--highlighted')))
            # Selecciona la primera opción
            self.driver.find_element(
                By.CLASS_NAME, 'select2-results__option--highlighted').click()
            # Añade la compañía seleccionada
            add_company_button.click()
            messages.block_company(company, i+1, self.n_companies)
        # Agrega compañías
        self.driver.find_element(
            By.XPATH, '/html/body/div/form/div/div/div[3]/button').click()

    def _block_new_telephone(self):
        # Redirige al formulario
        block_url = f"https://www.sernac.cl/no-molestar/solicitudes/new?p={self.session_key}"
        self.driver.get(block_url)
        messages.OK()
        # Ingresa número de teléfono
        self.driver.find_element(
            By.ID, 'telefono-sub').send_keys(self.telephone[3:])
        self.driver.find_element(By.ID, 'ingresar-bloqueo').click()
        # Guarda elementos recurrentes
        company_selector = self.driver.find_element(
            By.ID, 'select2-empresas-container')
        add_company_button = self.driver.find_element(
            By.ID, 'ingresar-empresa')
        messages.blocking()
        # Recorre compañías
        for i, company in enumerate(self.companies):
            # Despliega búsqueda de compañías
            company_selector.click()
            # Ingresa compañía
            search_companies = self.driver.find_element(
                By.CLASS_NAME, 'select2-search__field')
            search_companies.send_keys(company)
            # Espera que carguen las opciones
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'select2-results__option--highlighted')))
            # Selecciona la primera opción
            self.driver.find_element(
                By.CLASS_NAME, 'select2-results__option--highlighted').click()
            # Añade la compañía seleccionada
            add_company_button.click()
            messages.block_company(company, i+1, self.n_companies)
        # Agrega compañías
        self.driver.find_element(By.ID, 'fake-continuar').click()
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, 'finalizar')))
        self.driver.find_element(By.ID, 'finalizar').click()




if __name__ == "__main__":
    messages.welcome()
    no_molestar = NoMolestar()
    no_molestar.start()
