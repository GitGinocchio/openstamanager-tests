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

    def test_impostazioni_contratti(self):
        # Test Condizioni generali di fornitura contratti
        self.condizioni_generali_contratti()

        # Test Crea contratto rinnovabile di default
        self.crea_contratto_rinnovabile()

        # Test Giorni di preavviso di default
        self.giorni_preavviso()

        ## TODO: cambia automaticamente stato contratti fatturati

    def condizioni_generali_contratti(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Contratti"]', By.XPATH).click()
        sleep(1)

        element=self.get_element('//div[@class="form-group" and contains(., "Condizioni generali di fornitura contratti", By.XPATH)]//iframe')
        element.click()
        element.send_keys('Prova')
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Contratti")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="nome"]'))).send_keys("Manutenzione")
        self.get_element('//span[@id="select2-idanagrafica-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("Cliente", Keys.ENTER)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="data_accettazione"]'))).send_keys("01/01/2025")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="data_conclusione"]'))).send_keys("31/12/2025")
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()
        self.wait_loader()
        
        self.get_element('//a[@id="print-button_p"]', By.XPATH).click() 
        sleep(1)

        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(1)

        test=self.get_element('(//div[@class="page"])[2]//span[26]', By.XPATH).text
        self.assertEqual(test, "Prova")
        self.driver.close() 
        self.driver.switch_to.window(self.driver.window_handles[0])

        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()  
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Contratti"]', By.XPATH).click()
        sleep(1)

        element=self.get_element('//div[@class="form-group" and contains(., "Condizioni generali di fornitura contratti", By.XPATH)]//iframe')
        element.click()
        element.send_keys(Keys.BACKSPACE * 5)
        sleep(1)
        
    def crea_contratto_rinnovabile(self):
        wait = WebDriverWait(self.driver, 20)  
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Contratti"]', By.XPATH).click()
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Crea contratto rinnovabile di default", By.XPATH)]//div//label').click() 
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Contratti")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()  
        sleep(1)

        self.get_element('//button[@class="btn btn-tool"]', By.XPATH).click() 
        sleep(1)

        stato=self.get_element('//label[@class="btn btn-default active"]//span[1]', By.XPATH).text 
        self.assertEqual(stato, "Attivato")

        self.get_element('//button[@class="close"]', By.XPATH).click() 
        sleep(1)

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Contratti"]', By.XPATH).click()
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Crea contratto rinnovabile di default", By.XPATH)]//div//label').click() 
        sleep(1)

    def giorni_preavviso(self):
        wait = WebDriverWait(self.driver, 20)  
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Contratti"]', By.XPATH).click()
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Giorni di preavviso di default", By.XPATH)]//input').send_keys('3,00')
        sleep(1)

        self.expandSidebar("Vendite")
        self.navigateTo("Contratti")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()  
        sleep(1)

        self.get_element('//button[@class="btn btn-tool"]', By.XPATH).click() 
        sleep(1)

        giorni_element = self.get_element('//input[@id="giorni_preavviso_rinnovo_add"]', By.XPATH)  
        giorni = giorni_element.get_attribute("value")
        self.assertEqual(giorni, "3,00")
        self.get_element('//button[@class="close"]', By.XPATH).click() 
        sleep(1)

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Contratti"]', By.XPATH).click()
        sleep(1)

        self.get_element('//div[@class="form-group" and contains(., "Giorni di preavviso di default", By.XPATH)]//input').send_keys('2,00')
        sleep(1)