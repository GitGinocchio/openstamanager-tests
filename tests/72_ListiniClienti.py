from common.Test import Test, get_html
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Listini(Test):
    def setUp(self):
        super().setUp()
        self.navigateTo("Magazzino")


    def test_creazione_listino_cliente(self):
        # Crea un nuovo listino cliente. *Required*
        self.creazione_listino_cliente("Listino cliente di Prova da Modificare","01/12/2025", "01/01/2025")
        self.creazione_listino_cliente("Listino cliente di Prova da Eliminare", "01/12/2025", "01/01/2025")
        
        # Modifica listino cliente
        self.modifica_listino_cliente("Listino cliente di Prova")
        
        # Cancellazione listino cliente
        self.elimina_listino_cliente()
        
        # Verifica listino cliente
        self.verifica_listino_cliente()

        # Aggiorna listino cliente (Azione di gruppo) da anagrafiche
        self.aggiorna_listino_cliente()

        # Aggiungi a listino cliente (Azioni di gruppo) da Articoli
        self.aggiungi_a_listino_cliente()

    def creazione_listino_cliente(self, nome:str, dataatt: str, datascad: str):
        self.navigateTo("Listini cliente")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        self.input(modal, 'Data attivazione').setValue(dataatt)
        self.input(modal, 'Data scadenza default').setValue(datascad)
        self.input(modal, 'Nome').setValue(nome)

        # Submit
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

    def modifica_listino_cliente(self, modifica:str):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Listini cliente")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Listino cliente di Prova da Modificare', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()  

        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-selection select2-selection--single"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-search select2-search--dropdown"]//input[@type="search"]'))).send_keys("001")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-search select2-search--dropdown"]//input[@type="search"]'))).send_keys(Keys.ENTER)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="btn-group btn-group-flex"]//button[@class="btn btn-primary"]'))).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("10,00")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="sconto_percentuale"]'))).send_keys("10")
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//button[@class="btn btn-success"])[2]'))).click()
        sleep(1)

        self.input(None,'Nome').setValue(modifica)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@id="save"]'))).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@id="back"]'))).click()
        sleep(1)

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def elimina_listino_cliente(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Listini cliente")
        self.wait_loader() 

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Listino cliente di Prova da Eliminare', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        sleep(1)

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def verifica_listino_cliente(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Listini cliente")
        self.wait_loader()    

        # Verifica elemento modificato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Listino cliente di Prova", Keys.ENTER)
        sleep(1)

        modificato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[2]').text
        self.assertEqual("Listino cliente di Prova",modificato)
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

        # Verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Listino cliente di Prova da Eliminare", Keys.ENTER)
        sleep(1)

        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[1]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def aggiorna_listino_cliente(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Anagrafiche")
        self.wait_loader() 

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Ragione-sociale"]/input'))).send_keys("Cliente", Keys.ENTER)   
        sleep(1)

        self.get_element('//tbody//tr//td', By.XPATH).click() 
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@data-op="aggiorna-listino"]'))).click()    
        self.get_element('//span[@id="select2-id_listino-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Listino cliente di Prova", Keys.ENTER)  
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()  
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()  
        self.wait_loader()

        self.get_element('(//span[@class="select2-selection__clear"])[4]', By.XPATH).click()  
        self.get_element('//button[@id="save"]', By.XPATH).click() 
        self.wait_loader()

        self.navigateTo("Anagrafiche")
        self.wait_loader()

        self.get_element('//th[@id="th_Ragione-sociale"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click() 
        sleep(1)

        self.navigateTo("Magazzino")

    def aggiungi_a_listino_cliente(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Articoli")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Codice"]/input'))).send_keys("001", Keys.ENTER) 
        sleep(1)

        self.get_element('//tbody//tr//td', By.XPATH).click() 
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        self.get_element('//a[@data-op="add-listino"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//span[@id="select2-id_listino-container"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//li[@class="select2-results__option select2-results__option--highlighted"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="sconto_percentuale"]'))).send_keys("10")   
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click() 
        self.wait_loader()

        self.navigateTo("Listini cliente")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click() 
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//tr[1]//td[8]'))) 
        self.get_element('//tr[1]//td[9]//a[2]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-primary"]', By.XPATH).click() 
        self.wait_loader()
        