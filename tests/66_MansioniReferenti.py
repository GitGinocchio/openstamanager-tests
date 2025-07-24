from common.Test import Test, get_html
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class MansioniReferenti(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Strumenti")
        self.expandSidebar("Tabelle")
        self.navigateTo("Mansioni referenti")

    def test_creazione_mansioni_referenti(self):
        # Creazione mansione referente      *Required*
        self.creazione_mansioni_referenti("Mansione Referente di Prova da Modificare")
        self.creazione_mansioni_referenti("Mansione Referente di Prova da Eliminare")

        # Modifica Mansione Referente
        self.modifica_mansione_referente("Mansione Referente di Prova")
        
        # Cancellazione Mansione Referente
        self.elimina_mansione_referente()
        
        # Verifica Mansione Referente
        self.verifica_mansione_referente()

    def creazione_mansioni_referenti(self, mansione= str):
        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        self.input(modal, 'Mansione').setValue(mansione)
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

    def modifica_mansione_referente(self, modifica=str):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Mansioni referenti")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Mansione Referente di Prova da Modificare', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        sleep(1)

        self.driver.execute_script('window.scrollTo(0,0)')
        self.input(None,'Nome').setValue(modifica)
        self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Mansioni referenti")
        self.wait_loader()    

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def elimina_mansione_referente(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Mansioni referenti")
        self.wait_loader()    

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Mansione Referente di Prova da Eliminare', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        sleep(1)

        self.driver.execute_script('window.scrollTo(0,0)')
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        self.wait_loader()      

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)
        
    def verifica_mansione_referente(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Mansioni referenti")
        self.wait_loader()    

        # Verifica elemento modificato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Mansione Referente di Prova", Keys.ENTER)
        sleep(1)

        modificato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[2]').text
        self.assertEqual("Mansione Referente di Prova",modificato)
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

        # Verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Mansione Referente di Prova da Eliminare", Keys.ENTER)
        sleep(1)
        
        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)