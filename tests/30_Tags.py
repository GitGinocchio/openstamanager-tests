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


class Tags(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Attività")
        
    def test_creazione_tags(self):
        # Creazione tags 
        self.expandSidebar("Strumenti")
        self.expandSidebar("Tabelle")

        self.creazione_tags("Tags di Prova da Modificare")
        self.creazione_tags("Tags di Prova da Eliminare")
        
        # Modifica tags
        self.modifica_tags("Tags di Prova")

        # Cancellazione tags
        self.elimina_tags()

        # Verifica tags
        self.verifica_tags()

    def creazione_tags(self, descrizione: str):
        self.navigateTo("Tags")
        self.wait_loader()  

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        self.input(modal, 'Nome').setValue(descrizione)

        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

    def modifica_tags(self, modifica:str):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Tags")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Tags di Prova da Modificare', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()
        
        self.input(None,'Nome').setValue(modifica)
        self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Tags")
        self.wait_loader()  

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def elimina_tags(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Tags")
        self.wait_loader()  

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Tags di Prova da Eliminare', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        sleep(1)
        
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        self.wait_loader()

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)
        
    def verifica_tags(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Tags")
        self.wait_loader()    

        # Verifica elemento modificato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Tags di Prova", Keys.ENTER)
        sleep(1)

        modificato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[3]').text
        self.assertEqual("Tags di Prova",modificato)
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

        # Verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Tags di Prova da Eliminare", Keys.ENTER)
        sleep(1)

        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)