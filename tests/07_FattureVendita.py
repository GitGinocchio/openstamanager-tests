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

from datetime import datetime, timezone, timedelta
import time

class FattureVendita(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Vendite")

    def test_creazione_fattura_vendita(self):
        # Crea una nuova fattura per il cliente "Cliente". *Required*
        importi = RowManager.list()
        #self.creazione_fattura_vendita("Cliente", importi[0])
        #self.duplica()
        #self.modifica_fattura_vendita("Emessa")
        #self.controllo_fattura_vendita()
        #self.creazione_nota_credito()
        #self.modifica_nota_credito("Emessa")
        #self.controllo_nota_credito()
        #self.controllo_fattura_nota_credito()
        self.elimina_documento()
        self.verifica_fattura_di_vendita()
        self.verifica_xml_fattura_estera(importi[0], "1")
        self.movimenti_contabili()
        self.plugin_movimenti_contabili()
        self.regole_pagamenti()
        self.registrazioni()   
        self.controlla_allegati()
        self.duplica_selezionati()
        self.cambia_sezionale()    
        self.emetti_fatture()
        self.statistiche_vendita()
        self.controlla_fatture_elettroniche()
        self.registrazione_contabile()
        self.genera_fatture_elettroniche()
        self.elimina_selezionati()

    def creazione_fattura_vendita(self, cliente: str, file_importi: str):
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        # Crea una nuova fattura
        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        select = self.input(modal, 'Cliente')
        select.setByText(cliente)
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

        # Da capire a cosa serve RowManager e come usarlo
        row_manager = RowManager(self)
        self.valori=row_manager.compile(file_importi)

    def duplica(self):
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element("//tbody//tr/td", By.XPATH).click()

        self.scroll_to_bottom()

        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()
        self.get_element('//a[@data-op="copy_bulk"]', By.XPATH).click()

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()
        self.wait_loader()

        # Forse deve essere rimossa la fattura duplicata?

    def modifica_fattura_vendita(self, modifica=str):
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        self.scroll_to_top()

        results = self.get_select_search_results("Stato", label_for="idstatodocumento")
        if len(results) > 0: results[1].click()

        data = datetime.now(timezone.utc) + timedelta(weeks=2)

        data_competenza = self.get_input("Data competenza")
        data_competenza.click()
        data_competenza.send_keys(f"{data.day}/{data.month}/{data.year}", Keys.ENTER)

        self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()
        self.wait_loader()
        
    def controllo_fattura_vendita(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
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

        # Controllo Scadenzario
        scadenza_fattura = self.get_element('//div[@id="tab_0"]//strong[text()="Scadenze"]/ancestor::div[1]//following-sibling::p[2]', By.XPATH).text
        self.assertEqual(totale, scadenza_fattura[12:20])
        self.driver.execute_script('$("a").removeAttr("target")')
        self.get_element('//div[@id="tab_0"]//strong[text()="Scadenze"]/ancestor::div[1]//following-sibling::a', By.XPATH).click()
        self.wait_loader()

        scadenza_scadenzario = self.get_element('totale_utente').text + ' €'
        self.assertEqual(totale, scadenza_scadenzario)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()
        
        # Estrazione Totale widgets
        widget_fatturato = self.get_element('(//span[@class="info-box-number"])[1]', By.XPATH).text
        widget_crediti = self.get_element('(//span[@class="info-box-number"])[2]', By.XPATH).text

        # Confronto i due valori
        self.assertEqual(totale_imponibile, widget_fatturato)
        self.assertEqual(totale, widget_crediti)

        # Controllo importi fattura elettronica
        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        self.click_plugin("Fatturazione Elettronica")

        if (generate_btn:=self.exists('//button[@class="btn btn-primary btn-lg"]', By.XPATH)):
            generate_btn.click()

        self.get_element('//div[@class="text-center"]//a[@class="btn btn-info btn-lg "]', By.XPATH).click()

        self.driver.switch_to.window(self.driver.window_handles[1])
        perc_iva_FE = self.get_element('//table[@class="tbFoglio"][3]/tbody/tr[1]/td[2]', By.XPATH).text
        iva_FE = self.get_element('//table[@class="tbFoglio"][3]/tbody/tr[1]/td[6]', By.XPATH).text
        totale_imponibile_FE = self.get_element('//table[@class="tbFoglio"][3]/tbody/tr[1]/td[5]', By.XPATH).text + ' €'
        totale_FE = self.get_element('//table[@class="tbFoglio"][3]/tbody/tr[3]/td[4]', By.XPATH).text + ' €'
        scadenza_FE = self.get_element('//table[@class="tbFoglio"][4]/tbody/tr[1]/td[4]', By.XPATH).text + ' €'

        self.assertEqual('22,00', perc_iva_FE)
        self.assertEqual((self.valori["IVA"]), iva_FE)
        self.assertEqual((self.valori["Totale imponibile"]+ ' €'), totale_imponibile_FE)
        self.assertEqual((self.valori["Totale documento"] + ' €'), totale_FE)
        self.assertEqual((self.valori["Totale documento"] + ' €'), scadenza_FE)

        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.close()

        # Estrazione valori Piano dei conti
        super().setUp()
        self.expandSidebar("Contabilità")
        self.navigateTo("Piano dei conti")
        self.wait_loader()

        self.open_piano_conti_section("Ricavi").click()
        self.wait_loader()

        ricavi = self.open_piano_conti_section("Ricavi merci c/to vendite")
        self.wait_loader()
  
        conto_ricavi = self.get_element('//*[@class="text-right"]', By.XPATH, ricavi).text

        crediti = self.open_piano_conti_section("Crediti clienti e crediti diversi")

        cliente_section = self.open_piano_conti_section("Cliente")
        self.wait_loader()

        conto_cliente = self.get_element('//*[@class="text-right"]', By.XPATH, cliente_section).text

        conti_transitori = self.open_piano_conti_section("Conti transitori")
        iva_su_vendite = self.open_piano_conti_section("Iva su vendite")

        conto_iva = self.get_element('//*[@class="text-right"]', By.XPATH, iva_su_vendite).text

        self.assertEqual(totale_imponibile, conto_ricavi)
        self.assertEqual(totale, conto_cliente)
        self.assertEqual(iva, conto_iva)

        self.expandSidebar("Vendite")

    def creazione_nota_credito(self):
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()
        
        self.get_element('//button[@class="btn btn-primary unblockable dropdown-toggle "]', By.XPATH).click()
        self.get_element('//a[@class="btn dropdown-item bound clickable"]', By.XPATH).click()
        modal = self.wait_modal()

        self.get_element('//button[@id="submit_btn"]', By.XPATH).click()
        self.wait_loader()

    def modifica_nota_credito(self, modifica=str):
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr[3]//td[2]', By.XPATH).click()
        self.wait_loader()

        results = self.get_select_search_results("Stato*", modifica)
        if len(results) > 0: results[0].click()
        self.scroll_to_top()

        self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

    def controllo_nota_credito(self):
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//td[@class="bound clickable"]', By.XPATH).click()
        self.wait_loader()

        totale_imponibile = self.get_element('//div[@id="righe"]//tbody[2]//tr[3]//td[2]', By.XPATH).text
        totale_imponibile = '-'+totale_imponibile
        iva = self.get_element('//div[@id="righe"]//tbody[2]//tr[4]//td[2]', By.XPATH).text
        totale = self.get_element('//div[@id="tab_0"]//div[@id="righe"]//tbody[2]//tr[5]//td[2]', By.XPATH).text

        # Controllo Scadenzario
        scadenza_fattura = self.get_element('//div[@id="tab_0"]//strong[text()="Scadenze"]/ancestor::div[1]//following-sibling::p[2]', By.XPATH).text
        self.assertEqual(totale, scadenza_fattura[12:21])
        self.get_element('//div[@class="btn-group pull-right"]', By.XPATH).click()

        totale = '-'+totale
        self.driver.switch_to.window(self.driver.window_handles[1])
        scadenza_scadenzario = self.get_element('//div[@id="tab_0"]//td[@id="totale_utente"]', By.XPATH).text
        scadenza_scadenzario = scadenza_scadenzario +' €'
        self.assertEqual(totale, scadenza_scadenzario)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

        # Torno alla tabella delle Fatture
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        # Controllo importi fattura elettronica
        self.get_element('//div[@id="tab_0"]//tbody//tr[1]//td[2]', By.XPATH).click()
        self.wait_loader()

        # TODO: da sostituire con click_plugin
        self.get_element('//a[@id="link-tab_18"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//form[@id="form-xml"]/following-sibling::a[1]', By.XPATH).click()

        self.driver.switch_to.window(self.driver.window_handles[1])
        perc_iva_FE = self.get_element('//table[@class="tbFoglio"][3]/tbody/tr[1]/td[2]', By.XPATH).text
        iva_FE = self.get_element('//table[@class="tbFoglio"][3]/tbody/tr[1]/td[6]', By.XPATH).text
        iva_FE = iva_FE+' €'
        totale_imponibile_FE = self.get_element('//table[@class="tbFoglio"][3]/tbody/tr[1]/td[5]', By.XPATH).text
        totale_imponibile_FE = '-'+totale_imponibile_FE+' €'
        totale_FE = self.get_element('//table[@class="tbFoglio"][3]/tbody/tr[3]/td[4]', By.XPATH).text
        totale_FE = '-'+totale_FE+' €'
        scadenza_FE = self.get_element('//table[@class="tbFoglio"][4]/tbody/tr[1]/td[4]', By.XPATH).text
        scadenza_FE = '-'+scadenza_FE+' €'
        self.assertEqual('22,00', perc_iva_FE)
        self.assertEqual(iva, iva_FE)
        self.assertEqual(totale_imponibile, totale_imponibile_FE)
        self.assertEqual(totale, totale_FE)
        self.assertEqual(totale, scadenza_FE)
        iva = '-' + iva
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.close()
        
        # Estrazione valori Piano dei conti
        super().setUp()
        self.expandSidebar("Contabilità")
        self.navigateTo("Piano dei conti")
        self.wait_loader()

        self.open_piano_conti_section("Ricavi").click()
        section = self.open_piano_conti_section("Ricavi merci c/to vendite")
        section.click()

        conto_ricavi = self.get_element('//*[@class="text-right"]', By.XPATH, section).text

        self.scroll_to_bottom()

        self.open_piano_conti_section("Crediti clienti e crediti diversi").click()
        section = self.open_piano_conti_section("Cliente").click()
        conto_cliente = self.get_element('//*[@class="text-right"]', By.XPATH, section).text

        self.open_piano_conti_section("Conti transitori").click()
        section = self.open_piano_conti_section("Iva su vendite").click()

        conto_iva = self.get_element('//*[@class="text-right"]', By.XPATH, section).text
        conto_iva= '-'+ conto_iva
        conto_ricavi = '-' + conto_ricavi
        conto_cliente = '-' + conto_cliente
        self.assertEqual(totale_imponibile, conto_ricavi)
        self.assertEqual(totale, conto_cliente)
        self.assertEqual(iva, conto_iva)

    def controllo_fattura_nota_credito(self):
        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        fattura=self.get_element('//tbody//tr[2]//td[6]', By.XPATH).text
        notacredito=self.get_element('//tbody//tr[1]//td[6]', By.XPATH).text
        fattura='-'+ fattura
        self.assertEqual(fattura,notacredito)

    def elimina_documento(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr[3]//td[2]', By.XPATH).click()
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask "]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        self.wait_loader()

    def verifica_fattura_di_vendita(self):
        wait = WebDriverWait(self.driver, 20)

        #Creazione fattura di acquisto estera
        self.expandSidebar("Acquisti")
        self.navigateTo("Fatture di acquisto")
        self.wait_loader()  

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        results = self.get_select_search_results("Fornitore*", "Fornitore")
        if len(results) > 0: results[0].click()

        n_fattura_input = self.get_input("N. fattura del fornitore*", modal)
        n_fattura_input.click()
        n_fattura_input.clear()
        n_fattura_input.send_keys("02", Keys.ENTER)

        results = self.get_select_search_results("Tipo documento*")
        if len(results) > 0: results[0].click()

        results = self.get_select_search_results("Sezionale*")
        if len(results) > 0: results[0].click()

        # Submit
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

    def verifica_xml_fattura_estera(self, file_importi: str, pagamento: str):
        wait = WebDriverWait(self.driver, 20)

        # Inserisco le righe

        self.scroll_to_top()
        results = self.get_select_search_results("Pagamento", pagamento, label_for="idpagamento")
        if len(results) > 0: results[0].click()

        row_manager = RowManager(self)
        row_manager.compile(file_importi)

        self.close_toast_popups()
        self.get_element('(//a[@title="Modifica riga"])[1]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@id="select2-idiva-container"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('Non imponibile')
        wait.until(EC.visibility_of_element_located((By.XPATH, '//li[@class="select2-results__option select2-results__option--highlighted"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@onclick="submitForm()"]'))).click()
        
        self.wait_loader()

        self.close_toast_popups()
        self.get_element('(//a[@title="Modifica riga"])[2]', By.XPATH).click()  
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@id="select2-idiva-container"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('Non imponibile')
        wait.until(EC.visibility_of_element_located((By.XPATH, '//li[@class="select2-results__option select2-results__option--highlighted"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@onclick="submitForm()"]'))).click()
       
        self.wait_loader()

        self.close_toast_popups()
        self.get_element('(//a[@title="Modifica riga"])[3]', By.XPATH).click()  
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@id="select2-idiva-container"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('Non imponibile')
        wait.until(EC.visibility_of_element_located((By.XPATH, '//li[@class="select2-results__option select2-results__option--highlighted"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@onclick="submitForm()"]'))).click()
        
        self.wait_loader()

        self.close_toast_popups()
        self.get_element('(//a[@title="Modifica riga"])[4]', By.XPATH).click()  
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@id="select2-idiva-container"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('Non imponibile')
        wait.until(EC.visibility_of_element_located((By.XPATH, '//li[@class="select2-results__option select2-results__option--highlighted"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@onclick="submitForm()"]'))).click()
        sleep(1)

        self.close_toast_popups()
        self.get_element('(//a[@title="Modifica riga"])[5]', By.XPATH).click()  
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@id="select2-idiva-container"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('Non imponibile')
        wait.until(EC.visibility_of_element_located((By.XPATH, '//li[@class="select2-results__option select2-results__option--highlighted"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@onclick="submitForm()"]'))).click()
        
        self.wait_loader()

        self.scroll_to_top()

        results = self.get_select_search_results("Stato*", "Emessa")
        if len(results) > 0: results[0].click()
        self.scroll_to_top()
        
        self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()

        self.wait_loader()

        # Creazione autofattura
        """
        A che serve sta roba?
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="btn btn-primary unblockable dropdown-toggle "]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@class="btn dropdown-item bound clickable"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="modal-body"]//span[@class="select2-selection select2-selection--single"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-search select2-search--dropdown"]//input[@type="search"]'))).send_keys("TD17")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//li[@class="select2-results__option select2-results__option--highlighted"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="modal-body"]//button[@type="submit"]'))).click()
        """
        self.wait_loader()

        self.scroll_to_top()
    
        results = self.get_select_search_results("Stato*", "Emessa")
        if len(results) > 0: results[0].click()
        self.scroll_to_top()
        
        self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.scroll_to_bottom()

        totale_imponibile = self.get_element('//div[@id="righe"]//tbody[2]//tr[1]//td[2]', By.XPATH).text
        iva = self.get_element('//div[@id="righe"]//tbody[2]//tr[2]//td[2]', By.XPATH).text
        totale = self.get_element('//div[@id="tab_0"]//div[@id="righe"]//tbody[2]//tr[3]//td[2]', By.XPATH).text

        self.assertEqual(totale_imponibile, (self.valori["Totale imponibile"]+ ' €'))
        self.assertEqual(iva, (self.valori["IVA"] + ' €'))
        self.assertEqual(totale, (self.valori["Totale documento"] + ' €'))

    def movimenti_contabili(self):               
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        filter_input = self.find_filter_input("Tipo")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("Fattura immediata di vendita", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader() 

        self.get_element('//a[@id="link-tab_37"]', By.XPATH).click()
        self.get_element('//a[@class="btn btn-info btn-lg"]', By.XPATH).click()
        self.wait_loader() 

        print("qui")
        time.sleep(10000)
        
        # Verifica movimenti contabili
        dare=self.get_element('(//td[@class="text-right"])[21]', By.XPATH).text
        avere_1=self.get_element('(//td[@class="text-right"])[25]', By.XPATH).text
        avere_2=self.get_element('(//td[@class="text-right"])[28]', By.XPATH).text
        self.assertEqual(dare,"323,06 €")
        self.assertEqual(avere_1,"264,80 €")
        self.assertEqual(avere_2,"58,26 €")

        self.navigateTo("Fatture di vendita")
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def plugin_movimenti_contabili(self):
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

        self.get_element('//a[@id="link-tab_38"]', By.XPATH).click()
        self.get_element('//div[@id="tab_38"]//a[@class="btn btn-info btn-lg"]', By.XPATH).click()
        self.wait_loader()

        dare=self.get_element('//div[@id="tab_38"]//tr[1]//td[3]', By.XPATH).text
        self.assertEqual(dare, "323,06 €")

        self.navigateTo("Anagrafiche")
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def regole_pagamenti(self):
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

        self.get_element('//a[@id="link-tab_40"]', By.XPATH).click()
         
        self.get_element('//div[@id="tab_40"]//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="select2-mese-container"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//input[@class="select2-search__field"])[2]'))).send_keys("Agosto", Keys.ENTER)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="select2-giorno_fisso-container"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//input[@class="select2-search__field"])[2]'))).send_keys("8", Keys.ENTER)
        self.wait_loader()

        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

        self.get_element('//div[@id="tab_40"]//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="select2-mese-container"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//input[@class="select2-search__field"])[2]'))).send_keys("Aprile", Keys.ENTER)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="select2-giorno_fisso-container"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//input[@class="select2-search__field"])[2]'))).send_keys("8", Keys.ENTER)
        self.wait_loader()

        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH,  '//div[@id="tab_40"]//tbody//tr//td[2]'))).click()
        self.wait_loader()
             
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="btn btn-danger "]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        sleep(1)

        self.expandSidebar("Contabilità")
        self.navigateTo("Scadenzario")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Anagrafica"]/input'))).send_keys('Cliente', Keys.ENTER)
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH,  '//tbody//tr//td[2]'))).click()
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="data_concordata0"]'))).send_keys('13/08/2025')
        sleep(1)

        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        #wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="alert alert-warning"]')))

        element = self.get_element('//input[@id="data_concordata0"]', By.XPATH)
        element.clear()
        element.send_keys('20/01/2025')
        sleep(1)

        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        wait.until(EC.invisibility_of_element_located((By.XPATH, '//div[@class="alert alert-warning"]')))

        self.navigateTo("Anagrafiche")
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

        self.expandSidebar("Vendite")
        
    def registrazioni(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        filter_input = self.find_filter_input("Tipo")
        filter_input.click()
        filter_input.clear()
        filter_input.send_keys("Fattura immediata di vendita", Keys.ENTER)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()
        

        self.get_element('//a[@id="link-tab_42"]', By.XPATH).click()
        self.wait_loader()

        # A cosa serve?
        #wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_42"]//tr[5]//td'))) 
        #sleep(1)

        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def controlla_allegati(self): 
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

        self.get_element('//a[@id="link-tab_30"]', By.XPATH).click()
        self.get_element('//div[@id="tab_30"]//a[@class="btn btn-info btn-lg"]', By.XPATH).click()
        self.wait_loader()

        #wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_30"]//a[@class="btn btn-xs btn-primary"]')))

        self.navigateTo("Anagrafiche")
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()

        self.expandSidebar("Vendite")

    def duplica_selezionati(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr//td', By.XPATH).click() 
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()  
        self.get_element('//a[@data-op="copy_bulk"]', By.XPATH).click()
        self.wait_swal2_popup()
        
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//tbody//tr//td', By.XPATH).click()  

    def cambia_sezionale(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.scroll_to_bottom()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        self.get_element('//a[@data-op="change_segment"]', By.XPATH).click() 

        self.wait_swal2_popup()

        results = self.get_select_search_results("Sezionale*")
        if len(results) > 0: results[0].click()

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//span[@id="select2-id_segment_-container"]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Autofatture")
        sleep(1)

        self.get_element('//ul[@id="select2-id_segment_-results"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//tbody//tr//td', By.XPATH).click() 
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        self.get_element('//a[@data-op="change_segment"]', By.XPATH).click() 
        
        self.wait_swal2_popup()

        self.get_element('//span[@id="select2-id_segment-container"]', By.XPATH).click()   
        self.get_element('//ul[@id="select2-id_segment-results"]', By.XPATH).click() 
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//span[@id="select2-id_segment_-container"]', By.XPATH).click() 
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Standard")
        sleep(1)

        self.get_element('//ul[@id="select2-id_segment_-results"]', By.XPATH).click() 
        self.wait_loader()

    def emetti_fatture(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr//td', By.XPATH).click() 

        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()
        self.get_element('//a[@data-op="change_status"]', By.XPATH).click()

        self.wait_swal2_popup()

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click() 
        self.wait_loader()

        stato=self.get_element('//tbody//tr//td[11]', By.XPATH).text
        self.assertEqual(stato, "Emessa")   

        self.get_element('//tbody//tr//td', By.XPATH).click()  

    def statistiche_vendita(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Magazzino")
        self.navigateTo("Articoli")
        self.wait_loader()

        self.get_element('//a[@id="link-tab_44"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_44"]//tbody//tr//td'))) 
        sleep(1)

        self.expandSidebar("Vendite")

    def controlla_fatture_elettroniche(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr//td', By.XPATH).click() 
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()  
        self.get_element('//a[@data-op="check_bulk"]', By.XPATH).click()  
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click() 
        sleep(1)

        # Verifica successo operazione
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.get_element('//div[@class="toast toast-success"]', By.XPATH).click()
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def registrazione_contabile(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Numero"]/input'))).send_keys("0001", Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()
        self.get_element('//a[@data-op="registrazione_contabile"]', By.XPATH).click() 
        sleep(1)

        totale=self.get_element('//th[@id="totale_dare"]', By.XPATH).text 
        self.assertEqual(totale, "323,06 €")

        # TODO aggiungere registrazione contabile e verificare importo in prima nota anzichè chiuderla

        self.get_element('//button[@class="close"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//tbody//tr//td', By.XPATH).click() 
        self.get_element('(//i[@class="deleteicon fa fa-times"])[1]', By.XPATH).click() 
        sleep(1)

    def genera_fatture_elettroniche(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()  
        self.get_element('//a[@data-op="export_xml_bulk"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()
        sleep(1)

        self.driver.switch_to.window(self.driver.window_handles[1]) 
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//button[@class="btn btn-xs btn-info"]', By.XPATH).click()  
        sleep(1)

        self.get_element('//button[@class="close"]', By.XPATH).click() 
        sleep(1)

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        sleep(1)

        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr//td', By.XPATH).click()  
        sleep(1)

    def elimina_selezionati(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr//td', By.XPATH).click()  
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        self.get_element('//a[@data-op="delete_bulk"]', By.XPATH).click()  
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()   
        sleep(1)

        test=self.get_element('//tbody//tr//td[2]', By.XPATH).text
        self.assertEqual(test, "0002/2025")
