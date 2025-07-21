# Import necessary modules
import os
import time
import tempfile
import requests
# Selenium imports for browser automation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Get Slack webhook URL from environment variable
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# Function to send error messages to Slack
# Used for alerting when something goes wrong in the scraping process
def send_error_slack_message(error_message):
    message = f"⚠️ ¡Ups! Algo salió mal al obtener las tasas de cambio:\n\n{error_message}\n\nPor favor, revisa el script lo antes posible. 🚨"
    payload = {"text": message}
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print("Error notification sent to Slack")
    except Exception as e:
        print(f"Error sending Slack notification: {str(e)}")

# Scrapes Banamex website for USD and EUR sell rates
def get_banamex_rates():
    # Configure Chrome options for headless browsing
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # Use a temporary user data directory for Chrome
    user_data_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

    # Start Chrome WebDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    sell_rate_usd = None
    sell_rate_eur = None

    try:
        # Open Banamex exchange rates page
        driver.get("https://www.banamex.com/economia-finanzas/es/mercado-de-divisas/index.html")
        time.sleep(5)  # Wait for page to load
        wait = WebDriverWait(driver, 30)

        # Define XPaths for USD and EUR sell rates
        selectors = {"usd_ven": "//p[@ndivisa='usd_ven']", "euro_ven": "//p[@ndivisa='euro_ven']"}

        # Loop through selectors to extract rates
        for currency, selector in selectors.items():
            try:
                rate_element = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                if rate_element:
                    rate = rate_element.text.strip()
                    if currency == "usd_ven":
                        sell_rate_usd = rate
                    elif currency == "euro_ven":
                        sell_rate_eur = rate
            except Exception as e:
                error_msg = f"Failed to locate {currency} in Banamex with selector: {selector}"
                print(error_msg)
                send_error_slack_message(error_msg)
                continue

        # If any rate is missing, send error and return None
        if not sell_rate_usd or not sell_rate_eur:
            error_msg = "Could not fetch complete rates from Banamex"
            send_error_slack_message(error_msg)
            return None, None

        # Return both rates if successful
        return sell_rate_usd, sell_rate_eur

    except Exception as e:
        error_msg = f"An error occurred with Banamex: {str(e)}"
        print(error_msg)
        send_error_slack_message(error_msg)
        return None, None
    finally:
        driver.quit()  # Always close the browser

# Scrapes BBVA rates from a third-party aggregator (pesomxn.com)
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

    # Use a temporary user data directory for Chrome
    user_data_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

    # Start Chrome WebDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    sell_rate_usd = None
    sell_rate_eur = None

    try:
        # Get USD rate from BBVA page on pesomxn.com
        driver.get("https://www.pesomxn.com/dolar-a-peso/bbva-bancomer")
        time.sleep(5)  # Wait for page to load
        wait = WebDriverWait(driver, 30)
        
        sell_rate_usd = wait.until(
            EC.presence_of_element_located((By.ID, "mx-venta"))
        ).text.strip().replace("$", "").replace(",", "")

        # Get EUR rate from BBVA page on pesomxn.com
        driver.get("https://www.pesomxn.com/euro-a-peso/bbva-bancomer")
        time.sleep(5)
        
        sell_rate_eur = wait.until(
            EC.presence_of_element_located((By.ID, "mx-venta"))
        ).text.strip().replace("$", "").replace(",", "")

        # If any rate is missing, send error and return None
        if not sell_rate_usd or not sell_rate_eur:
            error_msg = "Could not fetch complete rates from BBVA"
            send_error_slack_message(error_msg)
            return None, None

        # Return both rates if successful
        return sell_rate_usd, sell_rate_eur
    except Exception as e:
        error_msg = f"An error occurred with BBVA: {str(e)}"
        print(error_msg)
        send_error_slack_message(error_msg)
        return None, None
    finally:
        driver.quit()  # Always close the browser

# Main function to get the dollar and euro sell rates
# Currently uses BBVA as the source (can switch to Banamex by uncommenting)
def get_dollar_rate():
    # Uncomment the source you want to use:
    # return get_banamex_rates()
    usd_rate, eur_rate = get_bbva_rates()
    return usd_rate, eur_rate, "BBVA"

# If run as a script, fetch and print the rates, or send error to Slack
if __name__ == "__main__":
    print("Fetching exchange rates...")
    usd_rate, eur_rate, bank_name = get_dollar_rate()
    if usd_rate and eur_rate:
        print(f"USD sell rate: {usd_rate}")
        print(f"EUR sell rate: {eur_rate}")
        print(f"Bank: {bank_name}")
    else:
        error_msg = "Failed to fetch the exchange rates"
        print(error_msg)
        send_error_slack_message(error_msg)
