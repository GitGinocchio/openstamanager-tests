from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from common.Test import Test, get_html


class AccountEmail(Test):
    def setUp(self):
        super().setUp()

        self.expandSidebar("Gestione email")


    def test_creazione_accountemail(self):
        # Creazione account email   *Required* 
        self.creazione_account_email("Account di Prova da Eliminare", self.getConfig('tests.email_user'), self.getConfig('tests.email_user'))

        # Modifica account email
        self.modifica_account_email(self.getConfig('tests.email_user'), "smtps.aruba.it", "465")

        # Cancellazione account email
        self.elimina_account_email()

        # Verifica account email
        self.verifica_account_email()

        # Invia mail (Azioni di gruppo) da Attività
        self.invia_mail()

    def creazione_account_email(self, nomeaccount=str, nomevisualizzato=str, emailmittente=str):
        self.navigateTo("Account email")

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()

        self.input(modal, 'Nome account').setValue(nomeaccount)
        self.input(modal, 'Nome visualizzato').setValue(nomevisualizzato)
        self.input(modal, 'Email mittente').setValue(emailmittente)

        modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.wait_loader()

    def modifica_account_email(self, emailmittente:str, server:str, porta:str):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Account email")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome-account"]/input'))).send_keys('Account Email da Impostazioni', Keys.ENTER)        
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        self.input(None, 'Email mittente').setValue(emailmittente)
        self.input(None, 'Server SMTP').setValue(server)
        self.input(None, 'Porta SMTP').setValue(porta)

        self.get_element('//div[@id="tab_0"]//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Account email")
        self.wait_loader()    

        self.get_element('//th[@id="th_Nome-account"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def elimina_account_email(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Account email")
        self.wait_loader()    

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome-account"]/input'))).send_keys('Account di Prova da Eliminare', Keys.ENTER)        
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        sleep(1)
        
        wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="tab_0"]//a[@class="btn btn-danger ask"]'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@class="swal2-confirm btn btn-lg btn-danger"]'))).click()
        self.wait_loader()

        self.get_element('//th[@id="th_Nome-account"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

        
    def verifica_account_email(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Account email")
        self.wait_loader()    

        # Verifica elemento modificato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome-account"]/input'))).send_keys("Account email da Impostazioni", Keys.ENTER)
        sleep(1)

        modificato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[3]').text
        self.assertEqual("Account email da Impostazioni",modificato)
        self.get_element('//i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

        # Verifica elemento eliminato
        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome-account"]/input'))).send_keys("Account di Prova da Eliminare", Keys.ENTER)
        sleep(1)
        
        eliminato=self.driver.find_element(By.XPATH,'//tbody//tr[1]//td[@class="dataTables_empty"]').text
        self.assertEqual("La ricerca non ha portato alcun risultato.",eliminato)

        self.get_element('//th[@id="th_Nome-account"]/i[@class="deleteicon fa fa-times"]', By.XPATH).click()
        sleep(1)

    def invia_mail(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Account email")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Nome-account"]/input'))).send_keys("Account email", Keys.ENTER)  
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click()
        self.wait_loader()

        self.get_element('//span[@id="select2-encryption-container"]', By.XPATH).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("SSL", Keys.ENTER)

        self.input(None, 'Password SMTP').setValue(self.getConfig('tests.email_password'))

        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Anagrafiche")
        self.wait_loader()

        wait.until(EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Ragione-sociale"]/input'))).send_keys("Cliente", Keys.ENTER)
        sleep(1)

        self.get_element('//tbody//tr//td[2]', By.XPATH).click() 
        sleep(1)

        self.input(None, 'Email').setValue(self.getConfig('tests.email_user'))
        self.get_element('//button[@id="save"]', By.XPATH).click()
        self.wait_loader()

        self.navigateTo("Attività")
        self.wait_loader()

        self.get_element('//tbody//tr//td', By.XPATH).click() 
        self.get_element('//button[@data-toggle="dropdown"]', By.XPATH).click() 
        sleep(1)

        self.get_element('//a[@data-op="send-mail"]', By.XPATH).click()
        sleep(1)

        self.get_element('//span[@id="select2-id_template-container"]', By.XPATH).click() 
        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys("rapportino")
        sleep(1)

        wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@class="select2-search__field"]'))).send_keys(Keys.ENTER)
        self.get_element('//button[@class="swal2-confirm btn btn-lg btn-warning"]', By.XPATH).click()  
        self.wait_loader()

        scritta=self.get_element('//tbody//tr//td[14]', By.XPATH).text 
        self.assertEqual(scritta, "Inviata via email")


        
