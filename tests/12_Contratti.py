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


class Contratti(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Vendite")


    def test_creazione_contratto(self):
        # Crea una nuovo contratto *Required*
        importi = RowManager.list()
        self.creazione_contratto("Contratto di Prova da Modificare", "Cliente", importi[0])

        # Duplica un contratto *Required*
        self.duplica_contratto()

        # Modifica Contratto
        self.modifica_contratto("Contratto di Prova")

        # Cancellazione contratto
        self.elimina_contratto()     

        # Verifica contratto
        self.verifica_contratto()

        # Plugin contratti del cliente da Anagrafiche
        self.contratti_del_cliente()

        # Plugin consuntivo
        self.consuntivo()
        
        # Plugin pianificazione attività
        self.pianificazione_attivita()

        # Plugin pianificazione fatturazione
        self.pianificazione_fatturazione()

        # Plugin rinnovi
        self.rinnovi()

        # Cambia stato (Azioni di gruppo)
        self.cambia_stato()

        # Fattura contratti (Azioni di gruppo)
        self.fattura_contratti()

        # Rinnova contratti (Azioni di gruppo)
        self.rinnova_contratti()

    def creazione_contratto(self, nome:str, cliente: str, file_importi: str):
        self.navigateTo("Contratti")
        self.wait_loader() 

        # Crea Contratto
        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        self.input(modal, 'Nome').setValue(nome)
        select = self.input(modal, 'Cliente')
        select.setByText(cliente)
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

        row_manager = RowManager(self)
        self.valori=row_manager.compile(file_importi)

    def duplica_contratto(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Contratti")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        sleep(1)
        
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="pulsanti"]//button[@class="btn btn-primary ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-primary"]'))).click()
        self.wait_loader()

        element=self.get_element('//input[@id="nome"]', By.XPATH)
        element.clear()
        element.send_keys("Contratto di Prova da Eliminare") 
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

    def modifica_contratto(self, modifica=str):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Contratti")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('=Contratto di Prova da Modificare', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()
        
        element=self.get_element('//input[@id="nome"]', By.XPATH)
        element.clear()
        element.send_keys(modifica) 
        self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()
        sleep(1)

        # Estrazione totali righe
        sconto = self.get_element('//div[@id="righe"]//tbody[2]//tr[2]//td[2]', By.XPATH).text
        totale_imponibile = self.get_element('//div[@id="righe"]//tbody[2]//tr[3]//td[2]', By.XPATH).text
        iva = self.get_element('//div[@id="righe"]//tbody[2]//tr[4]//td[2]', By.XPATH).text
        totale = self.get_element('//div[@id="tab_0"]//div[@id="righe"]//tbody[2]//tr[5]//td[2]', By.XPATH).text

        self.assertEqual(sconto, (self.valori["Sconto/maggiorazione"]+ ' €'))
        self.assertEqual(totale_imponibile, (self.valori["Totale imponibile"]+ ' €'))
        self.assertEqual(iva, (self.valori["IVA"] + ' €'))
        self.assertEqual(totale, (self.valori["Totale documento"] + ' €'))

        self.navigateTo("Contratti")
        self.wait_loader()

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def elimina_contratto(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Contratti")
        self.wait_loader()  

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Contratto di Prova da Eliminare', Keys.ENTER)        
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        self.wait_loader()

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def verifica_contratto(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Contratti")
        self.wait_loader()  

        # Verifica elemento modificato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Contratto di Prova", Keys.ENTER)
        sleep(1)

        modificato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[3]').text
        self.assertEqual("Contratto di Prova",modificato)
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

        # Verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Contratto di Prova da Eliminare", Keys.ENTER)
        sleep(1)

        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)
        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def contratti_del_cliente(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Anagrafiche")
        self.wait_loader() 

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Ragione-sociale"]/input'))).send_keys("Cliente", Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader() 

        self.get_element('//a[@id="link-tab_35"]', By.XPATH).click()
        sleep(1)
        
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_35"]//tbody//tr/td[2]')))

    def consuntivo(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Vendite")
        self.navigateTo("Contratti")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Contratto di Prova", Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr/td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@id="link-tab_13"]', By.XPATH).click()

        budget=self.get_element('//div[@id="tab_13"]//span[@class="text-success"]', By.XPATH).text
        self.assertEqual(budget, "+ 264,80 €")

        self.navigateTo("Contratti")
        self.wait_loader()

        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def pianificazione_attivita(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Contratti")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()
        
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="nome"]'))).send_keys("Manutenzione")
        self.get_element('//span[@id="select2-idanagrafica-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="data_accettazione"]'))).send_keys("01/01/2025")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="data_conclusione"]'))).send_keys("31/12/2025")
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("Manutenzione")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="qta"]'))).send_keys("12")
        self.get_element('//span[@id="select2-um-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//input[@class="select2-search__field"])[2]'))).send_keys("pz", Keys.ENTER)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("50")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()
        sleep(1)

        self.driver.execute_script('window.scrollTo(0,0)')
        self.get_element('//span[@id="select2-idstato-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//input[@class="select2-search__field"])[2]'))).send_keys("In lavorazione", Keys.ENTER)
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@id="link-tab_14"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//span[@id="select2-id_tipo_promemoria-container"]', By.XPATH).click()
        sleep(1)
        
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-search select2-search--dropdown"]//input[@class="select2-search__field"]'))).send_keys("Generico", Keys.ENTER)
        self.get_element('//button[@id="add_promemoria"]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '(//iframe[@class="cke_wysiwyg_frame cke_reset"])[3]'))).click()  
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//iframe[@class="cke_wysiwyg_frame cke_reset"])[3]'))).send_keys("Manutenzione")
        self.get_element('//span[@id="select2-id_segment-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-search select2-search--dropdown"]//input[@class="select2-search__field"]'))).send_keys("Standard attività", Keys.ENTER)
        self.get_element('//div[@class="modal-content"]//button[@class="btn btn-primary"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//button[@class="btn btn-primary btn-sm  "]', By.XPATH).click()
        sleep(1)

        self.get_element('(//button[@class="btn btn-primary"])[3]', By.XPATH).click()
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//tbody//tr[1]//a')))

    def pianificazione_fatturazione(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Contratti")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Manutenzione", Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()
 
        self.get_element('//a[@id="link-tab_26"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//button[@id="pianifica"]', By.XPATH).click()
        sleep(1)

        self.get_element('(//div[@class="nav-tabs-custom"]//a[@class="nav-link"])[2]', By.XPATH).click()
        self.get_element('//button[@id="btn_procedi"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('(//button[@class="btn btn-primary btn-sm "])[1]', By.XPATH).click()
        sleep(1)

        self.get_element('//span[@id="select2-idtipodocumento-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//input[@class="select2-search__field"])[2]'))).send_keys("Fattura immediata di vendita", Keys.ENTER)
        
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Dashboard")
        self.wait_loader() 

        self.get_element('(//div[@id="widget_11"]//div, By.XPATH)[2]').click()
        sleep(1)

        self.get_element('//a[@data-month="2"]', By.XPATH).click()
        sleep(1)

        self.get_element('(//button[@class="btn btn-default btn-sm"])[1]', By.XPATH).click()
        sleep(1)

        self.get_element('//span[@id="select2-idtipodocumento-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//input[@class="select2-search__field"])'))).send_keys("Fattura immediata di vendita", Keys.ENTER)
        
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Contratti")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()
 
        self.get_element('//a[@id="link-tab_26"]', By.XPATH).click()
        self.wait_loader()

        link=wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_26"]//tbody//tr//td[2]'))).text
        self.assertEqual(link, "Fattura num. del 01/01/2025 ( Bozza)")

        self.navigateTo("Contratti")
        self.wait_loader()

        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)
        
    def rinnovi(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Contratti")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//span[@id="select2-idstato-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//input[@class="select2-search__field"])[2]'))).send_keys("Bozza", Keys.ENTER)
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()
         
        self.get_element('//a[@id="link-tab_23"]', By.XPATH).click()

        self.get_element('(//label[@for="rinnovabile"])[2]', By.XPATH).click()
        self.get_element('//div[@id="tab_23"]//button[@type="submit"]', By.XPATH).click()
        self.wait_loader()


    def cambia_stato(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Contratti")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Numero"]/input'))).send_keys("2", Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td', By.XPATH).click()

        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()  
        self.get_element('//a[@data-op="cambia_stato"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//span[@id="select2-id_stato-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("In lavorazione")
        sleep(2)

        self.get_element('//ul[@id="select2-id_stato-results"]', By.XPATH).click() 
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click() 
        self.wait_loader()

        stato=self.get_element('//tbody//tr//td[5]', By.XPATH).text
        self.assertEqual(stato,"In lavorazione") 

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)


    def fattura_contratti(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Contratti")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Numero"]/input'))).send_keys("2", Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        self.get_element('//a[@data-op="crea_fattura"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//span[@id="select2-raggruppamento-container"]', By.XPATH).click()   
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click() 
        self.wait_loader()
        
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        tipo=self.get_element('//tbody//tr[1]//td[5]', By.XPATH).text
        self.assertEqual(tipo, "Fattura immediata di vendita")

        self.get_element('//tbody//tr[2]//td[4]', By.XPATH).click()    
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask "]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        self.wait_loader()

        self.navigateTo("Contratti")
        self.wait_loader()

        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)


    def rinnova_contratti(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Contratti")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Numero"]/input'))).send_keys("1", Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="data_accettazione"]'))).send_keys("01/01/2025")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="data_conclusione"]'))).send_keys("31/12/2025")
        self.get_element('//span[@id="select2-idstato-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//input[@class="select2-search__field"])[2]'))).send_keys("Accettato")
        sleep(1)

        self.get_element('//ul[@id="select2-idstato-results"]', By.XPATH).click()
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Contratti")
        self.wait_loader()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()  
        self.get_element('//a[@data-op="renew_contratto"]', By.XPATH).click() 
        sleep(2)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('(//i[@class="deleteicon fa fa-times"])[1]', By.XPATH).click() 
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Numero"]/input'))).send_keys("3", Keys.ENTER)
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//tbody//tr//td[2]'))) 
        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()  
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        self.wait_loader()

        self.get_element('(//i[@class="deleteicon fa fa-times"])[1]', By.XPATH).click() 
        sleep(1)
