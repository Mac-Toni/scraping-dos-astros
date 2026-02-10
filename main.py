import os
import time
import locale
import smtplib

# --- 1. BIBLIOTECAS DE SCRAPING (O ARSENAL) ---
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession  # <--- Requests-HTML aqui!
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# --- 2. BIBLIOTECAS DE IA E EMAIL ---
import google.generativeai as genai
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURAÇÃO DE LOCALE ---
try:
    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
except locale.Error:
    locale.setlocale(locale.LC_TIME, "Portuguese_Brazil.1252")

# --- CONFIGURAÇÃO DA IA ---
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

signos = {
    "Áries": "aries", "Touro": "taurus", "Gêmeos": "gemini",
    "Câncer": "cancer", "Leão": "leo", "Virgem": "virgo",
    "Libra": "libra", "Escorpião": "scorpio", "Sagitário": "sagittarius",
    "Capricórnio": "capricorn", "Aquário": "aquarius", "Peixes": "pisces"
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0'
}

# --- FUNÇÃO COM REQUESTS-HTML (Dinâmico Leve) ---
def coletar_com_requests_html(slug):
    try:
        session = HTMLSession()
        url = f"https://www.astrology.com/horoscope/daily/{slug}.html"
        r = session.get(url, headers=HEADERS)
        r.html.render(sleep=2)  # Renderiza o JavaScript
        conteudo = r.html.find('#content', first=True)
        texto = conteudo.text if conteudo else ""
        session.close()
        return texto
    except Exception as e:
        return f"Erro no Requests-HTML: {e}"

# --- FUNÇÃO COM SELENIUM (Dinâmico Pesado/Robusto) ---
def coletar_com_selenium(slug):
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    driver = webdriver.Chrome(options=chrome_options)
    try:
        url = f"https://www.astrology.com/horoscope/daily/{slug}.html"
        driver.get(url)
        time.sleep(3)
        elemento = driver.find_element(By.ID, "content")
        return elemento.text
    except Exception as e:
        return f"Erro no Selenium: {e}"
    finally:
        driver.quit()

# --- FUNÇÃO DE IA ---
def gerar_resumo_ia(signo, dados_brutos):
    if len(dados_brutos) < 50:
        return "Fonte de dados offline ou protegida."

    prompt = f"Como um astrólogo, resuma em 3 linhas motivadoras para {signo}: {dados_brutos}"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Erro Gemini: {str(e)[:50]}"

# --- FUNÇÃO DE EMAIL ---
def enviar_email(previsoes):
    remetente = "p8823661@gmail.com"
    senha = os.environ.get('ORACULO_APP_PASS')
    
    msg = MIMEMultipart()
    data_hj = time.strftime("%d/%m/%Y")
    msg["Subject"] = f"🔮 ORÁCULO MULTI-ENGINE - {data_hj}"

    corpo = "✨ PREVISÕES GERADAS COM SUCESSO ✨\n\n"
    for s, texto in previsoes.items():
        corpo += f"--- {s.upper()} ---\n{texto}\n\n"

    msg.attach(MIMEText(corpo, "plain", "utf-8"))
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(remetente, senha)
            server.sendmail(remetente, remetente, msg.as_string())
        print("🚀 E-mail enviado!")
    except Exception as e:
        print(f"Erro e-mail: {e}")

# --- EXECUÇÃO ---
if __name__ == "__main__":
    resumos_finais = {}
    
    for nome, slug in signos.items():
        print(f"🔍 Tentando {nome} via Requests-HTML...")
        texto_bruto = coletar_com_requests_html(slug)
        
        # Se falhar, você tem o Selenium ali em cima pronto para ser chamado!
        
        print(f"🤖 IA resumindo {nome}...")
        resumos_finais[nome] = gerar_resumo_ia(nome, texto_bruto)
        
    enviar_email(resumos_finais)