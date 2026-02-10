from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
import time

signos = {
    "Áries": "aries",
    "Touro": "taurus",
    "Gêmeos": "gemini",
    "Câncer": "cancer",
    "Leão": "leo",
    "Virgem": "virgo",
    "Libra": "libra",
    "Escorpião": "scorpio",
    "Sagitário": "sagittarius",
    "Capricórnio": "capricorn",
    "Aquário": "aquarius",
    "Peixes": "pisces"
}

def coletar_fonte():
    contexto_por_signo = {}

    options = webdriver.EdgeOptions()
    options.add_argument("--headless")
    service = Service(r"C:\Users\Paulo\Desktop\msedgedriver.exe")
    driver = webdriver.Edge(service=service, options=options)

    for nome, slug in signos.items():
        url = f"https://www.astrology.com/horoscope/daily/{slug}.html"
        driver.get(url)
        time.sleep(2)  # espera carregar JS

        paragrafos = driver.find_elements(By.CSS_SELECTOR, "div#content p")
        texto = "\n".join([p.text for p in paragrafos]) if paragrafos else ""
        contexto_por_signo[nome] = texto

    driver.quit()
    return contexto_por_signo


# Teste rápido
if __name__ == "__main__":
    dados = coletar_fonte()
    for signo, texto in dados.items():
        print(f"{signo}: {texto[:50]}...\n")