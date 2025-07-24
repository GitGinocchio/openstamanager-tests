from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from common.Test import Test

import time

class Anagrafiche(Test):
    def setUp(self):
        super().setUp()
        self.wait_driver = WebDriverWait(self.driver, 20)
        self.navigateTo("Anagrafiche")

    def test_creazione_anagrafica(self):
        self.add_anagrafica('Cliente', 'Cliente')
        self.add_anagrafica('Tecnico', 'Tecnico')
        self.add_anagrafica('Fornitore', 'Fornitore')
        self.add_anagrafica('Vettore', 'Vettore')
        self.add_anagrafica('Agente', 'Agente')
        self.add_anagrafica('Anagrafica di Prova da Eliminare', 'Cliente')
        self.modifica_anagrafica('Privato')
        self.elimina_anagrafica()
        self.verifica_anagrafica()
        self.crea_attivita()
        self.crea_preventivo()
        self.crea_contratto()
        self.crea_ordine_cliente()
        self.crea_DDT_uscita()
        self.crea_fattura_vendita()


    def add_anagrafica(self, nome: str, tipo: str):
        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()

        modal = self.wait_modal()
        self.input(modal, 'Denominazione').setValue(nome)
        select = self.input(modal, 'Tipo di anagrafica')
        select.setByText(tipo)

        # Usa XPath relativo al modal per trovare il pulsante
        self.get_element('.//div[@class="modal-footer"]//button[@type="submit"]', By.XPATH, modal).click()
        self.wait_loader()

    def modifica_anagrafica(self, tipologia: str):
        self.navigateTo("Anagrafiche")
        self.wait_loader()
        self.search_entity("Cliente")
        self.click_first_result()

        results = self.get_select_search_results("Tipologia", tipologia)
        if len(results) > 0: results[0].click()

        piva = self.get_input("Partita IVA")
        piva.clear()
        piva.send_keys("05024030287")

        codice_fiscale = self.get_input("Codice fiscale")
        codice_fiscale.clear()
        codice_fiscale.send_keys("05024030287")

        address_field = self.get_element("indirizzo")
        address_field.clear()
        address_field.send_keys("Via controllo caratteri speciali: &\"<>èéàòùì?'`")

        cap_field = self.get_element('//label[contains(., "C.A.P.")]/parent::div/parent::div//input', By.XPATH)
        cap_field.click()
        cap_field.clear()
        cap_field.send_keys("35042")

        self.wait_loader()

        city_field = self.get_element('//label[contains(., "Città")]/parent::div/parent::div//input', By.XPATH)
        city_field.click()
        city_field.clear()
        city_field.send_keys("Este")
        
        self.get_element('save', By.ID).click()
        self.wait_loader()

        self.navigateTo("Anagrafiche")
        self.wait_loader()

        self.clear_filters()

    def elimina_anagrafica(self):
        self.navigateTo("Anagrafiche")
        self.wait_loader()
        self.search_entity('Anagrafica di Prova da Eliminare')
        self.click_first_result()
        self.wait_loader()
        
        self.get_element('//div[@id="tab_0"]//a[@class="btn btn-danger ask"]', By.XPATH).click()
        
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.clear_filters()

    def verifica_anagrafica(self):
        self.navigateTo("Anagrafiche")
        self.wait_loader()

        self.clear_filters()
        
        search_input = self.find_filter_input("Tipologia")
        search_input.clear()
        search_input.send_keys("Privato", Keys.ENTER)
        self.wait_for_search_results()

        context = self.get_element("tab_0")
        entity_name = self.find_cell(row=1, col=3, context=context).text
        self.assertEqual("Cliente", entity_name)

        self.navigateTo("Anagrafiche")
        self.wait_loader()
        self.clear_filters()

        search_input = self.find_filter_input("Ragione sociale")
        search_input.clear()
        search_input.send_keys("Anagrafica di Prova da Eliminare", Keys.ENTER)
        self.wait_for_search_results()

        no_results_message = self.find_cell(col=1).text

        self.assertEqual("La ricerca non ha portato alcun risultato.", no_results_message)

        self.clear_filters()

    def crea_attivita(self):
        self.navigateTo("Anagrafiche")
        self.wait_loader()

        self.search_entity("Cliente")
        self.click_first_result()
        
        self.get_element('//button[@class="btn btn-info dropdown-toggle"]', By.XPATH).click()
        self.get_element('(//a[@class="btn dropdown-item bound clickable"])[1]', By.XPATH).click()

        self.wait_modal()

        results = self.get_select_search_results("Tipo", label_for="idtipointervento")
        if len(results) > 0:
            results[0].click()

        description_field = self.get_element('(//iframe[@class="cke_wysiwyg_frame cke_reset"])[2]', By.XPATH)
        description_field.click()
        description_field.send_keys("Test", Keys.ENTER)
        
        self.get_element('//div[@class="col-md-12 text-right"]//button[@type="button"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Anagrafiche")
        self.wait_loader()

        self.search_entity("Cliente")
        self.click_first_result()

        self.expand_plugin_sidebar()
        self.click_plugin("Storico attività")

        activity_number = self.get_element('//div[@id="tab_28"]//tbody//tr//td[2]', By.XPATH).text
        self.assertEqual("1", activity_number)
        
        self.get_element('//div[@id="tab_28"]//tbody//td[2]', By.XPATH).click()

        self.wait_loader()

        self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        delete_btn = self.get_element('//div[@id="tab_0"]//a[@class="btn btn-danger ask"]', By.XPATH)
        delete_btn.click()

        self.wait_swal2_popup()
        
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Anagrafiche")
        self.clear_filters()

    def crea_preventivo(self):
        self.navigateTo("Anagrafiche")
        self.wait_loader()

        self.search_entity("Cliente")
        self.click_first_result()
        
        self.get_element('//button[@class="btn btn-info dropdown-toggle"]', By.XPATH).click()
        self.get_element('(//a[@class="btn dropdown-item bound clickable"])[2]', By.XPATH).click()
        modal = self.wait_modal()

        results = self.get_select_search_results("Tipo di Attività")
        if len(results) > 0:
            results[0].click()

        results = self.get_select_search_results("Stato")
        if len(results) > 0:
            results[0].click()

        self.input(modal, 'Nome').setValue("Preventivo di prova anagrafica")
        
        self.get_element('(//div[@id="form_13-"]//button[@class="btn btn-primary"])', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Anagrafiche")
        self.wait_loader()
        self.search_entity("Cliente")
        self.click_first_result()

        self.scroll_to_bottom()
        
        self.get_element('//button[@class="btn btn-tool"]', By.XPATH).click()

        self.scroll_to_bottom()

        quote_text = self.get_element('(//div[@class="card-body"]//li)[7]', By.XPATH).text

        self.assertEqual("Preventivo 1", quote_text[0:12])
        
        self.get_element('(//div[@class="card-body"]//li//a)[5]', By.XPATH).click()

        self.open_new_window_when_available()

        self.wait_loader()
        self.scroll_to_bottom()
        
        self.get_element('//div[@id="tab_0"]//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.wait_loader()

        self.navigateTo("Anagrafiche")
        self.clear_filters()

    def crea_contratto(self):
        self.navigateTo("Anagrafiche")
        self.wait_loader()

        self.search_entity("Cliente")
        self.click_first_result()
        
        self.get_element('//button[@class="btn btn-info dropdown-toggle"]', By.XPATH).click()
        self.get_element('(//a[@class="btn dropdown-item bound clickable"])[3]', By.XPATH).click()
        modal = self.wait_modal()

        self.input(modal, 'Nome').setValue("Contratto di prova anagrafica")

        results = self.get_select_search_results("Stato", "Bozza")
        if len(results) > 0: results[0].click()

        self.get_element('(//div[@id="form_31-"]//button[@class="btn btn-primary"])', By.XPATH).click()

        self.wait_loader()

        self.get_element('//div[@id="tab_0"]//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Anagrafiche")
        self.wait_loader()
        self.clear_filters()

    def crea_ordine_cliente(self):
        self.navigateTo("Anagrafiche")
        self.wait_loader()

        self.search_entity("Cliente")
        self.click_first_result()

        self.get_element('//button[@class="btn btn-info dropdown-toggle"]', By.XPATH).click()
        self.get_element('(//a[@class="btn dropdown-item bound clickable"])[4]', By.XPATH).click()
        self.wait_modal()

        self.get_element('(//div[@id="form_24-"]//button[@class="btn btn-primary"])', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Anagrafiche")
        self.wait_loader()

        self.search_entity("Cliente")
        self.click_first_result()

        self.get_element('//button[@class="btn btn-tool"]', By.XPATH).click()

        order_text = self.get_element('(//div[@class="card-body"]//li)[7]', By.XPATH).text

        self.assertEqual("Ordine cliente 01", order_text[0:17])

        self.scroll_to_bottom()
        self.get_element('(//div[@class="card-body"]//li//a)[5]', By.XPATH).click()

        self.open_new_window_when_available()
        self.wait_loader()

        self.scroll_to_bottom()

        self.get_element('//div[@id="tab_0"]//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Anagrafiche")
        self.clear_filters()

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def crea_DDT_uscita(self):
        self.navigateTo("Anagrafiche")
        self.wait_loader()

        self.search_entity("Cliente")
        self.click_first_result()

        self.get_element('//button[@class="btn btn-info dropdown-toggle"]', By.XPATH).click()
        self.get_element('(//a[@class="btn dropdown-item bound clickable"])[5]', By.XPATH).click()
        modal = self.wait_modal()

        results = self.get_select_search_results("Causale trasporto")
        
        if len(results) > 0:
            results[0].click()

        self.get_element('(//div[@id="form_26-"]//button[@class="btn btn-primary"])', By.XPATH).click()

        self.navigateTo("Anagrafiche")
        self.wait_loader()
        self.search_entity("Cliente")
        self.click_first_result()

        self.click_plugin("Ddt del cliente")

        ddt_number_cell = self.get_element('//div[@id="tab_17"]//tbody//td[2]', By.XPATH)
        self.assertEqual("01", ddt_number_cell.text)
        ddt_number_cell.click()

        self.scroll_to_bottom()

        self.get_element('//div[@id="tab_0"]//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Anagrafiche")
        self.clear_filters()

    def crea_fattura_vendita(self):
        self.navigateTo("Anagrafiche")
        self.wait_loader()

        self.search_entity("Cliente")
        self.click_first_result()

        self.get_element('//button[@class="btn btn-info dropdown-toggle"]', By.XPATH).click()
        self.get_element('(//a[@class="btn dropdown-item bound clickable"])[6]', By.XPATH).click()

        self.wait_modal()

        self.get_element('(//div[@id="form_14-"]//button[@class="btn btn-primary"])', By.XPATH).click()

        self.navigateTo("Anagrafiche")
        self.wait_loader()
        self.search_entity("Cliente")
        self.click_first_result()

        self.get_element('//button[@class="btn btn-tool"]', By.XPATH).click()

        self.scroll_to_bottom()

        invoice_text = self.get_element('(//div[@class="card-body"]//li)[7]', By.XPATH).text
        self.assertEqual("Fattura immediata di vendita", invoice_text[0:28])

        self.get_element('(//div[@class="card-body"]//li//a)[5]', By.XPATH).click()

        self.wait_driver.until(lambda driver: len(driver.window_handles) > 1)

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


        self.delete_and_confirm()
        self.wait_loader()

        self.navigateTo("Anagrafiche")
        self.wait_loader()
        self.clear_filters()
