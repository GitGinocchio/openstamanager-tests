from common.Test import Test, get_html
from common.RowManager import RowManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DdtUscita(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Magazzino")


    def test_creazione_ddt_uscita(self):
        # Crea un nuovo ddt al cliente "Cliente". *Required*
        importi = RowManager.list()
        self.creazione_ddt_uscita("Cliente", "2", importi[0])

        # Duplica ddt uscita
        self.duplica_ddt_uscita()

        # Modifica Ddt
        self.modifica_ddt("Evaso")
        
        # Cancellazione Ddt
        self.elimina_ddt()

        # Verifica DDT
        self.verifica_ddt()

        # Verifica plugin DDT del cliente da Anagrafiche
        self.ddt_del_cliente()

        # Cambia stato (Azioni di gruppo)
        self.cambia_stato()

        # Fattura ddt in uscita (Azioni di gruppo)
        self.fattura_ddt_uscita()

        self.duplica_ddt_uscita()

        # Elimina selezionati (Azioni di gruppo)
        self.elimina_selezionati()

    def creazione_ddt_uscita(self, cliente: str, causale: str, file_importi: str):
        self.navigateTo("Ddt in uscita")

        # Crea DDT
        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        select = self.input(modal, 'Destinatario')
        select.setByText(cliente)
        select = self.input(modal, 'Causale trasporto')
        select.setByIndex(causale)
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

        row_manager = RowManager(self)
        self.valori=row_manager.compile(file_importi)

    def duplica_ddt_uscita(self):
        self.navigateTo("Ddt in uscita")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()  
        self.wait_loader()

        self.get_element('//button[@class="btn btn-primary ask"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-primary"]', By.XPATH).click()

    def modifica_ddt(self, modifica):
        self.navigateTo("Ddt in uscita")
        self.wait_loader()

        filter_input = self.find_filter_input("Numero")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("01", Keys.ENTER)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        self.scroll_to_top()

        results = self.get_select_search_results("Stato*", "Evaso")
        if len(results) > 0: results[0].click()

        self.get_element("save").click()

        # Estrazione totali righe
        sconto = self.get_element('//div[@id="righe"]//tbody[2]//tr[2]//td[2]', By.XPATH).text
        totale_imponibile = self.get_element('//div[@id="righe"]//tbody[2]//tr[3]//td[2]', By.XPATH).text
        iva = self.get_element('//div[@id="righe"]//tbody[2]//tr[4]//td[2]', By.XPATH).text
        totale = self.get_element('//div[@id="tab_0"]//div[@id="righe"]//tbody[2]//tr[5]//td[2]', By.XPATH).text

        self.assertEqual(sconto, (self.valori["Sconto/maggiorazione"]+ ' €'))
        self.assertEqual(totale_imponibile, (self.valori["Totale imponibile"]+ ' €'))
        self.assertEqual(iva, (self.valori["IVA"] + ' €'))
        self.assertEqual(totale, (self.valori["Totale documento"] + ' €'))

        self.navigateTo("Ddt in uscita")
        self.wait_loader()    

        self.get_element('//th[@id="th_Numero"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def elimina_ddt(self):
        self.navigateTo("Ddt in uscita")
        self.wait_loader()    
        
        filter_input = self.find_filter_input("Numero")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("02", Keys.ENTER)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//div[@id="tab_0"]//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()

        self.wait_loader()

        self.get_element('//th[@id="th_Numero"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        
    def verifica_ddt(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Ddt in uscita")
        self.wait_loader()    

        # Verifica elemento modificato
        filter_input = self.find_filter_input("Numero")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("01", Keys.ENTER)

        modificato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[11]').text
        self.assertEqual("Evaso",modificato)
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()

        # Verifica elemento eliminato
        filter_input = self.find_filter_input("Numero")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("02", Keys.ENTER)

        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)

        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def ddt_del_cliente(self):
        self.navigateTo("Anagrafiche")
        self.wait_loader() 
 
        filter_input = self.find_filter_input("Ragione sociale")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("Cliente", Keys.ENTER)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()

        self.get_element("link-tab_17").click()

        self.get_element('//tbody//tr[10]//td[2]', By.XPATH).click()
        self.wait_loader()

    def cambia_stato(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Ddt in uscita")
        self.wait_loader() 

        filter_input = self.find_filter_input("Numero")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("01", Keys.ENTER)

        self.get_element('//tbody//tr//td', By.XPATH).click() 
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()
        self.get_element('//a[@data-op="change_status"]', By.XPATH).click() 

        results = self.get_select_search_results("Stato*", "Evaso")
        if len(results) > 0: results[0].click()

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click() 
        self.wait_loader()

        stato=self.get_element('(//tr[1]//td[11]//span, By.XPATH)[2]').text
        self.assertEqual(stato, "Evaso")    
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def fattura_ddt_uscita(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Ddt in uscita")
        self.wait_loader()

        filter_input = self.find_filter_input("Numero")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("01", Keys.ENTER)
        self.wait_for_search_results()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        self.get_element('//a[@data-op="create_invoice"]', By.XPATH).click()  

        results = self.get_select_search_results("Raggruppa per*", "Cliente")
        if len(results) > 0: results[0].click()

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()  
        self.wait_loader()

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        tipo=self.get_element('//tbody//tr[3]//td[4]', By.XPATH).text  
        self.assertEqual(tipo, "Cliente")

        self.get_element('//tbody//tr[3]//td[5]', By.XPATH).click()
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask "]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        self.wait_loader()

        self.expandSidebar("Magazzino")
        self.navigateTo("Ddt in uscita")
        self.wait_loader()

        self.get_element('//tbody//tr//td', By.XPATH).click()   
        self.get_element('//th[@id="th_Numero"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click() 

    def elimina_selezionati(self):
        self.navigateTo("Ddt in uscita")
        self.wait_loader()

        self.get_element('//tbody//tr//td', By.XPATH).click()   
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        self.get_element('//a[@data-op="delete_bulk"]', By.XPATH).click()   

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()   
        self.wait_loader()

        filter_input = self.find_filter_input("Numero")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("02", Keys.ENTER)

        scritta=self.get_element('//tbody//tr', By.XPATH).text
        self.assertEqual(scritta, "La ricerca non ha portato alcun risultato.") 

        self.get_element('//th[@id="th_Numero"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click() 