from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_dollar_rate():
    # Configure Chrome options
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Temporarily disable headless mode for testing
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    try:
        # Navigate to the Banamex exchange rates page
        driver.get('https://www.banamex.com/economia-finanzas/es/mercado-de-divisas/index.html')
        
        # Add a longer initial wait
        time.sleep(5)
        
        # Wait for the exchange rate element to be present
        wait = WebDriverWait(driver, 30)
        
        # Try different selectors if one fails
        selectors = [
            "//p[@ndivisa='usd_ven']",
            "//td[contains(.,'Dólar')]//following::td[2]//p",
            "//p[@class='adp-h6'][@ndivisa='usd_ven']"
        ]
        
        sell_rate = None
        for selector in selectors:
            try:
                sell_rate_element = wait.until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                sell_rate = sell_rate_element.text.strip()
                if sell_rate:
                    break
            except Exception:
                continue
                
        if not sell_rate:
            # If all selectors fail, try to get page source for debugging
            print("Page source:", driver.page_source)
            raise Exception("Could not find exchange rate with any selector")
            
        return sell_rate

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

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