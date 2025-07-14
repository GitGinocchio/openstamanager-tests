#!/usr/bin/env python3
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from common.Test import Test

import logging
import time

class StatoServizi(Test):
    def setUp(self):
        super().setUp()
        self.wait_driver = WebDriverWait(self.driver, 10)
        self.logger = logging.getLogger(self.__class__.__name__)

    def test_stato_servizi(self):
        self.logger.info("Avvio del test di preparazione dello stato dei servizi")
        self.attiva_moduli()
        self.compila_azienda()
        self.creazione_fornitore_estero()
        self.creazione_cliente_estero()
        self.logger.info("Preparazione dello stato dei servizi completata con successo")

    # A volte funziona a volte no :/
    def attiva_moduli(self):
        self.logger.info("Attivazione dei moduli nascosti")
        self.expandSidebar("Strumenti")
        self.navigateTo("Stato dei servizi")

        self.wait_loader()

        loaders_xpath = "//i[contains(@class, 'fa') and contains(@class, 'fa-refresh') and contains(@class, 'fa-spin')]"


        moduli = [
            "Anagrafiche",
            "Gestione email",
            "Gestione documentale",
            "Attività",
            "Vendite"
        ]

        # Anagrafiche, Gestione email, Gestione documentale, Attivita, Vendite
        for modulo in moduli:
            # Aspetto che spariscano tutti gli elementi di caricamento
            self.wait_for_invisibility(loaders_xpath, By.XPATH)
            self.wait_loader()

            print(modulo)

            row_modulo = self.get_element(f'//tr[td[normalize-space()="{modulo}"]]', By.XPATH)

            self.scroll_to_element(row_modulo)

            # Se esiste il bottone abilitaModulo lo clicco
            # Se non esiste vuol dire che quel modulo è già stato abilitato, per sicurezza lo disabilito e riabilito
            if (enable_button:=self.exists('//button[@onclick="abilitaModulo(this)"]', By.XPATH)):
                enable_button.click()

                # Aspetto che si carichi il popup
                self.wait_swal2_popup()
                self.wait_for_invisibility(loaders_xpath, By.XPATH)
                self.wait_loader()

                # Confermo di voler abilitare il modulo
                confirm_button = self.get_element('//button[@class="swal2-confirm btn btn-lg btn-primary"]', By.XPATH)
                confirm_button.click()
            else:
                disable_button = self.get_element('//button[@onclick="disabilitaModulo(this)"]', By.XPATH, row_modulo)
                disable_button.click()

                self.wait_swal2_popup()
                self.wait_loader()

                # Confermo di voler disabilitare il modulo
                confirm_button = self.get_element('//button[@class="swal2-confirm btn btn-lg btn-primary"]', By.XPATH)
                confirm_button.click()

                self.wait_swal2_popup("disappear")
                self.wait_for_invisibility(loaders_xpath, By.XPATH)
                self.wait_loader()

                # Riabilito il modulo
                enable_button = self.get_element('//button[@onclick="abilitaModulo(this)"]', By.XPATH)
                enable_button.click()

                # Aspetto che si carichi il popup
                self.wait_swal2_popup()
                self.wait_loader()

                # Confermo di voler abilitare il modulo
                confirm_button = self.get_element('//button[@class="swal2-confirm btn btn-lg btn-primary"]', By.XPATH)
                confirm_button.click()

            self.wait_swal2_popup()
            self.wait_swal2_popup("disappear")
            self.wait_for_invisibility(loaders_xpath, By.XPATH)
            self.wait_loader()

            enable_submodules = self.get_element('//button[@onclick="abilitaSottoModuli(this)"]', By.XPATH)
            enable_submodules.click()

            self.wait_swal2_popup()
            self.wait_for_invisibility(loaders_xpath, By.XPATH)

            # Confermo di voler abilitare i sottomoduli
            confirm_button = self.get_element('//button[@class="swal2-confirm btn btn-lg btn-primary"]', By.XPATH)
            confirm_button.click()

            self.wait_for_invisibility(loaders_xpath, By.XPATH)
            self.wait_swal2_popup("disappear")
            self.wait_loader()

        self.logger.info("Tutti i moduli sono stati attivati con successo")

    def compila_azienda(self):
        self.logger.info("Compilazione delle informazioni aziendali")
        self.navigateTo("Anagrafiche")
        self.find_cell(col=2).click()
        self.wait_loader()
        self._compila_campi_azienda({
            'Partita IVA': '05024030289',
            'Codice fiscale': '05024030289',
            'Tipologia': 'Azienda',
            'C.A.P.': '35042',
            'Città': 'Este'
        })

        indirizzo = self.get_element("indirizzo")
        indirizzo.clear()
        indirizzo.send_keys("Via Rovigo, 51")
        
        self.get_element('save').click()
        self.wait_loader()
        self.logger.info("Informazioni aziendali salvate con successo")

    def creazione_fornitore_estero(self):
        self.logger.info("Creazione del fornitore estero")
        self._crea_anagrafica("Fornitore Estero", "Fornitore")
        self._compila_anagrafica_estera("Fornitore Estero", "05024030286", "Germania", "Berlino")
        self.logger.info("Fornitore estero creato con successo")

    def creazione_cliente_estero(self):
        self.logger.info("Creazione del cliente estero")
        self._crea_anagrafica("Cliente Estero", "Cliente")
        self._compila_anagrafica_estera("Cliente Estero", "05024030288", "Germania", "Piacenza d'Adige")
        self.logger.info("Cliente estero creato con successo")

    def _crea_anagrafica(self, nome: str, tipo: str):
        self.navigateTo("Anagrafiche")

        self.get_element('//i[@class="fa fa-plus"]', By.XPATH).click()
        modal = self.wait_modal()
        self.input(modal, 'Denominazione').setValue(nome)
        self.input(modal, 'Tipo di anagrafica').setByText(tipo)
        self.get_element('button[type="submit"]', By.CSS_SELECTOR).click()
        self.wait_loader()

    def _compila_anagrafica_estera(self, nome: str, piva: str, nazione: str, citta: str):
        self.navigateTo("Anagrafiche")

        filtro = self.find_filter_input("Ragione sociale")
        filtro.send_keys(nome)

        self.click_first_result()
        self.wait_loader()

        results = self.get_select_search_results("Nazione", nazione)
        if len(results) > 0: results[0].click()

        self._compila_campi_azienda({
            'Partita IVA': piva,
            'Codice fiscale': piva,
            'Tipologia': 'Azienda',
            'C.A.P.': '35042',
            'Città': citta
        })

        indirizzo = self.get_element("indirizzo")
        indirizzo.clear()
        indirizzo.send_keys('Via controllo caratteri speciali: &"<>èéàòùì?\'\'`')
        self.get_element('save', By.ID).click()
        self.wait_loader()

        self.clear_filters()
        self.navigateTo("Anagrafiche")
        self.wait_loader()

    def _compila_campi_azienda(self, campi: dict):
        for campo, valore in campi.items():
            input_field = self.input(None, campo)
            if input_field:
                input_field.setValue(valore)
            else:
                self.logger.warning(f"Campo '{campo}' non trovato")
