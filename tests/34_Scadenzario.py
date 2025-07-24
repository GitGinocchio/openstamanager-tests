from common.Test import Test, get_html
from selenium.webdriver.common.keys import Keys
from common.RowManager import RowManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class Scadenzario(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Contabilità")


    def test_creazione_scadenzario(self):
        # Crea una nuova scadenza. *Required*
        self.creazione_scadenzario("Cliente", "Scadenze generiche", "10", "Scadenza di Prova")
        self.creazione_scadenzario("Cliente", "Scadenze generiche", "10", "Scadenza di Prova da Eliminare")

        # Modifica scadenza
        self.modifica_scadenza("Scadenza di Prova")

        # Cancellazione scadenza
        self.elimina_scadenza()

        # Verifica scadenza
        self.verifica_scadenza()

        # Registrazione contabile (Azioni di gruppo)
        self.registrazione_contabile()

        # Info distinta (Azioni di gruppo)
        self.info_distinta()

    def creazione_scadenzario(self, nome: str, tipo: str, importo: str, descrizione: str):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Scadenzario")
        self.wait_loader() 

        # Crea una nuova scadenza. 
        # Apre la schermata di nuovo elemento
        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        self.input(modal, 'Tipo').setByText(tipo)
        self.input(modal, 'Anagrafica').setByText(nome)
        self.input(modal, 'Importo').setValue(importo)

        self.get_element('(//iframe[@class="cke_wysiwyg_frame cke_reset"])[1]', By.XPATH).click()  
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//iframe[@class="cke_wysiwyg_frame cke_reset"])[1]'))).send_keys(descrizione)

        # Submit
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()
    
    def modifica_scadenza(self, modifica:str):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Scadenzario")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione-scadenza"]/input'))).send_keys('Scadenza di Prova', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()
        
        self.get_element('(//iframe[@class="cke_wysiwyg_frame cke_reset"])[2]', By.XPATH).send_keys(modifica) 

        self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()
        sleep(1)
                
        self.navigateTo("Scadenzario")
        self.wait_loader()  

    def elimina_scadenza(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Scadenzario")
        self.wait_loader()  

        self.get_element('//th[@id="th_Descrizione-scadenza"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione-scadenza"]/input'))).send_keys('Scadenza di Prova da Eliminare', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        self.wait_loader()

        self.get_element('//th[@id="th_Descrizione-scadenza"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def verifica_scadenza(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Scadenzario")
        self.wait_loader()    

        # Verifica elemento modificato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione-scadenza"]/input'))).send_keys("Scadenza di Prova", Keys.ENTER)
        sleep(1)

        modificato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[2]').text
        self.assertEqual("Scadenza di Prova",modificato)
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

        # Verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione-scadenza"]/input'))).send_keys("Scadenza da Eliminare", Keys.ENTER)
        sleep(1)
        
        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)
        self.get_element('(//i[@class="deleteicon fa fa-times"])[1]', By.XPATH).click() 
        sleep(1)
        
    def registrazione_contabile(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Scadenzario")
        self.wait_loader() 

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione-scadenza"]/input'))).send_keys("Fattura immediata di acquisto numero 01", Keys.ENTER)  
        sleep(1)

        self.get_element('//tbody//tr//td', By.XPATH).click() 
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()
        self.get_element('//a[@data-op="registrazione-contabile"]', By.XPATH).click() 
        sleep(2)

        # TODO: fare la registrazione contabile
        
        self.get_element('//button[@class="close"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//tbody//tr//td', By.XPATH).click() 
        self.get_element('(//i[@class="deleteicon fa fa-times"])[1]', By.XPATH).click() 
        sleep(1)

    def info_distinta(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Scadenzario")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione-scadenza"]/input'))).send_keys("Fattura immediata di acquisto numero 01", Keys.ENTER)  
        sleep(1)

        self.get_element('//tbody//tr//td', By.XPATH).click() 
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        self.get_element('//a[@data-op="change_distinta"]', By.XPATH).click() 
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="distinta"]'))).send_keys("Prova") 
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click() 
        self.wait_loader()

        self.navigateTo("Scadenzario")
        self.wait_loader()

        self.get_element('(//i[@class="deleteicon fa fa-times"])[1]', By.XPATH).click() 
        sleep(1)