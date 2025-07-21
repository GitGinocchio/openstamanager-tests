from common.Test import Test, get_html
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class StampeContabili(Test):
    def setUp(self):
        super().setUp()
        self.navigateTo("Contabilità")
 
    def test_stampecontabili(self):
        # Test stampe contabili
        self.apri_stampe_contabili()

    def apri_stampe_contabili(self):
        self.navigateTo("Stampe contabili")
        self.wait_loader()

        # Stampa registro IVA vendite
        self.get_element('//button[@data-title="Stampa registro IVA vendite"]', By.XPATH).click()
        sleep(1)

        self.get_element('//span[@id="select2-id_sezionale-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-id_sezionale-results"]//li[1]', By.XPATH).click()
        self.get_element('//span[@id="select2-format-container"]', By.XPATH).click()
        self.get_element('//ul[@id="select2-format-results"]//li[1]', By.XPATH).click()
        self.get_element('//span[@id="select2-orientation-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-orientation-results"]//li[1]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary btn-block"]', By.XPATH).click()
        sleep(1)

        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(1)

        stampa=self.get_element('//div[@id="viewer"]//span[3]', By.XPATH).text
        self.assertEqual(stampa, "REGISTRO IVA VENDITE DAL 01/01/2025 AL 31/12/2025 - STANDARD VENDITE")
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

        # Stampa registro IVA acquisti
        self.get_element('//button[@data-title="Stampa registro IVA acquisti"]', By.XPATH).click()
        sleep(1)
        
        self.get_element('//span[@id="select2-id_sezionale-container"]', By.XPATH).click()
        sleep(1)

        self.get_element('//ul[@id="select2-id_sezionale-results"]//li[1]', By.XPATH).click()
        self.get_element('//button[@class="btn btn-primary btn-block"]', By.XPATH).click()
        sleep(1)

        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(1)

        stampa=self.get_element('//div[@id="viewer"]//span[3]', By.XPATH).text
        self.assertEqual(stampa, "REGISTRO IVA ACQUISTI DAL 01/01/2025 AL 31/12/2025 - STANDARD ACQUISTI")
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

        # Stampa liquidazione IVA
        self.get_element('//button[@data-title="Stampa liquidazione IVA"]', By.XPATH).click()
        sleep(1)
        
        self.get_element('//button[@class="btn btn-primary btn-block"]', By.XPATH).click() 
        sleep(1)

        self.driver.switch_to.window(self.driver.window_handles[1]) 
        sleep(1)

        stampa=self.get_element('(//div[@id="viewer"]//span, By.XPATH)[1]').text 
        self.assertEqual(stampa, "PROSPETTO LIQUIDAZIONE IVA DAL 01/01/2025 AL 31/12/2025")
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

        # Stampa Bilancio
        self.get_element('//button[@data-title="Stampa Bilancio"]', By.XPATH).click()
        sleep(1)
        
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()
        sleep(1)

        self.driver.switch_to.window(self.driver.window_handles[1]) 
        sleep(1)

        stampa=self.get_element('//div[@id="viewer"]//span', By.XPATH).text
        self.assertEqual(stampa, "STAMPA BILANCIO")
        self.driver.close() 
        self.driver.switch_to.window(self.driver.window_handles[0]) 
        self.get_element('//button[@class="close"]', By.XPATH).click()
        sleep(1)
        
        # Stampa Situazione patrimoniale
        self.get_element('(//a[@id="print-button"])[1]', By.XPATH).click()
        sleep(1)
        
        self.driver.switch_to.window(self.driver.window_handles[1]) 
        sleep(1)

        stampa=self.get_element('//div[@id="viewer"]//span', By.XPATH).text
        self.assertEqual(stampa, "STAMPA MASTRINO")
        self.driver.close() 
        self.driver.switch_to.window(self.driver.window_handles[0]) 

        # Stampa Situazione economica
        self.get_element('(//a[@id="print-button"])[2]', By.XPATH).click()
        sleep(1)
        
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(1)

        stampa=self.get_element('(//div[@id="viewer"]//span, By.XPATH)[1]').text 
        self.assertEqual(stampa, "STAMPA MASTRINO")
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0]) 

        # Stampa fatturato
        self.get_element('(//a[@id="print-button"])[3]', By.XPATH).click()
        sleep(1)
        
        self.driver.switch_to.window(self.driver.window_handles[1]) 
        sleep(1)

        stampa=self.get_element('(//div[@id="viewer"]//span, By.XPATH)[9]').text 
        self.assertEqual(stampa, "FATTURATO MENSILE DAL 01/01/2025 AL 31/12/2025")
        self.driver.close() 
        self.driver.switch_to.window(self.driver.window_handles[0]) 

        # Stampa acquisti
        self.get_element('(//a[@id="print-button"])[4]', By.XPATH).click()
        sleep(1)
        
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(1)

        stampa=self.get_element('(//div[@id="viewer"]//span, By.XPATH)[9]').text 
        self.assertEqual(stampa, "ACQUISTI MENSILI DAL 01/01/2025 AL 31/12/2025")
        self.driver.close() 
        self.driver.switch_to.window(self.driver.window_handles[0])

        # Stampa libro giornale
        self.get_element('//button[@data-title="Libro giornale"]', By.XPATH).click()
        sleep(1)
        
        self.get_element('//button[@class="btn btn-primary btn-block"]', By.XPATH).click()
        sleep(1)
        
        self.driver.switch_to.window(self.driver.window_handles[1]) 
        sleep(1)

        stampa=self.get_element('(//div[@id="viewer"]//span, By.XPATH)[1]').text 
        self.assertEqual(stampa, "STAMPA LIBRO GIORNALE")
        self.driver.close() 
        self.driver.switch_to.window(self.driver.window_handles[0])

        # Stampa scadenziario
        self.get_element('//button[@data-title="Stampa scadenzario"]', By.XPATH).click()
        sleep(1)
        
        self.get_element('//button[@class="btn btn-primary"]', By.XPATH).click()   
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(1)

        stampa=self.get_element('(//div[@id="viewer"]//span, By.XPATH)[6]').text  
        self.assertEqual(stampa, "SCADENZE DAL 01/01/2025 AL 31/12/2025")
        self.driver.close() 
        self.driver.switch_to.window(self.driver.window_handles[0]) 
