from common.Test import Test, get_html
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.RowManager import RowManager

class Impostazioni(Test):
    def setUp(self):
        super().setUp()

    def test_impostazioni_ddt(self):
        # Test Cambia automaticamente stato ddt fatturati
        importi = RowManager.list()
        self.cambia_stato_ddt_fatturati(importi[0])

    def cambia_stato_ddt_fatturati(self, file_importi: str):
        wait = WebDriverWait(self.driver, 20) 
        self.expandSidebar("Magazzino")
        self.navigateTo("Ddt in entrata")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Admin spa", Keys.ENTER)
        self.get_element('//span[@id="select2-idcausalet-container"]', By.XPATH).click()   
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Conto lavorazione", Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click() 
        self.wait_loader()


        row_manager = RowManager(self)
        self.valori=row_manager.compile(file_importi)
        sleep(1)

        self.get_element('//span[@id="select2-idstatoddt-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Evaso", Keys.ENTER)
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Ddt in entrata")
        self.wait_loader()

        self.get_element('//tbody//tr//td', By.XPATH).click()   
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        self.get_element('//a[@data-op="crea_fattura"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//span[@id="select2-raggruppamento-container"]', By.XPATH).click()   
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click() 
        self.wait_loader()

        stato=self.get_element('//tbody//tr//td[11]', By.XPATH).text 
        self.assertEqual(stato, "Fatturato")
        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.expandSidebar("Acquisti")
        self.navigateTo("Fatture di acquisto")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click() 
        self.wait_loader()
    
        self.get_element('//a[@id="elimina"]', By.XPATH).click()   
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()  
        self.wait_loader()

        self.expandSidebar("Magazzino")
        self.navigateTo("Ddt in uscita")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//span[@id="select2-idanagrafica_add-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Admin spa")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)

        self.get_element('//span[@id="select2-idcausalet-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Conto lavorazione")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()
        self.wait_loader()

        row_manager = RowManager(self)
        self.valori=row_manager.compile(file_importi)
        sleep(1)

        self.driver.execute_script('window.scrollTo(0,0)')
        self.get_element('//span[@id="select2-idstatoddt-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Evaso", Keys.ENTER)
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Ddt in uscita")
        self.wait_loader()

        self.get_element('//tbody//tr//td', By.XPATH).click()    
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        self.get_element('//a[@data-op="crea_fattura"]', By.XPATH).click()  
        sleep(1)

        self.get_element('//span[@id="select2-raggruppamento-container"]', By.XPATH).click()   
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click() 
        self.wait_loader()

        stato2=self.get_element('//tbody//tr//td[11]', By.XPATH).text  
        self.assertEqual(stato2, "Fatturato")
        self.get_element('//tbody//tr[1]//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.expandSidebar("Vendite")
        self.navigateTo("Fatture di vendita")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()  
        self.wait_loader()
    
        self.get_element('//a[@id="elimina"]', By.XPATH).click()  
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()  
        self.wait_loader()