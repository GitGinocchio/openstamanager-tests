from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from common.Test import Test

class Init(Test):
    def setUp(self):
        super().setUp(False)
        self.connect()

    def test_config(self):
        # TODO: Capire cosa vuole fare qui
        next_button_xpath = '//*[@id="smartwizard"]/div[2]/div/button[2]'
        self.get_element(next_button_xpath, By.XPATH).click()

        self.get_element('agree').click()
        self.get_element(next_button_xpath, By.XPATH).click()

        self.input(None, "Host del database").setValue(self.getConfig('database.host'))
        self.input(None, "Username dell'utente MySQL").setValue(self.getConfig('database.user'))
        self.input(None, "Password dell'utente MySQL").setValue(self.getConfig('database.pass'))
        self.input(None, "Nome del database").setValue(self.getConfig('database.name'))

        self.get_element('//*[@id="install"]', By.XPATH).click()
        self.wait(EC.visibility_of_element_located((By.ID, 'contine_button')))

        self.get_element('//*[@id="contine_button"]', By.XPATH).click()
        self.get_element('/html/body/div[2]/div/div[10]/button[1]', By.XPATH).click()

        self.wait(EC.visibility_of_element_located((By.XPATH, '//*[@id="result"]/a')), 300)
        self.get_element('//*[@id="result"]/a', By.XPATH).click()

        self.input(None, 'Username').setValue(self.getConfig('login.username'))
        self.input(None, 'Password').setValue(self.getConfig('login.password'))
        self.input(None, 'Email').setValue(self.getConfig('login.username') + '@test.com')
        self.input(None, 'Denominazione').setValue("Azienda")
        self.input(None, 'Regime Fiscale').setByText("Ordinario")
        self.input(None, 'Conto predefinito fatture di vendita').setByText("000010 - Ricavi merci c/to vendite")
        self.input(None, 'Conto predefinito fatture di acquisto').setByText("000010 - Costi merci c/acquisto di rivendita")
        self.input(None, 'Valuta').setByText("Euro - €")

        self.get_element('//*[@id="config"]', By.XPATH).click()
