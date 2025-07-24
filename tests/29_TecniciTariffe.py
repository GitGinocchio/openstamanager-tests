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


class TecniciTariffe(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Attività")
        
    def test_tecnici_tariffe(self):
        # Modifica Tariffe
        self.modifica_tariffe("28.00")

        # Verifica Tariffe
        self.verifica_tariffe()

    def modifica_tariffe(self, modifica):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Tecnici e tariffe")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Tecnico', Keys.ENTER)        
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="input-group"]/input[@id="costo_ore1"]'))).send_keys(modifica)
        sleep(1)
            
        self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()
        self.wait_loader()
        
        self.navigateTo("Tecnici e tariffe")
        self.wait_loader()

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def verifica_tariffe(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Tecnici e tariffe")
        self.wait_loader()    

        # Verifica elemento modificato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Tecnico", Keys.ENTER)
        sleep(1)

        self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[2]').click()
        sleep(1)

        self.get_element('//div[@class="input-group"]/input[@id="costo_ore1"][@value="28.000000"]', By.XPATH).click()
        modificato="28.000000"
        self.assertEqual("28.000000",modificato)

