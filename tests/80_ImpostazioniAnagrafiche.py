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

        self.navigateTo("Anagrafiche")
        self.wait_loader()

    def test_impostazioni_anagrafiche(self):
        # Test impostazione Formato codice anagrafica
        self.cambio_formato_codice()

        ## TODO: test geolocalizzazione automatica

    def cambio_formato_codice(self):
        wait = WebDriverWait(self.driver, 20)

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="ragione_sociale_add"]'))).send_keys('Test')
        self.get_element('//span[@class="select2-selection select2-selection--multiple"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idtipoanagrafica_add-results"]//li[5]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()
        self.wait_loader()

        codice_element = self.get_element('//input[@id="codice"]', By.XPATH)
        codice = codice_element.get_attribute("value")
        self.assertEqual(codice, "00000010")
        
        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.expandSidebar("Strumenti") 
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Anagrafiche"]', By.XPATH).click()
        sleep(1)

        formato = self.get_element('//div[@class="form-group" and contains(., "Formato codice anagrafica", By.XPATH)]//input')
        formato.clear()
        formato.send_keys("####", Keys.ENTER) 

        self.navigateTo("Anagrafiche")
        self.wait_loader()

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@id="ragione_sociale_add"]'))).send_keys('Test')
        self.get_element('//span[@class="select2-selection select2-selection--multiple"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-idtipoanagrafica_add-results"]//li[5]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()
        self.wait_loader()

        codice_element = self.get_element('//input[@id="codice"]', By.XPATH) 
        codice = codice_element.get_attribute("value")
        self.assertEqual(codice, "0010")
        self.get_element('//a[@class="btn btn-danger ask"]', By.XPATH).click()
        sleep(1)

        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.expandSidebar("Strumenti")
        self.navigateTo("Impostazioni")
        self.wait_loader()

        self.get_element('//div[@data-title="Anagrafiche"]', By.XPATH).click()
        sleep(1)

        formato = self.get_element('//div[@class="form-group" and contains(., "Formato codice anagrafica", By.XPATH)]//input')
        formato.clear()
        formato.send_keys("########", Keys.ENTER)
        sleep(1)

    