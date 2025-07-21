from common.Test import Test, get_html
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Impostazioni(Test):
    def setUp(self):
        super().setUp()

    def test_impostazioni_generali(self):
        pass
        ## TODO: Azienda predefinita

        # Nascondere la barra sinistra di default (2)
        #self.nascondi_barra_sx()

        # Cambio cifre decimali per importi (3)
        #self.cifre_decimali_importi()

        ## TODO: CSS personalizzato

        ## TODO: Attiva notifica di presenza utenti sul record

        ## TODO: Timeout notifica di presenza (minuti)

        # Prima pagina
        #self.prima_pagina()

        # Cifre decimali per quantità
        #self.cifre_decimali_quantita()

        ## TODO: Tempo di attesa ricerche in secondi

        ## TODO: Logo stampe

        # Abilita esportazione Excel e PDF 
        #self.esportazione_excel_pdf

        # Cambio valuta 
        #self.valuta()

        # Visualizza riferimento su ogni riga in stampa 
        #self.riferimento_riga_stampa()

        ## TODO: Lunghezza in pagine del buffer Datatables

        # Autocompletamento form 
        #self.autocompletamento_form()   #da finire

        ## TODO: Filigrana stampe

        ## TODO: attiva scorciatoie da tastiera

        ## TODO: Modifica viste di default

        ## TODO: Totali delle tabelle ristretti alla selezione

        ## TODO: Nascondere barra dei plugin di default

        ## TODO: Soft quota
        
        # Permetti selezione articoli con quantità minore o uguale a zero in Documenti di Vendita 
        #self.quantita_minore_uguale_zero()

        # Cambio periodo calendario 
        #self.periodo_calendario()

        # Permetti il superamento della soglia quantità dei documenti di origine 
        #self.superamento_soglia_quantita()

        # Aggiungi riferimento tra documenti
        #self.aggiungi_riferimento_documenti()

        # Aggiungi riferimento tra tutti i documenti collegati 
        #self.aggiungi_riferimenti_tutti_documenti()

        # Aggiungi le note delle righe tra documenti 
        #self.aggiungi_note_documenti()

        # Dimensione widget predefinita 
        #self.dimensione_widget_predefinita()

        ## TODO: Posizione del simbolo valuta

        ## TODO: Tile server osm

        ## TODO: Sistema di firma

        # Tipo di sconto predefinito 
        #self.tipo_sconto_predefinito()

        # Cifre decimali per importi in stampa 
        #self.importi_stampa()

        # Cifre decimali per quantità in stampa 
        #self.quantita_stampa()

        # Cifre decimali per totali in stampa 
        #self.totali_stampa()

        # Listino cliente predefinito 
        #self.listino_predefinito()

        # Cambio lingua 
        #self.lingua()

        ## TODO: Ridimensiona automaticamente le immagini caricate

        ## TODO: Larghezza per ridimensionamento immagini

        ## TODO: Gestore mappa

        ## TODO: Tile server satellite


    def nascondi_barra_sx(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[1]', By.XPATH).click() #attivo impostazione
        sleep(1)

        self.navigateTo("Impostazioni")
        self.wait_loader()
        sleep(1)

        self.get_element('//body[@class="sidebar-mini layout-fixed  sidebar-collapse"]', By.XPATH) #controlla se trova la classe sidebar-collapse
        #torno alle impostazioni di prima
        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[1]', By.XPATH).click() #disattivo impostazione
        sleep(1)

        self.navigateTo("Impostazioni")
        self.wait_loader()
        sleep(1)

    def cifre_decimali_importi(self):
        wait = WebDriverWait(self.driver, 20)
        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting47-container"]', By.XPATH).click()    #seleziono 4 cifre decimali per gli importi
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('4', Keys.ENTER)
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() #seleziono Cliente come anagrafica
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi
        self.wait_loader()

        self.get_element('//span[@id="select2-id_articolo-container"]', By.XPATH).click()  #aggiungo un articolo
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('Articolo 1')
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary tip tooltipstered"]', By.XPATH).click() #click su aggiungi
        sleep(1)

        importo=self.get_element('//tbody//tr[1]//td[9]', By.XPATH).text   #controllo se l'importo corrisponde a 20 euro con 4 cifre decimali
        self.assertEqual(importo, "20,0000 €")

        self.get_element('//a[@id="elimina"]', By.XPATH).click() #elimina fattura
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()
        #torno alle impostazioni di prima
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting47-container"]', By.XPATH).click()    #seleziono 2 cifre decimali per gli importi
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('2', Keys.ENTER)
        sleep(1)

    def prima_pagina(self):
        wait = WebDriverWait(self.driver, 20)  
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting59-container"]', By.XPATH).click()    #metto come prima pagina "Anagrafiche"
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Anagrafiche")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//ul[@id="select2-setting59-results"]//li[2]'))).click()
        sleep(1)

        self.get_element('//a[@class="nav-link bg-danger"]', By.XPATH).click() #logout
        self.wait_loader()
        sleep(1)

        #login
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="form-control"]'))).send_keys(self.getConfig('login.username'))
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="password"]'))).send_keys(self.getConfig('login.password')) #password da mettere prima del test
        self.get_element('//button[@class="btn btn-danger btn-block btn-flat"]', By.XPATH).click() 
        sleep(1)
        self.wait_loader()

        pagina=self.get_element('//a[@class="nav-link active"]', By.XPATH).text    #check se la prima pagina è quella delle Anagrafiche
        self.assertEqual(pagina[2:13], "Anagrafiche")
        #torno alle impostazioni di prima
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting59-container"]', By.XPATH).click()    #metto come prima pagina "Dashboard"
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Dashboard")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        sleep(1)

        self.get_element('//a[@class="nav-link bg-danger"]', By.XPATH).click() #logout
        self.wait_loader()
        sleep(1)

        #login
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="form-control"]'))).send_keys(self.getConfig('login.username'))
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="password"]'))).send_keys(self.getConfig('login.password')) #password da mettere prima del test
        self.get_element('//button[@class="btn btn-danger btn-block btn-flat"]', By.XPATH).click() 
        sleep(1)
        self.wait_loader()

    def cifre_decimali_quantita(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()
        sleep(1)

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() #seleziono Cliente come anagrafica
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi
        self.wait_loader()

        self.get_element('//span[@id="select2-id_articolo-container"]', By.XPATH).click()  #aggiungo un articolo
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('Articolo 1')
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary tip tooltipstered"]', By.XPATH).click() #click su aggiungi
        sleep(1)

        quantita_element = self.get_element('(//tbody[@id="righe"]//input, By.XPATH)[2]')   #check cifre decimali
        quantita = quantita_element.get_attribute("decimals")
        self.assertEqual(quantita, "2") 
        self.get_element('//a[@id="elimina"]', By.XPATH).click() #elimina fattura
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting60-container"]', By.XPATH).click()    #seleziono 4 cifre decimali per le quantità
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('4', Keys.ENTER)
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()
        sleep(1)

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() #seleziono Cliente come anagrafica
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi
        self.wait_loader()

        self.get_element('//span[@id="select2-id_articolo-container"]', By.XPATH).click()  #aggiungo un articolo
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('Articolo 1')
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary tip tooltipstered"]', By.XPATH).click() #click su aggiungi
        sleep(1)

        quantita_element = self.get_element('(//tbody[@id="righe"]//input, By.XPATH)[2]')   #check cifre decimali
        quantita = quantita_element.get_attribute("decimals")
        self.assertEqual(quantita, "4") 
        self.get_element('//a[@id="elimina"]', By.XPATH).click() #elimina fattura
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()
        #torno alle impostazioni di prima
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting60-container"]', By.XPATH).click()    #seleziono 2 cifre decimali per le quanità
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('2', Keys.ENTER)
        sleep(1)

    def esportazione_excel_pdf(self):
        wait = WebDriverWait(self.driver, 20)  
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[6]', By.XPATH).click()    #attiva impostazione
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[1]', By.XPATH).click()    #seleziono prima fattura
        self.get_element('//button[@class="btn btn-primary table-btn dropdown-toggle"]', By.XPATH).click() #click su esporta
        sleep(1)

        self.get_element('//ul[@class="dropdown-menu show"]//a[1]', By.XPATH).click()
        sleep(1)

        self.driver.close() #chiude scheda
        self.driver.switch_to.window(self.driver.window_handles[0]) #torna alla prima
        sleep(1)

        self.get_element('//button[@class="btn btn-primary table-btn dropdown-toggle"]', By.XPATH).click() #click su esporta
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//ul[@class="dropdown-menu show"]//a[2]'))) #controllo se c'è l'esporta excel
        self.get_element('//tbody//tr[1]//td[1]', By.XPATH).click()    #diseleziono prima fattura
        #torno alle impostazioni di prima
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[6]', By.XPATH).click()    #disattiva impostazione
        sleep(1)


    def valuta(self):
        wait = WebDriverWait(self.driver, 20)  
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting83-container"]', By.XPATH).click() #cambio valuta in sterline
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('Sterlina', Keys.ENTER)
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click() #apro prima fattura
        self.wait_loader()

        nuova_valuta=self.get_element('//tbody//tr[1]//td[5]//div//span', By.XPATH).text   #controllo se è cambiata la valuta
        self.assertEqual(nuova_valuta, "£")
        #torno alle impostazioni di prima
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting83-container"]', By.XPATH).click() #cambio valuta in euro
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('Euro', Keys.ENTER)
        sleep(1)

    def riferimento_riga_stampa(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[4]', By.XPATH).click()   #disattivo impostazione
        sleep(1)

        #crea ordine
        self.expandSidebar("Vendite")
        self.navigateTo("Ordini cliente")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su tasto +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica-container"]', By.XPATH).click()     #scelta di "Cliente" come anagrafica per l'ordine
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('Cliente')
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()   #click su tasto aggiungi
        self.wait_loader()
        #aggiungi articolo
        self.get_element('//span[@id="select2-id_articolo-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@class="select2-results__options select2-results__options--nested"]//li[1]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary tip tooltipstered"]', By.XPATH).click() #click su aggiungi
        sleep(1)

        #aggiungi articolo
        self.get_element('//span[@id="select2-id_articolo-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@class="select2-results__options select2-results__options--nested"]//li[1]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary tip tooltipstered"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #cambio stato
        self.get_element('//span[@id="select2-idstatoordine-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Accettato", Keys.ENTER)
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()
        #crea ddt
        self.get_element('//button[@class="btn btn-info dropdown-toggle "]', By.XPATH).click() #click su crea
        sleep(1)

        self.get_element('//ul[@class="dropdown-menu dropdown-menu-right show"]//a[3]', By.XPATH).click()  #click su crea ddt
        sleep(1)

        self.get_element('//span[@id="select2-id_causale_trasporto-container"]', By.XPATH).click() #causale trasporto
        sleep(1)

        self.get_element('//ul[@id="select2-id_causale_trasporto-results"]//li[1]', By.XPATH).click()
        self.get_element('//span[@id="select2-id_segment-container"]', By.XPATH).click()   #sezionale
        sleep(1)

        self.get_element('//ul[@id="select2-id_segment-results"]//li[1]', By.XPATH).click()
        self.get_element('//button[@id="submit_btn"]', By.XPATH).click()   #click su aggiungi
        self.wait_loader()
        #cambia stato
        self.get_element('//span[@id="select2-idstatoddt-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idstatoddt-results"]//li[2]', By.XPATH).click()    #stato evaso
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//button[@class="btn btn-info bound clickable"]', By.XPATH).click()  #crea fattura di vendita
        sleep(1)

        self.get_element('//button[@id="submit_btn"]', By.XPATH).click()   #click su aggiungi
        self.wait_loader()

        self.get_element('//a[@id="print-button_p"]', By.XPATH).click()    #stampa fattura
        sleep(1)

        self.driver.switch_to.window(self.driver.window_handles[1]) #cambia scheda
        sleep(1)

        primo_riferimento=self.get_element('(//div[@id="viewer"]//span, By.XPATH)[38]').text
        self.assertEqual(primo_riferimento[0:27], "Rif. ordine cliente num. 02")
        secondo_riferimento=self.get_element('(//div[@id="viewer"]//span, By.XPATH)[39]').text
        self.assertEqual(secondo_riferimento[0:27], "Ddt in uscita num. 02")
        self.driver.close() #chiude scheda
        self.driver.switch_to.window(self.driver.window_handles[0]) #torna alla prima
        sleep(1)
        #elimina fattura
        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()
        #elimina ordine
        self.navigateTo("Ordini cliente")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()
        #elimina ddt
        self.expandSidebar("Magazzino") 
        self.navigateTo("Ddt in uscita")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()
        #torna alle impostazioni di prima
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[4]', By.XPATH).click()   #attivo impostazione
        sleep(1)

        #crea ordine
        self.expandSidebar("Vendite")
        self.navigateTo("Ordini cliente")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su tasto +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica-container"]', By.XPATH).click()     #scelta di "Cliente" come anagrafica per l'ordine
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('Cliente')
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()   #click su tasto aggiungi
        self.wait_loader()
        #aggiungi articolo
        self.get_element('//span[@id="select2-id_articolo-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@class="select2-results__options select2-results__options--nested"]//li[1]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary tip tooltipstered"]', By.XPATH).click() #click su aggiungi
        sleep(1)

        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()   #click su tasto aggiungi
        self.wait_loader()
        #aggiungi articolo
        self.get_element('//span[@id="select2-id_articolo-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@class="select2-results__options select2-results__options--nested"]//li[1]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary tip tooltipstered"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #cambio stato
        self.get_element('//span[@id="select2-idstatoordine-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Accettato", Keys.ENTER)
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()
        #crea ddt
        self.get_element('//button[@class="btn btn-info dropdown-toggle "]', By.XPATH).click() #click su crea
        sleep(1)

        self.get_element('//ul[@class="dropdown-menu dropdown-menu-right show"]//a[3]', By.XPATH).click()  #click su crea ddt
        sleep(1)

        self.get_element('//span[@id="select2-id_causale_trasporto-container"]', By.XPATH).click() #causale trasporto
        sleep(1)

        self.get_element('//ul[@id="select2-id_causale_trasporto-results"]//li[1]', By.XPATH).click()
        self.get_element('//span[@id="select2-id_segment-container"]', By.XPATH).click()   #sezionale
        sleep(1)

        self.get_element('//ul[@id="select2-id_segment-results"]//li[1]', By.XPATH).click()
        self.get_element('//button[@id="submit_btn"]', By.XPATH).click()   #click su aggiungi
        self.wait_loader()
        #cambia stato
        self.get_element('//span[@id="select2-idstatoddt-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idstatoddt-results"]//li[2]', By.XPATH).click()    #stato evaso
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//button[@class="btn btn-info bound clickable"]', By.XPATH).click()  #crea fattura di vendita
        sleep(1)

        self.get_element('//button[@id="submit_btn"]', By.XPATH).click()   #click su aggiungi
        self.wait_loader()

        self.get_element('//a[@id="print-button_p"]', By.XPATH).click()    #stampa fattura
        sleep(1)

        self.driver.switch_to.window(self.driver.window_handles[1]) #cambia scheda
        sleep(1)

        primo_riferimento=self.get_element('(//div[@id="viewer"]//span, By.XPATH)[40]').text
        self.assertEqual(primo_riferimento[0:27], "Rif. ordine cliente num. 02")

        self.driver.close() #chiude scheda
        self.driver.switch_to.window(self.driver.window_handles[0]) #torna alla prima
        sleep(1)
        #elimina fattura
        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()
        #elimina ordine
        self.navigateTo("Ordini cliente")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()
        #elimina ddt
        self.expandSidebar("Magazzino") 
        self.navigateTo("Ddt in uscita")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()



    def autocompletamento_form(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting93-container"]', By.XPATH).click()    #autocopletamento on
        sleep(1)

        self.get_element('//ul[@id="select2-setting93-results"]//li[1]', By.XPATH).click()
        sleep(1)

        self.navigateTo("Anagrafiche")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su +
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="ragione_sociale_add"]'))).send_keys('Prova')
        self.get_element('//span[@class="select2-selection select2-selection--multiple"]', By.XPATH).click()   #tipo anagrafica cliente
        sleep(1)

        self.get_element('//ul[@id="select2-idtipoanagrafica_add-results"]//li[2]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()
        self.wait_loader()

        #elimino anagrafica
        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Anagrafiche")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su +
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="ragione_sociale_add"]'))).send_keys('Pro')
        sleep(1)

        #controllo se appare il suggerimento
        self.get_element('//button[@class="close"]', By.XPATH).click()
        sleep(1)
        #torno alle impostazioni di prima
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting93-container"]', By.XPATH).click()    #autocompletamento off
        sleep(1)

        self.get_element('//ul[@id="select2-setting93-results"]//li[2]', By.XPATH).click()
        sleep(1)


    def quantita_minore_uguale_zero(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()
        sleep(1)

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() #seleziono Cliente come anagrafica
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi
        self.wait_loader()

        self.get_element('//span[@id="select2-id_articolo-container"]', By.XPATH).click()  #aggiungo un articolo
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('Vestito')
        sleep(1)

        self.get_element('//ul[@class="select2-results__options select2-results__options--nested"]//li[1]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="btn btn-primary tip tooltipstered"]', By.XPATH).click() #click su aggiungi
        sleep(1) 

        messaggio=self.get_element('//div[@id="swal2-content"]', By.XPATH).text    #check se esce l'errore
        self.assertEqual(messaggio, "Nessun articolo corrispondente a magazzino")
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-primary"]', By.XPATH).click()  #esce dal errore
        sleep(1)

        self.get_element('//a[@id="elimina"]', By.XPATH).click() #elimina fattura
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[8]', By.XPATH).click() #attiva impostazione
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()
        sleep(1)

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() #seleziono Cliente come anagrafica
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi
        self.wait_loader()

        self.get_element('//span[@id="select2-id_articolo-container"]', By.XPATH).click()  #aggiungo un articolo
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('Vestito')
        sleep(1)

        self.get_element('//ul[@class="select2-results__options select2-results__options--nested"]//li[1]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="btn btn-primary tip tooltipstered"]', By.XPATH).click() #click su aggiungi
        sleep(1)

        articolo=self.get_element('//tbody[@id="righe"]//td[2]', By.XPATH).text    #check se l'articolo è stato aggiunto
        self.assertEqual(articolo, "1")
        self.get_element('//a[@id="elimina"]', By.XPATH).click() #elimina fattura
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()
        #torno alle impostazioni di prima
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[8]', By.XPATH).click() #disattiva impostazione
        sleep(1)



    def periodo_calendario(self):
        wait = WebDriverWait(self.driver, 20)  
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//input[@id="setting135"]', By.XPATH).click()
        data_inizio=self.get_element('//input[@id="setting135"]', By.XPATH) #cambio inizio periodo
        data_inizio.clear()
        data_inizio.send_keys("01/01/2025", Keys.ENTER)
        self.get_element('//input[@id="setting135"]', By.XPATH).click()
        data_fine=self.get_element('//input[@id="setting136"]', By.XPATH) #cambio fine periodo
        data_fine.clear()
        data_fine.send_keys("30/06/2025", Keys.ENTER)
        sleep(1)

        self.get_element('//a[@class="nav-link bg-danger"]', By.XPATH).click() #logout
        self.wait_loader()
        sleep(1)

        #login
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="form-control"]'))).send_keys(self.getConfig('login.username'))
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="password"]'))).send_keys('') #password da mettere prima del test
        self.get_element('//button[@class="btn btn-danger btn-block btn-flat"]', By.XPATH).click() 
        sleep(1)
        self.wait_loader()

        data=self.get_element('//a[@class="nav-link text-danger"]', By.XPATH).text #controllo se la data è cambiata
        self.assertEqual(data, "01/01/2025 - 30/06/2025")
        #torno alle impostazioni di prima
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        data_inizio=self.get_element('//input[@id="setting135"]', By.XPATH) #cambio inizio periodo
        data_inizio.clear()
        data_inizio.send_keys("01/01/2025", Keys.ENTER)
        data_fine=self.get_element('//input[@id="setting136"]', By.XPATH) #cambio fine periodo
        data_fine.clear()
        data_fine.send_keys("31/12/2025", Keys.ENTER)
        self.get_element('//a[@class="nav-link bg-danger"]', By.XPATH).click() #logout
        self.wait_loader()

        #login
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="form-control"]'))).send_keys(self.getConfig('login.username'))
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="password"]'))).send_keys(self.getConfig('login.password')) #password da mettere prima del test
        self.get_element('//button[@class="btn btn-danger btn-block btn-flat"]', By.XPATH).click() 
        sleep(1)
        self.wait_loader()

    def superamento_soglia_quantita(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Impostazioni")
        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[9]', By.XPATH).click()    #attivo impostazione
        sleep(1)
        #crea attività
        self.navigateTo("Attività")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()  #click su +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica-container"]', By.XPATH).click() #seleziono Cliente come anagrafica
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-dropdown select2-dropdown--below"]//input'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//span[@id="select2-idtipointervento-container"]', By.XPATH).click() #seleziono Generico come tipo di intervento
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-search select2-search--dropdown"]//input'))).send_keys("Generico")
        sleep(1)

        self.get_element('//li[@class="select2-results__option select2-results__option--highlighted"]', By.XPATH).click()  #click su primo risultato
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//iframe[@class="cke_wysiwyg_frame cke_reset"])[1]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//iframe[@class="cke_wysiwyg_frame cke_reset"])[1]'))).send_keys("Test")   #scrivo "Test" come richiesta
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()   #click su Aggiungi
        self.wait_loader()
        sleep(1)
        #aggiungi articolo
        self.get_element('//span[@id="select2-id_articolo-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@class="select2-results__options select2-results__options--nested"]//li[1]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary tip tooltipstered"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #cambio stato
        self.get_element('//span[@id="select2-idstatointervento-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idstatointervento-results"]//li[1]', By.XPATH).click() #imposto stato "Completato"
        self.get_element('//button[@id="save"]', By.XPATH).click() #click su salva
        self.wait_loader()

        #creo preventivo
        self.expandSidebar("Vendite")
        self.navigateTo("Preventivi")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su +
        sleep(1)
        #nome
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="nome"]'))).send_keys('Test')
        #cliente
        self.get_element('//span[@id="select2-idanagrafica-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idanagrafica-results"]//li[2]', By.XPATH).click()
        #tipo di attività
        self.get_element('//span[@id="select2-idtipointervento-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idtipointervento-results"]//li[1]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()   #click su aggiungi
        self.wait_loader()
        #aggiungi articolo
        self.get_element('//span[@id="select2-id_articolo-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@class="select2-results__options select2-results__options--nested"]//li[1]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary tip tooltipstered"]', By.XPATH).click() #click su aggiungi
        sleep(1)

        self.driver.execute_script('window.scrollTo(0,0)')
        sleep(1)

        #cambio stato
        self.get_element('//span[@id="select2-idstato-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idstato-results"]//li[1]', By.XPATH).click() #imposto stato "Accettato"
        self.get_element('//button[@id="save"]', By.XPATH).click() #click su salva
        self.wait_loader()

        #crea contratto
        self.navigateTo("Contratti")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="nome"]'))).send_keys("Test")
        self.get_element('//span[@id="select2-idanagrafica-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="data_accettazione"]'))).send_keys("01/01/2025")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="data_conclusione"]'))).send_keys("31/12/2025")
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()
        self.wait_loader()
        #aggiungi articolo
        self.get_element('//span[@id="select2-id_articolo-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@class="select2-results__options select2-results__options--nested"]//li[1]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary tip tooltipstered"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #cambio stato
        self.get_element('//span[@id="select2-idstato-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idstato-results"]//li[1]', By.XPATH).click() #imposto stato "Accettato"
        self.get_element('//button[@id="save"]', By.XPATH).click() #click su salva
        self.wait_loader()
        #creo ddt
        self.expandSidebar("Magazzino")
        self.navigateTo("Ddt in uscita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click() #click su +
        sleep(1)
        #seleziono destinatario
        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        #seleziono causale trasporto
        self.get_element('//span[@id="select2-idcausalet-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Conto lavorazione")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi
        self.wait_loader()

        #aggiungi articolo
        self.get_element('//span[@id="select2-id_articolo-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@class="select2-results__options select2-results__options--nested"]//li[1]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary tip tooltipstered"]', By.XPATH).click() #click su aggiungi
        sleep(1)

        self.get_element('//span[@id="select2-idstatoddt-container"]', By.XPATH).click() #cambio stato in evaso
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Evaso", Keys.ENTER)
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()
        #crea ordine
        self.expandSidebar("Vendite")
        self.navigateTo("Ordini cliente")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su tasto +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica-container"]', By.XPATH).click()     #scelta di "Cliente" come anagrafica per l'ordine
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('Cliente')
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()   #click su tasto aggiungi
        self.wait_loader()
        #aggiungi articolo
        self.get_element('//span[@id="select2-id_articolo-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@class="select2-results__options select2-results__options--nested"]//li[1]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary tip tooltipstered"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #cambio stato
        self.get_element('//span[@id="select2-idstatoordine-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Accettato", Keys.ENTER)
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()
        
        #crea fattura
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() #seleziono Cliente come anagrafica
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi
        self.wait_loader()

        self.get_element('//button[@class="btn btn-primary dropdown-toggle"]', By.XPATH).click() #click su altro
        #attività
        self.get_element('//ul[@class="dropdown-menu dropdown-menu-right show"]//a[3]', By.XPATH).click()
        sleep(1)

        self.get_element('//span[@id="select2-idintervento-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idintervento-results"]//li[2]', By.XPATH).click()  #seleziona attività creata prima
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()    #click su aggiungi
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//tbody[@id="righe"]//tr[2]//td[4]//input'))).send_keys("2", Keys.ENTER) #imposta quantità a 2
        sleep(1)

        qta_element = self.get_element('//tbody[@id="righe"]//tr[2]//td[4]//input', By.XPATH)    #controllo se la quantità è cambiata
        qta = qta_element.get_attribute("value")
        self.assertEqual(qta, "2,00") 
        self.get_element('//input[@id="check_all"]', By.XPATH).click() #elimino righe
        self.get_element('//button[@id="elimina_righe"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-primary"]', By.XPATH).click()
        sleep(1)
        #preventivi
        self.get_element('//button[@class="btn btn-primary dropdown-toggle"]', By.XPATH).click() #click su altro
        self.get_element('//ul[@class="dropdown-menu dropdown-menu-right show"]//a[4]', By.XPATH).click()
        sleep(1)

        self.get_element('//span[@id="select2-id_documento-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-id_documento-results"]//li[2]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//tbody[@id="righe_documento_importato"]//tr[1]//td[4]//input'))).send_keys("2", Keys.ENTER)
        sleep(1)

        qta_element = self.get_element('//tbody[@id="righe"]//tr[1]//td[4]//input', By.XPATH)    #controllo se la quantità è cambiata
        qta = qta_element.get_attribute("value")
        self.assertEqual(qta, "2,00") 
        self.get_element('//input[@id="check_all"]', By.XPATH).click() #elimino righe
        self.get_element('//button[@id="elimina_righe"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-primary"]', By.XPATH).click()
        sleep(1)
        #contratti
        self.get_element('//button[@class="btn btn-primary dropdown-toggle"]', By.XPATH).click() #click su altro
        self.get_element('//ul[@class="dropdown-menu dropdown-menu-right show"]//a[5]', By.XPATH).click()
        sleep(1)

        self.get_element('//span[@id="select2-id_documento-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-id_documento-results"]//li[3]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//tbody[@id="righe_documento_importato"]//tr[1]//td[4]//input'))).send_keys("2", Keys.ENTER)
        sleep(1)

        qta_element = self.get_element('//tbody[@id="righe"]//tr[1]//td[4]//input', By.XPATH)    #controllo se la quantità è cambiata
        qta = qta_element.get_attribute("value")
        self.assertEqual(qta, "2,00") 
        self.get_element('//input[@id="check_all"]', By.XPATH).click() #elimino righe
        self.get_element('//button[@id="elimina_righe"]', By.XPATH).click()
        sleep(1)
        #ddt
        self.get_element('//button[@class="btn btn-primary dropdown-toggle"]', By.XPATH).click() #click su altro
        self.get_element('//ul[@class="dropdown-menu dropdown-menu-right show"]//a[6]', By.XPATH).click()
        sleep(1)

        self.get_element('//span[@id="select2-id_documento-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-id_documento-results"]//li[1]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//tbody[@id="righe_documento_importato"]//tr[1]//td[4]//input'))).send_keys("2", Keys.ENTER)
        sleep(1)

        qta_element = self.get_element('//tbody[@id="righe"]//tr[1]//td[4]//input', By.XPATH)    #controllo se la quantità è cambiata
        qta = qta_element.get_attribute("value")
        self.assertEqual(qta, "2,00") 
        self.get_element('//input[@id="check_all"]', By.XPATH).click() #elimino righe
        self.get_element('//button[@id="elimina_righe"]', By.XPATH).click()
        sleep(1)
        #ordine
        self.get_element('//button[@class="btn btn-primary dropdown-toggle"]', By.XPATH).click() #click su altro
        self.get_element('//ul[@class="dropdown-menu dropdown-menu-right show"]//a[7]', By.XPATH).click()
        sleep(1)

        self.get_element('//span[@id="select2-id_documento-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-id_documento-results"]//li[1]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//tbody[@id="righe_documento_importato"]//tr[1]//td[4]//input'))).send_keys("2", Keys.ENTER)
        sleep(1)

        qta_element = self.get_element('//tbody[@id="righe"]//tr[1]//td[4]//input', By.XPATH)    #controllo se la quantità è cambiata
        qta = qta_element.get_attribute("value")
        self.assertEqual(qta, "2,00") 
        self.get_element('//input[@id="check_all"]', By.XPATH).click() #elimino righe
        self.get_element('//button[@id="elimina_righe"]', By.XPATH).click()
        sleep(1)

        #torno alle impostazioni di prima
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[9]', By.XPATH).click()    #disattivo impostazione
        sleep(1)
        
        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()    #apro fattura
        self.wait_loader()

        #attività
        self.get_element('//ul[@class="dropdown-menu dropdown-menu-right show"]//a[3]', By.XPATH).click()
        sleep(1)

        self.get_element('//span[@id="select2-idintervento-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idintervento-results"]//li[3]', By.XPATH).click()  #seleziona attività creata prima
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()    #click su aggiungi
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//tbody[@id="righe"]//tr[2]//td[4]//input'))).send_keys("2", Keys.ENTER) #imposta quantità a 2
        sleep(1)

        qta_element = self.get_element('//tbody[@id="righe"]//tr[2]//td[4]//input', By.XPATH)    #controllo se la quantità è cambiata a 1 e non a 2
        qta = qta_element.get_attribute("value")
        self.assertEqual(qta, "1") 
        self.get_element('//input[@id="check_all"]', By.XPATH).click() #elimino righe
        self.get_element('//button[@id="elimina_righe"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-primary"]', By.XPATH).click()
        sleep(1)

        #preventivi
        self.get_element('//button[@class="btn btn-primary dropdown-toggle"]', By.XPATH).click() #click su altro
        self.get_element('//ul[@class="dropdown-menu dropdown-menu-right show"]//a[4]', By.XPATH).click()
        sleep(1)

        self.get_element('//span[@id="select2-id_documento-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-id_documento-results"]//li[2]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//tbody[@id="righe_documento_importato"]//tr[1]//td[4]//input'))).send_keys("2", Keys.ENTER)
        sleep(1)

        qta_element = self.get_element('//tbody[@id="righe"]//tr[1]//td[4]//input', By.XPATH)    #controllo se la quantità è cambiata a 1 e non a 2
        qta = qta_element.get_attribute("value")
        self.assertEqual(qta, "1")
        self.get_element('//input[@id="check_all"]', By.XPATH).click() #elimino righe
        self.get_element('//button[@id="elimina_righe"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-primary"]', By.XPATH).click()
        sleep(1)
        #contratti
        self.get_element('//button[@class="btn btn-primary dropdown-toggle"]', By.XPATH).click() #click su altro
        self.get_element('//ul[@class="dropdown-menu dropdown-menu-right show"]//a[5]', By.XPATH).click()
        sleep(1)

        self.get_element('//span[@id="select2-id_documento-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-id_documento-results"]//li[3]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//tbody[@id="righe_documento_importato"]//tr[1]//td[4]//input'))).send_keys("2", Keys.ENTER)
        sleep(1)

        qta_element = self.get_element('//tbody[@id="righe"]//tr[1]//td[4]//input', By.XPATH)    #controllo se la quantità è cambiata a 1 e non a 2
        qta = qta_element.get_attribute("value")
        self.assertEqual(qta, "1")
        self.get_element('//input[@id="check_all"]', By.XPATH).click() #elimino righe
        self.get_element('//button[@id="elimina_righe"]', By.XPATH).click()
        sleep(1)
        #ddt
        self.get_element('//button[@class="btn btn-primary dropdown-toggle"]', By.XPATH).click() #click su altro
        self.get_element('//ul[@class="dropdown-menu dropdown-menu-right show"]//a[6]', By.XPATH).click()
        sleep(1)

        self.get_element('//span[@id="select2-id_documento-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-id_documento-results"]//li[1]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//tbody[@id="righe_documento_importato"]//tr[1]//td[4]//input'))).send_keys("2", Keys.ENTER)
        sleep(1)

        qta_element = self.get_element('//tbody[@id="righe"]//tr[1]//td[4]//input', By.XPATH)    #controllo se la quantità è cambiata a 1 e non a 2
        qta = qta_element.get_attribute("value")
        self.assertEqual(qta, "1")
        self.get_element('//input[@id="check_all"]', By.XPATH).click() #elimino righe
        self.get_element('//button[@id="elimina_righe"]', By.XPATH).click()
        sleep(1)
        #ordine
        self.get_element('//button[@class="btn btn-primary dropdown-toggle"]', By.XPATH).click() #click su altro
        self.get_element('//ul[@class="dropdown-menu dropdown-menu-right show"]//a[7]', By.XPATH).click()
        sleep(1)

        self.get_element('//span[@id="select2-id_documento-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-id_documento-results"]//li[1]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//tbody[@id="righe_documento_importato"]//tr[1]//td[4]//input'))).send_keys("2", Keys.ENTER)
        sleep(1)

        qta_element = self.get_element('//tbody[@id="righe"]//tr[1]//td[4]//input', By.XPATH)    #controllo se la quantità è cambiata a 1 e non a 2
        qta = qta_element.get_attribute("value")
        self.assertEqual(qta, "1")
        self.get_element('//input[@id="check_all"]', By.XPATH).click() #elimino righe
        self.get_element('//button[@id="elimina_righe"]', By.XPATH).click()
        sleep(1)

        self.get_element('//a[@id="elimina"]', By.XPATH).click() #elimina fattura
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()
        #elimino attività
        self.navigateTo("Attività")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()
        #elimino preventivo
        self.expandSidebar("Vendite")
        self.navigateTo("Preventivi")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()
        #elimina contratto
        self.navigateTo("Contratti")
        self.wait_loader()

        self.get_element('//tbody//tr[4]//td[2]', By.XPATH).click() #apre contratto
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()  #elimino contratto 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        self.wait_loader()
        #elimina ddt
        self.expandSidebar("Magazzino") 
        self.navigateTo("Ddt in uscita")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()
        #elimina ordini
        self.expandSidebar("Vendite")
        self.navigateTo("Ordini cliente")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

    def aggiungi_riferimento_documenti(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Impostazioni") #primo caso (no,no)
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[10]', By.XPATH).click()   #disattiva impostazione
        self.get_element('(//label[@class="btn btn-default active"])[11]', By.XPATH).click() #disattiva seconda impostazione da riattivare alla fine
        sleep(1)

        #creo ddt
        self.expandSidebar("Magazzino")
        self.navigateTo("Ddt in uscita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click() #click su +
        sleep(1)
        #seleziono destinatario
        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        #seleziono causale trasporto
        self.get_element('//span[@id="select2-idcausalet-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Conto lavorazione")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi
        self.wait_loader()

        #aggiungi articolo
        self.get_element('//span[@id="select2-id_articolo-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@class="select2-results__options select2-results__options--nested"]//li[1]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary tip tooltipstered"]', By.XPATH).click() #click su aggiungi
        sleep(1)

        self.get_element('//span[@id="select2-idstatoddt-container"]', By.XPATH).click() #cambio stato in evaso
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Evaso", Keys.ENTER)
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()
        #crea fattura
        self.get_element('//button[@class="btn btn-info bound clickable"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@id="submit_btn"]', By.XPATH).click()   #click su aggiungi
        self.wait_loader()

        riferimento=self.get_element('(//tbody[@id="righe"]//tr[1]//td[3]//a, By.XPATH)[2]').text  #controllo se è presente il riferimento
        self.assertEqual(riferimento, "001 - Articolo 1")
        #elimina riga
        self.get_element('//a[@class="btn btn-xs btn-danger"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-primary"]', By.XPATH).click()
        sleep(1)
        #rimetto stato in evaso del ddt
        self.expandSidebar("Magazzino")
        self.navigateTo("Ddt in uscita")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()    #apri ddt
        self.wait_loader()

        self.get_element('//span[@id="select2-idstatoddt-container"]', By.XPATH).click() #cambio stato in evaso
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Evaso", Keys.ENTER)
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Impianti")
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni") #secondo caso (si,no)
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[10]', By.XPATH).click()   #attiva impostazione
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()    #apri fattura
        self.wait_loader()

        self.get_element('//button[@class="btn btn-primary dropdown-toggle"]', By.XPATH).click() #click su altro
        self.get_element('//ul[@class="dropdown-menu dropdown-menu-right show"]//a[6]', By.XPATH).click()
        sleep(1)

        self.get_element('//span[@id="select2-id_documento-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-id_documento-results"]//li[1]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@id="submit_btn"]', By.XPATH).click()   #click su aggiungi
        self.wait_loader()

        riferimento=self.get_element('(//tbody[@id="righe"]//tr[1]//td[3]//a, By.XPATH)[2]').text  #controllo se è presente il riferimento
        self.assertEqual(riferimento[17:43], "Rif. ddt in uscita num. 02")
        self.get_element('//a[@id="elimina"]', By.XPATH).click() #elimina fattura
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        #elimino ddt
        self.expandSidebar("Magazzino")
        self.navigateTo("Ddt in uscita")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()    #apro primo ddt
        self.wait_loader()

        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Impianti")
        self.wait_loader()

        #torno alle impostazioni di prima
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)
        
        self.get_element('(//label[@class="btn btn-default active"])[11]', By.XPATH).click() #attiva seconda impostazione
        sleep(1)


    def aggiungi_riferimenti_tutti_documenti(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Impostazioni") #prima con opzione (no,si)
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali  
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[10]', By.XPATH).click() #disattiva prima impostazione
        sleep(1)

        #creo preventivo
        self.expandSidebar("Vendite")
        self.navigateTo("Preventivi")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su +
        sleep(1)
        #nome
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="nome"]'))).send_keys('Test')
        #cliente
        self.get_element('//span[@id="select2-idanagrafica-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idanagrafica-results"]//li[2]', By.XPATH).click()
        #tipo di attività
        self.get_element('//span[@id="select2-idtipointervento-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idtipointervento-results"]//li[1]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()   #click su aggiungi
        self.wait_loader()
        #aggiungi articolo
        self.get_element('//span[@id="select2-id_articolo-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@class="select2-results__options select2-results__options--nested"]//li[1]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary tip tooltipstered"]', By.XPATH).click() #click su aggiungi
        sleep(1)

        self.driver.execute_script('window.scrollTo(0,0)')
        sleep(1)

        #cambio stato
        self.get_element('//span[@id="select2-idstato-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idstato-results"]//li[1]', By.XPATH).click() #imposto stato "Accettato"
        self.get_element('//button[@id="save"]', By.XPATH).click() #click su salva
        self.wait_loader()

        self.get_element('//button[@class="btn btn-info dropdown-toggle "]', By.XPATH).click() #click su crea
        sleep(1)

        self.get_element('//div[@class="dropdown-menu dropdown-menu-right show"]//a[5]', By.XPATH).click()
        sleep(1)
        #ddt
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@id="select2-id_causale_trasporto-container"]'))).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//li[@class="select2-results__option select2-results__option--highlighted"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@id="select2-id_segment-container"]'))).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//li[@class="select2-results__option select2-results__option--highlighted"]'))).click()
        self.get_element('//button[@id="submit_btn"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//span[@id="select2-idstatoddt-container"]', By.XPATH).click()   #cambio stato
        sleep(1)

        self.get_element('//ul[@id="select2-idstatoddt-results"]//li[2]', By.XPATH).click()    #imposta stato "Evaso"
        self.get_element('//button[@id="save"]', By.XPATH).click() #click su salva
        self.wait_loader()

        self.get_element('//button[@class="btn btn-info bound clickable"]', By.XPATH).click()  #crea fattura
        sleep(1)

        self.get_element('//button[@id="submit_btn"]', By.XPATH).click()   #click su aggiungi
        self.wait_loader()

        riferimento1=self.get_element('(//tbody[@id="righe"]//tr[1]//td[3]//a, By.XPATH)[2]').text
        self.assertEqual(riferimento1[17:39], "Rif. preventivo num. 2")
        riferimento2=self.get_element('(//tbody[@id="righe"]//tr[1]//td[3]//a, By.XPATH)[2]').text
        self.assertEqual(riferimento2[55:81], "Rif. ddt in uscita num. 02")
        #elimina fattura
        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()   #click di conferma
        self.wait_loader()
        #elimino ddt
        self.expandSidebar("Magazzino")
        self.navigateTo("Ddt in entrata")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()
        #elimino preventivo
        self.expandSidebar("Vendite")
        self.navigateTo("Preventivi")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()
        self.navigateTo("Impianti")
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni") #test con opzioni messe a (si,si)
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[10]', By.XPATH).click() #attiva prima impostazione
        sleep(1)

        #creo preventivo
        self.expandSidebar("Vendite")
        self.navigateTo("Preventivi")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su +
        sleep(1)
        #nome
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="nome"]'))).send_keys('Test')
        #cliente
        self.get_element('//span[@id="select2-idanagrafica-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idanagrafica-results"]//li[2]', By.XPATH).click()
        #tipo di attività
        self.get_element('//span[@id="select2-idtipointervento-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idtipointervento-results"]//li[1]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()   #click su aggiungi
        self.wait_loader()
        #aggiungi articolo
        self.get_element('//span[@id="select2-id_articolo-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@class="select2-results__options select2-results__options--nested"]//li[1]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary tip tooltipstered"]', By.XPATH).click() #click su aggiungi
        sleep(1)

        self.driver.execute_script('window.scrollTo(0,0)')
        sleep(1)

        #cambio stato
        self.get_element('//span[@id="select2-idstato-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idstato-results"]//li[1]', By.XPATH).click() #imposto stato "Accettato"
        self.get_element('//button[@id="save"]', By.XPATH).click() #click su salva
        self.wait_loader()

        self.get_element('//button[@class="btn btn-info dropdown-toggle "]', By.XPATH).click() #click su crea
        sleep(1)

        self.get_element('//div[@class="dropdown-menu dropdown-menu-right show"]//a[5]', By.XPATH).click()
        sleep(1)
        #ddt
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@id="select2-id_causale_trasporto-container"]'))).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//li[@class="select2-results__option select2-results__option--highlighted"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@id="select2-id_segment-container"]'))).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//li[@class="select2-results__option select2-results__option--highlighted"]'))).click()
        self.get_element('//button[@id="submit_btn"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//span[@id="select2-idstatoddt-container"]', By.XPATH).click()   #cambio stato
        sleep(1)

        self.get_element('//ul[@id="select2-idstatoddt-results"]//li[2]', By.XPATH).click()    #imposta stato "Evaso"
        self.get_element('//button[@id="save"]', By.XPATH).click() #click su salva
        self.wait_loader()

        self.get_element('//button[@class="btn btn-info bound clickable"]', By.XPATH).click()  #crea fattura
        sleep(1)

        self.get_element('//button[@id="submit_btn"]', By.XPATH).click()   #click su aggiungi
        self.wait_loader()

        riferimento1=self.get_element('(//tbody[@id="righe"]//tr[1]//td[3]//a, By.XPATH)[2]').text
        self.assertEqual(riferimento1[17:39], "Rif. preventivo num. 2")
        riferimento2=self.get_element('(//tbody[@id="righe"]//tr[1]//td[3]//a, By.XPATH)[2]').text
        self.assertEqual(riferimento2[55:81], "Rif. ddt in uscita num. 02")
        #elimina fattura
        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()   #click di conferma
        self.wait_loader()
        #elimino ddt
        self.expandSidebar("Magazzino")
        self.navigateTo("Ddt in entrata")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()
        #elimino preventivo
        self.expandSidebar("Vendite")
        self.navigateTo("Preventivi")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

    def aggiungi_note_documenti(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[12]', By.XPATH).click()   #attiva impostazione
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Preventivi")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #crea preventivo
        sleep(1)
        #nome
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="nome"]'))).send_keys('Test')
        #cliente
        self.get_element('//span[@id="select2-idanagrafica-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idanagrafica-results"]//li[2]', By.XPATH).click()
        #tipo di attività
        self.get_element('//span[@id="select2-idtipointervento-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idtipointervento-results"]//li[1]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()   #click su aggiungi
        self.wait_loader()

        self.get_element('(//a[@class="btn btn-primary"])[1]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("Test") #scrivo "Test" come descrizione riga
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("1") #scrivo 1 come prezzo unitario
        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("Nota di prova")   #aggiungo note
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()    #click su aggiungi
        sleep(1)

        #cambio stato
        self.get_element('//span[@id="select2-idstato-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idstato-results"]//li[1]', By.XPATH).click() #imposto stato "Accettato"
        self.get_element('//button[@id="save"]', By.XPATH).click() #click su salva
        self.wait_loader()

        self.get_element('//button[@class="btn btn-info dropdown-toggle "]', By.XPATH).click() #click su crea
        self.get_element('//div[@class="dropdown-menu dropdown-menu-right show"]//a[6]', By.XPATH).click() #crea fattura
        sleep(1)

        self.get_element('//button[@id="submit_btn"]', By.XPATH).click()
        self.wait_loader()

        nota=self.get_element('//tbody[@id="righe"]//td[3]//span', By.XPATH).text  #controllo se ha aggiunto la nota dal preventivo
        self.assertEqual(nota, "Nota di prova")
        #elimina fattura
        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()   #click di conferma
        self.wait_loader()
        #elimino preventivo
        self.navigateTo("Preventivi")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.expandSidebar("Vendite")
        #torno alle impostazioni di prima
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1) 

        self.get_element('(//label[@class="btn btn-default active"])[12]', By.XPATH).click()   #disattiva impostazione
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Preventivi")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #crea preventivo
        sleep(1)
        #nome
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="nome"]'))).send_keys('Test')
        #cliente
        self.get_element('//span[@id="select2-idanagrafica-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idanagrafica-results"]//li[2]', By.XPATH).click()
        #tipo di attività
        self.get_element('//span[@id="select2-idtipointervento-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idtipointervento-results"]//li[1]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()   #click su aggiungi
        self.wait_loader()

        self.get_element('(//a[@class="btn btn-primary"])[1]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("Test") #scrivo "Test" come descrizione riga
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("1") #scrivo 1 come prezzo unitario
        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("Nota di prova")   #aggiungo note
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()    #click su aggiungi
        sleep(1)

        #cambio stato
        self.get_element('//span[@id="select2-idstato-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idstato-results"]//li[1]', By.XPATH).click() #imposto stato "Accettato"
        self.get_element('//button[@id="save"]', By.XPATH).click() #click su salva
        self.wait_loader()

        self.get_element('//button[@class="btn btn-info dropdown-toggle "]', By.XPATH).click() #click su crea
        self.get_element('//div[@class="dropdown-menu dropdown-menu-right show"]//a[6]', By.XPATH).click() #crea fattura
        sleep(1)

        self.get_element('//button[@id="submit_btn"]', By.XPATH).click()
        self.wait_loader()

        wait.until(EC.invisibility_of_element_located((By.XPATH, '//tbody[@id="righe"]//td[3]//span')))   #controllo se non ha aggiunto la nota dal preventivo
        
        #elimina fattura
        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()   #click di conferma
        self.wait_loader()
        #elimino preventivo
        self.navigateTo("Preventivi")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

    def dimensione_widget_predefinita(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting166-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-setting166-results"]//li[1]', By.XPATH).click()    #metto dimensione col-md-1
        sleep(1)

        self.navigateTo("Dashboard")
        self.wait_loader()

        dimensione_element = self.get_element('(//div[@id="widget-top"]//div, By.XPATH)[1]')    #controllo se la dimensione è cambiata
        dimensione = dimensione_element.get_attribute("class")
        self.assertEqual(dimensione[9:17], "col-md-1")
        self.navigateTo("Impianti")
        self.wait_loader()

        #torno alle impostazioni di prima
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting166-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-setting166-results"]//li[3]', By.XPATH).click()    #metto dimensione col-md-3
        sleep(1)

        self.navigateTo("Dashboard")
        self.wait_loader()

        dimensione_element = self.get_element('(//div[@id="widget-top"]//div, By.XPATH)[1]')    #controllo se la dimensione è cambiata
        dimensione = dimensione_element.get_attribute("class")
        self.assertEqual(dimensione[9:17], "col-md-3")


    def tipo_sconto_predefinito(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting189-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-setting189-results"]//li[2]', By.XPATH).click()    #sconto predefinito in eur
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() #seleziono Cliente come anagrafica
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi
        self.wait_loader()
        #aggiungo articolo
        self.get_element('//span[@id="select2-id_articolo-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@class="select2-results__options select2-results__options--nested"]//li[1]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="btn btn-primary tip tooltipstered"]', By.XPATH).click()
        sleep(1)

        sconto_element = self.get_element('//tbody[@id="righe"]//span[@class="select2-selection select2-selection--single"]//span[1]', By.XPATH)    #check valore dello sconto
        sconto = sconto_element.get_attribute("title")
        self.assertEqual(sconto, "€")
        #torno alle impostazioni di prima
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting189-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-setting189-results"]//li[1]', By.XPATH).click()    #sconto predefinito in percentuale
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()
        self.wait_loader()

        sconto_element = self.get_element('//tbody[@id="righe"]//span[@class="select2-selection select2-selection--single"]//span[1]', By.XPATH)    #check valore dello sconto
        sconto = sconto_element.get_attribute("title")
        self.assertEqual(sconto, "%")
        #elimina fattura
        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()


    def importi_stampa(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()
        sleep(1)

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() #seleziono Cliente come anagrafica
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi
        self.wait_loader()
        # riga 1
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("1")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("26,10")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 2
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("2")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,34")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 3
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("3")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,35")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 4
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("4")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,34")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 5
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("5")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,35")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 6
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("6")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("16,60")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 7
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("7")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("28,81")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)

        self.get_element('//span[@id="select2-idstatodocumento-container"]', By.XPATH).click() #cambio stato in "Emessa"
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Emessa", Keys.ENTER)
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@id="print-button_p"]', By.XPATH).click()
        sleep(1)

        self.driver.switch_to.window(self.driver.window_handles[1]) #cambia scheda
        sleep(1)

        importo1=self.get_element('//span[@style="left: 66.18%; top: 27.96%; font-size: calc(var(--scale-factor, By.XPATH)*7.82px); font-family: sans-serif; transform: scaleX(0.901707);"]').text
        self.assertEqual(importo1, "26,10 €")
        importo2=self.get_element('//span[@style="left: 81.57%; top: 27.96%; font-size: calc(var(--scale-factor, By.XPATH)*7.82px); font-family: sans-serif; transform: scaleX(0.901707);"]').text
        self.assertEqual(importo2, "26,10 €")

        self.driver.close() #chiude scheda
        self.driver.switch_to.window(self.driver.window_handles[0]) #torna alla prima
        sleep(1)

        self.get_element('//a[@id="elimina"]', By.XPATH).click() #elimina fattura
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting193-container"]', By.XPATH).click()    #seleziono 4 cifre decimali per gli importi
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('4', Keys.ENTER)
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()
        sleep(1)

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() #seleziono Cliente come anagrafica
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi
        self.wait_loader()
        # riga 1
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("1")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("26,10")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 2
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("2")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,34")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 3
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("3")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,35")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 4
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("4")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,34")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 5
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("5")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,35")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 6
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("6")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("16,60")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 7
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("7")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("28,81")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)

        self.get_element('//span[@id="select2-idstatodocumento-container"]', By.XPATH).click() #cambio stato in "Emessa"
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Emessa", Keys.ENTER)
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@id="print-button_p"]', By.XPATH).click()
        sleep(1)

        self.driver.switch_to.window(self.driver.window_handles[1]) #cambia scheda
        sleep(1)

        importo1=self.get_element('//span[@style="left: 64.67%; top: 27.96%; font-size: calc(var(--scale-factor, By.XPATH)*7.82px); font-family: sans-serif; transform: scaleX(0.901707);"]').text
        self.assertEqual(importo1, "26,1000 €")
        importo2=self.get_element('//span[@style="left: 80.07%; top: 27.96%; font-size: calc(var(--scale-factor, By.XPATH)*7.82px); font-family: sans-serif; transform: scaleX(0.901707);"]').text
        self.assertEqual(importo2, "26,1000 €")

        self.driver.close() #chiude scheda
        self.driver.switch_to.window(self.driver.window_handles[0]) #torna alla prima
        sleep(1)

        self.get_element('//a[@id="elimina"]', By.XPATH).click() #elimina fattura
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting193-container"]', By.XPATH).click()    #seleziono 2 cifre decimali per gli importi
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('2', Keys.ENTER)
        sleep(1)

    def quantita_stampa(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()
        sleep(1)

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() #seleziono Cliente come anagrafica
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi
        self.wait_loader()
        # riga 1
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("1")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("26,10")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 2
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("2")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,34")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 3
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("3")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,35")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 4
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("4")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,34")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 5
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("5")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,35")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 6
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("6")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("16,60")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 7
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("7")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("28,81")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)

        self.get_element('//span[@id="select2-idstatodocumento-container"]', By.XPATH).click() #cambio stato in "Emessa"
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Emessa", Keys.ENTER)
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@id="print-button_p"]', By.XPATH).click()
        sleep(1)

        self.driver.switch_to.window(self.driver.window_handles[1]) #cambia scheda
        sleep(1)

        quantita=self.get_element('//span[@style="left: 52.11%; top: 27.96%; font-size: calc(var(--scale-factor, By.XPATH)*7.82px); font-family: sans-serif; transform: scaleX(0.901707);"]').text
        self.assertEqual(quantita, "1,00")
        self.driver.close() #chiude scheda
        self.driver.switch_to.window(self.driver.window_handles[0]) #torna alla prima
        sleep(1)

        self.get_element('//a[@id="elimina"]', By.XPATH).click() #elimina fattura
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting194-container"]', By.XPATH).click()    #seleziono 4 cifre decimali per le quantità
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('4', Keys.ENTER)
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()
        sleep(1)

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() #seleziono Cliente come anagrafica
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi
        self.wait_loader()
        # riga 1
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("1")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("26,10")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 2
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("2")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,34")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 3
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("3")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,35")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 4
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("4")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,34")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 5
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("5")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,35")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 6
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("6")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("16,60")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 7
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("7")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("28,81")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)

        self.get_element('//span[@id="select2-idstatodocumento-container"]', By.XPATH).click() #cambio stato in "Emessa"
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Emessa", Keys.ENTER)
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@id="print-button_p"]', By.XPATH).click()
        sleep(1)

        self.driver.switch_to.window(self.driver.window_handles[1]) #cambia scheda
        sleep(1)

        quantita=self.get_element('//span[@style="left: 51.36%; top: 27.96%; font-size: calc(var(--scale-factor, By.XPATH)*7.82px); font-family: sans-serif; transform: scaleX(0.901707);"]').text
        self.assertEqual(quantita, "1,0000")
        self.driver.close() #chiude scheda
        self.driver.switch_to.window(self.driver.window_handles[0]) #torna alla prima
        sleep(1)

        self.get_element('//a[@id="elimina"]', By.XPATH).click() #elimina fattura
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting194-container"]', By.XPATH).click()    #seleziono 2 cifre decimali per le quantità
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('2', Keys.ENTER)
        sleep(1)

    def totali_stampa(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()
        sleep(1)

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() #seleziono Cliente come anagrafica
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi
        self.wait_loader()
        # riga 1
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("1")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("26,10")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 2
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("2")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,34")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 3
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("3")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,35")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 4
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("4")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,34")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 5
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("5")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,35")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 6
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("6")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("16,60")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 7
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("7")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("28,81")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)

        self.get_element('//span[@id="select2-idstatodocumento-container"]', By.XPATH).click() #cambio stato in "Emessa"
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Emessa", Keys.ENTER)
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@id="print-button_p"]', By.XPATH).click()
        sleep(1)

        self.driver.switch_to.window(self.driver.window_handles[1]) #cambia scheda
        sleep(1)

        totale=self.get_element('//span[@style="left: 76.88%; top: 90.82%; font-size: calc(var(--scale-factor, By.XPATH)*8.86px); font-family: sans-serif; transform: scaleX(0.900168);"]').text
        self.assertEqual(totale, "127,97 €")
        self.driver.close() #chiude scheda
        self.driver.switch_to.window(self.driver.window_handles[0]) #torna alla prima
        sleep(1)

        self.get_element('//a[@id="elimina"]', By.XPATH).click() #elimina fattura
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting195-container"]', By.XPATH).click()    #seleziono 1 cifra decimali per le quantità
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('1', Keys.ENTER)
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()
        sleep(1)

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() #seleziono Cliente come anagrafica
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi
        self.wait_loader()
        # riga 1
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("1")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("26,10")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 2
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("2")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,34")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 3
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("3")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,35")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 4
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("4")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,34")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 5
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("5")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("8,35")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 6
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("6")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("16,60")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)
        #riga 7
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("7")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("28,81")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)

        self.get_element('//span[@id="select2-idstatodocumento-container"]', By.XPATH).click() #cambio stato in "Emessa"
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Emessa", Keys.ENTER)
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@id="print-button_p"]', By.XPATH).click()
        sleep(1)

        self.driver.switch_to.window(self.driver.window_handles[1]) #cambia scheda
        sleep(1)

        totale=self.get_element('//span[@style="left: 77.32%; top: 90.82%; font-size: calc(var(--scale-factor, By.XPATH)*8.86px); font-family: sans-serif; transform: scaleX(0.900206);"]').text
        self.assertEqual(totale, "128,0 €")
        self.driver.close() #chiude scheda
        self.driver.switch_to.window(self.driver.window_handles[0]) #torna alla prima
        sleep(1)

        self.get_element('//a[@id="elimina"]', By.XPATH).click() #elimina fattura
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting195-container"]', By.XPATH).click()    #seleziono 2 cifre decimali per le quantità
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('2', Keys.ENTER)
        sleep(1)
        

    def listino_predefinito(self):
        wait = WebDriverWait(self.driver, 20)  
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting196-container"]', By.XPATH).click()   #seleziona listino di prova
        sleep(1)

        self.get_element('//ul[@id="select2-setting196-results"]//li', By.XPATH).click()
        sleep(1)

        self.navigateTo("Anagrafiche")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()   #click su +
        sleep(1)
        #creo anagrafica
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="ragione_sociale_add"]'))).send_keys('Test')    #nome anagrafica
        self.get_element('//span[@class="select2-selection select2-selection--multiple"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idtipoanagrafica_add-results"]//li[2]', By.XPATH).click()  #tipo anagrafica cliente
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()   #click su aggiungi
        self.wait_loader()

        listino=self.get_element('//span[@id="select2-id_listino-container"]', By.XPATH).text  #check se il listino è stato selezionato
        self.assertEqual(listino[2:26], "Listino cliente di Prova")
        #elimino anagrafica
        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.expandSidebar("Strumenti") 
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting196-container"]//span', By.XPATH).click()
        sleep(1)


    def lingua(self):
        wait = WebDriverWait(self.driver, 20)  
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting199-container"]', By.XPATH).click()   #metto la lingua in inglese
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('English')
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.navigateTo("Anagrafiche")
        self.wait_loader() 

        scritta=self.get_element('(//li[@id="2"]//p, By.XPATH)[1]').text   #controllo se ha cambiato lingua
        self.assertEqual(scritta, "Entities")
        #torno alle impostazioni di prima
        self.expandSidebar("Tools")
        self.navigateTo("Settings")
        self.wait_loader()

        self.get_element('//div[@id="impostazioni-11"]', By.XPATH).click() #apro Generali
        sleep(1)

        self.get_element('//span[@id="select2-setting199-container"]', By.XPATH).click()   #metto la lingua in italiano
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys('Italiano')
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.navigateTo("Settings")
        self.wait_loader()
        sleep(1)

