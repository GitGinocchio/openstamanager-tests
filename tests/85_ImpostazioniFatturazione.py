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
        self.expandSidebar("Strumenti")

    def test_impostazioni_fatturazione(self):
        # Test Iva predefinita
        self.iva_predefinita()

        # Test Tipo di pagamento predefinito
        self.tipo_pagamento_predefinito()

        # Test Ritenuta d'acconto predefinita
        self.ritenuta_acconto_predefinita()

        # Test Cassa previdenziale predefinita
        self.cassa_previdenziale_predefinita()

        # Test Importo marca da bollo
        self.importo_marca_bollo()

        # Test Soglia minima per l'applicazione della marca da bollo
        self.soglia_minima_marca_bollo()

        ## TODO: conto aziendale predefinito

        # Test Conto predefinito fatture di vendita
        self.conto_predefinito_vendita()

        # Test Conto predefinito fatture di acquisto
        self.conto_predefinito_acquisto()

        # Test Dicitura fissa fattura
        self.dicitura_fissa_fattura() 

        ## TODO: metodologia calcolo ritenuta d'acconto predefinito

        # Test Ritenuta previdenziale predefinita 
        self.ritenuta_previdenziale_predefinita()

        # Test Descrizione addebito bollo 
        #self.descrizione_marca_bollo()  

        # Test Conto predefinito per la marca da bollo
        #self.conto_marca_bollo()

        # Test Iva per lettere d'intento
        #self.iva_lettere_intento()

        # Test Utilizza prezzi di vendita comprensivi di IVA
        #self.prezzi_vendita_comprensivi_iva()

        # Test Liquidazione iva
        #self.liquidazione_iva()

        ## TODO: conto anticipo clienti

        ## TODO: conto anticipo fornitori

        # Test Descrizione fattura pianificata
        #self.descrizione_fattura_pianificata()

        ## TODO: aggiorna info di acquisto

        ## TODO: bloccare i prezzi inferiori al minimo di vendita

        # Test Permetti fatturazione delle attività collegate a contratti
        #self.fattura_attivita_collegate_contratti()

        ## TODO: data emissione fattura automatica

        # Test Permetti fatturazione delle attività collegate a ordini
        #self.fattura_attivita_collegate_ordini()

        ## TODO: permetti fatturazione delle attività collegate a preventivi

        ## TODO: data inizio verifica contatore fatture di vendita

        ## TODO: raggruppa attività per tipologia in fattura

        ## TODO: metodo di importazione XML fatture di vendita

    def iva_predefinita(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click()
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Iva predefinita", By.XPATH)]//div//span').click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-search select2-search--dropdown"]//input'))).send_keys("Aliq. Iva 10")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-search select2-search--dropdown"]//input'))).send_keys(Keys.ENTER)
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()  
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//textarea[@id="descrizione_riga"]', By.XPATH).send_keys("test")
        iva=self.get_element('//span[@id="select2-idiva-container"]', By.XPATH).text 
        self.assertEqual(iva[2:21], "10 - Aliq. Iva 10%")
        self.get_element('//button[@class="close"]', By.XPATH).click()
        sleep(1)

        self.get_element('//a[@id="elimina"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()   
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Iva predefinita", By.XPATH)]//div//span').click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-search select2-search--dropdown"]//input'))).send_keys("Aliq. Iva 22")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-search select2-search--dropdown"]//input'))).send_keys(Keys.ENTER)
        sleep(1)

    def tipo_pagamento_predefinito(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Tipo di pagamento predefinito", By.XPATH)]//div//span').click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-search select2-search--dropdown"]//input'))).send_keys("Rimessa diretta")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-search select2-search--dropdown"]//input'))).send_keys(Keys.ENTER)
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() 
        self.wait_loader()

        tipo=self.get_element('//span[@id="select2-idpagamento-container"]', By.XPATH).text
        self.assertEqual(tipo[2:24], "MP01 - Rimessa diretta")
        self.get_element('//a[@id="elimina"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click() 
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Tipo di pagamento predefinito", By.XPATH)]//div//span').click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-search select2-search--dropdown"]//input'))).send_keys("Bonifico 30gg d.f.f.m.")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-search select2-search--dropdown"]//input'))).send_keys(Keys.ENTER)
        sleep(1)

    def ritenuta_acconto_predefinita(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Ritenuta d\'acconto predefinita", By.XPATH)]//div//span').click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-search select2-search--dropdown"]//input'))).send_keys("Ritenuta Acconto di Prova")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-search select2-search--dropdown"]//input'))).send_keys(Keys.ENTER)
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click() 
        modal = self.wait_modal()

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click()
        sleep(1)

        ritenuta=self.get_element('//span[@id="select2-id_ritenuta_acconto-container"]', By.XPATH).text
        self.assertEqual(ritenuta[2:27], "Ritenuta Acconto di Prova")
        sleep(1)
        
        self.get_element('//div[@id="modals"]//button[@class="close"]', By.XPATH).click()
        sleep(1)

        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click() 
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Ritenuta d\'acconto predefinita", By.XPATH)]//div//span[@class="select2-selection__clear"]').click()
        sleep(1)

    def cassa_previdenziale_predefinita(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click()
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Cassa previdenziale predefinita", By.XPATH)]//div//span').click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-search select2-search--dropdown"]//input'))).send_keys("Cassa Previdenziale di Prova")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-search select2-search--dropdown"]//input'))).send_keys(Keys.ENTER)
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click()
        sleep(1)

        cassa_previdenziale=self.get_element('//span[@id="select2-id_rivalsa_inps-container"]', By.XPATH).text 
        self.assertEqual(cassa_previdenziale[2:30], "Cassa Previdenziale di Prova")
        sleep(1)

        self.get_element('//button[@class="close"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click() 
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click()
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Cassa previdenziale predefinita", By.XPATH)]//div//span[@class="select2-selection__clear"]').click()
        sleep(1)

    def importo_marca_bollo(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() 
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("test")

        prezzo_unitario=self.get_element('//input[@id="prezzo_unitario"]', By.XPATH)
        prezzo_unitario.clear()
        prezzo_unitario.send_keys("80")

        self.get_element('//span[@id="select2-idiva-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idiva-results"]//li[20]', By.XPATH).click()  
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()  
        self.wait_loader()
        sleep(1)

        totale=self.get_element('//tbody//tr[2]//td[9]', By.XPATH).text
        self.assertEqual(totale, "2,00 €")  

        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click() 
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click()
        sleep(1)

        element=self.get_element('//div[@class="form-group" and contains(., "Importo marca da bollo", By.XPATH)]//input')
        element.clear()
        element.send_keys('3,00', Keys.ENTER)
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()  
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click()  
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("test")

        prezzo_unitario=self.get_element('//input[@id="prezzo_unitario"]', By.XPATH)
        prezzo_unitario.clear()
        prezzo_unitario.send_keys("80")

        self.get_element('//span[@id="select2-idiva-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idiva-results"]//li[20]', By.XPATH).click()  
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()   
        self.wait_loader()
        sleep(1)

        totale=self.get_element('//tbody//tr[2]//td[9]', By.XPATH).text
        self.assertEqual(totale, "3,00 €", Keys.ENTER)   

        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Impianti")
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click()
        sleep(1)

        element=self.get_element('//div[@class="form-group" and contains(., "Importo marca da bollo", By.XPATH)]//input')
        element.clear()
        element.send_keys('2,00', Keys.ENTER)
        sleep(1)

    def soglia_minima_marca_bollo(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() 
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("test")

        prezzo_unitario=self.get_element('//input[@id="prezzo_unitario"]', By.XPATH)
        prezzo_unitario.clear()
        prezzo_unitario.send_keys("80")

        self.get_element('//span[@id="select2-idiva-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idiva-results"]//li[20]', By.XPATH).click() 
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() 
        self.wait_loader()
        sleep(1)

        totale=self.get_element('//tbody//tr[2]//td[9]', By.XPATH).text
        self.assertEqual(totale, "2,00 €")  

        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click() 
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click()
        sleep(1)

        element=self.get_element('//div[@class="form-group" and contains(., "Soglia minima per l\'applicazione della marca da bollo", By.XPATH)]//input')
        element.clear()
        element.send_keys('40')
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click()  
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("test")

        prezzo_unitario=self.get_element('//input[@id="prezzo_unitario"]', By.XPATH)
        prezzo_unitario.clear()
        prezzo_unitario.send_keys("45")   

        self.get_element('//span[@id="select2-idiva-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idiva-results"]//li[20]', By.XPATH).click()  
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()   
        self.wait_loader()
        sleep(1)

        totale=self.get_element('//tbody//tr[2]//td[9]', By.XPATH).text
        self.assertEqual(totale, "2,00 €")   

        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()  
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() 
        sleep(1)

        element=self.get_element('//div[@class="form-group" and contains(., "Soglia minima per l\'applicazione della marca da bollo", By.XPATH)]//input')
        element.clear()
        element.send_keys('77,47')
        element.send_keys(Keys.ENTER)
        sleep(1)

    def conto_predefinito_vendita(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Conto predefinito fatture di vendita", By.XPATH)]').click() 
        sleep(1)

        self.get_element('//ul[@id="select2-setting36-results"]//li[2]', By.XPATH).click()
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click()
        sleep(1)

        conto=self.get_element('//span[@id="select2-idconto-container"]', By.XPATH).text   
        self.assertEqual(conto[2:47], "700.000020 Ricavi vendita prestazione servizi")
        self.get_element('//button[@class="close"]', By.XPATH).click()
        sleep(1)

        #elimina fattura
        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()  
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Conto predefinito fatture di vendita", By.XPATH)]').click() 
        sleep(1)

        self.get_element('//ul[@id="select2-setting36-results"]//li[1]', By.XPATH).click()
        sleep(1)

    def conto_predefinito_acquisto(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Conto predefinito fatture di acquisto", By.XPATH)]').click() 
        sleep(1)

        self.get_element('//ul[@id="select2-setting37-results"]//li[2]', By.XPATH).click()
        sleep(1)

        self.expandSidebar("Acquisti")
        self.navigateTo("Fatture di acquisto")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click() 
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="numero_esterno"]'))).send_keys("05") 
        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Fornitore", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()  
        self.wait_loader()

        self.get_element('//span[@id="select2-idpagamento-container"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//ul[@id="select2-idpagamento-results"]//li[1]', By.XPATH).click()
        sleep(1)

        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click()  
        sleep(1)

        conto=self.get_element('//span[@id="select2-idconto-container"]', By.XPATH).text
        self.assertEqual(conto[2:50], "600.000020 Costi merci c/acquisto di produzione")
        self.get_element('//button[@class="close"]', By.XPATH).click()   
        sleep(1)

        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()
        
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Conto predefinito fatture di acquisto", By.XPATH)]').click() 
        sleep(1)

        self.get_element('//ul[@id="select2-setting37-results"]//li[1]', By.XPATH).click()
        sleep(1)

    def dicitura_fissa_fattura(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()  
        self.wait_loader()

        self.get_element('//a[@id="print-button_p"]', By.XPATH).click()   
        sleep(1)

        self.driver.switch_to.window(self.driver.window_handles[1]) 
        sleep(1)

        dicitura=self.get_element('(//div[@id="viewer"]//span, By.XPATH)[196]').text
        self.assertEqual(dicitura, "Ai sensi del D.Lgs. 196/2003 Vi informiamo che i Vs. dati saranno utilizzati esclusivamente per i ﬁni connessi ai rapporti commerciali tra di noi in essere. Contributo CONAI assolto ove dovuto - Vi")

        self.driver.close() 
        self.driver.switch_to.window(self.driver.window_handles[0]) 
        sleep(1)

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() 
        sleep(1)

        dicitura = self.get_element('//iframe[@class="cke_wysiwyg_frame cke_reset"]', By.XPATH)
        self.driver.switch_to.frame(dicitura)
        self.driver.execute_script('document.body.innerHTML = ""')
        self.driver.execute_script('document.body.innerHTML = "Test"')
        self.driver.switch_to.default_content()
        dicitura.send_keys(Keys.ENTER)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()  
        self.wait_loader()

        self.get_element('//a[@id="print-button_p"]', By.XPATH).click()   
        sleep(1)

        self.driver.switch_to.window(self.driver.window_handles[1]) 
        sleep(1)

        dicitura=self.get_element('(//div[@id="viewer"]//span, By.XPATH)[196]').text
        self.assertEqual(dicitura, "Test")

        self.driver.close() 
        self.driver.switch_to.window(self.driver.window_handles[0]) 
        sleep(1)

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click()
        sleep(1)

        dicitura=self.get_element('//iframe[@class="cke_wysiwyg_frame cke_reset"]', By.XPATH)
        self.driver.switch_to.frame(dicitura)
        self.driver.execute_script('document.body.innerHTML = ""')
        self.driver.execute_script('document.body.innerHTML = "Ai sensi del D.Lgs. 196/2003 Vi informiamo che i Vs. dati saranno utilizzati esclusivamente per i fini connessi ai rapporti commerciali tra di noi in essere. Contributo CONAI assolto ove dovuto - Vi preghiamo di controllare i Vs. dati anagrafici, la P. IVA e il Cod. Fiscale. Non ci riteniamo responsabili di eventuali errori."')
        self.driver.switch_to.default_content()
        dicitura.send_keys(Keys.ENTER)
        sleep(1)

    def ritenuta_previdenziale_predefinita(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Ritenuta previdenziale predefinita", By.XPATH)]').click()
        sleep(1)

        self.get_element('//ul[@id="select2-setting82-results"]//li[1]', By.XPATH).click() 
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() 
        self.wait_loader()

        ritenuta_element=self.get_element('//span[@id="select2-id_ritenuta_contributi-container"]', By.XPATH) 
        ritenuta = ritenuta_element.get_attribute("title")
        self.assertEqual(ritenuta, "Ritenuta Previdenziale di Prova - 80.00% sul 60.00% imponibile")

        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click() 
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Ritenuta previdenziale predefinita", By.XPATH)]//span[@class="select2-selection__clear"]').click()
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() 
        self.wait_loader()

        ritenuta_element=self.get_element('//span[@id="select2-id_ritenuta_contributi-container"]', By.XPATH) 
        ritenuta = ritenuta_element.get_attribute("title")
        self.assertEqual(ritenuta, "")

        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click() 
        self.wait_loader()

    def descrizione_marca_bollo(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()  
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() 
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("test")
        prezzo_unitario=self.get_element('//input[@id="prezzo_unitario"]', By.XPATH)
        prezzo_unitario.clear()
        prezzo_unitario.send_keys("80")

        self.get_element('//span[@id="select2-idiva-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idiva-results"]//li[20]', By.XPATH).click()  
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()  
        self.wait_loader()
        sleep(1)

        descrizione=self.get_element('//tbody//tr[2]//td[3]', By.XPATH).text
        self.assertEqual(descrizione[31:61], "Marca da bollo")

        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click() 
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() 
        sleep(1)

        element=self.get_element('//div[@class="form-group" and contains(., "Descrizione addebito bollo", By.XPATH)]//input')
        element.clear()
        element.send_keys('Descrizione test', Keys.ENTER)
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()  
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() 
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("test")
        prezzo_unitario=self.get_element('//input[@id="prezzo_unitario"]', By.XPATH)
        prezzo_unitario.clear()
        prezzo_unitario.send_keys("80")

        self.get_element('//span[@id="select2-idiva-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idiva-results"]//li[20]', By.XPATH).click()   
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()  
        self.wait_loader()
        sleep(1)

        descrizione=self.get_element('//tbody//tr[2]//td[3]', By.XPATH).text
        self.assertEqual(descrizione[31:47], "Descrizione test")

        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()  
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() 
        sleep(1)

        element=self.get_element('//div[@class="form-group" and contains(., "Descrizione addebito bollo", By.XPATH)]//input')
        element.clear()
        element.send_keys('Marca da bollo', Keys.ENTER)
        sleep(1)

    def conto_marca_bollo(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click()  
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("test")
        prezzo_unitario=self.get_element('//input[@id="prezzo_unitario"]', By.XPATH)
        prezzo_unitario.clear()
        prezzo_unitario.send_keys("80")
        self.get_element('//span[@id="select2-idiva-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idiva-results"]//li[20]', By.XPATH).click()  
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()  
        self.wait_loader()
        conto=self.get_element('//tbody//tr[2]//td[3]//small', By.XPATH).text 
        self.assertEqual(conto, "Rimborso spese marche da bollo")
        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click() 
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Conto predefinito per la marca da bollo", By.XPATH)]').click()
        sleep(1)

        self.get_element('//ul[@id="select2-setting90-results"]//li[1]', By.XPATH).click()
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()  
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click()   
        sleep(1)


        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("test")
        prezzo_unitario=self.get_element('//input[@id="prezzo_unitario"]', By.XPATH)
        prezzo_unitario.clear()
        prezzo_unitario.send_keys("80")
        self.get_element('//span[@id="select2-idiva-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idiva-results"]//li[20]', By.XPATH).click()  
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()   
        self.wait_loader()

        conto=self.get_element('//tbody//tr[2]//td[3]//small', By.XPATH).text 
        self.assertEqual(conto, "Ricavi merci c/to vendite")
        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()   
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Conto predefinito per la marca da bollo", By.XPATH)]').click()
        sleep(1)

        self.get_element('//ul[@id="select2-setting90-results"]//li[6]', By.XPATH).click()
        sleep(1)

    def iva_lettere_intento(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Anagrafiche")
        self.wait_loader() 

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Ragione-sociale"]/input'))).send_keys("Cliente", Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()
        self.wait_loader() 

        
        self.get_element('//a[@id="link-tab_25"]', By.XPATH).click()
        self.get_element('//div[@id="tab_25"]//i[@class="fa fa-plus"]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="numero_protocollo"]'))).send_keys("012345678901234567890123")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="data_protocollo"]'))).send_keys("06/11/2025")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="numero_progressivo"]'))).send_keys("001")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="data_inizio"]'))).send_keys("06/11/2025")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="data_fine"]'))).send_keys("06/12/2025")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="massimale"]'))).send_keys("50000")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="data_emissione"]'))).send_keys("06/11/2025", Keys.ENTER)
        self.get_element('(//button[@class="btn btn-primary"])[2]', By.XPATH).click()
        self.wait_loader()

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click() 
        self.wait_modal()

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        sleep(1)

        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click()  
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("prova per dichiarazione")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="qta"]'))).send_keys("100")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("1")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()
        sleep(1)

        iva=self.get_element('//tbody[@id="righe"]//tr[1]//td[8]//small', By.XPATH).text
        self.assertEqual(iva, "Non imp. art. 8 c.1 lett. c DPR 633/1972 (I) (N3.5)")
        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Anagrafiche")
        self.wait_loader() 

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()
        self.wait_loader() 

        
        self.get_element('//a[@id="link-tab_25"]', By.XPATH).click()
        sleep(1)

        self.get_element('(//div[@id="tab_25"]//tr[1]//td[2])[2]', By.XPATH).click()
        sleep(1)

        self.get_element('//a[@class="btn btn-danger ask "]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Iva per lettere d\'intento", By.XPATH)]').click()
        sleep(1)

        self.get_element('//ul[@id="select2-setting94-results"]//li[1]', By.XPATH).click() 
        sleep(1)

        self.navigateTo("Anagrafiche")
        self.wait_loader() 

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()
        self.wait_loader() 

        
        self.get_element('//a[@id="link-tab_25"]', By.XPATH).click()
        self.get_element('//div[@id="tab_25"]//i[@class="fa fa-plus"]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="numero_protocollo"]'))).send_keys("012345678901234567890123")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="data_protocollo"]'))).send_keys("06/11/2025")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="numero_progressivo"]'))).send_keys("001")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="data_inizio"]'))).send_keys("06/11/2025")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="data_fine"]'))).send_keys("06/12/2025")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="massimale"]'))).send_keys("50000")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="data_emissione"]'))).send_keys("06/11/2025", Keys.ENTER)
        self.get_element('(//button[@class="btn btn-primary"])[2]', By.XPATH).click()
        self.wait_loader()

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click() 
        self.wait_modal()

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        sleep(1)

        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click()  
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("prova per dichiarazione")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="qta"]'))).send_keys("100")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("1")
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click()
        sleep(1)

        iva=self.get_element('//tbody[@id="righe"]//tr[1]//td[8]//small', By.XPATH).text
        self.assertEqual(iva, "Art. 2 c. 2, n. 4 DPR 633/1972 (I) (N3.6)")
        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Anagrafiche")
        self.wait_loader() 

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()
        self.wait_loader() 

        
        self.get_element('//a[@id="link-tab_25"]', By.XPATH).click()
        sleep(1)

        self.get_element('(//div[@id="tab_25"]//tr[1]//td[2])[2]', By.XPATH).click()
        sleep(1)

        self.get_element('//a[@class="btn btn-danger ask "]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Anagrafiche")
        self.wait_loader() 

        self.get_element('//th[@id="th_Ragione-sociale"]//i', By.XPATH).click()  

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click()
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Iva per lettere d\'intento", By.XPATH)]').click() 
        sleep(1)

        self.get_element('//ul[@id="select2-setting94-results"]//li[9]', By.XPATH).click() 
        sleep(1)

    def prezzi_vendita_comprensivi_iva(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Utilizza prezzi di vendita comprensivi di IVA", By.XPATH)]').click()
        sleep(1)

        self.expandSidebar("Magazzino")
        self.navigateTo("Articoli")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click() 
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione"]'))).send_keys("Prova") 

        self.get_element('(//div[@id="modals"]//i[@class="fa fa-plus"])[3]', By.XPATH).click()
        modal = self.wait_modal()

        self.input(modal, 'Quantità iniziale').setValue('1')
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_vendita"]'))).send_keys("12") 
        self.get_element('//button[@class="btn btn-success"]', By.XPATH).click()
        self.wait_loader()

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//span[@id="select2-id_articolo-container"]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Prova")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        sleep(1)

        self.get_element('//button[@class="btn btn-primary tip tooltipstered"]', By.XPATH).click()
        sleep(1)

        prezzo = self.get_element('//tbody[2]//tr[1]//td[2]', By.XPATH).text
        self.assertEqual(prezzo, "12,00 €")

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Utilizza prezzi di vendita comprensivi di IVA", By.XPATH)]').click()
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr[3]//td[2]', By.XPATH).click() 
        self.wait_loader()

        prezzo_element = self.get_element('//tbody[2]//tr[1]//td[2]', By.XPATH).text
        self.assertEqual(prezzo, "12,00 €")

        self.get_element('//a[@id="elimina"]', By.XPATH).click()  
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click() 
        self.wait_loader()

        self.expandSidebar("Magazzino")
        self.navigateTo("Articoli")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Descrizione"]/input'))).send_keys('Prova', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//th[@id="th_Descrizione"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click() 
        sleep(1)

        self.expandSidebar("Strumenti")

    def liquidazione_iva(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click()
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Liquidazione iva", By.XPATH)]').click()
        sleep(1)

        self.get_element('//ul[@id="select2-setting128-results"]//li[2]', By.XPATH).click()
        sleep(1)

        self.navigateTo("Contabilità")
        self.navigateTo("Stampe contabili")
        self.wait_loader()

        self.get_element('(//div[@class="row"]//div[3]//button, By.XPATH)[1]').click()
        sleep(1)

        self.get_element('//span[@id="select2-periodo-container"]', By.XPATH).click() 
        sleep(1)

        periodo=self.get_element('//ul[@id="select2-periodo-results"]//li[2]', By.XPATH).text
        self.assertEqual(periodo, "1° Trimestre 2024")
        self.get_element('//button[@class="close"]', By.XPATH).click() 
        sleep(1)

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Liquidazione iva", By.XPATH)]').click()
        sleep(1)

        self.get_element('//ul[@id="select2-setting128-results"]//li[1]', By.XPATH).click()
        sleep(1)

        self.navigateTo("Contabilità")
        self.navigateTo("Stampe contabili")
        self.wait_loader()

        self.get_element('(//div[@class="row"]//div[3]//button, By.XPATH)[1]').click()
        sleep(1)

        self.get_element('//span[@id="select2-periodo-container"]', By.XPATH).click()  
        sleep(1)

        periodo=self.get_element('//ul[@id="select2-periodo-results"]//li[2]', By.XPATH).text
        self.assertEqual(periodo, "gennaio 2024")
        self.get_element('//button[@class="close"]', By.XPATH).click() 
        sleep(1)

    def descrizione_fattura_pianificata(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Vendite")
        self.navigateTo("Contratti")
        self.wait_loader()

        self.get_element('//tbody//tr[2]//td[2]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//a[@id="link-tab_26"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//div[@id="tab_26"]//tbody//tr//td[2]//a', By.XPATH).click() 
        
        self.driver.switch_to.window(self.driver.window_handles[1]) 
        self.wait_loader()

        descrizione=self.get_element('//textarea[@id="note"]', By.XPATH).text  
        self.assertEqual(descrizione, "Canone 1 del contratto numero 2")
        self.get_element('//button[@class="close"]', By.XPATH).click()
        sleep(1)
        
        self.get_element('//button[@class="ask btn btn-danger pull-right tip tooltipstered"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() 
        sleep(1)

        descrizione = self.get_element('//div[@class="form-group" and contains(., "Descrizione fattura pianificata", By.XPATH)]//input').click()
        descrizione.clear() 
        descrizione.send_keys("prova")
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Contratti")
        self.wait_loader()

        self.get_element('//tbody//tr[2]//td[2]', By.XPATH).click()  
        self.wait_loader()

        self.get_element('//a[@id="link-tab_26"]', By.XPATH).click()  
        sleep(1)

        self.get_element('//button[@id="pianifica"]', By.XPATH).click()  
        sleep(1)

        self.get_element('(//div[@class="nav-tabs-custom"]//a, By.XPATH)[2]').click()
        sleep(1)

        self.get_element('//button[@id="btn_procedi"]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//button[@class="btn btn-primary btn-sm "]', By.XPATH).click()
        sleep(1)

        descrizione=self.get_element('//textarea[@id="note"]', By.XPATH).text 
        self.assertEqual(descrizione, "prova")
        self.get_element('//button[@class="close"]', By.XPATH).click() 
        sleep(1)
        
        self.get_element('//button[@class="ask btn btn-danger pull-right tip tooltipstered"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()
        
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() 
        sleep(1)

        descrizione = self.get_element('//div[@class="form-group" and contains(., "Descrizione fattura pianificata", By.XPATH)]//input').click()
        descrizione.clear() 
        descrizione.send_keys("Canone {rata} del contratto numero {numero}")
        sleep(1)

    def fattura_attivita_collegate_contratti(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() #apro Fatturazione
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[4]', By.XPATH).click()    #attivo impostazione
        sleep(1)

        #crea contratto
        self.expandSidebar("Vendite")
        self.navigateTo("Contratti")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="nome"]'))).send_keys("Prova")
        self.get_element('//span[@id="select2-idanagrafica-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="data_accettazione"]'))).send_keys("01/01/2025")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="data_conclusione"]'))).send_keys("31/12/2025")
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()
        self.wait_loader()
        #aggiungi riga
        self.get_element('//a[@class="btn btn-primary"]', By.XPATH).click() #click su aggiungi riga
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@id="descrizione_riga"]'))).send_keys("Test")    #scrivo "Test" come descrizione della riga
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="prezzo_unitario"]'))).send_keys("1") #scrivo 1 come prezzo unitario
        self.get_element('//button[@class="btn btn-primary pull-right"]', By.XPATH).click() #click su aggiungi
        sleep(1)

        #cambio stato
        self.get_element('//span[@id="select2-idstato-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idstato-results"]//li[6]', By.XPATH).click() #imposto stato "In lavorazione"
        self.get_element('//button[@id="save"]', By.XPATH).click() #click su salva
        self.wait_loader()

        #crea attività
        self.navigateTo("Attività")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()  #click su +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica-container"]', By.XPATH).click() #seleziono Cliente come anagrafica
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-dropdown select2-dropdown--below"]//input'))).send_keys("Cliente")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-dropdown select2-dropdown--below"]//input'))).send_keys(Keys.ENTER)
        self.get_element('//span[@id="select2-idtipointervento-container"]', By.XPATH).click() #seleziono Generico come tipo di intervento
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-search select2-search--dropdown"]//input'))).send_keys("Generico")
        sleep(1)

        self.get_element('//li[@class="select2-results__option select2-results__option--highlighted"]', By.XPATH).click()  #click su primo risultato
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//iframe[@class="cke_wysiwyg_frame cke_reset"])[1]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//iframe[@class="cke_wysiwyg_frame cke_reset"])[1]'))).send_keys("Test")   #scrivo "Test" come richiesta
        self.get_element('//span[@id="select2-idcontratto-container"]', By.XPATH).click()  #aggiungi contratto
        sleep(1)

        self.get_element('//ul[@id="select2-idcontratto-results"]//li[2]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()   #click su Aggiungi
        self.wait_loader()

        self.get_element('//span[@id="select2-nuovo_tecnico-container"]', By.XPATH).click()    #aggiungi sessione
        sleep(1)

        self.get_element('//ul[@id="select2-nuovo_tecnico-results"]//li[2]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary btn-block"]', By.XPATH).click()
        sleep(1)

        self.get_element('//span[@id="select2-idstatointervento-container"]', By.XPATH).click()    #click su stato
        sleep(1)

        self.get_element('(//input[@class="select2-search__field"])[3]', By.XPATH).send_keys("Completato", Keys.ENTER) #seleziono Completato come nuovo stato
        sleep(1)

        self.get_element('//button[@id="save"]', By.XPATH).click() #click su salva
        self.wait_loader()

        self.navigateTo("Attività")
        self.wait_loader()
        
        self.get_element('//tbody//tr[1]//td[1]', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() #apro azioni di gruppo
        wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@data-op="crea_fattura"]'))).click()    #click su crea fattura
        sleep(1)

        self.get_element('//span[@id="select2-raggruppamento-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente")    #seleziono cliente
        self.get_element('//ul[@id="select2-raggruppamento-results"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()  #click di conferma
        self.wait_loader()

        stato=self.get_element('//tbody//tr[1]//td[7]//div', By.XPATH).text    #controllo se l'attività è stata fatturata
        self.assertEqual(stato, "Fatturato")
        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()    #apro attività
        self.wait_loader()
        #elimino attività
        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()
        #elimino fattura
        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click() #apro prima fattura
        self.wait_loader()

        self.get_element('//a[@id="elimina"]', By.XPATH).click() #elimina fattura
        self.wait_loader()

        #torno alle impostazioni di prima
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() #apro Fatturazione
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[4]', By.XPATH).click()    #disattivo impostazione
        sleep(1)

        #crea attività
        self.navigateTo("Attività")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()  #click su +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica-container"]', By.XPATH).click() #seleziono Cliente come anagrafica
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-dropdown select2-dropdown--below"]//input'))).send_keys("Cliente")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-dropdown select2-dropdown--below"]//input'))).send_keys(Keys.ENTER)
        self.get_element('//span[@id="select2-idtipointervento-container"]', By.XPATH).click() #seleziono Generico come tipo di intervento
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-search select2-search--dropdown"]//input'))).send_keys("Generico")
        sleep(1)

        self.get_element('//li[@class="select2-results__option select2-results__option--highlighted"]', By.XPATH).click()  #click su primo risultato
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//iframe[@class="cke_wysiwyg_frame cke_reset"])[1]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//iframe[@class="cke_wysiwyg_frame cke_reset"])[1]'))).send_keys("Test")   #scrivo "Test" come richiesta
        self.get_element('//span[@id="select2-idcontratto-container"]', By.XPATH).click()  #aggiungi contratto
        sleep(1)

        self.get_element('//ul[@id="select2-idcontratto-results"]//li[2]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()   #click su Aggiungi
        self.wait_loader()

        self.get_element('//span[@id="select2-nuovo_tecnico-container"]', By.XPATH).click()    #aggiungi sessione
        sleep(1)

        self.get_element('//ul[@id="select2-nuovo_tecnico-results"]//li[2]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary btn-block"]', By.XPATH).click()
        sleep(1)

        self.get_element('//span[@id="select2-idstatointervento-container"]', By.XPATH).click()    #click su stato
        sleep(1)

        self.get_element('(//input[@class="select2-search__field"])[3]', By.XPATH).send_keys("Completato", Keys.ENTER) #seleziono Completato come nuovo stato
        sleep(1)

        self.get_element('//button[@id="save"]', By.XPATH).click() #click su salva
        self.wait_loader()

        self.navigateTo("Attività")
        self.wait_loader()
        
        self.get_element('//tbody//tr[1]//td[1]', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() #apro azioni di gruppo
        wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@data-op="crea_fattura"]'))).click()    #click su crea fattura
        sleep(1)

        self.get_element('//span[@id="select2-raggruppamento-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente")    #seleziono cliente
        self.get_element('//ul[@id="select2-raggruppamento-results"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()  #click di conferma
        self.wait_loader()

        stato=self.get_element('//tbody//tr[1]//td[7]//div', By.XPATH).text    #controllo se l'attività non è stata fatturata
        self.assertEqual(stato, "Completato")
        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()    #apro attività
        self.wait_loader()
        #elimino attività
        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()
        #elimino contratto
        self.expandSidebar("Vendite")
        self.navigateTo("Contratti")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]//input'))).send_keys("Prova", Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr[2]//td[2]', By.XPATH).click()    #apro contratto
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()  #elimina contratto 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        self.wait_loader()

        self.get_element('//th[@id="th_Nome"]//i', By.XPATH).click()   #cancella ricerca
        sleep(1)

    def fattura_attivita_collegate_ordini(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() #apro Fatturazione
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[6]', By.XPATH).click()    #attivo impostazione
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
        #cambio stato
        self.get_element('//span[@id="select2-idstatoordine-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Accettato", Keys.ENTER)
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()
        #crea attività
        self.navigateTo("Attività")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()  #click su +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica-container"]', By.XPATH).click() #seleziono Cliente come anagrafica
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-dropdown select2-dropdown--below"]//input'))).send_keys("Cliente")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-dropdown select2-dropdown--below"]//input'))).send_keys(Keys.ENTER)
        self.get_element('//span[@id="select2-idtipointervento-container"]', By.XPATH).click() #seleziono Generico come tipo di intervento
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-search select2-search--dropdown"]//input'))).send_keys("Generico")
        sleep(1)

        self.get_element('//li[@class="select2-results__option select2-results__option--highlighted"]', By.XPATH).click()  #click su primo risultato
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//iframe[@class="cke_wysiwyg_frame cke_reset"])[1]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//iframe[@class="cke_wysiwyg_frame cke_reset"])[1]'))).send_keys("Test")   #scrivo "Test" come richiesta
        self.get_element('//span[@id="select2-idordine-container"]', By.XPATH).click() #aggiungo ordine
        sleep(1)

        self.get_element('//ul[@id="select2-idordine-results"]//li[2]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()   #click su Aggiungi
        self.wait_loader()

        self.get_element('//span[@id="select2-nuovo_tecnico-container"]', By.XPATH).click()    #aggiungi sessione
        sleep(1)

        self.get_element('//ul[@id="select2-nuovo_tecnico-results"]//li[2]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary btn-block"]', By.XPATH).click()
        sleep(1)
    
        self.get_element('//span[@id="select2-idstatointervento-container"]', By.XPATH).click()    #click su stato
        sleep(1)

        self.get_element('(//input[@class="select2-search__field"])[3]', By.XPATH).send_keys("Completato", Keys.ENTER) #seleziono Completato come nuovo stato
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Attività")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[1]', By.XPATH).click() #seleziono attività 
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() #apro azioni di gruppo
        wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@data-op="crea_fattura"]'))).click()    #click su crea fattura
        sleep(1)

        self.get_element('//span[@id="select2-raggruppamento-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente")    #seleziono cliente
        self.get_element('//ul[@id="select2-raggruppamento-results"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()  #click di conferma
        self.wait_loader()

        stato=self.get_element('//tbody//tr[1]//td[7]', By.XPATH).text #controllo se lo stato è passato a "Fatturato"
        self.assertEqual(stato, "Fatturato")
        #elimina fattura
        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@id="elimina"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()   #click di conferma
        self.wait_loader()
        #elimina ordine
        self.navigateTo("Ordini cliente")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()
        
        #torno alle impostazioni di prima
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Fatturazione"]', By.XPATH).click() #apro Fatturazione
        sleep(1)

        self.get_element('(//label[@class="btn btn-default active"])[6]', By.XPATH).click()    #disattivo impostazione
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
        #cambio stato
        self.get_element('//span[@id="select2-idstatoordine-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Accettato", Keys.ENTER)
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()
        #crea attività
        self.navigateTo("Attività")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()  #click su +
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica-container"]', By.XPATH).click() #seleziono Cliente come anagrafica
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-dropdown select2-dropdown--below"]//input'))).send_keys("Cliente")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-dropdown select2-dropdown--below"]//input'))).send_keys(Keys.ENTER)
        self.get_element('//span[@id="select2-idtipointervento-container"]', By.XPATH).click() #seleziono Generico come tipo di intervento
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@class="select2-search select2-search--dropdown"]//input'))).send_keys("Generico")
        sleep(1)

        self.get_element('//li[@class="select2-results__option select2-results__option--highlighted"]', By.XPATH).click()  #click su primo risultato
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//iframe[@class="cke_wysiwyg_frame cke_reset"])[1]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//iframe[@class="cke_wysiwyg_frame cke_reset"])[1]'))).send_keys("Test")   #scrivo "Test" come richiesta
        self.get_element('//span[@id="select2-idordine-container"]', By.XPATH).click() #aggiungo ordine
        sleep(1)

        self.get_element('//ul[@id="select2-idordine-results"]//li[2]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()   #click su Aggiungi
        self.wait_loader()

        self.get_element('//span[@id="select2-nuovo_tecnico-container"]', By.XPATH).click()    #aggiungi sessione
        sleep(1)

        self.get_element('//ul[@id="select2-nuovo_tecnico-results"]//li[2]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary btn-block"]', By.XPATH).click()
        sleep(1)

        self.get_element('//span[@id="select2-idstatointervento-container"]', By.XPATH).click()    #click su stato
        sleep(1)

        self.get_element('(//input[@class="select2-search__field"])[3]', By.XPATH).send_keys("Completato", Keys.ENTER) #seleziono Completato come nuovo stato
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        #fattura attività
        self.navigateTo("Attività")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[1]', By.XPATH).click()
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() #apro azioni di gruppo
        wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@data-op="crea_fattura"]'))).click()    #click su crea fattura
        sleep(1)

        self.get_element('//span[@id="select2-raggruppamento-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente")    #seleziono cliente
        self.get_element('//ul[@id="select2-raggruppamento-results"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()  #click di conferma
        self.wait_loader()

        stato=self.get_element('//tbody//tr[1]//td[7]', By.XPATH).text #controllo se lo stato è passato a "Fatturato"
        self.assertEqual(stato, "Fatturato")
        #elimina ordine
        self.expandSidebar("Vendite")
        self.navigateTo("Ordini cliente")
        self.wait_loader() 

        self.get_element('//tbody//tr[1//td[2]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()
        #elimina fattura
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@id="elimina"]', By.XPATH).click() #elimina fattura
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()   #click di conferma
        self.wait_loader()
        #elimina attività
        self.navigateTo("Attività")
        self.wait_loader()
        
        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()




