from common.Test import Test, get_html
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Checklists(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Strumenti")


    def test_checklists(self):
        # Creazione Checklist
        self.checklists("Checklist di Prova da Modificare", "Attività", "Interventi svolti")
        self.checklists("Checklist di Prova da Eliminare", "Attività", "Interventi svolti")

        # Modifica Checklist
        self.modifica_checklist("Checklist di Prova")
        
        # Cancellazione Checklist
        self.elimina_checklist()
        
        # Verifica Checklist
        self.verifica_checklist()

    def checklists(self, nome=str, modulo= str, plugin=str):
        self.navigateTo("Checklists")
        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        self.input(modal, 'Nome').setValue(nome)
        select = self.input(modal, 'Modulo del template')
        select.setByText(modulo)
        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

    def modifica_checklist(self, modifica=str):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Checklists")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Checklist di Prova da Modificare', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        sleep(1)

        self.driver.execute_script('window.scrollTo(0,0)')
        self.input(None,'Nome').setValue(modifica)

        self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('(//iframe[@class="cke_wysiwyg_frame cke_reset"])[1]', By.XPATH).click()  
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//iframe[@class="cke_wysiwyg_frame cke_reset"])[1]'))).send_keys("TestPadre")
        self.get_element('(//button[@type="submit"])[2]', By.XPATH).click()
        sleep(1)

        self.get_element('(//iframe[@class="cke_wysiwyg_frame cke_reset"])[1]', By.XPATH).click()  
        wait.until(EC.visibility_of_element_located((By.XPATH, '(//iframe[@class="cke_wysiwyg_frame cke_reset"])[1]'))).send_keys("TestFiglio")
        self.get_element('(//span[@class="select2-selection select2-selection--single"])[3]', By.XPATH).click()
        self.get_element('//li[@class="select2-results__option select2-results__option--highlighted"]', By.XPATH).click()
        self.get_element('(//button[@type="submit"])[2]', By.XPATH).click()
        sleep(1)

        self.navigateTo("Checklists")
        self.wait_loader()    

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def elimina_checklist(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Checklists")
        self.wait_loader()    

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys('Checklist di Prova da Eliminare', Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        sleep(1)

        self.driver.execute_script('window.scrollTo(0,0)')
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        self.wait_loader()      

        self.get_element('//th[@id="th_Nome"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)
        
    def verifica_checklist(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Checklists")
        self.wait_loader()    

        # Verifica elemento modificato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Checklist di Prova", Keys.ENTER)
        sleep(1)

        modificato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[2]').text
        self.assertEqual("Checklist di Prova",modificato)
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

        # Verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome"]/input'))).send_keys("Checklist di Prova da Eliminare", Keys.ENTER)
        sleep(1)

        self.navigateTo("Attività")  

        self.get_element('//div[@id="tab_0"]//tbody//tr[2]//td[2]', By.XPATH).click()
        self.wait_loader()


        self.get_element('//a[@href="#tab_checks"]', By.XPATH).click()
        self.wait_loader()

        self.get_element('(//a[@data-title="Aggiungi check"])[2]', By.XPATH).click()
        sleep(1)

        self.get_element('//div[@class="modal-content"]//span[@class="select2-selection__placeholder"]', By.XPATH).click()
        self.get_element('//li[@class="select2-results__option select2-results__option--highlighted"]', By.XPATH).click()
        self.get_element('//button[@id="check-add"]', By.XPATH).click()
        sleep(1)

        TestPadre = self.get_element('(//div[@id="tab_checks"]//tbody//td[2]//span, By.XPATH)[1]').text
        TestFiglio = self.get_element('(//div[@id="tab_checks"]//tbody//td[2]//span, By.XPATH)[2]').text
        self.assertEqual("TestPadre", TestPadre)
        self.assertEqual("TestFiglio", TestFiglio)

        self.get_element('(//input[@class="checkbox unblockable"])[2]', By.XPATH).click()

        test1 = self.get_element('(//input[@class="checkbox unblockable"])[1]', By.XPATH).is_selected()
        test2 = self.get_element('(//input[@class="checkbox unblockable"])[2]', By.XPATH).is_selected()
        self.assertEqual(test1, False)
        self.assertEqual(test2, True)                