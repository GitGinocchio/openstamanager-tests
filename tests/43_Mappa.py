from common.Test import Test, get_html
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class Mappa(Test):
    def setUp(self):
        super().setUp()

        
    def test_mappa(self):
        self.navigateTo("Mappa")

        self.get_element('//div[@id="mappa"]', By.XPATH).click()