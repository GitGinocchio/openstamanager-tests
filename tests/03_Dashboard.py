from common.Test import Test
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Dashboard(Test):
    def setUp(self):
        super().setUp()
        self.wait_driver = WebDriverWait(self.driver, 20)

    def test_Dashboard(self):
        self.navigateTo("Dashboard")
        self.wait_loader()

        actions = webdriver.common.action_chains.ActionChains(self.driver)
        calendar = self.driver.find_element(By.ID, 'calendar')
        actions.move_to_element(calendar).move_by_offset(300, 100).click().perform()
        modal = self.wait_modal()

        self.input(modal, 'Cliente').setByText("Cliente")
        self.input(modal, 'Tipo').setByIndex("1")
        expected_text = "Int. 1 Cliente\nTecnici: Stefano Bianchi"

        self.get_element('//a[@id="tecnici-sessioni-tab"]', By.XPATH).click()
        self.get_element('(//div[@id="tab_tecnici_sessioni"]//i[@class="fa fa-plus"])[2]', By.XPATH).click()
        self.wait_loader()
        technician_modal = self.wait_modal()

        denominazione_input = self.get_input("Denominazione")
        denominazione_input.send_keys("Stefano Bianchi")

        self.get_element('//div[@class="col-md-12 text-right"]//button[@type="submit"]', By.XPATH).click()
        self.wait_loader()

        #https://stackoverflow.com/questions/49603312/interacting-with-ckeditor-in-selenium-python

        request_xpath = '(//iframe[@class="cke_wysiwyg_frame cke_reset"])[1]'
        frame = self.get_element(request_xpath, By.XPATH)

        # Entra nel contesto dell'iframe
        self.driver.switch_to.frame(frame)

        body = self.driver.find_element(By.TAG_NAME, 'p')
        body.click()
        body.send_keys('Test')

        # Esce dal contesto dell'iframe
        self.driver.switch_to.default_content()

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        close_toast_button = self.wait_driver.until(EC.element_to_be_clickable((By.CLASS_NAME, "toast-close-button")))
        close_toast_button.click()

        self.get_element('//div[@class="col-md-12 text-right"]//button[@type="button"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Dashboard")
        self.wait_loader()

        self.get_element('//div[@class="tab-content"]//div[@class="row"]//div[@id="dashboard_tecnici"]//button[@type="button"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//div[@id="dashboard_tecnici"]//button[@class="btn btn-primary btn-sm seleziona_tutto"]', By.XPATH).click()
        self.wait_loader()

        activity = self.wait_driver.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="fc-event-main"]')))

        self.assertEqual(activity.text, expected_text)
        self.verifica_attività()

    def verifica_attività(self):
        self.navigateTo("Attività")
        self.wait_loader()

        search_input = self.find_filter_input("Numero")
        search_input.click()
        search_input.send_keys("1")
        self.wait_loader()

        technician_name = self.wait_driver.until(EC.visibility_of_element_located((By.XPATH, '//tbody//tr[1]//td[12]'))).text
        self.assertEqual("Stefano Bianchi", technician_name)

        self.navigateTo("Attività")
        self.wait_loader()

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//div[@id="tab_0"]//a[@class="btn btn-danger ask"]', By.XPATH).click()
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-danger"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Attività")
        self.wait_loader()

        empty_message = self.driver.find_element(By.XPATH, '//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("Nessun dato presente nella tabella", empty_message)
