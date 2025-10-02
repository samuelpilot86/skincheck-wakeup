from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import os

# URL de votre app SkinCheck
STREAMLIT_URL = "https://skincheckmvp.streamlit.app"

def main():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(STREAMLIT_URL)
        print(f"Ouverture de {STREAMLIT_URL}")

        wait = WebDriverWait(driver, 15)
        try:
            # Recherche du bouton de réveil
            button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]"))
            )
            print("Bouton de réveil trouvé. Clic en cours...")
            button.click()

            # Vérification que le bouton disparaît après clic
            try:
                wait.until(EC.invisibility_of_element_located((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]")))
                print("Bouton cliqué et disparu ✅ (l'app se réveille)")
            except TimeoutException:
                print("Bouton cliqué mais n'a pas disparu ❌ (échec possible)")
                exit(1)

        except TimeoutException:
            # Pas de bouton → app déjà active
            print("Aucun bouton de réveil trouvé. App déjà active ✅")

    except Exception as e:
        print(f"Erreur inattendue : {e}")
        exit(1)
    finally:
        driver.quit()
        print("Script terminé.")

if __name__ == "__main__":
    main()
