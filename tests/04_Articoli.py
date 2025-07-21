from common.Test import Test, get_html
from selenium.webdriver.common.keys import Keys
from common.RowManager import RowManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Articoli(Test):
    def setUp(self):
        super().setUp()
        self.expandSidebar("Magazzino")
        self.wait_loader()

    def test_creazione_articolo(self):
        self.creazione_articolo("001", "Articolo 1", "2")
        self.creazione_articolo("002", "Articolo di Prova da Eliminare", "2")
        self.modifica_articolo("20", "1")
        self.elimina_articolo()
        self.verifica_articolo()
        self.serial()
        self.provvigioni()
        self.listino_fornitori()
        self.giacenze()
        self.statistiche()
        self.netto_clienti()
        self.aggiorna_prezzo_acquisto()
        self.aggiorna_prezzo_vendita()
        self.coefficiente_vendita()
        self.aggiorna_quantita()
        self.crea_preventivo()
        self.aggiorna_iva()
        self.aggiorna_unita_misura()
        self.conto_predefinito_acquisto()
        self.conto_predefinito_vendita()
        self.imposta_provvigione()
        self.aggiorna_prezzo_unitario()
        self.copia_listini()
        self.imposta_prezzo_da_fattura()
        self.stampa_etichette()
        self.elimina_selezionati()

    def creazione_articolo(self, codice: str, descrizione: str, qta: str):
        self.navigateTo("Articoli")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        self.input(modal, 'Codice').setValue(codice)
        self.input(modal, 'Descrizione').setValue(descrizione)

        self.get_element('//button[@class="btn btn-tool"]', By.XPATH).click()

        self.wait(EC.visibility_of_element_located((By.XPATH, '//label[contains(text(), "Quantità iniziale")]/following-sibling::div/input')))

        self.input(modal, 'Quantità iniziale').setValue(qta)
        self.get_element('button[type="submit"]', By.CSS_SELECTOR).click()

    def modifica_articolo(self, acquisto:str, coefficiente:str):
        self.navigateTo("Articoli")
        self.wait_loader()

        # Scrive "Articolo 1" nel filtro Descrizione
        search_input = self.find_filter_input("Descrizione")
        search_input.click()
        search_input.clear()
        search_input.send_keys("Articolo 1", Keys.ENTER)

        self.wait_for_search_results()

        # Clicca il primo risultato
        self.find_cell(row=1, col=2).click()

        # Scrive nelle input i valori
        self.input(None, 'Prezzo di acquisto').setValue(acquisto)
        self.input(None, 'Coefficiente').setValue(coefficiente)

        # Clicca il pulsante salva
        self.get_element("save").click()

        self.get_element("back").click()

        verificaqta = self.get_element('//div[@id="tab_0"]//tbody//td[10]//div[1][1]', By.XPATH).text
        self.assertEqual(verificaqta, "2,00")
        
        if (filter_icon:=self.exists('//th[@id="th_Descrizione"]/i[@class="deleteicon fa fa-times"]', By.XPATH)):
            filter_icon.click()

    def elimina_articolo(self):
        self.navigateTo("Articoli")
        self.wait_loader()

        search_input = self.find_filter_input("Descrizione")
        search_input.click()
        search_input.send_keys("Articolo di Prova da Eliminare", Keys.ENTER)

        self.wait_for_search_results()
        cella = self.find_cell(col=2)
        cella.click()

        self.scroll_to_bottom()

        self.get_element('//div[@id="tab_0"]//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()

        if (filter_icon:=self.exists('//th[@id="th_Descrizione"]/i[@class="deleteicon fa fa-times"]', By.XPATH)):
            filter_icon.click()

    def verifica_articolo(self):
        self.navigateTo("Articoli")
        self.wait_loader()

        # Scrive "001" nel filtro Codice
        search_input = self.find_filter_info("Codice")
        search_input.click()
        search_input.clear()
        search_input.send_keys("001")

        # nella prima riga trova la cella 9 e controlla se il test è uguale a 20
        modificato = self.find_cell(row=1, col=9)
        self.assertEqual("20,00", modificato.text)

        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()

        search_input = self.find_filter_input("Descrizione")
        search_input.click()
        search_input.clear()
        search_input.send_keys("Articolo di prova da Eliminare", Keys.ENTER)

        self.wait_for_search_results()

        elemento = self.find_cell(row=1, col=1)
        self.assertEqual("La ricerca non ha portato alcun risultato.", elemento.text)

        if (filter_icon:=self.exists('//th[@id="th_Descrizione"]/i[@class="deleteicon fa fa-times"]', By.XPATH)):
            filter_icon.click()

    def serial(self):
        self.navigateTo("Articoli")
        self.wait_loader()

        search_input = self.find_filter_input("Descrizione")
        search_input.click()
        search_input.clear()
        search_input.send_keys("Articolo 1")

        self.wait_for_search_results()

        self.get_element('//tbody//td[2]//div[1]', By.XPATH).click()

        self.get_element('(//i[@class="fa fa-plus"])[2]', By.XPATH).click()

        self.get_element('//label[@for="abilita_serial"]', By.XPATH).click()
        self.get_element('save').click()

        self.click_plugin("Serial")

        serial_start = self.get_element('serial_start')
        serial_start.click()
        serial_start.clear()
        serial_start.send_keys("1")

        serial_end = self.get_element('serial_end')
        serial_end.click()
        serial_end.clear()
        serial_end.send_keys("2")

        self.get_element('//div[@id="tab_11"]//button[@type="button"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-primary"]', By.XPATH).click()

        serial = self.get_element('//div[@id="tab_11"]//div[@class="card"]//tbody//tr[2]//td[1]', By.XPATH).text
        self.assertEqual(serial, "1")

        self.get_element('(//a[@class="btn btn-danger btn-sm ask"])[2]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()

        self.wait(EC.invisibility_of_element_located((By.XPATH, '//div[@id="tab_11"]//div[@class="card"]//tbody//tr[2]//td[1]')))

        self.navigateTo("Articoli")
        self.wait_loader()

        if (filter_icon:=self.exists('//th[@id="th_Descrizione"]/i[@class="deleteicon fa fa-times"]', By.XPATH)):
            filter_icon.click()

    def provvigioni(self):
        self.navigateTo("Articoli")
        self.wait_loader()

        # Cerca un articolo dalla tabella principale della sezione articoli con descrizione "Articolo 1"
        search_input = self.find_filter_input("Descrizione")
        search_input.click()
        search_input.send_keys("Articolo 1", Keys.ENTER)
        self.wait_loader()

        self.wait_for_search_results()

        # Ottiene la cella dell'articolo trovato e la clicca
        cella = self.find_cell(row=1, col=2)
        cella.click()

        # clicca il pulsante di aggiunta provvigioni dal plugin provvigioni e aggiunge una provvigione
        self.click_plugin("Provvigioni")
        self.get_element('//div[@id="tab_43"]//i[@class="fa fa-plus"]', By.XPATH).click()
        self.wait_modal()

        # Inserisce 
        results = self.get_select_search_results("Agente", "Agente")
        if len(results) > 0:
            results[0].click()

        provvigione_input = self.get_element("provvigione")
        provvigione_input.click() # Click necessario per prendere il focus della input
        provvigione_input.send_keys("2", Keys.ENTER)

        tab_provvigioni = self.get_element("tab_43")
        provvigione = self.find_cell(col=3, context=tab_provvigioni)
        self.assertEqual(provvigione.text, "2.00 €")

        cella = self.find_cell(col=3, context=tab_provvigioni)
        cella.click()
        self.wait_modal()

        provvigione_input = self.get_element("provvigione")
        provvigione_input.click()
        provvigione_input.send_keys("1", Keys.ENTER)


        tab_provvigioni = self.get_element("tab_43")
        provvigione = self.find_cell(col=3, context=tab_provvigioni)
        self.assertEqual(provvigione.text, "1.00 €")

        provvigione.click()

        # Forse si può sostituire con: self.delete_and_confirm()
        self.get_element('(//a[@class="btn btn-danger ask"])[2]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()

        self.navigateTo("Articoli")
        self.wait_loader()

        self.get_element('//th[@id="th_Descrizione"]//i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def listino_fornitori(self):
        # Si sposta nella sezione Articoli
        self.navigateTo("Articoli")
        self.wait_loader()

        # Inserisce nel filtro Descrizione "Articolo 1"
        search_input = self.find_filter_input("Descrizione")
        search_input.click()
        search_input.send_keys("Articolo 1", Keys.ENTER)

        self.wait_for_search_results()

        # Ottiene la prima riga e ci clicca sopra
        cella = self.find_cell(row=1,col=2)
        cella.click()

        # Clicca il plugin "Listino Fornitori"
        element = self.get_element("link-tab_32")
        element.click()

        # Scrive nella select Fornitore "Fornitore" e clicca il primo risultato
        # (Viene passato label_for perchè questo campo è facilmente confondibile con la label "Fornitore" con for="id_fornitore")
        results = self.get_select_search_results("Fornitore", label_for="id_fornitore_informazioni", search_query="Fornitore")
        if len(results) > 0: results[0].click()

        # Clicca il pulsante info e aspetta l'apertura della modal
        self.get_element('//button[@class="btn btn-info"]', By.XPATH).click()
        modal = self.wait_modal()

        # Ottiene l'input e scrive 100
        quota_minima = self.get_input("Qta minima ordinabile")
        quota_minima.click()
        quota_minima.send_keys("100")

        # Ottiene l'input e scrive 15
        giorni_consegna = self.get_input("Tempi di consegna")
        giorni_consegna.click()
        giorni_consegna.send_keys("15")

        # Ottiene l'elemento checkbox e lo clicca
        prezzo_specifico_checkbox = self.get_element('//label[@for="modifica_prezzi" and @class="btn btn-default active"]', By.XPATH)
        prezzo_specifico_checkbox.click()

        # Ottiene la input "Prezzo specifico" e inserisce 15
        prezzo_unitario = self.get_input("Prezzo specifico")
        prezzo_unitario.click()
        prezzo_unitario.send_keys("15")

        # Preme invio chiudendo la modal
        prezzo_unitario.send_keys(Keys.ENTER)

        # Espande la sidebar, va nella sezione Acquisti/Fatture di acquisto e aspetta il caricamento della pagina
        self.expandSidebar("Acquisti")
        self.navigateTo("Fatture di acquisto")
        self.wait_loader()

        # Aggiunge una nuova voce e aspetta la modal
        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        # Ottiene e scrive nella input 78
        numero_esterno = self.get_input("N. fattura del fornitore")
        numero_esterno.send_keys("78")

        # Scrive "Fornitore" nella select Fornitore e clicca la prima opzione
        results = self.get_select_search_results("Fornitore", "Fornitore")
        if len(results) > 0:
            results[0].click()
        
        # Clicca il pulsante primario e aspetta l'apertura di una modal
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()
        self.wait_loader()

        # Clicca la select e sceglie il primo suggerimento
        results = self.get_select_search_results("Pagamento")
        if len(results) > 0: results[0].click()

        # Clicca la select e sceglie il primo suggerimento
        self.get_element("select2-id_articolo-container", By.ID).click()
        self.get_element('//ul[@class="select2-results__options select2-results__options--nested"]//li[1]', By.XPATH).click()

        # L'idea era sostituire queste due righe sopra con questo ma non so perchè non funziona (comunque il risultato è uguale)
        #results = self.get_select_search_results("Articolo")
        #if len(results) > 0:
            #results[0].click()

        # Clicca il tasto Aggiungi
        self.get_element('//button[@class="btn btn-primary tip tooltipstered"]', By.XPATH).click()

        # Controlla il prezzo
        prezzo = self.find_cell(row=1, col=8, context=self.get_element("righe")).text
        self.assertEqual(prezzo, "15,00 €")

        # Elimina la fattura
        self.get_element("elimina").click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()

        self.expandSidebar("Magazzino")
        self.navigateTo("Articoli")
        self.wait_loader()

        # Clicca il primo articolo
        self.find_cell(row=1, col=2).click()

        # Scrive "Fornitore" dentro al select Fornitore predefinito
        results = self.get_select_search_results("Fornitore predefinito", "Fornitore")
        if len(results) > 0: results[0].click()

        # Clicca il pulsante salva (Altrimenti non è possibile spostarsi in un altra pagina)
        save_btn = self.get_element("save", By.ID).click()

        self.navigateTo("Articoli")
        self.wait_loader()

        # Seleziona il primo articolo
        self.find_cell(row=1, col=2).click()

        # Modifica listino fornitore
        self.get_element("link-tab_32").click()
        self.get_element('//a[@class="btn btn-secondary btn-warning"]', By.XPATH).click()

        self.wait_modal()

        # Ottiene e scrive 1 nella input Codice Fornitore e poi clicca invio (salvando)
        codice_fornitore = self.get_element("codice_fornitore")
        codice_fornitore.clear()
        codice_fornitore.send_keys("1", Keys.ENTER)

        # Ottiene il contesto attuale delal tab aperta
        tab_32 = self.get_element("tab_32")

        # Trova la cella con il codice dell'articolo
        codice = self.get_element('//div[@id="tab_32"]//tbody//tr//td[3]', By.XPATH).text
        self.assertEqual(codice, "1")

        # Elimina listino fornitore
        #self.delete_and_confirm()
    
        self.get_element('//a[@class="btn btn-secondary btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()

        messaggio = self.get_element('(//div[@class="alert alert-info"])[4]', By.XPATH).text
        self.assertEqual(messaggio, "Nessuna informazione disponibile...")

        self.navigateTo("Articoli")
        self.wait_loader()

        # Non ho capito perchè viene fatto ma nel dubbio lo lascio
        xpath = '//th[@id="th_Descrizione"]/i[@class="deleteicon fa fa-times"]'
        if (element:=self.exists(xpath, By.XPATH)):
            element.click()

    def giacenze(self):
        self.navigateTo("Articoli")
        self.wait_loader()

        search_input = self.find_filter_input("Descrizione")
        search_input.click()
        search_input.clear()
        search_input.send_keys("Articolo 1", Keys.ENTER)
        
        self.wait_for_search_results()

        self.find_cell(row=1, col=2).click()
        self.click_plugin("Giacenze")

        context = self.get_element("tab_22")
        totale = self.find_cell(row=1, col=2, context=context).text
        self.assertEqual(totale, "3,00")

        self.get_element('//a[@class="btn btn-xs btn-info"]', By.XPATH).click()

        modal = self.wait_modal()

        # TODO: Capire se si può togliere questo sleep
        time.sleep(1)

        # Non capisco che elemento vuole prendere e comunque non riesce a trovarlo
        #context = self.get_element('//div[@class="modal-body"]', By.XPATH)
        #totale = self.find_cell(row=1, col=1, context=context).text
        self.assertEqual(totale, "3,00")

        # Non capisco perchè cliccando in tutti i modi su questo pulsante non si chiude la modal
        # A volte si chiude a volte no
        #self.get_element('//button[@class="close"]/span[@aria-hidden="true"]', By.XPATH).click()
        close_btn = self.get_element('//button[@class="close"]', By.XPATH)
        close_btn.click()
        close_btn.click()

        self.navigateTo("Articoli")
        self.wait_loader()

        # Non ho capito perchè viene fatto ma nel dubbio lo lascio
        xpath = '//th[@id="th_Descrizione"]/i[@class="deleteicon fa fa-times"]'
        if (element:=self.exists(xpath, By.XPATH)):
            element.click()

    def statistiche(self):
        self.navigateTo("Articoli")
        self.wait_loader()

        # Trova il filtro Descrizione e scrive "Articolo 1"
        search_input = self.find_filter_input("Descrizione")
        search_input.send_keys("Articolo 1")

        # Clicca la prima riga
        self.find_cell(row=1, col=2).click()

        # Clicca il plugin Statistiche
        self.click_plugin("Statistiche")

        # Viene controllato il numero # a sinistra della tabella
        numero_1 = self.get_element('(//div[@id="tab_24"]//td[@class="text-center"])[1]', By.XPATH).text
        self.assertEqual(numero_1, "1")

        # Viene controllato il numero # a sinistra della tabella
        numero_2 = self.get_element('(//div[@id="tab_24"]//td[@class="text-center"])[2]', By.XPATH).text
        self.assertEqual(numero_2, "1")

        # Non ho capito perchè viene fatto ma nel dubbio lo lascio
        self.navigateTo("Articoli")
        self.wait_loader()

        # Non ho capito perchè viene fatto ma nel dubbio lo lascio
        xpath = '//th[@id="th_Descrizione"]/i[@class="deleteicon fa fa-times"]'
        if (element:=self.exists(xpath, By.XPATH)):
            element.click()

    def netto_clienti(self):
        self.navigateTo("Articoli")
        self.wait_loader()

        # Trova il filtro Descrizione e scrive "Articolo 1"
        search_input = self.find_filter_input("Descrizione")
        search_input.click()
        search_input.clear()
        search_input.send_keys("Articolo 1")

        # Clicca il primo risultato e clicca il plugin "Netto Client"
        self.find_cell(row=1, col=2).click()
        self.click_plugin("Netto clienti")

        # Nella select Cliente scrive "Cliente" e clicca il primo risultato
        results = self.get_select_search_results("Cliente", "Cliente")
        if len(results) > 0: results[0].click()

        self.get_element('//button[@class="btn btn-info btn-block"]', By.XPATH).click()

        self.wait_modal()

        self.get_element('(//label[@class="btn btn-default"])[4]', By.XPATH).click()
        
        prezzo_unitario = self.get_element('prezzo_unitario_fisso')
        prezzo_unitario.click()
        prezzo_unitario.send_keys("5", Keys.ENTER)

        # Verifica listino cliente
        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        self.wait_modal()

        results = self.get_select_search_results("Cliente", "Cliente")
        if len(results) > 0: results[0].click()

        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()

        results = self.get_select_search_results("Articolo", "001")
        if len(results) > 0: results[0].click()

        prezzo = self.get_element('//tbody[@id="righe"]//tr[1]//td[9]', By.XPATH).text
        self.assertEqual(prezzo, "5,00 €")

        self.delete_and_confirm()

        self.expandSidebar("Magazzino")
        self.navigateTo("Articoli")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()

        self.click_plugin("Netto clienti")

        # Modifica listino cliente
        self.get_element('//button[@class="btn btn-xs btn-warning"]', By.XPATH).click()

        prezzo_unitario = self.get_element('prezzo_unitario_fisso', By.ID)
        prezzo_unitario.send_keys(Keys.BACK_SPACE)
        prezzo_unitario.send_keys("2", Keys.ENTER)

        prezzo = self.get_element('//div[@id="tab_27"]//tr[3]//td[4]', By.XPATH).text
        self.assertEqual(prezzo[0:6], "2,00 €")

        # Elimina listino cliente
        self.get_element('//button[@class="btn btn-xs btn-warning"]', By.XPATH).click()
        self.get_element('(//label[@class="btn btn-default"]).click()[3]').click()
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()

        messaggio = self.get_element('//div[@id="tab_27"]//div[@class="alert alert-info"]', By.XPATH).text
        self.assertEqual(messaggio, "Nessuna informazione disponibile...")

        self.navigateTo("Articoli")
        self.wait_loader()

        if (filter_icon:=self.exists('//th[@id="th_Descrizione"]/i[@class="deleteicon fa fa-times"]', By.XPATH)):
            filter_icon.click()

    def aggiorna_prezzo_acquisto(self):
        self.navigateTo("Articoli")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        self.wait_modal()

        codice_input = self.get_element('//input[@id="codice"]', By.XPATH)
        codice_input.click()
        codice_input.clear()
        codice_input.send_keys("08")

        descrizione_input = self.get_element('//textarea[@id="descrizione"]', By.XPATH)
        descrizione_input.send_keys("Prova")

        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()

        prezzo_acquisto = self.get_element('//input[@id="prezzo_acquisto"]', By.XPATH)
        prezzo_acquisto.clear()
        prezzo_acquisto.click()
        prezzo_acquisto.send_keys("1")

        prezzo_vendita = self.get_element('//input[@id="prezzo_vendita"]', By.XPATH)
        prezzo_vendita.clear()
        prezzo_vendita.click()
        prezzo_vendita.send_keys("1")

        self.get_element('//button[@id="save"]', By.XPATH).click()

        self.navigateTo("Articoli")
        self.wait_loader()

        search_input = self.find_filter_input("Codice")
        search_input.click()
        search_input.clear()
        search_input.send_keys("08", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()
        self.get_element('//a[@data-op="change_purchase_price"]', By.XPATH).click()

        percentuale_input = self.get_element('//input[@id="percentuale"]', By.XPATH)
        percentuale_input.clear()
        percentuale_input.click()
        percentuale_input.send_keys(Keys.BACKSPACE,Keys.BACKSPACE, "10", Keys.ENTER)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()

        prezzo = self.get_element('//tbody//tr//td[8]', By.XPATH).text
        self.assertEqual(prezzo, "1,10")

        self.get_element('//th[@id="th_Codice"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def aggiorna_prezzo_vendita(self):
        self.navigateTo("Articoli")
        self.wait_loader()

        search_input = self.find_filter_input("Codice")
        search_input.click()
        search_input.clear()
        search_input.send_keys("08", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()
        self.get_element('//a[@data-op="change_sale_price"]', By.XPATH).click()

        self.get_element('//span[@id="select2-prezzo_partenza-container"]', By.XPATH).click()

        prezzo_input = self.get_element('//input[@class="select2-search__field"]', By.XPATH)
        prezzo_input.send_keys("Prezzo di vendita")

        self.get_element('//ul[@id="select2-prezzo_partenza-results"]', By.XPATH).click()

        percentuale_input = self.get_element('//input[@id="percentuale"]', By.XPATH)
        percentuale_input.click()
        percentuale_input.clear()
        percentuale_input.send_keys("20")

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()

        prezzo = self.get_element('//tbody//tr//td[9]', By.XPATH).text
        self.assertEqual(prezzo, "0,98")

        self.get_element('//th[@id="th_Codice"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def coefficiente_vendita(self):
        self.navigateTo("Articoli")
        self.wait_loader()

        search_input = self.find_filter_input("Codice")
        search_input.click()
        search_input.clear()
        search_input.send_keys("08", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()
        self.get_element('//a[@data-op="change_coefficient"]', By.XPATH).click()

        coefficiente_input = self.get_element('coefficiente')
        coefficiente_input.click()
        coefficiente_input.clear()
        coefficiente_input.send_keys("12")

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()

        prezzo = self.get_element('//tbody//tr[1]//td[9]//div', By.XPATH).text
        self.assertEqual(prezzo, "13,20")

        self.get_element('//th[@id="th_Codice"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def aggiorna_quantita(self):
        self.navigateTo("Articoli")
        self.wait_loader()

        search_input = self.find_filter_input("Codice")
        search_input.click()
        search_input.clear()
        search_input.send_keys("08", Keys.ENTER)
        self.wait_for_search_results()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()
        self.get_element('//a[@data-op="change_quantity"]', By.XPATH).click()

        qta_input = self.get_element('//input[@id="qta"]', By.XPATH)
        qta_input.click()
        qta_input.clear()
        qta_input.send_keys("3")

        descrizione_input = self.get_element('//input[@id="descrizione"]', By.XPATH)
        descrizione_input.send_keys("test")

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()

        quantita = self.get_element('//tbody//tr//td[10]', By.XPATH).text
        self.assertEqual(quantita, "3,00")

        self.get_element('//th[@id="th_Codice"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def crea_preventivo(self):
        self.navigateTo("Articoli")
        self.wait_loader()

        search_input = self.find_filter_input("Codice")
        search_input.click()
        search_input.clear()
        search_input.send_keys("08", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()
        self.get_element('//a[@data-op="create_estimate"]', By.XPATH).click()

        nome_input = self.get_element('nome')
        nome_input.click()
        nome_input.clear()
        nome_input.send_keys("Prova")
    
        results = self.get_select_search_results("Cliente", "Cliente")
        if len(results) > 0: results[0].click()

        results = self.get_select_search_results("Sezionale", "Standard preventivi")
        if len(results) > 0: results[0].click()
        
        results = self.get_select_search_results("Tipo di attività", "Generico")
        if len(results) > 0: results[0].click()

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()
        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()

        self.expandSidebar("Magazzino")
        self.navigateTo("Articoli")
        self.wait_loader()

        self.get_element('//th[@id="th_Codice"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def aggiorna_iva(self):
        self.navigateTo("Articoli")
        self.wait_loader()

        search_input = self.find_filter_input("Codice")
        search_input.click()
        search_input.clear()
        search_input.send_keys("08", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()
        self.get_element('//a[@data-op="change_vat"]', By.XPATH).click()

        results = self.get_select_search_results("Iva", "Iva 10%")
        if len(results) > 0: results[0].click()

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()

        iva = self.get_element('//span[@id="select2-idiva_vendita-container"]', By.XPATH).text
        self.assertEqual(iva[2:20], "10 - Aliq. Iva 10%")

        self.navigateTo("Articoli")
        self.wait_loader()

        self.get_element('//th[@id="th_Codice"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def aggiorna_unita_misura(self):
        self.navigateTo("Articoli")
        self.wait_loader()

        search_input = self.find_filter_input("Codice")
        search_input.click()
        search_input.clear()
        search_input.send_keys("08", Keys.ENTER)
        self.wait_for_search_results()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()
        self.get_element('//a[@data-op="change_unit"]', By.XPATH).click()

        results = self.get_select_search_results("Unità di misura", "pz")
        if len(results) > 0: results[0].click()

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.get_element('(//i[@class="fa fa-plus"])[2]', By.XPATH).click()

        unita_misura = self.get_element('//span[@id="select2-um-container"]', By.XPATH).text
        self.assertEqual(unita_misura[2:5], "pz")

        self.navigateTo("Articoli")
        self.wait_loader()

        self.get_element('//th[@id="th_Codice"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def conto_predefinito_acquisto(self):
        self.navigateTo("Articoli")
        self.wait_loader()

        search_input = self.find_filter_input("Codice")
        search_input.click()
        search_input.clear()
        search_input.send_keys("08", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()
        self.get_element('//a[@data-op="change_purchase_account"]', By.XPATH).click()

        results = self.get_select_search_results("Conto acquisto", "Fabbricati")
        if len(results) > 0: results[0].click()

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()

        conto = self.get_element('//span[@id="select2-idconto_acquisto-container"]', By.XPATH).text
        self.assertEqual(conto[2:24], "220.000010 Fabbricati")

        self.navigateTo("Articoli")
        self.wait_loader()

        self.get_element('//th[@id="th_Codice"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def conto_predefinito_vendita(self):
        self.navigateTo("Articoli")
        self.wait_loader()

        search_input = self.find_filter_input("Codice")
        search_input.click()
        search_input.clear()
        search_input.send_keys("08", Keys.ENTER)
        self.wait_for_search_results()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()

        self.get_element('//a[@data-op="change_sale_account"]', By.XPATH).click()

        results = self.get_select_search_results("Conto vendita", "Automezzi")
        if len(results) > 0: results[0].click()

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()

        conto = self.get_element('//span[@id="select2-idconto_vendita-container"]', By.XPATH).text
        self.assertEqual(conto[2:24], "220.000030 Automezzi")

        self.navigateTo("Articoli")
        self.wait_loader()

        self.get_element('//th[@id="th_Codice"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def imposta_provvigione(self):
        self.navigateTo("Articoli")
        self.wait_loader()

        search_input = self.find_filter_input("Codice")
        search_input.click()
        search_input.clear()
        search_input.send_keys("08", Keys.ENTER)
        self.wait_for_search_results()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()
        self.get_element('//a[@data-op="set_commission"]', By.XPATH).click()

        results = self.get_select_search_results("Agente")
        if len(results) > 0: results[0].click()

        provvigione_input = self.get_element('provvigione')
        provvigione_input.click()
        provvigione_input.clear()
        provvigione_input.send_keys("10")

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.click_plugin("Provvigioni")

        provvigione = self.get_element('(//div[@id="tab_43" ]//tr[1]//td[3]//div)[2]', By.XPATH).text
        self.assertEqual(provvigione, "10.00 %")

        self.navigateTo("Articoli")
        self.wait_loader()

        self.get_element('//th[@id="th_Codice"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def aggiorna_prezzo_unitario(self):
        self.navigateTo("Articoli")
        self.wait_loader()

        search_input = self.find_filter_input("Codice")
        search_input.click()
        search_input.clear()
        search_input.send_keys("08", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.click_plugin("Listino fornitori")
        self.wait_loader()

        results = self.get_select_search_results("Fornitore", "Fornitore", label_for="id_fornitore_informazioni")
        if len(results) > 0: results[0].click()

        self.get_element('//button[@class="btn btn-info"]', By.XPATH).click()

        qta_minima = self.get_element('//input[@id="qta_minima"]', By.XPATH)
        qta_minima.click()
        qta_minima.clear()
        qta_minima.send_keys("100")

        giorni_consegna = self.get_element('//input[@id="giorni_consegna"]', By.XPATH)
        giorni_consegna.click()
        giorni_consegna.clear()
        giorni_consegna.send_keys("15")

        self.get_element('//div[@class="modal-content"]//div[@class="btn-group checkbox-buttons"]', By.XPATH).click()

        prezzo_unitario = self.get_element('prezzo_unitario_fisso')
        prezzo_unitario.click()
        prezzo_unitario.clear()
        prezzo_unitario.send_keys("15", Keys.ENTER)

        self.navigateTo("Listini")
        self.wait_loader()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()
        self.get_element('//a[@data-op="change_prezzo"]', By.XPATH).click()

        percentuale_input = self.get_element('percentuale')
        percentuale_input.click()
        percentuale_input.clear()
        percentuale_input.send_keys("20")

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()

        prezzo = self.get_element('(//tr[1]//td[8])[2]', By.XPATH).text
        self.assertEqual(prezzo, "18,00")

        self.navigateTo("Listini")
        self.wait_loader()

        self.get_element('//tbody//tr//td', By.XPATH).click()

        self.navigateTo("Articoli")
        self.wait_loader()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//th[@id="th_Codice"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def copia_listini(self):
        self.navigateTo("Listini")
        self.wait_loader()

        segment_span = self.get_element('//span[@id="select2-id_segment_-container"]', By.XPATH)
        segment_span.click()

        segment_input = self.get_element('//input[@aria-controls="select2-id_segment_-results"]', By.XPATH)
        segment_input.click()
        segment_input.send_keys("Fornitori", Keys.ENTER)

        results_xpath = "select2-id_segment_-results"
        # 4. Attendi che il caricamento termini (loading-results)
        loading_li_xpath = f'.//ul[@id="{results_xpath}"]/li[contains(@class, "loading-results")]'
        loading_elements = self.driver.find_elements(By.XPATH, loading_li_xpath)
        if loading_elements:
            self.wait_driver.until(EC.invisibility_of_element_located((By.XPATH, loading_li_xpath)))

        results = self.wait_driver.until(lambda d: self.driver.find_elements(By.ID, results_xpath))
        if len(results) > 0: results[0].click()

        for i in range(5): self.wait_loader()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()

        self.get_element('//a[@data-op="copy_listino"]', By.XPATH).click()

        multiple_select = self.get_element('//span[@class="select2-selection select2-selection--multiple"]', By.XPATH)
        multiple_select.send_keys("Estero", Keys.ENTER)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()

        self.get_element('//tbody//tr//td', By.XPATH).click()

        search_input = self.find_filter_input("Ragione sociale")
        search_input.click()
        search_input.clear()
        search_input.send_keys("Fornitore Estero", Keys.ENTER)

        articolo = self.get_element('//tbody//tr//td[2]', By.XPATH).text
        self.assertEqual(articolo, "08 - Prova")

        self.navigateTo("Articoli")
        self.wait_loader()

        search_input = self.find_filter_input("Codice")
        search_input.send_keys("08", Keys.ENTER)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()

        self.click_plugin("Listino fornitori")
        self.get_element('//a[@class="btn btn-secondary btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-warning"]', By.XPATH).click()
        self.get_element('(//label[@class="btn btn-default active"]).click()[4]').click()
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()

        self.navigateTo("Articoli")
        self.wait_loader()

        self.get_element('//th[@id="th_Codice"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def imposta_prezzo_da_fattura(self):
        self.expandSidebar("Acquisti")
        self.navigateTo("Fatture di acquisto")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        numero_esterno = self.get_element('numero_esterno')
        numero_esterno.click()
        numero_esterno.clear()
        numero_esterno.send_keys("04")

        results = self.get_select_search_results("Fornitore", "Fornitore")
        if len(results) > 0: results[0].click()

        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()

        results = self.get_select_search_results("Pagamento", "Assegno")
        if len(results) > 0: results[0].click()

        results = self.get_select_search_results("Articolo", "Articolo 1")
        if len(results) > 0: results[0].click()

        self.get_element('//button[@class="btn btn-primary tip tooltipstered"]', By.XPATH).click()
        self.get_element('//a[@class="btn btn-xs btn-warning"]', By.XPATH).click()

        prezzo_unitario = self.get_element('prezzo_unitario', By.ID)
        prezzo_unitario.click()
        prezzo_unitario.clear()
        prezzo_unitario.send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, "10", Keys.ENTER)

        self.close_toast_popups()

        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()
        self.get_element('save').click()

        self.expandSidebar("Magazzino")
        self.navigateTo("Articoli")
        self.wait_loader()

        search_input = self.find_filter_input("Codice")
        search_input.click()
        search_input.clear()
        search_input.send_keys("001", Keys.ENTER)
        self.wait_for_search_results()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()

        self.get_element('//a[@data-op="set_purchase_price_if_zero"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()

        prezzo = self.get_element('//tbody//tr//td[8]', By.XPATH).text
        self.assertEqual(prezzo, "20,00")

        self.get_element('(//i[@class="deleteicon fa fa-times"])[1]').click()

        self.expandSidebar("Acquisti")
        self.navigateTo("Fatture di acquisto")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()

        self.delete_and_confirm()

        self.expandSidebar("Magazzino")

    def stampa_etichette(self):
        self.navigateTo("Articoli")
        self.wait_loader()

        search_input = self.find_filter_input("Codice")
        search_input.click()
        search_input.clear()
        search_input.send_keys("08", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr/td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()
        self.get_element('//a[@data-op="print_labels"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()

        self.driver.switch_to.window(self.driver.window_handles[1])

        # TODO: Capire cosa vuole prendere dalla stampa
        #prezzo = self.get_element('(//div[@id="viewer"]//span)[3]', By.XPATH).text
        self.assertEqual(prezzo, "13,20 €")

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//th[@id="th_Codice"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()

    def elimina_selezionati(self):
        self.navigateTo("Articoli")
        self.wait_loader()

        search_input = self.find_filter_input("Codice")
        search_input.click()
        search_input.clear()
        search_input.send_keys("08", Keys.ENTER)

        self.wait_for_search_results()

        self.get_element('//tbody//tr//td', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click()

        self.get_element('//a[@data-op="delete_bulk"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()

        risultato = self.get_element('//tbody//tr//td', By.XPATH).text
        self.assertEqual(risultato, "La ricerca non ha portato alcun risultato.")

        self.get_element('//th[@id="th_Codice"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
