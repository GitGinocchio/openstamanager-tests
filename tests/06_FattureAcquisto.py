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

class FattureAcquisto(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Acquisti")

    def test_creazione_fattura_acquisto(self):
        # Crea una nuova fattura *Required*
        importi = RowManager.list()
        self.creazione_fattura_acquisto("Fornitore", "1", "1", importi[0])
        self.modifica_fattura_acquisto("Emessa")
        self.controllo_fattura_acquisto()
        self.elimina_documento()
        self.verifica_fattura_acquisto()
        self.verifica_xml_autofattura(importi[0], "1")
        self.registrazioni()
        self.movimenti_contabili()
        self.cambia_sezionale()
        self.duplica_selezionati()
        self.registrazione_contabile()
        self.elimina_selezionati()

    def creazione_fattura_acquisto(self, fornitore: str, numero: str, pagamento: str, file_importi: str):
        self.navigateTo("Fatture di acquisto")
        self.wait_loader()

        # Crea fattura
        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        self.input(modal, 'N. fattura del fornitore').setValue(numero)
        select = self.input(modal, 'Fornitore')
        select.setByText(fornitore)
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

        select = self.input(self.get_element('//div[@id="tab_0"]', By.XPATH), 'Pagamento')
        select.setByIndex(pagamento)

        row_manager = RowManager(self)
        self.valori=row_manager.compile(file_importi)

    def modifica_fattura_acquisto(self, modifica=str):
        self.navigateTo("Fatture di acquisto")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()
        
        self.input(None,'Stato*').setByText(modifica)
        self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

    def controllo_fattura_acquisto(self):
        self.navigateTo("Fatture di acquisto")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()
        
        # Estrazione totali righe
        sconto = self.get_element('//div[@id="righe"]//tbody[2]//tr[2]//td[2]', By.XPATH).text
        totale_imponibile = self.get_element('//div[@id="righe"]//tbody[2]//tr[3]//td[2]', By.XPATH).text
        iva = self.get_element('//div[@id="righe"]//tbody[2]//tr[2]//td[2]', By.XPATH).text
        totale = self.get_element('//div[@id="righe"]//tbody[2]//tr[3]//td[2]', By.XPATH).text

        self.assertEqual(sconto, self.valori["Sconto/maggiorazione"] + ' €')
        self.assertEqual(totale_imponibile, self.valori["Totale imponibile"]+ ' €')
        self.assertEqual(iva, self.valori["IVA"] + ' €')
        self.assertEqual(totale, self.valori["Totale documento"] + ' €')

        # Controllo Scadenzario
        scadenza_fattura = self.get_element('//div[@id="tab_0"]//strong[text()="Scadenze"]/ancestor::div[1]//following-sibling::p[2]', By.XPATH).text
        self.assertEqual(totale, scadenza_fattura[12:21])
        
        self.driver.execute_script('$("a").removeAttr("target")')
        self.get_element('//div[@id="tab_0"]//strong[text()="Scadenze"]/ancestor::div[1]//following-sibling::a', By.XPATH).click()
        self.wait_loader()

        totale = '-'+ totale
        scadenza_scadenzario = (self.get_element('//div[@id="tab_0"]//td[@id="totale_utente"]', By.XPATH).text + ' €')
        self.assertEqual(totale, scadenza_scadenzario)

        self.expandSidebar("Acquisti")
        self.navigateTo("Fatture di acquisto")

        self.wait_loader()

        # Estrazione Totale widgets
        widget_fatturato = self.get_element('(//span[@class="info-box-number"])[1]', By.XPATH).text
        widget_crediti = self.get_element('(//span[@class="info-box-number"])[2]', By.XPATH).text
        widget_crediti='-'+widget_crediti

        # Confronto i due valori
        self.assertEqual(totale_imponibile, widget_fatturato)
        self.assertEqual(totale, widget_crediti)

        # Estrazione valori Piano dei conti
        self.expandSidebar("Contabilità")
        self.navigateTo("Piano dei conti")
        self.wait_loader()

        # Clicca sulla + e aspetta che si espanda
        self.open_piano_conti_section("Costi merci c/acquisto")
        self.wait_loader()

        self.open_piano_conti_section("Costi merci c/acquisto di rivendita")
        self.wait_loader()

        # Ottiene il testo
        conto_costi = self.get_element('//*[@id="conto_55"]//*[@class="text-right"]', By.XPATH).text

        # ---

        # Scrolla verso il basso
        self.scroll_to_bottom()

        self.open_piano_conti_section("240 Debiti fornitori e debiti diversi")
        self.wait_loader()
        #self.wait_for_visibility("conto2_8")

        self.scroll_to_bottom()

        # Attualmente trovo questo movimento ma non è all'interno del conto 2-8
        #self.get_element('//*[@id="movimenti-122"]//*[@class="fa fa-plus"]', By.XPATH).click()
        #self.wait_for_visibility("movimenti-122")

        # Penso che si volesse cercare all'interno del conto 2-8 la sezione Fornitore Estero
        fornitore_section = self.open_piano_conti_section("Fornitore Estero")
        self.wait_loader()

        conto_fornitore = self.get_element('//*[@class="text-right"]', By.XPATH, context=fornitore_section).text
        conto_fornitore='-'+conto_fornitore

        self.open_piano_conti_section("Conti transitori")
        self.wait_loader()

        iva_acquisti = self.open_piano_conti_section("Iva su acquisti")
        self.wait_loader()

        conto_iva = self.get_element('//*[@class="text-right"]', By.XPATH, iva_acquisti).text

        self.assertEqual(totale_imponibile, conto_costi)
        self.assertEqual(totale, conto_fornitore)
        self.assertEqual(iva, conto_iva)

    def elimina_documento(self):
        self.navigateTo("Fatture di acquisto")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()

        self.wait_loader()

        self.get_element('//div[@id="tab_0"]//a[@class="btn btn-danger ask "]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

    def verifica_fattura_acquisto(self):
        self.navigateTo("Fatture di acquisto")
        self.wait_loader()

        # Verifica elemento eliminato
        filter_input = self.find_filter_input("Numero")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("1", Keys.ENTER)
        self.wait_for_search_results()

        eliminato = self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("Nessun dato presente nella tabella",eliminato)

        self.get_element('(//i[@class="deleteicon fa fa-times"])[1]', By.XPATH).click() 

    def verifica_xml_autofattura(self, file_importi: str, pagamento: str):
        # Creazione fattura di acquisto estera
        self.navigateTo("Fatture di acquisto")
        self.wait_loader()  

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        results = self.get_select_search_results("Fornitore", "Fornitore Estero")
        if len(results) > 0: results[0].click()

        self.input(modal, 'N. fattura del fornitore').setValue("01")
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

        select = self.input(self.get_element('//div[@id="tab_0"]', By.XPATH), 'Pagamento')
        select.setByIndex(pagamento)
        row_manager = RowManager(self)
        row_manager.compile(file_importi)

        self.scroll_to_top()
        self.close_toast_popups()

        results = self.get_select_search_results("Stato*", "Emessa")
        if len(results) > 0: results[0].click()

        self.scroll_to_top()
        
        self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()

        self.wait_loader()

        # Non capisco cosa aspetta se non abbiamo fatto niente
        # Creazione autofattura
        #self.wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="btn btn-primary unblockable dropdown-toggle "]'))).click()
        #self.wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//a[@class="btn dropdown-item bound clickable"]'))).click()
        #self.wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="modal-body"]//span[@class="select2-selection select2-selection--single"]'))).click()
        #self.wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-search select2-search--dropdown"]//input[@type="search"]'))).send_keys("TD17")
        #self.wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//li[@class="select2-results__option select2-results__option--highlighted"]'))).click()
        #self.wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="modal-body"]//button[@type="submit"]'))).click()
        #self.wait_loader()

        # Lo abbiamo appena fatto sopra...

        #self.input(None,'Stato*').setByText("Emessa")
        #self.scroll_to_top()
        #self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()
        #self.wait_loader()

        totale_imponibile = self.get_element('//div[@id="righe"]//tbody[2]//tr[1]//td[2]', By.XPATH).text
        totale = self.get_element('//div[@id="tab_0"]//div[@id="righe"]//tbody[2]//tr[2]//td[2]', By.XPATH).text

        self.assertEqual(totale_imponibile, ('0,00 €'))
        self.assertEqual(totale, ('0,00 €'))

    def registrazioni(self):
        self.navigateTo("Fatture di acquisto")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('link-tab_41').click()
        self.wait_loader()
        
        self.wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_41"]//tr[5]//td[1]'))) 
    
    def movimenti_contabili(self):
        self.navigateTo("Fatture di acquisto")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()


        self.get_element('//a[@id="link-tab_36"]', By.XPATH).click()
        self.get_element('//a[@class="btn btn-info btn-lg"]', By.XPATH).click()
        self.wait_loader()

        avere=self.get_element('//div[@id="tab_36"]//tr//td[4]', By.XPATH).text
        self.assertEqual(avere,"323,06 €")

    def cambia_sezionale(self):
        self.navigateTo("Fatture di acquisto")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        numero_esterno = self.get_element("numero_esterno")
        numero_esterno.click()
        numero_esterno.clear()
        numero_esterno.send_keys("2")

        results = self.get_select_search_results("Fornitore", "Fornitore")
        if len(results) > 0: results[0].click()

        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Fatture di acquisto") 
        self.wait_loader()

        filter_input = self.find_filter_input("Numero")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("2", Keys.ENTER)
        self.wait_for_search_results()

        self.get_element('//tbody//tr//td', By.XPATH).click() 
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        self.get_element('//a[@data-op="change_segment"]', By.XPATH).click()

        results = self.get_select_search_results("Sezionale", "Autofatture")
        if len(results) > 0: results[0].click()

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        self.get_element('//a[@data-op="change_segment"]', By.XPATH).click() 

        results = self.get_select_search_results("Sezionale", "Standard")
        if len(results) > 0: results[0].click()

    def duplica_selezionati(self):
        self.navigateTo("Fatture di acquisto")
        self.wait_loader()

        self.get_element('//tbody//tr//td[1]', By.XPATH).click() 
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()
        self.get_element('//a[@data-op="copy_bulk"]', By.XPATH).click()

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click() 
        self.wait_loader()
    
        self.get_element('elimina').click()  
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()  
        self.wait_loader()

    def registrazione_contabile(self):
        self.navigateTo("Fatture di acquisto")
        self.wait_loader()

        filter_input = self.find_filter_input("Numero")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("2", Keys.ENTER)
        self.wait_for_search_results()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        self.scroll_to_top()

        numero_esterno = self.get_element("numero_esterno")
        numero_esterno.click()
        numero_esterno.clear()
        numero_esterno.send_keys("2")

        results = self.get_select_search_results("Pagamento", "Assegno")
        if len(results) > 0: results[0].click()

        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click()

        descrizione = self.get_element("descrizione_riga")
        descrizione.click()
        descrizione.clear()
        descrizione.send_keys("Prova")

        prezzo_unitario = self.get_element("prezzo_unitario")
        prezzo_unitario.click()
        prezzo_unitario.clear()
        prezzo_unitario.send_keys("1")
  
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() 

        self.scroll_to_top()

        results = self.get_select_search_results("Stato","Emessa")
        if len(results) > 0: results[0].click()

        # in caso il codice sopra non dovesse andare
        #self.get_element('//span[@id="select2-idstatodocumento-container"]', By.XPATH).click() 
        #self.wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Emessa", Keys.ENTER) 
        
        self.get_element('save').click() 
        self.wait_loader()

        self.navigateTo("Fatture di acquisto") 
        self.wait_loader()

        self.get_element('//tbody//tr//td[1]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        self.get_element('//a[@data-op="registrazione_contabile"]', By.XPATH).click()

        # TODO: Selezionare il conto Banca C/C e aggiungere la registrazione contabile

        prezzo=self.get_element('//th[@id="totale_avere"]', By.XPATH).text
        self.assertEqual(prezzo, "1,22 €")

        self.get_element('//button[@class="close"]', By.XPATH).click()

        self.get_element('(//i[@class="deleteicon fa fa-times"])[1]', By.XPATH).click()

    def elimina_selezionati(self):
        self.navigateTo("Fatture di acquisto")
        self.wait_loader()

        filter_input = self.find_filter_input("Numero")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("2", Keys.ENTER)

        self.get_element('//tbody//tr//td', By.XPATH).click() 
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()
        self.get_element('//a[@data-op="delete_bulk"]', By.XPATH).click()

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        scritta=self.get_element('//tbody//tr//td', By.XPATH).text
        self.assertEqual(scritta, "La ricerca non ha portato alcun risultato.")
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()