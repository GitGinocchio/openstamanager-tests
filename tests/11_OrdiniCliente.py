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



class OrdiniCliente(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Vendite")


    def test_creazione_ordine_cliente(self):
        # Crea una nuovo ordine cliente per il cliente "Cliente". *Required*
        importi = RowManager.list()
        self.creazione_ordine_cliente("Cliente", importi[0])
        self.creazione_ordine_cliente("Cliente", importi[0])

        # Modifica ordine cliente
        self.modifica_ordine_cliente()

        # Cancellazione ordine cliente
        self.elimina_ordine_cliente()

        # Verifica ordine cliente
        self.verifica_ordine_cliente()

        # Plugin consuntivi
        self.consuntivi()

        # Cambia stato (Azioni di gruppo)
        self.cambia_stato()

        # Fattura ordini cliente (Azioni di gruppo)
        self.fattura_ordini_clienti()


    def creazione_ordine_cliente(self, cliente: str, file_importi: str):
        self.navigateTo("Ordini cliente")
        self.wait_loader() 

        # Crea rdine
        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        select = self.input(modal, 'Cliente')
        select.setByText(cliente)
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

        row_manager = RowManager(self)
        self.valori=row_manager.compile(file_importi)

    def modifica_ordine_cliente(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Ordini cliente")
        self.wait_loader()

        filter_input = self.find_filter_input("Numero")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("1", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        self.scroll_to_top()

        results = self.get_select_search_results("Stato*", "Accettato")
        if len(results) > 0: results[0].click()

        self.get_element('save').click()

        # Estrazione totali righe
        sconto = self.get_element('//div[@id="righe"]//tbody[2]//tr[2]//td[2]', By.XPATH).text
        totale_imponibile = self.get_element('//div[@id="righe"]//tbody[2]//tr[3]//td[2]', By.XPATH).text
        iva = self.get_element('//div[@id="righe"]//tbody[2]//tr[4]//td[2]', By.XPATH).text
        totale = self.get_element('//div[@id="tab_0"]//div[@id="righe"]//tbody[2]//tr[5]//td[2]', By.XPATH).text

        self.assertEqual(sconto, (self.valori["Sconto/maggiorazione"]+ ' €'))
        self.assertEqual(totale_imponibile, (self.valori["Totale imponibile"]+ ' €'))
        self.assertEqual(iva, (self.valori["IVA"] + ' €'))
        self.assertEqual(totale, (self.valori["Totale documento"] + ' €'))

        self.navigateTo("Ordini cliente")
        self.wait_loader()  

        self.get_element('//th[@id="th_Numero"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def elimina_ordine_cliente(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Ordini cliente")
        self.wait_loader()

        filter_input = self.find_filter_input("Numero")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("2", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        self.wait_loader()

        self.get_element('//th[@id="th_Numero"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        
    def verifica_ordine_cliente(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Ordini cliente")
        self.wait_loader()  

        # Verifica elemento modificato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_icon_title_Stato"]/input'))).send_keys("Accettato", Keys.ENTER)
        sleep(1)

        self.wait_for_search_results()

        modificato=self.driver.find_element(By.XPATH,'//tbody//tr//td[7]').text
        self.assertEqual("Accettato",modificato)
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

        # Verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Numero"]/input'))).send_keys("2", Keys.ENTER)
        sleep(1)

        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)
        self.get_element('//th[@id="th_Numero"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def consuntivi(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Ordini cliente")
        self.wait_loader()

        filter_input = self.find_filter_input("Numero")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("1", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@id="link-tab_29"]', By.XPATH).click()
        budget=self.get_element('//div[@id="tab_29"]//span[@class="text-success"]', By.XPATH).text

        self.assertEqual(budget, "+ 264,80 €")

        self.navigateTo("Ordini cliente")
        self.wait_loader()

        self.get_element('//th[@id="th_Numero"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def cambia_stato(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Ordini cliente")
        self.wait_loader()

        filter_input = self.find_filter_input("Numero")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("01", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td', By.XPATH).click() 
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        self.get_element('//a[@data-op="change_status"]', By.XPATH).click()

        self.wait_swal2_popup()

        results = self.get_select_search_results("Stato*", "Accettato")
        if len(results) > 0: results[0].click()

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click() 
        self.wait_loader()

        stato=self.get_element('(//tbody//tr[1]//td[7]//span)[2]', By.XPATH).text 
        self.assertEqual(stato, "Accettato")

        self.get_element('//th[@id="th_Numero"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def fattura_ordini_clienti(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Ordini cliente")
        self.wait_loader()

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

        tipo=self.get_element('//tbody//tr[3]//td[5]', By.XPATH).text
        self.assertEqual(tipo, "Fattura immediata di vendita") 

        self.get_element('//tbody//tr//td[4]', By.XPATH).click()
        self.wait_loader()
    
        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()