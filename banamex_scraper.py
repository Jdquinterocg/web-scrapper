import time
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_banamex_rates():
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    user_data_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    sell_rate_usd = None
    sell_rate_eur = None

    try:
        driver.get("https://www.banamex.com/economia-finanzas/es/mercado-de-divisas/index.html")
        time.sleep(5)
        wait = WebDriverWait(driver, 30)

        selectors = {"usd_ven": "//p[@ndivisa='usd_ven']", "euro_ven": "//p[@ndivisa='euro_ven']"}

        for currency, selector in selectors.items():
            try:
                rate_element = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                if rate_element:
                    rate = rate_element.text.strip()
                    if currency == "usd_ven":
                        sell_rate_usd = rate
                    elif currency == "euro_ven":
                        sell_rate_eur = rate
            except Exception:
                print(f"Failed to locate {currency} in Banamex with selector: {selector}")
                continue

        return sell_rate_usd, sell_rate_eur

    except Exception as e:
        print(f"An error occurred with Banamex: {str(e)}")
        return None, None
    finally:
        driver.quit()


def get_bbva_rates():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    user_data_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    sell_rate_usd = None
    sell_rate_eur = None

    try:
        driver.get("https://finmatcher.com/currency-converter/es/tipo-de-cambio-bbva/")
        time.sleep(5)
        wait = WebDriverWait(driver, 30)

        # Buscar directamente las filas por su clase
        rows = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.converter__rates-table-row"))
        )

        for row in rows:
            try:
                # Buscar las celdas dentro de la fila
                cells = row.find_elements(By.CSS_SELECTOR, "div")

                if len(cells) >= 3:
                    currency = cells[0].text
                    buy_rate = cells[1].text.strip()  # Precio de compra
                    sell_rate = cells[2].text.strip()  # Precio de venta

                    if "EUR" in currency:
                        sell_rate_eur = sell_rate.replace(" MXN", "")
                        # print(f"Found EUR rate (sell): {sell_rate_eur}")
                    elif "USD" in currency:
                        # Para USD usamos el precio de compra ya que está trocado
                        sell_rate_usd = buy_rate.replace(" MXN", "")
                        # print(f"Found USD rate (buy): {sell_rate_usd}")
            except Exception as e:
                print(f"Error processing row: {str(e)}")
                continue

        return sell_rate_usd, sell_rate_eur
    except Exception as e:
        print(f"An error occurred with BBVA: {str(e)}")
        return None, None
    finally:
        driver.quit()


def get_dollar_rate():
    # Uncomment the source you want to use:
    # return get_banamex_rates()
    usd_rate, eur_rate = get_bbva_rates()
    return usd_rate, eur_rate, "BBVA"


if __name__ == "__main__":
    print("Fetching exchange rates...")
    usd_rate, eur_rate, bank_name = get_dollar_rate()
    if usd_rate and eur_rate:
        print(f"USD sell rate: {usd_rate}")
        print(f"EUR sell rate: {eur_rate}")
        print(f"Bank: {bank_name}")
    else:
        print("Failed to fetch the exchange rates")
