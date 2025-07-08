from argparse import ArgumentParser
from pathlib import Path
import os
import glob
import string
import random
import json
import time
from typing import Dict, List, Optional, Callable, Union

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver, WebElement


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

    def find_cell(self, row: int | None = None, col: int | None = None) -> WebElement:
        """
            Finds one cell (`<td>`) in an HTML table by specifying the row and/or column (1-based).

            :param row: Row number (1-based), or None
            :param col: Column number (1-based), or None
            :return: A single WebElement
        """
        return find_cells(self.driver, self.wait_driver, row, col, multiple=False)

    def find_cells(self, row: int | None = None, col: int | None = None, multiple : bool = False) -> Union[WebElement, List[WebElement]]:
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
        return find_cells(self.driver, self.wait_driver, row, col, multiple)

    def get_select_search_results(self, field_name : str, search_query : str | None = None) -> list[WebElement]:
        return get_select_search_results(self.driver, self.wait_driver, field_name, search_query)

    def get_input(self, label : str) -> WebElement:
        return get_input(self.driver, self.wait_driver, label)

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

def get_select_search_results(driver: WebDriver, wait_driver: WebDriverWait, field_name : str, search_query : str | None = None) -> list[WebElement]:
    """
    Retrieves the list of `<li>` elements representing search results from a Select2 dropdown 
    associated with a label that matches the given field name.

    This function performs the following steps:
    1. Locates the `<label>` with exact text matching `field_name`.
    2. Uses the 'for' attribute of the label to determine the Select2 container ID.
    3. Clicks the Select2 `<span>` element to open the dropdown.
    4. Optionally enters a search query if `search_query` is provided.
    5. Waits for the loading indicator ("loading-results" `<li>`) to disappear.
    6. Returns all `<li>` result elements from the dropdown.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        wait_driver (WebDriverWait): An instance of WebDriverWait for explicit waits.
        field_name (str): The exact text content of the label associated with the Select2 element.
        search_query (str | None, optional): The text to enter in the search input. Defaults to None.

    Returns:
        list[WebElement]: A list of `<li>` elements representing the available search results.
    """
    label = wait_driver.until(EC.presence_of_element_located((By.XPATH,f'//label[text()="{field_name}"]')))

    label_for = label.get_attribute("for")

    # Necessario per aprire la select (e caricare i dati)
    select_id = f"select2-{label_for}-container"
    select_span = wait_driver.until(
        EC.presence_of_element_located((By.XPATH, f'//span[@id="{select_id}"]'))
    )
    select_span.click()

    results_id = f"select2-{label_for}-results"

    if search_query:
        input_element = wait_driver.until(
            EC.presence_of_element_located((
                By.XPATH,
                f'//input[@aria-controls="{results_id}"]'
            ))
        )
        input_element.send_keys(search_query, Keys.ENTER)
    

    # Aspetto fino a quando l'elemento "Sto cercando..." viene rimosso
    loading_li_xpath = f'//ul[@id="{results_id}"]/li[contains(@class, "loading-results")]'
    loading_elements = driver.find_elements(By.XPATH, loading_li_xpath)

    # Se esiste almeno uno, aspetta che scompaia
    if loading_elements:
        wait_driver.until(EC.invisibility_of_element_located((By.XPATH, loading_li_xpath)))

    # Se esiste 
    clear_buttons = select_span.find_elements(By.CSS_SELECTOR, "span.select2-selection__clear")
    if len(clear_buttons) == 0:
        select_results = wait_driver.until(EC.presence_of_element_located((By.ID,results_id)))
    
    # Aspetto fino a che gli elementi li siano visibili
    results_xpath = f'//ul[@id="{results_id}"]/li'
    results = driver.find_elements(By.XPATH, results_xpath)

    return results

def click_first_result(driver: WebDriver, wait_driver: WebDriverWait) -> None:
    wait_loader(driver, wait_driver)

    try:
        wait_driver.until(
            EC.visibility_of_element_located((By.XPATH, '//tbody//tr//td[2]'))
        ).click()
        wait_loader(driver, wait_driver)
    except Exception as e:
        wait_loader(driver, wait_driver)
        wait_driver.until(
            EC.visibility_of_element_located((By.XPATH, '//tbody//tr//td[2]'))
        ).click()
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

def find_cells(driver: WebDriver, wait_driver: WebDriverWait, row: int | None = None, col: int | None = None, multiple : bool = False) -> Union[WebElement, List[WebElement]]:
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

    xpath = f'//tbody//tr{row_fmt}//td{col_fmt}'

    if multiple:
        return wait_driver.until(
            EC.visibility_of_all_elements_located((By.XPATH, xpath))
        )
    else:
        return wait_driver.until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )


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
        wait_loader(driver, wait_driver)
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
    label = wait_driver.until(EC.presence_of_element_located((By.XPATH,f'//label[text()="{label}"]')))

    label_for = label.get_attribute("for")

    return wait_driver.until(EC.element_to_be_clickable((By.XPATH, f'//input[@id="{label_for}"]')))
