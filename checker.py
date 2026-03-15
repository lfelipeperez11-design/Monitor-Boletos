from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import os
import time

URL = "https://www.priceless.com/sports/product/224382/uefa-champions-league-ko-ticket-only-package-spain"

def send_telegram(mensaje):
    token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": mensaje}
    )

def check():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    time.sleep(5)

    todos = driver.find_elements(By.CLASS_NAME, "buyButton")
    disponibles = [b for b in todos if "disabledButton" not in b.get_attribute("class")]

    print(f"Total botones: {len(todos)} | Disponibles: {len(disponibles)}")

    if len(disponibles) > 0:
        textos = [b.text.strip() for b in disponibles]
        send_telegram(
            f"BOLETO DISPONIBLE en priceless.com!\n"
            f"Botones activos: {len(disponibles)}\n"
            f"Opciones: {', '.join(textos)}\n"
            f"{URL}"
        )
    
    driver.quit()

if __name__ == "__main__":
    check()
