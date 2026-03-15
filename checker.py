import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.ticketmaster.es/event/TU-URL-AQUI"
SELECTOR = "button.buy-tickets"      # cámbialo según la web
TEXTO_BOTON = "Comprar entradas"     # opcional, deja "" para ignorar

def send_telegram(mensaje):
    token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": mensaje}
    )

def check():
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(URL, headers=headers, timeout=15)
    soup = BeautifulSoup(resp.text, "html.parser")

    botones = soup.select(SELECTOR)
    if TEXTO_BOTON:
        botones = [b for b in botones if TEXTO_BOTON.lower() in b.get_text().lower()]

    disponibles = [b for b in botones if not b.get("disabled")]

    if disponibles:
        print("BOTÓN ENCONTRADO - enviando alerta")
        send_telegram(f"Boletos disponibles: {URL}")
    else:
        print(f"Sin boletos. Botones encontrados: {len(botones)}")

if __name__ == "__main__":
    check()
```

**`requirements.txt`**:
```
requests
beautifulsoup4
