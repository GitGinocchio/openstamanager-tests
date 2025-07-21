from common.Test import Test, get_html
from common.RowManager import RowManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GiacenzeSedi(Test):
    def setUp(self):
        super().setUp()

        
    def test_giacenze_sedi(self):
        wait = WebDriverWait(self.driver, 20)
        self.navigateTo("Statistiche")
        self.wait_loader()
        
        periodi = self.get_element('(//h4[@class="card-title"])[1]', By.XPATH).text
        self.assertEqual(periodi, "Vendite e acquisti")

        vendite = self.get_element('(//h4[@class="card-title"])[2]', By.XPATH).text
        self.assertEqual(vendite, "Periodi temporali")

        clienti = self.get_element('(//h4[@class="card-title"])[3]', By.XPATH).text
        articoli = self.get_element('(//h4[@class="card-title"])[4]', By.XPATH).text
        periodo = "01/01/2025 - 31/12/2025"

        self.assertEqual(clienti, "I 20 clienti TOP per il periodo: "+periodo)
        self.assertEqual(articoli, "I 20 articoli più venduti per il periodo: "+periodo)

        numero_interventi = self.get_element('(//h4[@class="card-title"])[5]', By.XPATH).text
        self.assertEqual(numero_interventi, "Numero interventi per tipologia")

        ore_interventi = self.get_element('(//h4[@class="card-title"])[6]', By.XPATH).text
        self.assertEqual(ore_interventi, "Ore interventi per tipologia")

        ore_tecnico = self.get_element('(//h4[@class="card-title"])[7]', By.XPATH).text
        self.assertEqual(ore_tecnico, "Ore di lavoro per tecnico")

        anagrafiche = self.get_element('(//h4[@class="card-title"])[8]', By.XPATH).text
        self.assertEqual(anagrafiche, "Nuove anagrafiche")