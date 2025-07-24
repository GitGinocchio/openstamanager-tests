from common.Test import Test, get_html
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class CassePrevidenziali(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Strumenti")
        self.expandSidebar("Tabelle")
        

    def test_creazione_casse_previdenziali(self):
        # Creazione cassa previdenziale     *Required*
        self.creazione_casse_previdenziali("Cassa Previdenziale di Prova da Modificare","80,00", "60,00")
        self.creazione_casse_previdenziali("Cassa Previdenziale di Prova da Eliminare", "20,00", "40,00")        

        # Modifica Cassa Previdenziale
        self.modifica_casse_previdenziali("Cassa Previdenziale di Prova")

        # Cancellazione Cassa Previdenziale
        self.elimina_casse_previdenziali()
        
        # Verifica Cassa Previdenziale
        self.verifica_casse_previdenziali()


    def creazione_casse_previdenziali(self, descrizione=str, percentuale=str, indetraibile=str):
        self.navigateTo("Casse previdenziali")
        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        self.input(modal, 'Descrizione').setValue(descrizione)
        self.input(modal, 'Percentuale').setValue(percentuale)
        self.input(modal, 'Indetraibile').setValue(indetraibile)
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

    def modifica_casse_previdenziali(self, modifica=str):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Casse previdenziali")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione"]/input'))).send_keys('Cassa Previdenziale di Prova da Modificare', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        sleep(1) 

        self.driver.execute_script('window.scrollTo(0,0)')
        self.input(None,'Descrizione').setValue(modifica)
        self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Casse previdenziali")
        self.wait_loader()    

        self.get_element('//th[@id="th_Descrizione"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def elimina_casse_previdenziali(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Casse previdenziali")
        self.wait_loader()    

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione"]/input'))).send_keys('Cassa Previdenziale di Prova da Eliminare', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        sleep(1)   

        self.driver.execute_script('window.scrollTo(0,0)')
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        self.wait_loader
         

        self.get_element('//th[@id="th_Descrizione"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)
        
    def verifica_casse_previdenziali(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Casse previdenziali")
        self.wait_loader()    

        # Verifica elemento modificato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione"]/input'))).send_keys("Cassa Previdenziale di Prova", Keys.ENTER)
        sleep(1)

        modificato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[2]').text
        self.assertEqual("Cassa Previdenziale di Prova",modificato)
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

        # Verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione"]/input'))).send_keys("Cassa Previdenziale di Prova da Eliminare", Keys.ENTER)
        sleep(1)
        
        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)