from common.Test import Test, get_html
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Dashboard(Test):
      
    def test_Dashboard(self):
        self.navigateTo("Dashboard")
        self.wait_loader()

        self.get_element('(//div[@class="info-box"])[1]', By.XPATH).click()
        sleep(1)
        widget=self.get_element('//div[@class="modal-body"]//p', By.XPATH).text
        self.assertEqual(widget, "Non ci sono promemoria da pianificare.")
        self.get_element('//div[@class="modal-content"]//button[@class="close"]', By.XPATH).click()
        sleep(1)

        self.get_element('(//div[@class="info-box"])[2]', By.XPATH).click()
        sleep(1)
        widget=self.get_element('//div[@id="modals"]//tbody//tr//td', By.XPATH).text
        self.assertEqual(widget, "2")
        self.get_element('//div[@class="modal-content"]//button[@class="close"]', By.XPATH).click()
        sleep(1)

        self.get_element('(//div[@class="info-box"])[3]', By.XPATH).click()
        sleep(1)
        widget=self.get_element('//div[@class="modal-body"]//p', By.XPATH).text
        self.assertEqual(widget, "Non ci sono note da notificare.")
        self.get_element('//div[@class="modal-content"]//button[@class="close"]', By.XPATH).click()
        sleep(1)

        self.get_element('(//div[@class="info-box"])[4]', By.XPATH).click()
        sleep(1)
        verifica = self.get_element('//tbody//tr[1]//td[2]', By.XPATH).text
        self.assertEqual(verifica, "Fattura immediata di acquisto numero 01")

        self.navigateTo("Dashboard")
        self.wait_loader()

        self.get_element('(//div[@class="info-box"])[5]', By.XPATH).click()
        sleep(1)
        widget=self.get_element('//div[@class="modal-body"]//div', By.XPATH).text
        self.assertEqual(widget, "Non ci sono articoli in esaurimento.")
        self.get_element('//div[@class="modal-content"]//button[@class="close"]', By.XPATH).click()
        sleep(1)

        self.get_element('(//div[@class="info-box"])[6]', By.XPATH).click()
        sleep(1)
        widget=self.get_element('//div[@class="modal-body"]//tr//th', By.XPATH).text
        self.assertEqual(widget, "Preventivo")
        self.get_element('//div[@class="modal-content"]//button[@class="close"]', By.XPATH).click()
        sleep(1)
        
        self.get_element('(//div[@class="info-box"])[7]', By.XPATH).click()
        sleep(1)
        widget=self.get_element('//div[@class="modal-content"]//p', By.XPATH).text
        self.assertEqual(widget, "Non ci sono contratti in scadenza.")
        self.get_element('//div[@class="modal-content"]//button[@class="close"]', By.XPATH).click()
        sleep(1)

        self.get_element('(//div[@class="info-box"])[8]', By.XPATH).click()
        sleep(1)
        widget=self.get_element('(//table[@id="tbl-rate"]//tr//th, By.XPATH)[2]').text
        self.assertEqual(widget, "Scadenza")
        self.get_element('//div[@class="modal-content"]//button[@class="close"]', By.XPATH).click()
        sleep(1)

        self.get_element('(//div[@class="info-box"])[9]', By.XPATH).click()
        sleep(1)
        widget=self.get_element('//div[@class="modal-body"]//label', By.XPATH).text
        self.assertEqual(widget, "Mese e anno*")
        self.get_element('//div[@class="modal-content"]//button[@class="close"]', By.XPATH).click()
        sleep(1)

        self.get_element('(//div[@class="info-box"])[10]', By.XPATH).click()
        sleep(1)
        widget=self.get_element('//div[@class="modal-body"]//label', By.XPATH).text
        self.assertEqual(widget, "Settimana*")
        self.get_element('//div[@class="modal-content"]//button[@class="close"]', By.XPATH).click()
        sleep(1)

        self.get_element('(//div[@class="info-box"])[11]', By.XPATH).click()
        sleep(1)
        widget=self.get_element('//div[@class="modal-body"]//tbody//tr//th', By.XPATH).text
        self.assertEqual(widget, "Codice")
        self.get_element('//div[@class="modal-content"]//button[@class="close"]', By.XPATH).click()
        sleep(1)

        self.get_element('(//div[@class="info-box"])[12]', By.XPATH).click()
        sleep(1)
        widget=self.get_element('//div[@class="modal-body"]//tbody//tr//th', By.XPATH).text
        self.assertEqual(widget, "Attività")
        self.get_element('//div[@class="modal-content"]//button[@class="close"]', By.XPATH).click()
        sleep(1)