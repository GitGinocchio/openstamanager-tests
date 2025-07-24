from common.Test import Test, get_html
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class StatiContratti(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Strumenti")
        self.expandSidebar("Tabelle")
        

    def test_creazione_stati_contratti(self):
        # Creazione stato contratti     *Required*
        self.creazione_stato_contratti("Stato dei Contratti di Prova da Modificare", "fa fa-check text-success", "#9d2929" )
        self.creazione_stato_contratti("Stato dei Contratti di Prova da Eliminare", "fa fa-thumbs-down text-danger", "#38468f")

        # Modifica Stato dei contratti
        self.modifica_stato_contratti("Stato dei Contratti di Prova")
        
        # Cancellazione Stato dei contratti
        self.elimina_stato_contratti()
           
        # Verifica Stato dei contratti
        self.verifica_stato_contratti()

    def creazione_stato_contratti(self, descrizione=str, icona=str, colore=str):
        self.navigateTo("Stati dei contratti")
        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        self.input(modal, 'Descrizione').setValue(descrizione)
        self.input(modal, 'Colore').setValue(colore)
        self.input(modal, 'Icona').setValue(icona)
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

    def modifica_stato_contratti(self, modifica=str):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Stati dei contratti")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione"]/input'))).send_keys('Stato dei Contratti di Prova da Modificare', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        sleep(1)  

        self.driver.execute_script('window.scrollTo(0,0)')
        self.input(None,'Descrizione').setValue(modifica)
        self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Stati dei contratti")
        self.wait_loader()    

        self.get_element('//th[@id="th_Descrizione"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def elimina_stato_contratti(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Stati dei contratti")
        self.wait_loader()    

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione"]/input'))).send_keys('Stato dei Contratti di Prova da Eliminare', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        sleep(1)

        self.driver.execute_script('window.scrollTo(0,0)')
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        self.wait_loader()     

        self.get_element('//th[@id="th_Descrizione"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)
        
    def verifica_stato_contratti(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Stati dei contratti")
        self.wait_loader()    

        # Verifica elemento modificato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione"]/input'))).send_keys("Stato dei Contratti di Prova", Keys.ENTER)
        sleep(1)

        modificato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[2]').text
        self.assertEqual("Stato dei Contratti di Prova",modificato)
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

        # Verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione"]/input'))).send_keys("Stato dei Contratti di Prova da Eliminare", Keys.ENTER)
        sleep(1)
        
        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)