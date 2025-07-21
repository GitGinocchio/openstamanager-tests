from common.Test import Test, get_html
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Impianti(Test):
    def setUp(self):
        super().setUp()

        
    def test_creazione_impianto(self):
        # Crea un nuovo impianto.   *Required*
        self.add_impianto('01', 'Impianto di Prova da Modificare', 'Cliente')
        self.add_impianto('02', 'Impianto di Prova da Eliminare', 'Cliente')

        # Modifica Impianto
        self.modifica_impianto("Impianto di Prova")

        # Cancellazione Impianto
        self.elimina_impianto()

        # Verifica Impianto
        self.verifica_impianto()

        # Plugin impianti del cliente da anagrafiche 
        self.apri_impianti()

        # Plugin impianti da attività
        self.plugin_impianti()

        # Plugin interventi svolti
        self.plugin_interventi_svolti()

        # Plugin componenti
        self.componenti()

        # Elimina selezionati (Azioni di gruppo)
        self.elimina_selezionati()
        
    def add_impianto(self, matricola: str, nome:str, cliente: str):
        self.navigateTo("Impianti")
        # Crea un nuovo impianto
        # Apre la schermata di nuovo elemento
        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        # Completamento dei campi per il nuovo elemento
        self.input(modal, 'Matricola').setValue(matricola)
        self.input(modal, 'Nome').setValue(nome)
        select = self.input(modal, 'Cliente')
        select.setByText(cliente)

        # Submit
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

    def modifica_impianto(self, modifica=str):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Impianti")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Impianto di Prova da Modificare', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()
        
        self.input(None,'Nome').setValue(modifica)
        self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Impianti")
        self.wait_loader()    

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def elimina_impianto(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Impianti")
        self.wait_loader()    

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Impianto di Prova da Eliminare', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask "]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        sleep(1)

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)
        
    def verifica_impianto(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Impianti")
        self.wait_loader()    

        # Verifica elemento modificato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Impianto di Prova", Keys.ENTER)
        sleep(1)

        modificato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[3]').text
        self.assertEqual("Impianto di Prova",modificato)
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

        # Verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Impianto di Prova da Eliminare", Keys.ENTER)
        sleep(1)
        
        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)
        self.navigateTo("Impianti")
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def apri_impianti(self): 
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Anagrafiche")
        self.wait_loader() 

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Ragione-sociale"]/input'))).send_keys("Cliente", Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        sleep(1) 

        self.get_element('//a[@id="link-tab_1"]', By.XPATH).click()
        self.get_element('//div[@class="text-right"]', By.XPATH).click()
        impianto=self.get_element('//div [@class="text-right"]', By.XPATH).text
        self.assertEqual(impianto,"01")

        self.navigateTo("Anagrafiche")
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def plugin_impianti(self):     
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Attività")
        self.wait_loader()    

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Numero"]//input'))).send_keys("2", Keys.ENTER)
        sleep(1) 

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader() 

        self.get_element('//a[@id="link-tab_2"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//span[@id="select2-id_impianto_add-container"]', By.XPATH).click()
        sleep(1)
        
        self.get_element('//li[@class="select2-results__option select2-results__option--highlighted"]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-default tip tooltipstered"]', By.XPATH).click()
        sleep(1)

        matricola=self.get_element('//div[@id="tab_2"]//tbody//tr//td[2]', By.XPATH).text
        self.assertEqual(matricola,"01")
        self.get_element('//button[@class="btn btn-sm btn-danger "]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-primary"]', By.XPATH).click()
        sleep(1)

        self.get_element('//span[@id="select2-id_impianto_add-container"]', By.XPATH).click()
        self.get_element('//li[@class="select2-results__option select2-results__option--highlighted"]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-default tip tooltipstered"]', By.XPATH).click()
        sleep(1)

        self.navigateTo("Attività")
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def plugin_interventi_svolti(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Impianti")
        self.wait_loader()    

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Impianto di Prova", Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[3]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@id="link-tab_8"]', By.XPATH).click()
        self.wait_loader()

        totale=self.get_element('//tbody//tr[3]//td[2]', By.XPATH).text
        self.assertEqual(totale, "36,60 €")
        self.navigateTo("Impianti")
        self.wait_loader()

        self.get_element('//th[@id="th_Nome"]//i', By.XPATH).click()
        sleep(1)

    def componenti(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Impianti")
        self.wait_loader()    

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Impianto di Prova", Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[3]', By.XPATH).click()
        self.wait_loader()
 
        self.get_element('//a[@id="link-tab_31"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('(//button[@class="btn btn-primary bound clickable"])[2]', By.XPATH).click()
        sleep(1)

        self.get_element('//span[@id="select2-id_articolo-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Articolo 1", Keys.ENTER)
        self.get_element('(//form//button[@class="btn btn-primary"])[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//div[@id="tab_31"]//button[@class="btn btn-tool"]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="data_installazione_1"]'))).send_keys("01/01/2025")
        self.get_element('//button[@class="btn btn-success pull-right"]', By.XPATH).click()
        self.wait_loader()

        data_installazione=self.get_element('//div[@id="tab_31"]//tr[1]//td[3]', By.XPATH).text
        self.assertEqual(data_installazione, "01/01/2025")
        self.get_element('//div[@id="tab_31"]//button[@class="btn btn-tool"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="btn btn-warning pull-right"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-primary"]', By.XPATH).click()
        self.wait_loader()
        
        sostituito=self.get_element('(//div[@id="tab_31"]//tr[1]//td[1])[1]', By.XPATH).text
        self.assertEqual(sostituito, "#2")
        self.navigateTo("Impianti")
        self.wait_loader()

        self.get_element('//th[@id="th_Nome"]//i', By.XPATH).click()
        sleep(1)

    def elimina_selezionati(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Impianti")
        self.wait_loader()  

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="matricola"]'))).send_keys("02")   
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="nome"]'))).send_keys("Prova")     
        self.get_element('//span[@id="select2-idanagrafica_impianto-container"]', By.XPATH).click()  
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() 
        self.wait_loader()

        self.navigateTo("Impianti") 
        self.wait_loader() 
        
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Matricola"]/input'))).send_keys("02", Keys.ENTER)  
        sleep(1)

        self.get_element('//tbody//tr//td', By.XPATH).click() 
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        self.get_element('//a[@data-op="delete-bulk"]', By.XPATH).click()  
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click() 
        self.wait_loader()

        scritta=self.get_element('//tbody//tr', By.XPATH).text
        self.assertEqual(scritta, "La ricerca non ha portato alcun risultato.") 
        self.get_element('//th[@id="th_Matricola"]//i', By.XPATH).click()  
        sleep(1)
