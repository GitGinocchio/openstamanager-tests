from common.Test import Test, get_html
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class Combinazioni(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Magazzino")


    def test_creazione_combinazioni(self):
        # Creazione combinazioni *Required*
        self.creazione_combinazioni(codice="0001", nome="Combinazione di Prova da Modificare", attributi="Taglie")
        self.creazione_combinazioni(codice="0002", nome="Combinazione di Prova da Eliminare", attributi="Taglie")

        # Modifica Combinazioni
        self.modifica_combinazioni("Vestito")

        # Cancellazione Combinazioni
        self.elimina_combinazioni()
        
        # Verifica Combinazioni
        self.verifica_combinazioni()

        # Plugin varianti articoli da Articoli
        self.varianti_articoli()

    def creazione_combinazioni(self, codice: str, nome: str, attributi: str):
        self.navigateTo("Combinazioni")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        self.input(modal, 'Codice').setValue(codice)
        self.input(modal, 'Nome').setValue(nome)
        select = self.input(modal, 'Attributi')
        select.setByText(attributi)
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()
       
    def modifica_combinazioni(self, modifica):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Combinazioni")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Combinazione di Prova da Modificare', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()
        
        self.input(None,'Nome').setValue(modifica)
        self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//button[@onclick="generaVarianti(this, By.XPATH)"]').click()
        self.wait_loader()

        self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Combinazioni")
        self.wait_loader()

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def elimina_combinazioni(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Combinazioni")
        self.wait_loader()    

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Combinazione di Prova da Eliminare', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        sleep(1)
        
        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)
        
    def verifica_combinazioni(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Combinazioni")
        self.wait_loader()    

        # Verifica elemento modificato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Vestito", Keys.ENTER)
        sleep(1)

        modificato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[3]').text
        self.assertEqual("Vestito",modificato)
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

        # Verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Attributo di Prova da Eliminare", Keys.ENTER)
        sleep(1)

        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)

    def varianti_articoli(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Articoli")
        self.wait_loader()

        # Verifica combinazioni
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione"]/input'))).send_keys('Vestito', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@id="link-tab_34"]', By.XPATH).click() 
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_34"]//tr[3]')))

        # Modifica combinazioni
        self.navigateTo("Attributi Combinazioni")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('(//button[@class="btn btn-warning btn-xs"])[1]', By.XPATH).click()
        sleep(1)

        element = self.get_element('//input[@id="nome"]', By.XPATH)
        element.clear()
        element.send_keys("XS",Keys.ENTER)
        sleep(2)

        self.navigateTo("Articoli")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@id="link-tab_34"]', By.XPATH).click() 
        self.wait_loader()

        taglia=self.get_element('//div[@id="tab_34"]//div[@class="card card-primary"]//tbody//tr//td[2]', By.XPATH).text
        self.assertEqual(taglia, "Taglie: XS")

        # Elimina combinazioni
        self.navigateTo("Combinazioni")
        self.wait_loader()

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()