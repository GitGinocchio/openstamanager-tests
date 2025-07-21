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


class Preventivi(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Vendite")

    def test_creazione_preventivo(self):
        # Crea un nuovo preventivo *Required*
        importi = RowManager.list()
        self.creazione_preventivo("Preventivo di Prova","Cliente", "1", importi[0])

        # Duplica un preventivo *Required*
        self.duplica_preventivo()

        # Modifica preventivo *Required*
        self.modifica_preventivo("Accettato")

        # Cancellazione preventivo
        self.elimina_preventivo()

        # Creazione contratto da preventivo
        self.creazione_contratto
         

        # Creazione ordine cliente da preventivo
        self.creazione_ordine_cliente()

        # Creazione ordine fornitore da preventivo
        self.creazione_ordine_fornitore()

        # Creazione attività
        self.creazione_attività()

        # Creazione DDT in uscita
        self.creazione_ddt_uscita()

        # Creazione fattura
        self.creazione_fattura()

        # Verifica preventivi
        self.verifica_preventivi()

        # Plugin consuntivo
        self.consuntivo()

        # Plugin revisioni
        self.revisioni()

        # Cambia stato (Azioni di gruppo)
        self.cambia_stato()

        # Fattura preventivi (Azioni di gruppo)
        self.fattura_preventivi()

    def creazione_preventivo(self, nome:str, cliente:str, idtipo: str, file_importi: str):
        self.navigateTo("Preventivi")
        self.wait_loader() 

        # Creazione preventivo
        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        self.input(modal, 'Nome').setValue(nome)
        select = self.input(modal, 'Cliente')
        select.setByText(cliente)
        select = self.input(modal, 'Tipo di Attività')
        select.setByIndex(idtipo)
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

        row_manager = RowManager(self)
        self.valori=row_manager.compile(file_importi)
        sleep(1)

    def duplica_preventivo(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Preventivi")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="pulsanti"]//button[@class="btn ask btn-primary"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-primary"]'))).click()
        sleep(1)

        self.driver.execute_script('window.scrollTo(0,0)')
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="nome"]'))).send_keys(" da Eliminare")
        sleep(1)
        
        self.get_element('//button[@class="btn btn-success"]', By.XPATH).click()
        sleep(1)

    def modifica_preventivo(self, stato:str):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Preventivi")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('=Preventivo di Prova', Keys.ENTER)
        sleep(1)
        
        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()
        
        # Modifica stato preventivo
        select = self.input(None, 'Stato')
        select.setByText(stato)
        self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()
        sleep(1)

        # Estrazione totali righe
        sconto = self.get_element('//div[@id="righe"]//tbody[2]//tr[2]//td[2]', By.XPATH).text
        totale_imponibile = self.get_element('//div[@id="righe"]//tbody[2]//tr[3]//td[2]', By.XPATH).text
        iva = self.get_element('//div[@id="righe"]//tbody[2]//tr[4]//td[2]', By.XPATH).text
        totale = self.get_element('//div[@id="tab_0"]//div[@id="righe"]//tbody[2]//tr[5]//td[2]', By.XPATH).text

        self.assertEqual(sconto, (self.valori["Sconto/maggiorazione"]+ ' €'))
        self.assertEqual(totale_imponibile, (self.valori["Totale imponibile"]+ ' €'))
        self.assertEqual(iva, (self.valori["IVA"] + ' €'))
        self.assertEqual(totale, (self.valori["Totale documento"] + ' €'))

        self.navigateTo("Preventivi")
        self.wait_loader()  

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def elimina_preventivo(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Preventivi")
        self.wait_loader()  

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('=Preventivo di Prova da Eliminare', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        sleep(1)

        self.navigateTo("Preventivi")
        self.wait_loader()  

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def creazione_contratto(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Preventivi")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Preventivo di Prova', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        sleep(1)
        totalepreventivo=self.get_element('//div[@id="righe"]//tbody[2]//tr[3]//td[2]', By.XPATH).text

        # Creazione contratto
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="pulsanti"]//button[@class="btn btn-info dropdown-toggle "]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@class="btn dropdown-item bound clickable"][@data-title="Crea contratto"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@id="select2-id_segment-container"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//li[@class="select2-results__option select2-results__option--highlighted"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@id="submit_btn"]'))).click()
        sleep(1)

        totalecontratto=self.get_element('//div[@id="righe"]//tbody[2]//tr[3]//td[2]', By.XPATH).text
        
        # Controllo valori righe preventivo
        self.assertEqual(totalecontratto,totalepreventivo)

        # Eliminazione contratto
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()

        # Verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Preventivo di Prova", Keys.ENTER)
        sleep(1)

        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)  
        self.navigateTo("Preventivi")
        self.wait_loader()

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def creazione_ordine_cliente(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Preventivi")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Preventivo di Prova', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        totalepreventivo=self.get_element('//div[@id="righe"]//tbody[2]//tr[3]//td[2]', By.XPATH).text

        # Creazione ordine cliente
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="btn btn-info dropdown-toggle "]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@class="btn dropdown-item bound clickable"][@data-title="Crea ordine cliente"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@id="select2-id_segment-container"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//li[@class="select2-results__option select2-results__option--highlighted"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@id="submit_btn"]'))).click()
        sleep(1)

        totaleordinecliente=self.get_element('//div[@id="righe"]//tbody[2]//tr[3]//td[2]', By.XPATH).text
        
        # Controllo valori righe preventivo
        self.assertEqual(totaleordinecliente,totalepreventivo)

        # Eliminazione ordine
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()

        # Verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_icon_title_Stato"]/input'))).send_keys("Bozza", Keys.ENTER)
        sleep(1)

        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)  
        self.navigateTo("Preventivi")
        self.wait_loader()  

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def creazione_ordine_fornitore(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Preventivi")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Preventivo di Prova', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        # Creazione ordine fornitore
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="btn btn-info dropdown-toggle "]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@class="btn dropdown-item bound clickable"][@data-title="Crea ordine fornitore"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//span [@id="select2-idanagrafica-container"])[2]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//li[@class="select2-results__option select2-results__option--highlighted"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@id="select2-id_segment-container"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//li[@class="select2-results__option select2-results__option--highlighted"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@id="submit_btn"]'))).click()
        sleep(1)

        totaleordinefornitore=self.get_element('//div[@id="righe"]//tbody[2]//tr[3]//td[2]', By.XPATH).text
        
        # Controllo valori righe preventivo
        self.assertEqual(totaleordinefornitore, self.valori["Totale imponibile"] + ' €')
        sleep(1)

        # Eliminazione ordine
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()

        # Verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_icon_title_Stato"]/input'))).send_keys("Bozza", Keys.ENTER)
        sleep(1)

        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)  
        self.expandSidebar("Vendite") 
        self.navigateTo("Preventivi")
        self.wait_loader()  

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def creazione_attività(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Preventivi")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Preventivo di Prova', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        totalepreventivo=self.get_element('//div[@id="righe"]//tbody[2]//tr[3]//td[2]', By.XPATH).text

        # Creazione attività
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="btn btn-info dropdown-toggle "]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@class="btn dropdown-item bound clickable"][@data-title="Crea attività"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@id="select2-id_tipo_intervento-container"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//li[@class="select2-results__option select2-results__option--highlighted"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@id="select2-id_stato_intervento-container"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//li[@class="select2-results__option"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@id="select2-id_segment-container"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//li[@class="select2-results__option select2-results__option--highlighted"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@id="submit_btn"]'))).click()
        sleep(1)

        totaleattività=self.get_element('//div[@id="righe"]//tbody[2]//tr[3]//td[2]', By.XPATH).text
        
        # Controllo valori righe preventivo
        self.assertEqual(totaleattività,totalepreventivo)

        # Eliminazione attività
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()

        # Verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Numero"]/input'))).send_keys("03", Keys.ENTER)
        sleep(1)

        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)  
        self.expandSidebar("Vendite")        
        self.navigateTo("Preventivi")
        self.wait_loader()  

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def creazione_ddt_uscita(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Preventivi")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Preventivo di Prova', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        totalepreventivo=self.get_element('//div[@id="righe"]//tbody[2]//tr[3]//td[2]', By.XPATH).text

        # Creazione ddt uscita
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="btn btn-info dropdown-toggle "]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@class="btn dropdown-item bound clickable"][@data-title="Crea ordine cliente"]//i[@class="fa fa-truck"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@id="select2-id_causale_trasporto-container"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//li[@class="select2-results__option select2-results__option--highlighted"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//span[@id="select2-id_segment-container"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//li[@class="select2-results__option select2-results__option--highlighted"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@id="submit_btn"]'))).click()
        sleep(1)

        totaleddtuscita=self.get_element('//div[@id="righe"]//tbody[2]//tr[3]//td[2]', By.XPATH).text
        
        # Controllo valori righe preventivo
        self.assertEqual(totaleddtuscita,totalepreventivo)

        # Eliminazione ddt uscita
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        sleep(1)

        # Verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Numero"]/input'))).send_keys("03", Keys.ENTER)
        sleep(1)

        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)  
        self.expandSidebar("Vendite")
        self.navigateTo("Preventivi")
        self.wait_loader()  

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def creazione_fattura(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Preventivi")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Preventivo di Prova', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        totalepreventivo=self.get_element('//div[@id="righe"]//tbody[2]//tr[3]//td[2]', By.XPATH).text

        # Creazione fattura
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="btn btn-info dropdown-toggle "]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@class="btn dropdown-item bound clickable"][@data-title="Crea fattura"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@id="submit_btn"]'))).click()
        sleep(1)

        totalefattura=self.get_element('//div[@id="righe"]//tbody[2]//tr[3]//td[2]', By.XPATH).text
        
        # Controllo valori righe preventivo
        self.assertEqual(totalefattura,totalepreventivo)

        # Eliminazione fattura
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask "]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()

        # Verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Numero"]/input'))).send_keys("0003/2025", Keys.ENTER)
        sleep(1)

        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)  
        self.navigateTo("Preventivi")
        self.wait_loader()  

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def verifica_preventivi(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Preventivi")
        self.wait_loader()  

        # Verifica elemento modificato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Preventivo di Prova", Keys.ENTER)
        sleep(1)

        modificato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[3]').text
        self.assertEqual("Preventivo di Prova",modificato)
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

        # Verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Preventivo di Prova da Eliminare", Keys.ENTER)
        sleep(1)

        eliminato=self.driver.find_element(By.XPATH,'//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def consuntivo(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Preventivi")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@id="link-tab_12"]', By.XPATH).click()
        budget=self.get_element('//span[@class="text-success"]', By.XPATH).text
        self.assertEqual(budget,"+ 264,80 €")     
    def revisioni(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Preventivi")
        self.wait_loader()

        self.get_element('//tbody//tr//td[3]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@id="link-tab_20"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_20"]//td[@class="text-center"][1]')))

    def cambia_stato(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Preventivi")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Numero"]/input'))).send_keys("1", Keys.ENTER)  
        sleep(1)

        self.get_element('//tbody//tr//td', By.XPATH).click()   
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        self.get_element('//a[@data-op="cambia_stato"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//span[@id="select2-id_stato-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Bozza")
        sleep(1)

        self.get_element('//ul[@id="select2-id_stato-results"]', By.XPATH).click() 
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click() 
        self.wait_loader()

        stato=self.get_element('//tbody//tr//td[6]', By.XPATH).text
        self.assertEqual(stato,"Bozza") 

        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        self.get_element('//a[@data-op="cambia_stato"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//span[@id="select2-id_stato-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Accettato")
        sleep(1)

        self.get_element('//ul[@id="select2-id_stato-results"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click() 
        sleep(1)

    def fattura_preventivi(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Preventivi")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Numero"]/input'))).send_keys("1", Keys.ENTER) 
        sleep(1)

        self.get_element('//tbody//tr//td[1]', By.XPATH).click() 
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        self.get_element('//a[@data-op="crea_fattura"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//span[@id="select2-raggruppamento-container"]', By.XPATH).click()  
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente")
        sleep(1)

        self.get_element('//ul[@id="select2-raggruppamento-results"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click() 
        self.wait_loader()

        self.get_element('//span[@id="select2-idstato-container"]', By.XPATH).click()  
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("In lavorazione", Keys.ENTER)
        self.get_element('//button[@id="save"]', By.XPATH)
        self.wait_loader()
