from common.Test import Test, get_html
from common.RowManager import RowManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GiacenzeSedi(Test):
    def setUp(self):
        super().setUp()
        self.expandSidebar("Magazzino")
        
    def test_giacenze_sedi(self):
        # Aggiunta sede
        self.aggiunta_sede()

        # Creazione ddt in uscita
        importi = RowManager.list()
        self.creazione_ddt_uscita("Admin spa", "Vendita", importi[0])

        # Trasporto sedi
        self.trasporto()

        # Verifica movimenti sede  
        self.verifica_movimenti()


    def aggiunta_sede(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Anagrafiche")
 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Ragione-sociale"]/input'))).send_keys("Admin spa", Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()    
        sleep(1) 

        #Aggiunta sede
        wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@id="link-tab_4"]'))).click()
        sleep(1)

        self.get_element('//div[@id="tab_4"]//i[@class="fa fa-plus"]', By.XPATH).click()
        sleep(1)

        self.input(None, 'Nome sede').setValue("Sede di Roma")
        self.get_element('(//input[@id="cap"])[2]', By.XPATH).send_keys("35042")
        self.get_element('(//input[@id="citta"])[2]', By.XPATH).click()
        self.get_element('(//input[@id="citta"])[2]', By.XPATH).send_keys("Roma")

        self.get_element('(//span[@id="select2-id_nazione-container"])[2]', By.XPATH).click()
        self.get_element('//li[@class="select2-results__option select2-results__option--highlighted"]', By.XPATH).click()

        wait.until(EC.visibility_of_element_located((By.XPATH, '(//div[@id="form_2-4"]//i[@class="fa fa-plus"])[4]'))).click()
        sleep(1)


    def creazione_ddt_uscita(self, cliente: str, causale: str, file_importi: str):  
        self.expandSidebar("Magazzino")
        self.navigateTo("Ddt in uscita")
        sleep(1)

        # Crea un nuovo ddt al cliente indicato. 
        # Apre la schermata di nuovo elemento
        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        select = self.input(modal, 'Destinatario')
        select.setByText(cliente)
        self.get_element('//li[@class="select2-results__option select2-results__option--highlighted"]', By.XPATH).click()
        sleep(1)

        select = self.input(modal, 'Causale trasporto')
        select.setByText(causale)
        sleep(1)

        # Submit
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        sleep(1)

        row_manager = RowManager(self)
        self.valori=row_manager.compile(file_importi)

        self.get_element('//span[@id="select2-idsede_destinazione-container"]', By.XPATH).click()
        self.get_element('//input[@class="select2-search__field"]', By.XPATH).send_keys("Roma")
        sleep(1)

        self.get_element('//input[@class="select2-search__field"]', By.XPATH).send_keys(Keys.ENTER)
        sleep(1)

        self.get_element('//span[@id="select2-idstatoddt-container"]', By.XPATH).click()
        self.get_element('//input[@class="select2-search__field"]', By.XPATH).send_keys("Evaso", Keys.ENTER)    
        self.get_element('//button[@id="save"]', By.XPATH).click()    
        sleep(1) 

    def trasporto(self):  
        self.navigateTo("Ddt in uscita")
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()    
        sleep(1) 

        self.get_element('//button[@onclick="completaTrasporto(, By.XPATH)"]').click()
        self.get_element('//span[@id="select2-id_segment-container"]', By.XPATH).click()
        self.get_element('//input[@class="select2-search__field"]', By.XPATH).send_keys("Standard ddt in entrata")
        sleep(1)

        self.get_element('//li[@class="select2-results__option select2-results__option--highlighted"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-success"]', By.XPATH).click()  
        sleep(1)

    def verifica_movimenti(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Articoli")
        self.wait_loader()

        # Verifica elemento modificato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Codice"]/input'))).send_keys("001", Keys.ENTER)
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//tbody//tr//td[2]'))).click()
        self.wait_loader()
 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@id="link-tab_10"]'))).click()

        scarico = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_10"]//tbody//tr//td[6]'))).text
        carico = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_10"]//tbody//tr[3]//td[6]'))).text

        self.assertEqual(scarico, "Sede di Roma")
        self.assertEqual(carico, "Sede legale")