from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import tempfile

def get_dollar_rate():
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    
    user_data_dir = tempfile.mkdtemp()  # Crea un directorio temporal único
    chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
    
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
     #Initialize variables for rates
    sell_rate_usd = None
    sell_rate_eur = None
        
    try:
        # Navigate to the Banamex exchange rates page
        driver.get('https://www.banamex.com/economia-finanzas/es/mercado-de-divisas/index.html')
        
        # Add a longer initial wait
        time.sleep(5)
        
        # Wait for the exchange rate element to be present
        wait = WebDriverWait(driver, 30)
        
        # Try different selectors if one fails
        selectors = {
            'usd_ven': "//p[@ndivisa='usd_ven']",
            'euro_ven': "//p[@ndivisa='euro_ven']"
        }
                
        for currency, selector in selectors.items():
            try:
                rate_element = wait.until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                if rate_element:
                    rate = rate_element.text.strip()
                    if currency == 'usd_ven':
                        sell_rate_usd = rate
                    elif currency == 'euro_ven':
                        sell_rate_eur = rate
            except Exception:
                print(f"Failed to locate {currency} with selector: {selector}")
                continue


        if not sell_rate_usd or not sell_rate_eur:
            # If any rate is missing, raise an exception
            print("Missing exchange rate(s).")
            raise Exception("Could not find all required exchange rates.")
                
        return sell_rate_usd, sell_rate_eur

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None, None

    finally:
        # Always close the browser
        driver.quit()

if __name__ == "__main__":
    print("Fetching dollar sell rate from Banamex...")
    rate = get_dollar_rate()
    if rate:
        print(f"Current dollar sell rate: {rate}")
    else:
        print("Failed to fetch the exchange rate") 