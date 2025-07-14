from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from common.Test import Test

import time

class AnagraficheBis(Test):
    def setUp(self):
        super().setUp()
        self.wait_driver = WebDriverWait(self.driver, 20)
        self.navigateTo("Anagrafiche")

    def test_funzionalita_aggiuntive_anagrafica(self):
        self.aggiunta_referente()
        self.aggiunta_sede()
        self.plugin_statistiche()
        self.dichiarazione_di_intento()
        self.assicurazione_crediti()
        self.ricerca_coordinate()      # Questo non funziona a causa di un bug
        self.elimina_selezionati()
        self.cambia_relazione()
        self.logger.info("Test di funzionalità aggiuntive anagrafica completato con successo")

    def aggiunta_referente(self):
        self.navigateTo("Anagrafiche")
        self.wait_loader()

        self.search_entity("Cliente")
        self.click_first_result()

        self.click_plugin("Referenti")

        self.get_element('//h4//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        self.input(modal,'Nominativo').setValue("Referente di prova")

        self.get_element('//div[@class="modal-dialog modal-lg"]//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        context = self.get_element("form_82-")
        job_title_input = self.get_element("nome", context=context)
        job_title_input.send_keys("Segretario", Keys.ENTER)
        modal = self.wait_modal()

        results = self.get_select_search_results("Mansione", "Segretario")
        if len(results) > 0: results[0].click()

        self.get_element('//div[@class="modal-footer"]//button[@class="btn btn-primary"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//div[@id="tab_3"]//tbody//tr//td[2]', By.XPATH).click()
        self.wait_modal()

        name_input = self.get_element('(//input[@id="nome"])[2]', By.XPATH)
        name_input.clear()
        name_input.send_keys("Prova", Keys.ENTER)
        self.wait_loader()

        contact_name = self.get_element('//div[@id="tab_3"]//tbody//tr//td[2]', By.XPATH).text
        self.assertEqual(contact_name, "Prova")

        self.get_element('//div[@id="tab_3"]//tbody//tr//td[2]', By.XPATH).click()

        self.wait_modal()

        self.get_element('(//a[@class="btn btn-danger ask"])[2]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        empty_message = self.get_element('//div[@id="tab_3"]//tbody//tr', By.XPATH).text
        self.assertEqual(empty_message, "Nessun dato presente nella tabella")

        self.get_element('//h4//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        contact_name_input = self.get_element('(//input[@id="nome"])[2]', By.XPATH)
        contact_name_input.send_keys("Referente di prova", Keys.ENTER)

        results = self.get_select_search_results("Mansione")
        if len(results) > 0:
            results[0].click()

        self.get_element('(//button[@type="submit"])[3]', By.XPATH).click()
        self.wait_loader()

        search_input = self.find_filter_input("Mansione")
        search_input.send_keys("Segretario", Keys.ENTER)
        self.wait_for_search_results()

        job_title = self.get_element('//div[@id="tab_3"]//tbody//tr//td[3]', By.XPATH).text
        self.assertEqual("Segretario", job_title)

        self.navigateTo("Anagrafiche")
        self.wait_loader()
        self.clear_filters()

    def aggiunta_sede(self):
        self.navigateTo("Anagrafiche")
        self.wait_loader()

        self.search_entity("Cliente")
        self.click_first_result()

        self.click_plugin("Sedi aggiuntive")

        self.get_element('//div[@id="tab_4"]//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        self.input(None, 'Nome sede').setValue("Filiale XY")

        postal_code_input = self.get_element('(//input[@id="cap"])[2]', By.XPATH)
        postal_code_input.send_keys("35042")

        city_input = self.get_element('(//input[@id="citta"])[2]', By.XPATH)
        city_input.click()
        city_input.send_keys("Padova", Keys.ENTER)

        context = self.get_element("modals")
        results = self.get_select_search_results("Nazione", context=context)
        if len(results) > 0: results[0].click()

        self.get_element('(//button[@type="submit"])[3]', By.XPATH).click()

        self.wait_loader()

        self.get_element('//div[@id="tab_4"]//tbody/tr//td[2]', By.XPATH).click()

        location_name_input = self.get_input("Nome sede")
        location_name_input.clear()
        location_name_input.send_keys("Prova")

        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()
        self.wait_loader()

        # Wait for the table to be fully loaded
        self.wait_loader()

        # Wait explicitly for the table row to be visible
        location_name = self.get_element('//div[@id="tab_4"]//tbody/tr//td[2]', By.XPATH).text
        self.assertEqual(location_name, "Prova")

        self.get_element('//div[@id="tab_4"]//tbody/tr//td[2]', By.XPATH).click()

        self.wait_modal()

        self.get_element('//button[@class="btn btn-danger "]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        empty_message = self.get_element('//div[@id="tab_4"]//tbody//tr', By.XPATH).text
        self.assertEqual(empty_message, "Nessun dato presente nella tabella")

        self.get_element('//div[@id="tab_4"]//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        self.input(None, 'Nome sede').setValue("Filiale XY")

        postal_code_input = self.get_element('(//input[@id="cap"])[2]', By.XPATH)
        postal_code_input.send_keys("35042")

        city_input = self.get_element('(//input[@id="citta"])[2]', By.XPATH)
        city_input.click()
        city_input.send_keys("Padova")

        context = self.get_element("modals")
        results = self.get_select_search_results("Nazione", context=context)
        if len(results) > 0: results[0].click()

        self.get_element('(//button[@type="submit"])[3]', By.XPATH).click()

        search_input = self.find_filter_input("Nome")
        search_input.send_keys("Filiale XY")

        location_name = self.get_element('//div[@id="tab_4"]//tbody//td[2]', By.XPATH).text
        self.assertEqual("Filiale XY", location_name)

        self.navigateTo("Anagrafiche")
        self.wait_loader()
        self.clear_filters()

    def plugin_statistiche(self):
        self.navigateTo("Anagrafiche")
        self.wait_loader()

        self.search_entity("Cliente")
        self.click_first_result()

        self.click_plugin("Statistiche")

        stats_labels = [
            ("Preventivi", '//span[@class="info-box-text pull-left"]'),
            ("Contratti", '(//span[@class="info-box-text pull-left"])[2]'),
            ("Ordini cliente", '(//span[@class="info-box-text pull-left"])[3]'),
            ("Attività", '(//span[@class="info-box-text pull-left"])[4]'),
            ("Ddt in uscita", '(//span[@class="info-box-text pull-left"])[5]'),
            ("Fatture", '(//span[@class="info-box-text pull-left"])[6]'),
            ("Ore lavorate", '(//span[@class="info-box-text pull-left"])[7]')
        ]

        for expected_label, xpath in stats_labels:
            actual_label = self.get_element(xpath, By.XPATH).text
            self.assertEqual(actual_label, expected_label)

        self.navigateTo("Anagrafiche")
        self.wait_loader()
        self.clear_filters()

    def dichiarazione_di_intento(self):
        self.navigateTo("Anagrafiche")
        self.wait_loader()

        self.search_entity("Cliente")
        self.click_first_result()

        self.click_plugin("Dichiarazioni d'Intento")

        self.get_element('//div[@id="tab_25"]//i[@class="fa fa-plus"]', By.XPATH).click()

        self.wait_modal()

        form_fields = [
            ('Numero protocollo', "012345678901234567890123"),
            ('Data protocollo', "01/01/2025"),
            ('Progressivo int.', "001"),
            ('Data inizio', "01/01/2025"),
            ('Data fine', "31/12/2028"),
            ('Massimale', "50000"),
            ('Data di emissione', "13/01/2025")
        ]

        for label, value in form_fields:
            field = self.get_input(label)
            field.click()
            field.send_keys(value)

        data_emissione = self.get_element("data_emissione")
        data_emissione.send_keys("")

        self.get_element('(//button[@class="btn btn-primary"])[2]', By.XPATH).click()
        self.wait_loader()

        # Attende che l'elemento sia presente
        self.get_element('//div[@id="tab_25"]//tbody//tr//td[1]', By.XPATH)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        self.wait_modal()

        context = self.get_element("modals")
        results = self.get_select_search_results("Cliente", "Cliente", context=context)
        if len(results) > 0: results[0].click()

        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()
        self.wait_loader()

        declaration_message = self.get_element('(//div[@class="alert alert-info"])[1]', By.XPATH).text
        self.assertEqual("La fattura è collegata ad una dichiarazione d'intento", declaration_message[0:53])

        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click()

        description_field = self.get_element("descrizione_riga")
        description_field.send_keys("prova per dichiarazione")

        quantity_field = self.get_element("qta")
        quantity_field.click()
        quantity_field.send_keys("100,0", Keys.ENTER)

        context = self.get_element("modals")
        results = self.get_select_search_results("Unità di misura", "pz", context=context)
        if len(results) > 0: results[0].click()

        price_field = self.get_element("prezzo_unitario")
        price_field.click()
        price_field.send_keys("1")

        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()

        self.get_element('save').click()
        self.wait_loader()

        self.navigateTo("Anagrafiche")
        self.wait_loader()
        self.search_entity("Cliente")
        self.click_first_result()

        self.click_plugin("Dichiarazioni d'Intento")

        self.wait_loader()

        total_amount = self.get_element('//div[@id="tab_25"]//tbody//tr//td[5]', By.XPATH).text
        self.assertEqual(total_amount, "102.00")

        self.get_element('//div[@id="tab_25"]//tbody//tr//td[5]', By.XPATH).click()
        modal = self.wait_modal()

        self.input(modal, 'Progressivo int.').setValue("01")

        self.get_element('//div[@id="modals"]//button[@type="submit"]', By.XPATH).click()
        self.wait_loader()

        progressive = self.get_element('//div[@id="tab_25"]//tbody//td[3]', By.XPATH).text
        self.assertEqual(progressive, "01")

        self.get_element('//div[@id="tab_25"]//tbody//td[3]', By.XPATH).click()
        self.get_element('//a[@class="btn btn-danger ask "]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        empty_message = self.get_element('//div[@id="tab_25"]//td[@class="dataTables_empty"]', By.XPATH).text
        self.assertEqual(empty_message, "Nessun dato presente nella tabella")

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.find_cell(col=2).click()
        self.wait_loader()

        self.get_element('elimina', By.ID).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Anagrafiche")
        self.clear_filters()

    def assicurazione_crediti(self):
        self.navigateTo("Anagrafiche")
        self.wait_loader()

        self.search_entity("Cliente")
        self.click_first_result()

        self.click_plugin("Assicurazione crediti")

        self.get_element('//div[@id="tab_45"]//i[@class="fa fa-plus"]', By.XPATH).click()
        self.wait_loader()

        start_date_field = self.get_element("data_inizio")
        start_date_field.send_keys("01/01/2025")

        end_date_field = self.get_element("data_fine")
        end_date_field.clear()
        end_date_field.send_keys("31/12/2025")

        credit_limit_field = self.get_element("fido_assicurato")
        credit_limit_field.click()
        credit_limit_field.send_keys("50000", Keys.ENTER)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        date_field = self.get_element('data')
        date_field.click()
        date_field.clear()
        date_field.send_keys("01/01/2025")

        context = self.get_element("modals")
        results = self.get_select_search_results("Cliente", "Cliente", context=context)
        if len(results) > 0: results[0].click()

        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click()

        description_field = self.get_element("descrizione_riga")
        description_field.click()
        description_field.send_keys("prova")

        price_field = self.get_element("prezzo_unitario")
        price_field.click()
        price_field.send_keys("51000")

        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()

        self.get_element('save', By.ID).click()
        self.wait_loader()

        warning_message = self.get_element('//div[@class="alert alert-warning text-center"]', By.XPATH).text
        self.assertEqual("Attenzione!", warning_message[0:11])

        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Anagrafiche")
        self.wait_loader()
        self.search_entity("Cliente")
        self.click_first_result()

        self.click_plugin("Assicurazione crediti")

        self.get_element('//div[@id="tab_45"]//tbody//tr//td[2]', By.XPATH).click()

        credit_limit_field = self.get_element("fido_assicurato")
        credit_limit_field.clear()
        credit_limit_field.click()
        credit_limit_field.send_keys("49000")

        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()

        modified_limit = self.get_element('//div[@id="tab_45"]//tbody//tr//td[2]', By.XPATH).text
        self.assertEqual(modified_limit, "49000.00")

        self.get_element('//div[@id="tab_45"]//tbody//tr//td[2]', By.XPATH).click()
        self.get_element('//div[@id="modals"]//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Anagrafiche")
        self.clear_filters()

    def ricerca_coordinate(self):
        self.navigateTo("Anagrafiche")
        self.wait_loader()

        search_input = self.find_filter_input("Ragione sociale")
        search_input.send_keys("Admin spa")
        self.wait_for_search_results()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()

        self.get_element('//a[@data-op="search_coordinates"]', By.XPATH).click()

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        # TODO: Tutta questa parte qui non può funzionare per un bug nella pagina...
        #       Dopo che è stato sistemato il bug capire se è funzionante o no
        self.get_element('//a[@onclick="modificaPosizione()"]', By.XPATH).click()

        self.get_element('//ul//li[2]//div', By.XPATH).click()

        latitude = self.get_element('lat', By.ID).text
        self.assertNotEqual(latitude, "0")

        longitude = self.get_element('lng', By.ID).text
        self.assertNotEqual(longitude, "0")

        self.get_element('//button[@class="close"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Anagrafiche")
        self.wait_loader()
        self.clear_filters()

    def elimina_selezionati(self):
        self.navigateTo("Anagrafiche")
        self.wait_loader()

        search_input = self.find_filter_input("Ragione sociale")
        search_input.clear()
        search_input.send_keys("Vettore")
        self.wait_for_search_results()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()

        self.get_element('//a[@data-op="delete_bulk"]', By.XPATH).click()

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        search_input = self.find_filter_input("Ragione sociale")
        search_input.clear()
        search_input.send_keys("Vettore")
        self.wait_for_search_results()

        no_results_message = self.get_element('//tbody//tr[1]', By.XPATH).text
        self.assertEqual(no_results_message, "La ricerca non ha portato alcun risultato.")

        self.clear_filters()

    def cambia_relazione(self):
        self.navigateTo("Anagrafiche")
        self.wait_loader()

        self.search_entity("Cliente")
        self.wait_for_search_results()

        self.get_element('//tbody//tr[1]//td[1]', By.XPATH).click()

        self.scroll_to_bottom()

        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()

        self.get_element('//a[@data-op="change_relation"]', By.XPATH).click()

        self.wait_swal2_popup()

        results = self.get_select_search_results("Relazione con il cliente", "Attivo")
        if len(results) > 0: results[0].click()

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()
        self.wait_loader()

        relation = self.find_cell(col=7).text
        self.assertEqual(relation, "Attivo")

        self.find_cell(col=7).click()
        self.wait_loader()

        #results = self.get_select_search_results("Relazione", "Contattare", label_for="idrelazione")
        #if len(results) > 0: results[0].click()

        # TODO: Questo non sembra essere propriamente giusto, il test passa comunque perchè non viene controllato ma sarebbe da ricontrollare
        self.get_element('//span[@id="select2-idrelazione-container"]//span[@class="select2-selection__clear"]', By.XPATH).click()
        search_field = self.wait_driver.until(
            EC.visibility_of_element_located((By.XPATH, '(//input[@class="select2-search__field"])[2]'))
        )
        search_field.clear()
        search_field.send_keys("Da contattare")


        self.get_element('save', By.ID).click()
        self.wait_loader()

        self.navigateTo("Anagrafiche")
        self.wait_loader()

        new_relation = self.find_cell(col=7).text
        self.assertNotEqual(new_relation, "Attivo")

        self.clear_filters()
