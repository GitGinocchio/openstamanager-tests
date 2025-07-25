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
        #self.creazione_contratto("Contratto di Prova da Modificare", "Cliente", importi[0])

        # Duplica un contratto *Required*
        #self.duplica_contratto()

        # Modifica Contratto
        #self.modifica_contratto("Contratto di Prova")

        # Cancellazione contratto
        #self.elimina_contratto()     

        # Verifica contratto
        #self.verifica_contratto()

        # Plugin contratti del cliente da Anagrafiche
        #self.contratti_del_cliente()

        # Plugin consuntivo
        #self.consuntivo()
        
        # Plugin pianificazione attività
        #self.pianificazione_attivita()

        # Plugin pianificazione fatturazione
        #self.pianificazione_fatturazione()

        # Plugin rinnovi
        #self.rinnovi()

        # Cambia stato (Azioni di gruppo)
        #self.cambia_stato()

        # Fattura contratti (Azioni di gruppo)
        #self.fattura_contratti()

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
        self.wait_loader()
        
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="pulsanti"]//button[@class="btn btn-primary ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-primary"]'))).click()
        self.wait_loader()

        self.wait_swal2_popup()

        element = self.get_element('//input[@id="nome"]', By.XPATH)
        element.clear()
        element.send_keys("Contratto di Prova da Eliminare")

        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

    def modifica_contratto(self, modifica : str):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Contratti")
        self.wait_loader()

        filter_input = self.find_filter_input("Nome")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys('Contratto di Prova da Modificare', Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        self.scroll_to_top()
        
        element=self.get_element('//input[@id="nome"]', By.XPATH)
        element.click()
        element.clear()
        element.send_keys(modifica)

        self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

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

    def elimina_contratto(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Contratti")
        self.wait_loader()  

        filter_input = self.find_filter_input("Nome")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys('Contratto di Prova da Eliminare', Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        self.wait_loader()

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def verifica_contratto(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Contratti")
        self.wait_loader()  

        # Verifica elemento modificato
        filter_input = self.find_filter_input("Nome")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("Contratto di Prova", Keys.ENTER)

        self.wait_for_search_results()

        modificato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[3]').text
        self.assertEqual("Contratto di Prova",modificato)
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        self.wait_loader()

        # Verifica elemento eliminato
        filter_input = self.find_filter_input("Nome")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("Contratto di Prova da Eliminare", Keys.ENTER)

        self.wait_for_search_results()

        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)
        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def contratti_del_cliente(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Anagrafiche")
        self.wait_loader() 

        filter_input = self.find_filter_input("Ragione sociale")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("Cliente", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader() 

        self.get_element('//a[@id="link-tab_35"]', By.XPATH).click()
        self.wait_loader()
        
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_35"]//tbody//tr/td[2]')))

    def consuntivo(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Vendite")
        self.navigateTo("Contratti")
        self.wait_loader()

        filter_input = self.find_filter_input("Nome")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("Contratto di Prova", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr/td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@id="link-tab_13"]', By.XPATH).click()

        # Dov'e' questo elemento?
        #budget=self.get_element('//div[@id="tab_13"]//span[@class="text-success"]', By.XPATH).text
        #self.assertEqual(budget, "+ 264,80 €")

        self.navigateTo("Contratti")
        self.wait_loader()

        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def pianificazione_attivita(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Contratti")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        nome_input = self.get_input("Nome*", context=modal)
        nome_input.click()
        nome_input.clear()
        nome_input.send_keys("Manutenzione")

        results = self.get_select_search_results("Cliente*", "Cliente", context=modal)
        if len(results) > 0: results[0].click()

        accettazione = self.get_input("Data accettazione", modal)
        accettazione.click()
        accettazione.clear()
        accettazione.send_keys("01/01/2025")

        accettazione = self.get_input("Data conclusione", modal)
        accettazione.click()
        accettazione.clear()
        accettazione.send_keys("01/01/2025")
        
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click()
        self.wait_loader()

        textarea = self.get_element("descrizione_riga")
        textarea.click()
        textarea.clear()
        textarea.send_keys("Manutenzione")

        quota = self.get_input("Q.tà*")
        quota.click()
        quota.clear()
        quota.send_keys("12")

        results = self.get_select_search_results("Unità di misura", "pz")
        if len(results) > 0: results[0].click()

        prezzo_unitario = self.get_input("Prezzo unitario di vendita*")
        prezzo_unitario.click()
        prezzo_unitario.clear()
        prezzo_unitario.send_keys("50")

        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()
        self.wait_loader()

        self.scroll_to_top()
        results = self.get_select_search_results("Stato*", "In lavorazione")
        if len(results) > 0: results[0].click()

        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@id="link-tab_14"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('select2-id_tipo_promemoria-container').click()
        sleep(1)
        select = self.get_element('//span[@class="select2-search select2-search--dropdown"]//input[@class="select2-search__field"]', By.XPATH)
        select.click()
        select.clear()
        select.send_keys("Generico", Keys.ENTER)

        selected = self.get_element('//li[@class="select2-results__option select2-results__option--highlighted"]', By.XPATH)
        selected.click()

        self.get_element('//button[@id="add_promemoria"]', By.XPATH).click()
        self.wait_loader()

        element = self.get_element('(//iframe[@class="cke_wysiwyg_frame cke_reset"])[3]', By.XPATH)
        element.click()
        element.send_keys("Manutenzione")

        results = self.get_select_search_results("Sezionale*", "Standard attività")
        if len(results) > 0: results[0].click()

        self.scroll_to_bottom()

        request_xpath = '(//iframe[@class="cke_wysiwyg_frame cke_reset"])[3]'
        frame = self.get_element(request_xpath, By.XPATH)

        # Entra nel contesto dell'iframe
        self.driver.switch_to.frame(frame)

        body = self.driver.find_element(By.TAG_NAME, 'p')
        body.click()
        body.send_keys('Test')

        # Esce dal contesto dell'iframe
        self.driver.switch_to.default_content()

        self.get_element('(//button[@class="btn btn-primary"])[3]', By.XPATH).click()
        self.wait_loader()

    def pianificazione_fatturazione(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Contratti")
        self.wait_loader()

        filter_input = self.find_filter_input("Nome")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("Manutenzione", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()
 
        self.get_element('//a[@id="link-tab_26"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//button[@id="pianifica"]', By.XPATH).click()

        self.get_element('(//div[@class="nav-tabs-custom"]//a[@class="nav-link"])[2]', By.XPATH).click()
        self.get_element('//button[@id="btn_procedi"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('(//button[@class="btn btn-primary btn-sm "])[1]', By.XPATH).click()
        modal = self.wait_modal()

        results = self.get_select_search_results("Tipo di fattura*", "Fattura immediata di vendita")
        if len(results) > 0: results[0].click()

        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Dashboard")
        self.wait_loader() 

        self.get_element('(//div[@id="widget_11"]//div)[2]', By.XPATH).click()
        sleep(1)

        self.get_element('//a[@data-month="2"]', By.XPATH).click()
        sleep(1)

        self.get_element('(//button[@class="btn btn-default btn-sm "])[1]', By.XPATH).click()
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
        
    def rinnovi(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Contratti")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        self.scroll_to_top()

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

        filter_input = self.find_filter_input("Numero")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("2", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td', By.XPATH).click()

        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()  
        self.get_element('//a[@data-op="change_status"]', By.XPATH).click() 
        self.wait_swal2_popup()

        self.get_element('//span[@id="select2-id_stato-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("In lavorazione")
        sleep(2)

        self.get_element('//ul[@id="select2-id_stato-results"]', By.XPATH).click() 
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click() 
        self.wait_loader()

        stato=self.get_element('//tbody//tr//td[5]', By.XPATH).text
        #self.assertEqual(stato,"In lavorazione") 

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()


    def fattura_contratti(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Contratti")
        self.wait_loader()

        filter_input = self.find_filter_input("Numero")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("2", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        self.get_element('//a[@data-op="create_invoice"]', By.XPATH).click()
        self.wait_swal2_popup()

        results = self.get_select_search_results("Raggruppa per*", "Cliente")
        if len(results) > 0: results[0].click()

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


    def rinnova_contratti(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Contratti")
        self.wait_loader()

        filter_input = self.find_filter_input("Numero")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("1", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        accettazione = self.get_element("data_accettazione")
        accettazione.click()
        accettazione.send_keys("01/01/2025")

        accettazione = self.get_element("data_conclusione")
        accettazione.click()
        accettazione.send_keys("31/12/2025")

        results = self.get_select_search_results("Stato*", "Accettato")
        if len(results) > 0: results[0].click()

        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Contratti")
        self.wait_loader()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()  
        self.get_element('//a[@data-op="renew_contract"]', By.XPATH).click() 
        self.wait_swal2_popup()

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('(//i[@class="deleteicon fa fa-times"])[1]', By.XPATH).click() 

        filter_input = self.find_filter_input("Numero")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("3", Keys.ENTER)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()  
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        self.wait_loader()