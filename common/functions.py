from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, List, Optional, Callable, Union
from bs4 import BeautifulSoup
from typing import Literal
import os
import re
import glob
import string
import random
import json
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

class TestHelperMixin:
    """Mixin class that provides helper methods for Selenium tests.

    This mixin wraps the helper functions to avoid passing driver and wait_driver
    parameters repeatedly. It assumes the class has self.driver and self.wait_driver attributes.
    """

    def search_entity(self, name: str) -> None:
        """Search for an entity by name."""
        search_entity(self.driver, self.wait_driver, name)

    def click_first_result(self) -> None:
        """Click on the first result in the search results."""
        click_first_result(self.driver, self.wait_driver)

    def wait_for_filter_cleared(self) -> None:
        """Wait for filters to be cleared."""
        wait_for_filter_cleared(self.driver, self.wait_driver)

    def find_filter_input(self, name: str) -> WebElement:
        """Finds and returns the input element associated with the specified filter name.

        The filter is identified by a `<th>` element whose `id` attribute follows the format:

            \t th_[filter-name] (with spaces replaced by hyphens)

        Example:
            name = "Regione sociale"
            The function will look for an input inside:

            `<th id="th_Regione-sociale"><input ...></th>`

        Args:
            name (str): The name of the filter to search for.

        Returns:
            WebElement: The visible <input> element inside the matching filter.
        """
        return find_filter_input(self.driver, self.wait_driver, name)

    def clear_filters(self) -> None:
        """Clear all filters."""
        clear_filters(self.driver, self.wait_driver)

    # TODO: Modificare find_cell/find_cells -> get_cell/get_cells
    def find_cell(self, row: int | None = None, col: int | None = None, context : WebElement | None = None) -> WebElement:
        """
            Finds one cell (`<td>`) in an HTML table by specifying the row and/or column (1-based).

            :param row: Row number (1-based), or None
            :param col: Column number (1-based), or None
            :return: A single WebElement
        """
        return find_cells(self.driver, self.wait_driver, row, col, multiple=False, context=context)

    def find_cells(self, row: int | None = None, col: int | None = None, multiple : bool = False, context : WebElement | None = None) -> Union[WebElement, List[WebElement]]:
        """
            Finds one or more cells (<td>) in an HTML table by specifying the row and/or column (1-based).

            If multiple is False (default), returns a single element.
            If multiple is True, returns a list of elements.

            :param wait_driver: WebDriverWait used to wait for the elements
            :param row: Row number (1-based), or None
            :param col: Column number (1-based), or None
            :param multiple: If True, returns multiple elements; otherwise, a single element
            :return: A single WebElement or a list of WebElements
        """
        return find_cells(self.driver, self.wait_driver, row, col, multiple=multiple, context=context)

    def get_select_search_results(self, field_name : str, search_query : str | None = None, label_for : str | None = None, context: WebElement | None = None) -> list[WebElement]:
        return get_select_search_results(self.driver, self.wait_driver, field_name, search_query, label_for, context=context)

    def get_input(self, label : str) -> WebElement:
        return get_input(self.driver, self.wait_driver, label)

    def get_elements(self, selector : str, by: By = By.ID, context : WebElement | None = None) -> list[WebElement]:
        return get_elements(self.driver, self.wait_driver, selector, by, context)

    def get_element(self, selector : str, by: By = By.ID, context : WebElement | None = None) -> WebElement:
        return get_element(self.driver, self.wait_driver, selector, by, context)

    def exists(self, selector : str, by: By = By.ID, context : WebElement | None = None) -> WebElement | None:
        return exists(self.driver, self.wait_driver, selector, by, context)

    def is_clickable(self, element : WebElement) -> bool:
        return is_clickable(self.driver, self.wait_driver, element)

    def wait_for_search_results(self) -> None:
        """Wait for search results to load."""
        wait_for_search_results(self.driver, self.wait_driver)

    def wait_for_element_and_click(self, selector: str, by: By = By.XPATH) -> WebElement:
        """Wait for an element to be clickable and click it."""
        return wait_for_element_and_click(self.driver, self.wait_driver, selector, by)

    def wait_for_dropdown_and_select(self, dropdown_xpath: str, option_xpath: str = None, option_text: str = None, by: By = By.XPATH) -> None:
        """Wait for a dropdown to be clickable, click it, and select an option."""
        wait_for_dropdown_and_select(self.driver, self.wait_driver, dropdown_xpath, option_xpath, option_text)

    def wait_loader(self) -> None:
        """Wait for all loaders to disappear."""
        wait_loader(self.driver, self.wait_driver)

    def send_keys_and_wait(self, element, text, wait_modal=True) -> None:
        """Send keys to an element and wait for the page to load after pressing Enter."""
        # Use the global function for consistency
        return send_keys_and_wait(self.driver, self.wait_driver, element, text, wait_modal)

    def delete_and_confirm(self, context: WebElement | None = None):
        delete_and_confirm(self.driver, self.wait_driver)

    def click_plugin(self, name : str) -> None:
        click_plugin(self.driver, self.wait_driver, name)

    def wait_for_invisibility(self, selector: str, by : By = By.ID) -> None:
        wait_for_invisibility(self.driver, self.wait_driver, selector, by)
    
    def wait_for_visibility(self, selector: str, by: By = By.ID) -> WebElement:
        return wait_for_visibility(self.driver, self.wait_driver, selector, by)

    def wait_swal2_popup(self, mode: Literal["appear", "disappear"] = "appear") -> None:
        """
        Waits for the SweetAlert2 modal popup to either appear or disappear on the page.

        This function pauses execution until an element with the class 'swal2-modal'
        becomes visible or invisible, depending on the specified mode.

        Args:
            driver (WebDriver): The Selenium WebDriver instance controlling the browser.
            wait_driver (WebDriverWait): An instance of WebDriverWait configured with a timeout.
            mode (Literal["appear", "disappear"]): Determines the wait condition:
                - "appear": Waits until the modal becomes visible.
                - "disappear": Waits until the modal is no longer visible or is removed from the DOM.

        Returns:
            None
        """
        wait_swal2_popup(self.driver, self.wait_driver, mode)

    def scroll_to_element(self, element: WebElement, offset: int = 0) -> None:
        """
        Scrolls the page vertically to bring the specified element into view, with an optional offset.

        This function uses JavaScript to scroll the window to the vertical position of the given element,
        minus an optional offset. The scroll behavior is smooth by default. Useful when elements are
        hidden under fixed headers or need to be centered in the viewport.

        Args:
            driver (WebDriver): The Selenium WebDriver instance controlling the browser.
            wait_driver (WebDriverWait): An instance of WebDriverWait (currently unused but included for consistency).
            element (WebElement): The element to scroll to.
            offset (int, optional): The number of pixels to offset from the top of the element. 
                                    Use a positive value to scroll above the element. Defaults to 0.

        Returns:
            None
        """
        scroll_to_element(self.driver, self.wait_driver, element, offset)

    def scroll_to_bottom(self, pause_time: float = 1.0, max_tries: int = 30) -> None:
        """
        Scrolla fino in fondo alla pagina web.

        :param driver: Il WebDriver Selenium.
        :param wait_driver: Un'istanza di WebDriverWait.
        :param pause_time: Tempo in secondi tra uno scroll e l'altro.
        :param max_tries: Numero massimo di tentativi per rilevare nuovo contenuto.
        """
        scroll_to_bottom(self.driver, self.wait_driver, pause_time, max_tries)

    def expand_plugin_sidebar(self):
        expand_plugin_sidebar(self.driver, self.wait_driver)

def random_string(size: int = 32, chars: str = string.ascii_letters + string.digits) -> str:
    return ''.join(random.choice(chars) for _ in range(size))

def get_cache_directory() -> Path:
    current_dir = Path(__file__).parent
    cache_dir = current_dir.parent / 'cache'
    cache_dir.mkdir(exist_ok=True)
    return cache_dir

def get_config() -> Dict:
    config_file = get_cache_directory().parent / 'config.json'

    try:
        if config_file.exists():
            with config_file.open('r', encoding='utf-8') as f:
                return json.load(f)
    except json.JSONDecodeError:
        print(f"Errore nel parsing del file {config_file}")
    except Exception as e:
        print(f"Errore nella lettura del file {config_file}: {e}")

    return {}

def update_config(config: Dict) -> None:
    config_file = get_cache_directory().parent / 'config.json'

    try:
        with config_file.open('w+', encoding='utf-8') as f:
            json.dump(config, f, indent=4, sort_keys=True, ensure_ascii=False)
    except Exception as e:
        print(f"Errore nell'aggiornamento del file {config_file}: {e}")

def get_args() -> ArgumentParser:
    parser = ArgumentParser(description='Script di gestione test')
    parser.add_argument(
        "-a",
        "--action",
        dest="action",
        help="Imposta l'azione da eseguire",
        metavar="ACTION"
    )
    return parser.parse_args()

def list_files(path: str, include_hidden: bool = True) -> List[str]:
    path = Path(path)
    if not path.exists():
        return []

    files = glob.glob(str(path / '**' / '*'), recursive=True)

    if include_hidden:
        hidden_files = glob.glob(str(path / '**' / '.*'), recursive=True)
        files.extend(hidden_files)

    return sorted(files)

def safe_path_join(*paths: str) -> str:
    return os.path.normpath(os.path.join(*paths))

def ensure_directory(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)

#TODO: generalizzare
def search_entity(driver: WebDriver, wait_driver: WebDriverWait, name: str) -> None:
    try:
        clear_buttons = driver.find_elements(By.XPATH, '//i[@class="deleteicon fa fa-times"]')
        for button in clear_buttons:
            try:
                button.click()
                wait_driver.until(
                    EC.invisibility_of_element_located((By.XPATH, '//div[@class="select2-search select2-search--dropdown"]'))
                )
            except:
                pass
    except:
        pass

    search_input = wait_driver.until(
        EC.visibility_of_element_located((By.XPATH, '//th[@id="th_Ragione-sociale"]/input'))
    )
    search_input.clear()
    search_input.send_keys(name, Keys.ENTER)

def get_select_search_results(driver: WebDriver, wait_driver: WebDriverWait, field_name : str, search_query : str | None = None, label_for : str = None, context : WebElement | None = None) -> list[WebElement]:
    """
    Returns a list of `<li>` elements representing search results inside a Select2 dropdown 
    associated with a specific `<label>` element.

    The function performs the following steps:
    1. Locates a `<label>` containing `field_name` in its visible text (including text inside child tags).
       If provided, it also verifies that the `for` attribute matches `label_for`.
    2. Extracts the value of the `for` attribute, which corresponds to the ID of the associated field.
    3. Builds the Select2 container ID and clicks the corresponding `<span>` element to open the dropdown.
    4. If `search_query` is provided, it enters the text into the Select2 search input.
    5. Waits for the loading indicator (`.loading-results` `<li>`) to disappear.
    6. Waits for the result elements to become visible and clickable.
    7. Returns a list of all matching `<li>` elements found in the dropdown.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        wait_driver (WebDriverWait): An instance of WebDriverWait for handling explicit waits.
        field_name (str): The visible text (or partial text) of the `<label>` associated with the Select2 element.
        search_query (str | None, optional): The text to type into the Select2 search box. Defaults to None.
        label_for (str | None, optional): Expected value of the label's `for` attribute, if known. Defaults to None.
        context: (WebElement | None): Optional context to search elements into it

    Returns:
        list[WebElement]: A list of `<li>` elements representing the available search results.

    Raises:
        TimeoutException: If a required element is not found within the specified timeout.
    """
    search_root = context if context else driver

    # 1. Trova il <label> corrispondente
    inner_xpath = f'@for="{label_for}" and ' if label_for else ""
    xpath = f'.//label[{inner_xpath}contains(normalize-space(string(.)), "{field_name}")]'

    try:
        label = wait_driver.until(lambda d: search_root.find_element(By.XPATH, xpath))
    except TimeoutException:
        print(f"Label con testo '{field_name}' non trovato.")
        return []

    label_for = label.get_attribute("for")
    print(f"[DEBUG] label_for: {label_for}")

    # 2. Apri la Select2
    select_id = f"select2-{label_for}-container"
    try:
        select_span = wait_driver.until(lambda d: search_root.find_element(By.XPATH, f'.//span[@id="{select_id}"]'))
        select_span.click()
    except TimeoutException:
        print(f"Elemento con id 'select2-{label_for}-container' non cliccabile.")
        return []

    results_id = f"select2-{label_for}-results"

    # 3. Scrivi nella casella di ricerca, se richiesto
    if search_query:
        input_xpath = f'.//input[@aria-controls="{results_id}"]'
        try:
            input_element = wait_driver.until(lambda d: driver.find_element(By.XPATH, input_xpath))
            input_element.clear()
            input_element.click()
            input_element.send_keys(search_query, Keys.ENTER)
        except TimeoutException:
            print(f"Input di ricerca per '{results_id}' non trovato.")
            return []

    # 4. Attendi che il caricamento termini (loading-results)
    loading_li_xpath = f'.//ul[@id="{results_id}"]/li[contains(@class, "loading-results")]'
    try:
        loading_elements = driver.find_elements(By.XPATH, loading_li_xpath)
        if loading_elements:
            wait_driver.until(EC.invisibility_of_element_located((By.XPATH, loading_li_xpath)))
    except TimeoutException:
        print("L'elemento 'loading-results' potrebbe essere ancora visibile dopo il timeout.")

    # 5. Rimuovi eventuali filtri precedenti con il pulsante "x"
    clear_buttons = select_span.find_elements(By.CSS_SELECTOR, "span.select2-selection__clear")
    if clear_buttons:
        clear_buttons[0].click()

    # 6. Raccogli i risultati <li>
    results_xpath = f'.//ul[@id="{results_id}"]/li'
    try:
        results = wait_driver.until(lambda d: driver.find_elements(By.XPATH, results_xpath))
        if not search_query and results:
            wait_driver.until(EC.element_to_be_clickable(results[0]))  # Aspetta che almeno il primo sia cliccabile
        return results
    except TimeoutException:
        print("Nessun risultato trovato o risultato non cliccabile.")
        return []

# Dovrei crearla per assicurarmi che i click ai risultati siano sempre validi
def click_select_search_result(): pass

def click_first_result(driver: WebDriver, wait_driver: WebDriverWait) -> None:
    wait_loader(driver, wait_driver)

    result = find_cells(driver, wait_driver, row=0, col=2)
    result.click()

    wait_loader(driver, wait_driver)

def wait_for_filter_cleared(driver: WebDriver, wait_driver: WebDriverWait) -> None:
    wait_driver.until(
        EC.invisibility_of_element_located((By.XPATH, '//div[@class="select2-search select2-search--dropdown"]'))
    )

def find_filter_input(driver: WebDriver, wait_driver: WebDriverWait, name: str) -> WebElement:
    """Finds and returns the input element associated with the specified filter name.

    The filter is identified by a `<th>` element whose `id` attribute follows the format:

        \t th_[filter-name] (with spaces replaced by hyphens)

    Example:
        name = "Regione sociale"
        The function will look for an input inside:

        `<th id="th_Regione-sociale"><input ...></th>`

    Args:
        driver (WebDriver): Instance of the Selenium WebDriver.
        wait_driver (WebDriverWait): Instance of WebDriverWait used to wait for the element.
        name (str): The name of the filter to search for.

    Returns:
        WebElement: The visible <input> element inside the matching filter.
    """
    return wait_driver.until(
        EC.visibility_of_element_located((By.XPATH, f'//th[@id="th_{name.replace(" ", "-")}"]/input'))
    )

def clear_filters(driver: WebDriver, wait_driver: WebDriverWait) -> None:
    try:
        wait_loader(driver, wait_driver)

        clear_buttons = driver.find_elements(By.XPATH, '//i[@class="deleteicon fa fa-times"]')

        if not clear_buttons:
            search_inputs = driver.find_elements(By.XPATH, '//th//input[not(@type="checkbox")]')
            for input_field in search_inputs:
                if input_field.get_attribute('value'):
                    input_field.clear()
                    input_field.send_keys(Keys.ENTER)
                    wait_loader(driver, wait_driver)
        else:
            for button in clear_buttons:
                try:
                    button.click()
                    wait_for_filter_cleared(driver, wait_driver)
                    wait_loader(driver, wait_driver)
                except:
                    pass

        wait_loader(driver, wait_driver)
    except Exception as e:
        print(f"Warning: Could not clear filters: {str(e)}")

def find_cells(driver: WebDriver, wait_driver: WebDriverWait, row: int | None = None, col: int | None = None, multiple : bool = False, context: WebElement | None = None) -> Union[WebElement, List[WebElement]]:
    """
        Finds one or more cells (<td>) in an HTML table by specifying the row and/or column (1-based).

        If multiple is False (default), returns a single element.
        If multiple is True, returns a list of elements.

        :param wait_driver: WebDriverWait used to wait for the elements
        :param row: Row number (1-based), or None
        :param col: Column number (1-based), or None
        :param multiple: If True, returns multiple elements; otherwise, a single element
        :return: A single WebElement or a list of WebElements
    """
    row_fmt = f"[{row}]" if row else ""
    col_fmt = f"[{col}]" if col else ""

    xpath = f'{"." if context else ""}//tbody//tr{row_fmt}//td{col_fmt}'

    if context:
        return wait_driver.until(lambda d: context.find_elements(By.XPATH, xpath)
                          if multiple else context.find_element(By.XPATH, xpath))
    
    return wait_driver.until((
        EC.visibility_of_all_elements_located((By.XPATH, xpath))
        if multiple else 
        EC.element_to_be_clickable((By.XPATH, xpath))
    ))


class AnyOf:
    def __init__(self, *conditions):
        self.conditions = conditions

    def __call__(self, driver):
        for condition in self.conditions:
            try:
                if condition(driver):
                    return True
            except:
                pass
        return False

class AllOf:
    def __init__(self, *conditions):
        self.conditions = conditions

    def __call__(self, driver):
        results = []
        for condition in self.conditions:
            try:
                result = condition(driver)
                results.append(result)
            except:
                return False
        return all(results)


def wait_for_search_results(driver: WebDriver, wait_driver: WebDriverWait) -> None:
    wait_loader(driver, wait_driver)

    wait_driver.until(
        AnyOf(
            EC.visibility_of_element_located((By.XPATH, '//tbody//tr//td[2]')),
            EC.visibility_of_element_located((By.XPATH, '//tbody//tr//td[@class="dataTables_empty"]'))
        )
    )

    time.sleep(1)


def wait_for_element_and_click(driver: WebDriver, wait_driver: WebDriverWait, selector: str, by: By = By.XPATH) -> WebElement:
    wait_loader(driver, wait_driver)

    try:
        element = wait_driver.until(
            EC.element_to_be_clickable((by, selector))
        )
        element.click()

        wait_loader(driver, wait_driver)
        return element
    except Exception as e:
        element = wait_driver.until(
            EC.element_to_be_clickable((by, selector))
        )
        element.click()
        wait_loader(driver, wait_driver)
        return element

"""
TODO: trovare tutti i posti in cui viene utilizzato questo metodo e sostituirlo con .get_select_search_results()

PS: Quel metodo permette (opzionalmente) di fare una ricerca ad un Select e successivamente di ottenere i risultati/opzioni
    ottenendo le opzioni del select possiamo chiamare il metodo .click() per selezionarle

PPS: Se .get_select_search_results() non trova il select, probabilmente perchè è all'interno di una modal
     quindi va chiamato prima .wait_modal()
"""
def wait_for_dropdown_and_select(driver: WebDriver, wait_driver: WebDriverWait, dropdown_xpath: str, option_xpath: str = None, option_text: str = None) -> None:
    wait_for_element_and_click(driver, wait_driver, dropdown_xpath, By.XPATH)

    if option_xpath:
        wait_for_element_and_click(driver, wait_driver, option_xpath, By.XPATH)
    elif option_text:
        option = wait_driver.until(
            EC.visibility_of_element_located((By.XPATH, f'//li[contains(text(), "{option_text}")]'))
        )
        option.click()

    wait_driver.until(
        EC.invisibility_of_element_located((By.XPATH, '//div[@class="select2-search select2-search--dropdown"]'))
    )
    wait_loader(driver, wait_driver)


def wait_loader(driver: WebDriver, wait_driver: WebDriverWait) -> None:
    try:
        wait_driver.until(AllOf(
            EC.invisibility_of_element_located((By.ID, 'main_loading')),
            EC.invisibility_of_element_located((By.ID, 'mini-loader')),
            EC.invisibility_of_element_located((By.ID, 'tiny-loader')),
        ))
    except:
        pass

def wait_for_invisibility(driver : WebDriver, wait_driver : WebDriverWait, selector : str, by : By = By.ID) -> None:
    def all_invisible(_):
        try:
            elements = driver.find_elements(by, selector)
            return all(not e.is_displayed() for e in elements)
        except StaleElementReferenceException:
            # One or more elements were detached from the DOM — assume they are gone
            return True

    wait_driver.until(all_invisible)

# In teoria questo metodo non ha molto senso, visto che abbiamo già un metodo wait_modal 
# (che da quel che ho capito aspetta che compaia una qualsiasi modal)
def send_keys_and_wait(driver: WebDriver, wait_driver: WebDriverWait, element: WebElement, text: str, wait_for_modal: bool = True) -> Optional[WebElement]:
    """Send keys to an element and wait for the page to load after pressing Enter.

    Args:
        driver: The WebDriver instance
        wait_driver: The WebDriverWait instance
        element: The element to send keys to
        text: The text to send
        wait_for_modal: Whether to wait for a modal to appear after sending keys

    Returns:
        The modal element if wait_for_modal is True and a modal appears, None otherwise
    """
    # Store the current page state to detect changes
    old_html = driver.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML')

    # Send keys and press Enter
    element.send_keys(text, Keys.ENTER)

    # Wait for loaders to disappear
    wait_loader(driver, wait_driver)

    # Wait for page content to change (indicating the search results have loaded)
    # Use a shorter timeout for this check
    # è necessario? non basta solo wait_loader?
    try:
        WebDriverWait(driver, 1).until(lambda d: d.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML') != old_html)
    except:
        pass

    # Wait for search results to appear with a shorter timeout
    try:
        WebDriverWait(driver, 1).until(
            AnyOf(
                EC.visibility_of_element_located((By.XPATH, '//tbody//tr//td[2]')),
                EC.visibility_of_element_located((By.XPATH, '//tbody//tr//td[@class="dataTables_empty"]'))
            )
        )
    except:
        pass

    # Add a minimal delay to ensure everything is loaded
    time.sleep(0.1)

    # Wait for loaders again to ensure everything is fully loaded
    wait_loader(driver, wait_driver)

    # If we need to wait for a modal
    if wait_for_modal:
        try:
            wait_driver.until(EC.visibility_of_element_located((By.CLASS_NAME, 'modal-dialog')))
            modal = driver.find_elements(By.CSS_SELECTOR, '.modal')[-1]
            return modal
        except:
            return None

    return None

def get_input(driver: WebDriver, wait_driver: WebDriverWait, label : str) -> WebElement:
    """
    Finds an <input> element associated with a <label> by its visible text and waits until the input is clickable.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        wait_driver (WebDriverWait): A WebDriverWait instance used for waiting on elements.
        label (str): The visible text of the <label> element linked to the desired input.

    Returns:
        WebElement: The <input> WebElement associated with the given label, once it becomes clickable.

    Raises:
        TimeoutException: If the label or input element is not found or doesn't become clickable in time.
    """
    xpath = f'//label[contains(normalize-space(string(.)), "{label}")]'
    label = wait_driver.until(EC.presence_of_element_located((By.XPATH, xpath)))

    label_for = label.get_attribute("for")

    return wait_driver.until(EC.element_to_be_clickable((By.XPATH, f'//input[@id="{label_for}"]')))

def get_element(driver: WebDriver, wait_driver: WebDriverWait, selector : str, by: By, context : WebElement | None = None) -> WebElement:
    if context and by == By.XPATH and not selector.strip().startswith('.'):
        selector = f".{selector}"
    search_context = context if context else driver

    element = wait_driver.until(lambda d: search_context.find_element(by, selector))
    return wait_driver.until(EC.element_to_be_clickable(element))

def get_elements(driver: WebDriver, wait_driver: WebDriverWait, selector : str, by: By, context : WebElement | None = None) -> list[WebElement]:
    def elements_are_clickable(driver: WebDriver) -> List[WebElement] | bool:
        elements = WebDriverWait(context if context else driver, wait_driver._timeout).until(
            EC.presence_of_all_elements_located((by, selector))
        )
        clickable = []
        for element in elements:
            try:
                if element.is_displayed() and element.is_enabled():
                    clickable.append(element)
            except StaleElementReferenceException as e:
                # L'elemento non è più valido
                pass
        return clickable if clickable else False

    return wait_driver.until(elements_are_clickable)

def close_toast_popup(driver: WebDriver, wait_driver: WebDriverWait):
    """
    <div id="toast-container" class="toast-bottom-right">
        <div class="toast toast-success" aria-live="polite" style="">
            <div class="toast-progress" style="width: 44.05%;">
            </div>
        <button type="button" class="toast-close-button" role="button">×</button>
        <div class="toast-title"></div>
        <div class="toast-message">Informazioni salvate correttamente!</div>
        </div>
    </div>
    """
    pass

def delete_and_confirm(driver: WebDriver, wait_driver: WebDriverWait, context: WebElement | None = None):
    """
    Clicks a delete button (typically located within a specific tab or section) and confirms the deletion 
    through a modal confirmation dialog.

    This function locates and clicks the "Delete" button (usually styled with 'btn btn-danger ask'), 
    waits until it's clickable, then clicks the confirmation button in the modal (with class 'swal2-confirm').

    If a context element is provided, the search for both buttons is limited to that context; otherwise,
    the whole DOM is used.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        wait_driver (WebDriverWait): A WebDriverWait instance for waiting on conditions.
        context (WebElement | None): An optional context element to scope the search within.

    Raises:
        TimeoutException: If any of the elements are not found or not interactable within the wait time.
    """
    # Aspetto che il pulsante Elimina in basso a sinistra (solitamente) sia presente e cliccabile
    xpath = f'{"." if context else ""}//a[@class="btn btn-danger ask "]'
    delete_btn = context.find_element(By.XPATH, xpath) if context else driver.find_element(By.XPATH, xpath)
    wait_driver.until(EC.element_to_be_clickable(delete_btn))
    delete_btn.click()

    # Aspetto la comparsa della modal e del bottone per confermare e lo clicco
    xpath = f'{"." if context else ""}//button[@class="swal2-confirm btn btn-lg btn-danger"]'
    confirm_btn = context.find_element(By.XPATH, xpath) if context else driver.find_element(By.XPATH, xpath)
    confirm_btn.click()

# Avrebbe senso crearlo questo metodo? o andrebbe a creare confusione?
def click_add_button(driver : WebDriver, wait_driver: WebDriverWait, context: WebElement | None = None):
    pass

def click_save_button():
    pass

def expand_plugin_sidebar(driver : WebDriver, wait_driver: WebDriverWait):
    try:
        sidebar_btn = wait_driver.until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="control-sidebar-button"]'))
        )
        sidebar_btn.click()
    except TimeoutException as e:
        # Probabilmente la sidebar è già estesa
        pass

def click_plugin(driver : WebDriver, wait_driver: WebDriverWait, name: str):
    plugins = driver.find_elements(By.XPATH, '//li[@class="btn-default nav-item plugin-tab-item"]')

    for plugin in plugins:
        if name in plugin.text.strip():
            scroll_to_element(driver, wait_driver, plugin)
            plugin.click()
            break
    else:
        raise TimeoutException("Plugin da cliccare non trovato nella sidebar")


def is_clickable(driver : WebDriver, wait_driver: WebDriverWait, element : WebElement) -> bool:
    """
    Checks if the given WebElement is clickable (visible and enabled).

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        wait_driver (WebDriverWait): An instance of WebDriverWait to apply the wait.
        element (WebElement): The WebElement to check for clickability.

    Returns:
        bool: True if the element is clickable within the timeout, False otherwise.
    """
    try:
        wait_driver.until(EC.element_to_be_clickable(element))
        return True
    except TimeoutException:
        return False

def exists(driver : WebDriver, wait_driver: WebDriverWait, selector : str, by : By, context : WebElement | None = None) -> WebElement | None:
    """
    Checks if an element exists in the DOM using the specified selector and strategy.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        wait_driver (WebDriverWait): An instance of WebDriverWait to apply the wait.
        selector (str): The locator string (e.g., XPath, CSS selector).
        by (By): The Selenium By strategy (e.g., By.ID, By.XPATH, By.CSS_SELECTOR).

    Returns:
        WebElement | None
    """
    try:
        return (context if context else driver).find_element(by, f"{'.' if by == By.XPATH and context and not selector.strip().startswith('.') else ''}{selector}")
    except NoSuchElementException:
        return None

def wait_swal2_popup(driver: WebDriver, wait_driver: WebDriverWait, mode: Literal["appear", "disappear"] = "appear") -> None:
    """
    Waits for the SweetAlert2 modal popup to either appear or disappear on the page.

    This function pauses execution until an element with the class 'swal2-modal'
    becomes visible or invisible, depending on the specified mode.

    Args:
        driver (WebDriver): The Selenium WebDriver instance controlling the browser.
        wait_driver (WebDriverWait): An instance of WebDriverWait configured with a timeout.
        mode (Literal["appear", "disappear"]): Determines the wait condition:
            - "appear": Waits until the modal becomes visible.
            - "disappear": Waits until the modal is no longer visible or is removed from the DOM.

    Returns:
        None
    """
    location = (By.CLASS_NAME, "swal2-modal")
    try:
        wait_driver.until(
            EC.visibility_of_element_located(location)
            if mode == "appear" else
            EC.invisibility_of_element_located(location)
        )
    except TimeoutException as e:
        pass

def scroll_to_element(driver: WebDriver, wait_driver: WebDriverWait, element : WebElement, offset: int = 0):
    """
    Scrolls the page vertically to bring the specified element into view, with an optional offset.

    This function uses JavaScript to scroll the window to the vertical position of the given element,
    minus an optional offset. The scroll behavior is smooth by default. Useful when elements are
    hidden under fixed headers or need to be centered in the viewport.

    Args:
        driver (WebDriver): The Selenium WebDriver instance controlling the browser.
        wait_driver (WebDriverWait): An instance of WebDriverWait (currently unused but included for consistency).
        element (WebElement): The element to scroll to.
        offset (int, optional): The number of pixels to offset from the top of the element. 
                                Use a positive value to scroll above the element. Defaults to 0.

    Returns:
        None
    """
    y = element.location['y'] - offset
    driver.execute_script(f"window.scrollTo({{ top: {y}, behavior: 'smooth' }});")

def scroll_to_bottom(driver: WebDriver, wait_driver: WebDriverWait, pause_time: float = 1.0, max_tries: int = 30):
    """
    Scrolla fino in fondo alla pagina web.

    :param driver: Il WebDriver Selenium.
    :param wait_driver: Un'istanza di WebDriverWait.
    :param pause_time: Tempo in secondi tra uno scroll e l'altro.
    :param max_tries: Numero massimo di tentativi per rilevare nuovo contenuto.
    """
    last_height = driver.execute_script("return document.body.scrollHeight")

    tries = 0
    while tries < max_tries:
        # Scroll fino in fondo
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)  # Aspetta il caricamento di nuovi contenuti

        # Calcola nuova altezza della pagina
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            # Non c'è più contenuto da caricare
            break
        last_height = new_height
        tries += 1