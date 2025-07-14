from common.Test import Test
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Backup(Test):
    def setUp(self):
        super().setUp()
        self.wait_driver = WebDriverWait(self.driver, 20)
        self.expandSidebar("Strumenti")

    def test_creazione_backup(self):
        self.navigateTo("Backup")
        self.wait_loader()

        self.get_element('//a[@onclick="creaBackup(this)"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-success"]', By.XPATH).click()

        self.wait_loader()