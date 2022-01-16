#from twill.commands import go, fv, submit, find, showlinks, save_html, redirect_output, reset_output
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values



class NoMolestar:
    def __init__(self):
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service )
        self.config = dotenv_values("data.txt")
        self.rut = self.search_config('RUT')
        self.clave_unica = self.search_config('CLAVE_UNICA')
        self.telephone = self.search_config('TELEFONO')
        del self.config

    def search_config(self, key):
        if key in self.config.keys():
            return self.config[key].strip()
        return None


    def start(self):
        print("Cargando...")
        self.login()
        #self.input_telephone()
        #print("Cargando...")
        #self.block()
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
        mqs_link = mqs_button.get_attribute('href').strip('/')
        session_key = mqs_link.split('?p=')[-1]
        no_molestar_link = f"https://www.sernac.cl/no-molestar/solicitudes?p={session_key}"
        self.driver.get(no_molestar_link)
        cards = self.driver.find_elements(By.XPATH, '/html/body/div/div[4]/div/div/div/div[1]/div[3]/div')
        print(len(cards), cards)
        print()
        for card in cards:
            print('text:', card.find_element(By.TAG_NAME, 'button').text, '*')
            if card.find_element(By.TAG_NAME, 'button').text.strip() == self.telephone:
                return self._block_telephone_already_added(card)
        return self._block_new_telephone()

    def _block_telephone_already_added(self, card):
        input()

    def _block_new_telephone(self):
        input()



if __name__ == "__main__":
    no_molestar = NoMolestar()
    no_molestar.start()
