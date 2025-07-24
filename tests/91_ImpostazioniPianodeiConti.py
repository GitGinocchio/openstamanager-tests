from common.Test import Test, get_html
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Impostazioni(Test):
    def setUp(self):
        super().setUp()

    def test_impostazioni_piano_dei_conti(self):
        pass
        # Conto per Riepilogativo fornitori
        #self.conto_riepilogativo_fornitori()

        # Conto per Riepilogativo clienti
        #self.conto_riepilogativo_clienti()

        # Conto per Iva indetraibile
        #self.conto_iva_indetraibile()

        # Conto per Iva su vendite
        #self.conto_iva_vendite()

        # Conto per Iva su acquisti
        #self.conto_iva_acquisti()

        # Conto per Erario c/ritenute d'acconto
        #self.conto_erario_ritenute_acconto()

        # Conto per Erario c/INPS 
        #self.conto_erario_inps()

        # Conto per Erario c/enasarco 
        #self.conto_erario_enasarco()

        # Conto per Apertura conti patrimoniali 
        #self.conto_apertura_conti_patrimoniali()

        # Conto per Chiusura conti patrimoniali 
        #self.conto_chiusura_conti_patrimoniali()

        # Conto per autofattura 
        #self.conto_autofattura()

        # Conto di secondo livello per i crediti clienti
        #self.conto_secondo_livello_crediti_clienti()

        # Conto di secondo livello per i debiti fornitori
        #self.conto_secondo_livello_debiti_fornitori()

    def conto_riepilogativo_fornitori(self):
        wait = WebDriverWait(self.driver, 20)
        self.expandSidebar("Contabilità")
        self.navigateTo("Piano dei conti")
        self.wait_loader()

        self.get_element('//button[@id="conto2-8"]', By.XPATH).click() #apro sezione "240 Debiti fornitori e debiti diversi"
        sleep(1)

        conto=self.get_element('//span[@id="movimenti-34"]', By.XPATH).text    #controllo presenza del conto
        self.assertEqual(conto, " 240.000010 Riepilogativo fornitori")

    def conto_riepilogativo_clienti(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Piano dei conti")
        self.wait_loader()

        self.get_element('//button[@id="conto2-2"]', By.XPATH).click() #apro sezione "110 Crediti clienti e crediti diversi "
        sleep(1)

        conto=self.get_element('//span[@id="movimenti-6"]', By.XPATH).text    #controllo presenza del conto
        self.assertEqual(conto, " 110.000010 Riepilogativo clienti")

    def conto_iva_indetraibile(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Piano dei conti")
        self.wait_loader()

        self.get_element('//button[@id="conto2-22"]', By.XPATH).click() #apro sezione "900 Conti transitori "
        sleep(1)

        conto=self.get_element('//span[@id="movimenti-108"]', By.XPATH).text    #controllo presenza del conto
        self.assertEqual(conto, " 900.000030 Iva indetraibile")

    def conto_iva_vendite(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Piano dei conti")
        self.wait_loader()

        self.get_element('//button[@id="conto2-22"]', By.XPATH).click() #apro sezione "900 Conti transitori "
        sleep(1)

        conto=self.get_element('//span[@id="movimenti-106"]', By.XPATH).text    #controllo presenza del conto
        self.assertEqual(conto, " 900.000010 Iva su vendite")

    def conto_iva_acquisti(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Piano dei conti")
        self.wait_loader()

        self.get_element('//button[@id="conto2-22"]', By.XPATH).click() #apro sezione "900 Conti transitori "
        sleep(1)

        conto=self.get_element('//span[@id="movimenti-107"]', By.XPATH).text    #controllo presenza del conto
        self.assertEqual(conto, " 900.000020 Iva su acquisti")

    def conto_erario_ritenute_acconto(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Piano dei conti")
        self.wait_loader()

        self.get_element('//button[@id="conto2-5"]', By.XPATH).click() #apro sezione "200 Erario iva, INPS, IRPEF, INAIL, ecc "
        sleep(1)

        conto=self.get_element('//span[@id="movimenti-23"]', By.XPATH).text    #controllo presenza del conto
        self.assertEqual(conto, " 200.000060 Erario c/ritenute d'acconto")

    def conto_erario_inps(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Piano dei conti")
        self.wait_loader()

        self.get_element('//button[@id="conto2-5"]', By.XPATH).click() #apro sezione "200 Erario iva, INPS, IRPEF, INAIL, ecc "
        sleep(1)

        conto=self.get_element('//span[@id="movimenti-19"]', By.XPATH).text    #controllo presenza del conto
        self.assertEqual(conto, " 200.000010 Erario c/INPS")

    def conto_erario_enasarco(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Piano dei conti")
        self.wait_loader()

        self.get_element('//button[@id="conto2-5"]', By.XPATH).click() #apro sezione "200 Erario iva, INPS, IRPEF, INAIL, ecc "
        sleep(1)

        conto=self.get_element('//span[@id="movimenti-24"]', By.XPATH).text    #controllo presenza del conto
        self.assertEqual(conto, " 200.000070 Erario c/enasarco")

    def conto_apertura_conti_patrimoniali(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Piano dei conti")
        self.wait_loader()

        self.get_element('//button[@id="conto2-21"]', By.XPATH).click() #apro sezione "810 Perdite e profitti "
        sleep(1)

        conto=self.get_element('//span[@id="movimenti-104"]', By.XPATH).text    #controllo presenza del conto
        self.assertEqual(conto, " 810.000010 Apertura conti patrimoniali")

    def conto_chiusura_conti_patrimoniali(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Piano dei conti")
        self.wait_loader()

        self.get_element('//button[@id="conto2-21"]', By.XPATH).click() #apro sezione "810 Perdite e profitti "
        sleep(1)

        conto=self.get_element('//span[@id="movimenti-105"]', By.XPATH).text    #controllo presenza del conto
        self.assertEqual(conto, " 810.000900 Chiusura conti patrimoniali")

    def conto_autofattura(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Piano dei conti")
        self.wait_loader()

        self.get_element('//button[@id="conto2-23"]', By.XPATH).click() #apro sezione "910 Conti compensativi"
        sleep(1)

        conto=self.get_element('//span[@id="movimenti-115"]', By.XPATH).text    #controllo presenza del conto
        self.assertEqual(conto, " 910.000010 Compensazione per autofattura")

    def conto_secondo_livello_crediti_clienti(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Piano dei conti")
        self.wait_loader()

        sezionale=self.get_element('//span[@id="conto2-2"]//b', By.XPATH).text    #controllo presenza del sezionale
        self.assertEqual(sezionale, "110 Crediti clienti e crediti diversi")

    def conto_secondo_livello_debiti_fornitori(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Piano dei conti")
        self.wait_loader()

        sezionale=self.get_element('//span[@id="conto2-8"]//b', By.XPATH).text    #controllo presenza del sezionale
        self.assertEqual(sezionale, "240 Debiti fornitori e debiti diversi")

