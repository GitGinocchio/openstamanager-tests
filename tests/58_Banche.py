from common.Test import Test, get_html
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Banche(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Strumenti")
        self.expandSidebar("Tabelle")


    def test_creazione_banca(self):
        # Creazione banca       *Required*
        self.creazione_banca("Cliente", "Banca di Prova da Modificare", "IT11C1234512345678912345679", "12345678")
        self.creazione_banca("Cliente", "Banca di Prova da Eliminare", "IT11C1234512345678912345679", "12345678")

        # Modifica Banca
        self.modifica_banca("Banca di Prova")
        
        # Cancellazione Banca
        self.elimina_banca()
        
        # Verifica Banca
        self.verifica_banca()

        # Aggiorna Banca (Azioni di gruppo) da Fatture di acquisto
        self.aggiorna_banca_fatture_acquisto()

        # Aggiorna Banca (Azioni di gruppo) da Scadenzario
        self.aggiorna_banca_scadenzario()

        # Aggiorna Banca (Azioni di gruppo) da Fatture di Vendita
        self.aggiorna_banca_fatture_vendita()

    def creazione_banca(self, anagrafica: str, nome: str, iban: str, bic: str):
        self.navigateTo("Banche")
        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        select = self.input(modal, 'Anagrafica')
        select.setByText(anagrafica)
        self.input(modal, 'Nome').setValue(nome)
        self.input(modal, 'IBAN').setValue(iban)
        self.input(modal, 'BIC').setValue(bic)
        
        # Submit
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

    def modifica_banca(self, modifica=str):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Banche")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Banca di Prova da Modificare', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        sleep(1)

        self.driver.execute_script('window.scrollTo(0,0)')
        self.input(None,'Nome').setValue(modifica)
        self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Banche")
        self.wait_loader()    

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def elimina_banca(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Banche")
        self.wait_loader()    

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Banca di Prova da Eliminare', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        sleep(1)

        self.driver.execute_script('window.scrollTo(0,0)')
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        self.wait_loader()      

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)
        
    def verifica_banca(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Banche")
        self.wait_loader()    

        # Verifica elemento modificato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Banca di Prova", Keys.ENTER)
        sleep(1)
        
        modificato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[2]').text
        self.assertEqual("Banca di Prova",modificato)
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

        # Verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Banca di Prova da Eliminare", Keys.ENTER)
        sleep(1)
        
        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)

    def aggiorna_banca_fatture_acquisto(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Banche") 
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//span[@id="select2-id_anagrafica-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Admin spa")
        sleep(1)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="nome"]'))).send_keys("Banca Admin spa") 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="iban"]'))).send_keys("IT11C1234512345678912345679")
        sleep(1)
        
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()
        self.wait_loader()

        self.expandSidebar("Acquisti")
        self.navigateTo("Fatture di acquisto")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Numero"]//input'))).send_keys("3", Keys.ENTER) 
        self.wait_loader()
        sleep(1)

        self.get_element('//tbody//tr//td', By.XPATH).click() 
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        self.get_element('//a[@data-op="change-bank"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//span[@id="select2-id_banca-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Banca Admin spa")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()
        self.wait_loader()

        banca=self.get_element('//tbody//tr//td[9]', By.XPATH).text 
        self.assertEqual(banca, "Banca Admin spa - IT11C1234512345678912345679")
        sleep(1)

    def aggiorna_banca_scadenzario(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Contabilità")
        self.navigateTo("Scadenzario")
        self.wait_loader()

        self.get_element('//span[@id="select2-id_segment_-container"]', By.XPATH).click()  
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Scadenzario clienti")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.wait_loader()
        sleep(1)

        # TODO: allineare ai documenti presenti, nessuna scadenza ha metodo di pagamento Bonifico
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Tipo-di-pagamento"]//input'))).send_keys("Bonifico", Keys.ENTER) #cerca il bonifico
        sleep(1)

        self.get_element('//tbody//tr//td', By.XPATH).click() 
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//a[@data-op="change-bank"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//span[@id="select2-id_banca-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Banca Admin spa")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()
        self.wait_loader()
        sleep(1)

        widget=self.get_element('//div[@class="toast toast-success"]//div[3]', By.XPATH).text 
        self.assertEqual(widget, "Banca aggiornata per le Fatture 0001/2025 !")  

        self.get_element('//tbody//tr//td', By.XPATH).click() 
        self.get_element('//span[@class="select2-selection__clear"]', By.XPATH).click() 
        self.wait_loader()

    def aggiorna_banca_fatture_vendita(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        self.get_element('//a[@data-op="change-bank"]', By.XPATH).click()  
        sleep(1)

        self.get_element('//span[@id="select2-id_banca-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Banca Admin spa")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()
        self.wait_loader()
        sleep(1)

        banca=self.get_element('//tbody//tr//td[7]', By.XPATH).text  
        self.assertEqual(banca, "Banca Admin spa - IT11C1234512345678912345679")
        self.get_element('//tbody//tr//td[2]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

