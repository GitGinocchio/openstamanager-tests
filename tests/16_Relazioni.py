from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from common.Test import Test, get_html

class Relazioni(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Anagrafiche")
        self.navigateTo("Relazioni")
        self.wait_loader()

    def test_creazione_relazioni(self):
        # Creazione relazione *Required*
        self.creazione_relazioni("Relazione di Prova da Modificare","#9d2929")
        self.creazione_relazioni("Relazione di Prova da Eliminare","#3737db")

        # Modifica relazione
        self.modifica_relazioni("Relazione di Prova")

        # Cancellazione relazione
        self.elimina_relazioni()

        # Verifica relazione
        self.verifica_relazione()

    def creazione_relazioni(self, descrizione=str, colore=str):
        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        self.input(modal, 'Colore').setValue(colore)
        self.input(modal, 'Descrizione').setValue(descrizione)

        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        sleep(1)

    def modifica_relazioni(self, modifica=str):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Relazioni")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione"]/input'))).send_keys('Relazione di Prova da Modificare', Keys.ENTER)        
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()
        
        colore=self.get_element('//input[@id="colore"]', By.XPATH)
        colore.clear()
        colore.send_keys("#436935")

        self.input(None,'Descrizione').setValue(modifica)
        self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Relazioni")
        self.wait_loader()    

        self.get_element('//th[@id="th_Descrizione"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def elimina_relazioni(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Relazioni")
        self.wait_loader()    

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione"]/input'))).send_keys('Relazione di Prova da Eliminare', Keys.ENTER)        
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()    
        sleep(1)
        
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        self.wait_loader()

        self.get_element('//th[@id="th_Descrizione"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)
        
    def verifica_relazione(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Relazioni")
        self.wait_loader()    

        # Verifica elemento modificato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione"]/input'))).send_keys("Relazione di Prova", Keys.ENTER)
        sleep(1)

        modificato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[2]').text
        self.assertEqual("Relazione di Prova",modificato)
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

        # Verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione"]/input'))).send_keys("Relazione di Prova da Eliminare", Keys.ENTER)
        sleep(1)

        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[1]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)
