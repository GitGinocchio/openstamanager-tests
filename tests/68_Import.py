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
import os

class Import_(Test):
    def setUp(self):
        super().setUp()

     
    def test_import(self):
        self.expandSidebar("Strumenti")
        self.navigateTo("Import")

        #self.get_element('//*[@id="select2-id_import-container"]', By.XPATH).click()
        #self.get_element('//input[@class="select2-search__field"]', By.XPATH).send_keys("Anagrafiche", Keys.ENTER)
        #self.wait_loader()

        #self.get_element('//input[@id="file"]', By.XPATH).send_keys(os.path.join(os.getcwd(), 'example-anagrafiche.csv'))
        #sleep(1)

        #self.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()