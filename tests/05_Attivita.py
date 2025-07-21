from common.Test import Test, get_html
from common.RowManager import RowManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Attivita(Test):
    def setUp(self):
        super().setUp()
        self.expandSidebar("Attività")
        self.navigateTo("Attività")

    def test_attivita(self):
        # Crea un nuovo intervento. *Required*
        importi = RowManager.list()
        self.attivita("Cliente", 1, "2", importi[0])
        self.duplica_attività()
        self.modifica_attività("4")
        self.elimina_attività()
        self.controllo_righe()
        self.verifica_attività()
        self.storico_attivita()             # Controllo storico attività plugin in Anagrafica
        self.cambio_stato()                 # Cambia stato (Azioni di gruppo)
        self.duplica()                      # Duplica attività (Azioni di gruppo)
        self.elimina_selezionati()          # Elimina selezionati (Azioni di gruppo)
        self.firma_interventi()             # Firma interventi (Azioni di gruppo)
        self.fattura_attivita()             # Fattura attività (Azioni di gruppo)
        self.stampa_riepilogo()             # Stampa riepilogo (Azioni di gruppo)

    def attivita(self, cliente: str, tipo: int, stato: str, file_importi: str):
        self.navigateTo("Attività")

        # Crea attività
        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        self.input(modal, 'Cliente').setByText(cliente)
        self.input(modal, 'Tipo').setByIndex(tipo)

        self.wait_loader()

        request_xpath = '(//iframe[@class="cke_wysiwyg_frame cke_reset"])[1]'
        frame = self.get_element(request_xpath, By.XPATH)

        # Entra nel contesto dell'iframe
        self.driver.switch_to.frame(frame)

        body = self.driver.find_element(By.TAG_NAME, 'p')
        body.click()
        body.send_keys('Test')

        # Esce dal contesto dell'iframe
        self.driver.switch_to.default_content()

        self.get_element('//div[@class="col-md-12 text-right"]//button[@type="button"]', By.XPATH).click()
        

        row_manager = RowManager(self)
        self.valori = row_manager.compile(file_importi)

    def duplica_attività(self):
        self.navigateTo("Attività")

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.get_element('//div[@id="pulsanti"]//button[1]', By.XPATH).click()
        self.get_element('//span[@id="select2-id_stato-container"]', By.XPATH).click()
        self.get_element('//span[@class="select2-results"]//li[2]', By.XPATH).click()
        self.get_element('//div[@class="modal-content"]//button[@type="submit"]', By.XPATH).click()

    def modifica_attività(self, modifica:str):
        self.navigateTo("Attività")

        search_input = self.find_filter_input("Numero")
        search_input.send_keys("1", Keys.ENTER)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()

        self.input(None, 'Stato').setValue(modifica)
        self.get_element('save').click()

        self.navigateTo("Attività")

        self.get_element('//th[@id="th_Numero"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def elimina_attività(self):
        self.navigateTo("Attività")

        search_input = self.find_filter_input("Numero")
        search_input.click()
        search_input.clear()
        search_input.send_keys("2", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()

        self.get_element('//div[@id="tab_0"]//a[@class="btn btn-danger ask"]', By.XPATH).click()

        self.wait_swal2_popup()

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()

        if (numero_filter:=self.exists('//th[@id="th_Numero"]/i[@class="deleteicon fa fa-times"]', By.XPATH)):
            numero_filter.click()

        self.wait_loader()

        self.navigateTo("Attività")

    def controllo_righe(self):
        self.navigateTo("Attività")

        search_input = self.find_filter_input("Numero")
        search_input.click()
        search_input.clear()
        search_input.send_keys("1", Keys.ENTER)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()

        imponibile = self.get_element('//div[@id="righe"]//tbody[2]//tr[1]//td[2]', By.XPATH).text
        sconto = self.get_element('//div[@id="righe"]//tbody[2]//tr[2]//td[2]', By.XPATH).text
        totale = self.get_element('//div[@id="righe"]//tbody[2]//tr[3]//td[2]', By.XPATH).text

        self.assertEqual(imponibile, (self.valori["Imponibile"] + ' €'))
        self.assertEqual(sconto, (self.valori["Sconto/maggiorazione"] + ' €'))
        self.assertEqual(totale, (self.valori["Totale imponibile"] + ' €'))

        imponibilefinale = self.get_element('//div[@id="costi"]//tbody[2]//tr[1]//td[2]', By.XPATH).text
        scontofinale = self.get_element('//div[@id="costi"]//tbody[2]//tr[2]//td[2]', By.XPATH).text
        totaleimpfinale = self.get_element('//div[@id="costi"]//tbody[2]//tr[3]//td[2]', By.XPATH).text
        IVA = self.get_element('//div[@id="costi"]//tbody[2]//tr[4]//td[2]', By.XPATH).text
        totalefinale = self.get_element('//div[@id="costi"]//tbody[2]//tr[5]//td[2]', By.XPATH).text

        self.assertEqual(imponibilefinale, imponibile)
        self.assertEqual(scontofinale, sconto)
        self.assertEqual(totaleimpfinale, totale)
        self.assertEqual(IVA, (self.valori["IVA"] + ' €'))
        self.assertEqual(totalefinale, (self.valori["Totale documento"] + ' €'))

        self.navigateTo("Attività")

        self.get_element('//th[@id="th_Numero"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def verifica_attività(self):
        self.navigateTo("Attività")

        # Verifica elemento modificato
        search_input = self.find_filter_input("Numero")
        search_input.click()
        search_input.clear()
        search_input.send_keys("1", Keys.ENTER)

        self.wait_for_search_results()

        modificato = self.driver.find_element(By.XPATH, '//tbody//tr[1]//td[7]').text
        self.assertEqual("Completato", modificato)
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()

        # Verifica elemento eliminato
        search_input = self.find_filter_input("Numero")
        search_input.click()
        search_input.clear()
        search_input.send_keys("2", Keys.ENTER)

        self.wait_for_search_results()

        eliminato = self.driver.find_element(By.XPATH, '//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.", eliminato)
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def storico_attivita(self):
        self.navigateTo("Anagrafiche")

        search_input = self.find_filter_input("Ragione sociale")
        search_input.click()
        search_input.clear()
        search_input.send_keys("Cliente", Keys.ENTER)

        self.find_cell(col=2).click()

        self.click_plugin("Storico attività")

        # Verifica attività
        self.wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_28"]//tbody//tr//td[1]')))

    def cambio_stato(self):
        self.navigateTo("Attività")

        search_input = self.find_filter_input("Numero")
        search_input.click()
        search_input.clear()
        search_input.send_keys("1", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()

        self.get_element('//a[@data-op="change_status"]', By.XPATH).click()

        self.get_element('//span[@id="select2-id_stato-container"]', By.XPATH).click()
        search_field = self.wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]')))
        search_field.send_keys("Da programmare")

        self.get_element('//li[@class="select2-results__option select2-results__option--highlighted"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()

        stato = self.get_element('//tbody//tr//td[7]', By.XPATH).text
        self.assertEqual(stato, "Da programmare")

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def duplica(self):
        self.navigateTo("Attività")

        search_input = self.find_filter_input("Numero")
        search_input.click()
        search_input.clear()
        search_input.send_keys("1", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()
        self.get_element('//a[@data-op="copy_bulk"]', By.XPATH).click()

        self.get_element('//span[@id="select2-idstatointervento-container"]', By.XPATH).click()
        search_field = self.wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]')))
        search_field.send_keys("Da programmare")

        self.get_element('//li[@class="select2-results__option select2-results__option--highlighted"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()

        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()

        search_input = self.find_filter_input("Numero")
        search_input.send_keys("2", Keys.ENTER)

        numero = self.find_cell(col=2).text
        self.assertEqual(numero, "2")

        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def elimina_selezionati(self):
        self.navigateTo("Attività")

        search_input = self.find_filter_input("Numero")
        search_input.click()
        search_input.clear()
        search_input.send_keys("2", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()
        self.get_element('//a[@data-op="delete_bulk"]', By.XPATH).click()

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()

        scritta = self.get_element('//tbody//tr//td', By.XPATH).text
        self.assertEqual(scritta, "La ricerca non ha portato alcun risultato.")
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def firma_interventi(self):
        self.navigateTo("Attività")

        # Aggiunta attività
        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()

        results = self.get_select_search_results("Cliente", "Cliente")
        if len(results) > 0: results[0].click()

        results = self.get_select_search_results("Tipo", "Generico")
        if len(results) > 0: results[0].click()

        request_xpath = '(//iframe[@class="cke_wysiwyg_frame cke_reset"])[1]'
        frame = self.get_element(request_xpath, By.XPATH)

        # Entra nel contesto dell'iframe
        self.driver.switch_to.frame(frame)

        body = self.driver.find_element(By.TAG_NAME, 'p')
        body.click()
        body.send_keys('Test')

        # Esce dal contesto dell'iframe
        self.driver.switch_to.default_content()

        self.scroll_to_bottom()

        self.get_element('//button[@class="btn btn-lg btn-success"]', By.XPATH).click()

        # Firma attività
        self.navigateTo("Attività")

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()
        self.get_element('//a[@data-op="firma-intervento"]', By.XPATH).click()

        self.get_element('//button[@id="firma"]', By.XPATH).click()
        firma_input = self.get_element("firma_nome")
        firma_input.send_keys("firma")

        self.get_element('//button[@class="btn btn-success pull-right"]', By.XPATH).click()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()

        # Verifica firma
        self.wait_driver.until(EC.visibility_of_element_located((By.XPATH, '(//div[@class="text-center row"]//div)[3]')))

    def fattura_attivita(self):
        self.navigateTo("Attività")

        search_input = self.find_filter_input("Numero")
        search_input.click()
        search_input.clear()
        search_input.send_keys("2", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()

        self.wait_loader()

        self.scroll_to_top()

        results = self.get_select_search_results("Stato", "Completato")
        if len(results) > 0: results[0].click()

        self.get_element('save').click()

        self.get_element('back').click()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()
        self.get_element('//a[@data-op="create_invoice"]', By.XPATH).click()

        self.wait_swal2_popup()

        results = self.get_select_search_results("Raggruppa per", "Cliente")
        if len(results) > 0: results[0].click()

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()

        stato = self.get_element('//tbody//tr//td[7]', By.XPATH).text
        self.assertEqual(stato, "Fatturato")

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()

        self.delete_and_confirm()

        self.navigateTo("Attività")

        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def stampa_riepilogo(self):
        self.navigateTo("Attività")

        search_input = self.find_filter_input("Numero")
        search_input.click()
        search_input.clear()
        search_input.send_keys("2", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()
        self.get_element('//a[@data-op="print_summary"]', By.XPATH).click()

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()

        # TODO: Capire se si può fare
        #self.driver.switch_to.window(self.driver.window_handles[1])
        #prezzo = self.get_element('(//div[@id="viewer"]//span)[59]', By.XPATH).text
        #self.assertEqual(prezzo, "0,00 €")
        #self.driver.close()
        #self.driver.switch_to.window(self.driver.window_handles[0])

        self.find_cell(col=2).click()

        self.delete_and_confirm()
