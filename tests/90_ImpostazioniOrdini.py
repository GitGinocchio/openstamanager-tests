from common.Test import Test, get_html
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Impostazioni(Test):
    def setUp(self):
        super().setUp()

    def test_impostazioni_ordini(self):
        pass
        # Cambia automaticamente stato ordini fatturati (1)
        #self.cambia_stato_ordini()

        # Conferma automaticamente le quantità negli ordini cliente (2)
        #self.conferma_quantita_ordini_cliente()

        # Conferma automaticamente le quantità negli ordini fornitore (3)
        #self.conferma_quantita_ordini_fornitore()

        ## TODO: Visualizza numero ordine cliente

    def cambia_stato_ordini(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-15"]', By.XPATH).click() #apro Ordini
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[1]', By.XPATH).click() #disattivo impostazione
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Ordini cliente")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su tasto +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica-container"]', By.XPATH).click()     #scelta di "Cliente" come anagrafica per l'ordine
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('Cliente')
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()   #click su tasto aggiungi
        self.wait_loader()

        self.get_element('//div[@id="tab_0"]//a[@class="btn btn-primary"]', By.XPATH).click()  #click su tasto aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys('Test') #aggiunta descrizione riga
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys('1')   #aggiunta prezzo unitario
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()    #click su aggiungi
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@id="select2-idstatoordine-container"]'))).click()   #cambio stato in Accettato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('Accettato', Keys.ENTER)
        self.get_element('//button[@id="save"]', By.XPATH).click() #click su salva
        self.wait_loader()

        self.navigateTo("Ordini cliente")   #torna in pagina principale
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Numero"]/input'))).send_keys('02', Keys.ENTER) #cerco l'ordine 02     
        sleep(1)

        self.get_element('//tbody//tr//td', By.XPATH).click()  #seleziono l'ordine
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() #click su azioni di gruppo
        self.get_element('//a[@data-op="crea_fattura"]', By.XPATH).click() #click su fattura ordini clienti
        sleep(1)

        self.get_element('//span[@id="select2-raggruppamento-container"]', By.XPATH).click() #ragruppa per cliente
        sleep(1)

        self.get_element('//ul[@id="select2-raggruppamento-results"]//li[1]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()
        self.wait_loader()

        stato=self.get_element('(//tr[1]//td[7]//span, By.XPATH)[2]').text
        self.assertEqual(stato, "Accettato")    #check se lo stato non è cambiato
        self.get_element('//tbody//tr//td[2]', By.XPATH).click()   #elimino ordine
        self.wait_loader()

        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//th[@id="th_Numero"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click() #cancello la ricerca
        sleep(1)

        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click() #elimino fattura
        self.wait_loader()

        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click() #click di conferma
        self.wait_loader()
        #torno alle impostazioni di prima
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-15"]', By.XPATH).click() #apro Ordini
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[1]', By.XPATH).click() #attivo impostazione
        sleep(1)

    def conferma_quantita_ordini_cliente(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Vendite")
        self.navigateTo("Ordini cliente")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su tasto +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica-container"]', By.XPATH).click()     #scelta di "Cliente" come anagrafica per l'ordine
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('Cliente')
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()   #click su tasto aggiungi
        self.wait_loader()

        self.get_element('//div[@id="tab_0"]//a[@class="btn btn-primary"]', By.XPATH).click()  #click su tasto aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys('Test') #aggiunta descrizione riga
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys('1')   #aggiunta prezzo unitario
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()    #click su aggiungi
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '(//i[@class="fa fa-check text-success"])[1]'))) #check se la quantita è stata confermata automaticamente
        #elimino ordine
        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-15"]', By.XPATH).click() #apro Ordini
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[2]', By.XPATH).click() #disattivo impostazione
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Ordini cliente")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su tasto +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica-container"]', By.XPATH).click()     #scelta di "Cliente" come anagrafica per l'ordine
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('Cliente')
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()   #click su tasto aggiungi
        self.wait_loader()

        self.get_element('//div[@id="tab_0"]//a[@class="btn btn-primary"]', By.XPATH).click()  #click su tasto aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys('Test') #aggiunta descrizione riga
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys('1')   #aggiunta prezzo unitario
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()    #click su aggiungi
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//i[@class="fa fa-clock-o text-warning"]')))    #check se è stato confermata la quantita
        #elimino ordine
        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()
        #torno alle impostazioni di prima
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-15"]', By.XPATH).click() #apro Ordini
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[2]', By.XPATH).click() #attivo impostazione
        sleep(1)

    def conferma_quantita_ordini_fornitore(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Acquisti")
        self.navigateTo("Ordini fornitore")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click() #crea ordine fornitore
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica-container"]', By.XPATH).click() #imposta fornitore
        sleep(1)

        self.get_element('//ul[@id="select2-idanagrafica-results"]//li[1]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()   #click su aggiungi
        self.wait_loader()

        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click()    #aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys('Test') #aggiunta descrizione riga
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys('1')   #aggiunta prezzo unitario
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()    #click su aggiungi
        sleep(1)
        
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//i[@class="fa fa-check text-success"])[1]')))    #check se è stato confermata la quantita
        #elimino ordine
        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-15"]', By.XPATH).click() #apro Ordini
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[3]', By.XPATH).click() #disattivo impostazione
        sleep(1)

        self.expandSidebar("Acquisti")
        self.navigateTo("Ordini fornitore")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click() #crea ordine fornitore
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica-container"]', By.XPATH).click() #imposta fornitore
        sleep(1)

        self.get_element('//ul[@id="select2-idanagrafica-results"]//li[1]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()   #click su aggiungi
        self.wait_loader()

        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click()    #aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys('Test') #aggiunta descrizione riga
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys('1')   #aggiunta prezzo unitario
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()    #click su aggiungi
        sleep(1)
        
        wait.until(EC.visibility_of_element_located((By.XPATH, '//i[@class="fa fa-clock-o text-warning"]')))    #check se è stato confermata la quantita
        #elimino ordine
        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        #torno alle impostazioni di prima
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-15"]', By.XPATH).click() #apro Ordini
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[3]', By.XPATH).click() #attivo impostazione
        sleep(1)