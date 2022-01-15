from twill.commands import go, fv, submit, find, showlinks, save_html, redirect_output, reset_output
from getpass import getpass


class NoMolestar:
    def start(self):
        print("Cargando...")
        self.login()
        self.input_telephone()
        self.block()
        
    @staticmethod
    def login():
        redirect_output('output.log')
        go('https://www.sernac.cl/app/consumidor/claveunica.php')
        reset_output()
        rut = input("Rut: ")
        fv('1', 'run', rut)
        del rut
        password = getpass("Clave única: ")
        fv('1', 'password', password)
        del password
        redirect_output('output.log')
        submit('4')
        reset_output()
        #TODO: Confirmar que se inició sesión correctamente
        print("Sesión iniciada correctamente!")

    def input_telephone(self, text="Número de teléfono (+56912345678): "):
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
        redirect_output('output.log')
        go('https://www.sernac.cl/app/consumidor/index.php?c=home&a=nomolestar')
        save_html('prueba1.html')
        mqs_link = next(link for link in showlinks() if link.text.strip() == "Me Quiero Salir").url.strip('/')
        session_key = mqs_link.split('?p=')[-1]
        no_molestar_link = f"https://www.sernac.cl/no-molestar/solicitudes?p={session_key}"
        reset_output()
        print(no_molestar_link)
        #BUG: Si se abre 'no_molestar_link' desde el navegador todo se despliega bien, sin embargo la línea a
        # continuación retorna un HTML en blanco. Una posible solición es cambiar twill por selenium.
        a = go(no_molestar_link)
        print(a)
        save_html('prueba2.html')
        
        print(find(self.telephone[1:]))
        #TODO: Si el celular está, utilizar el formulario de bloqueo del número.
        # Si no está, ingresar al formulario de nuevo número.


if __name__ == "__main__":
    no_molestar = NoMolestar()
    no_molestar.start()
