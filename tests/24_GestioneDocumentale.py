from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from common.Test import Test, get_html

class GestioneDocumentale(Test):
    def setUp(self):
        super().setUp()


    def test_creazione_gestione_documentale(self):
        # Crea un nuovo documento di prova   *Required* 
        self.add_documento_di_prova('Documento di Prova da Modificare', 'Documenti società')
        self.add_documento_di_prova('Documento di Prova da Eliminare', 'Documenti società')

        # Modifica documento 
        self.modifica_documento("Documento di prova")

        # Cancellazione documento 
        self.elimina_documento()

        # Verifica documento
        self.verifica_documento()
        
    def add_documento_di_prova(self, nome: str, categoria: str):
        self.navigateTo("Gestione documentale")

        # Crea una nuova newsletter
        # Apre la schermata di nuovo elemento
        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        # Completamento dei campi per il nuovo elemento
        self.input(modal, 'Nome').setValue(nome)

        select = self.input(modal, 'Categoria')
        select.setByText(categoria)

        # Submit
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

    def modifica_documento(self, modifica:str):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Gestione documentale")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Documento di Prova da Modificare', Keys.ENTER)        
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()
        
        self.input(None,'Nome').setValue(modifica)
        self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Gestione documentale")
        self.wait_loader()  

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def elimina_documento(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Gestione documentale")
        self.wait_loader()  

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Documento di Prova da Eliminare', Keys.ENTER)        
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        sleep(1)
        
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        self.wait_loader()

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)
        
    def verifica_documento(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Gestione documentale")
        self.wait_loader()    

        # Verifica elemento modificato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Documento di prova", Keys.ENTER)
        sleep(1)

        modificato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[3]').text
        self.assertEqual("Documento di prova",modificato)
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

        # Verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Documento di prova da Eliminare", Keys.ENTER)
        sleep(1)
        
        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)