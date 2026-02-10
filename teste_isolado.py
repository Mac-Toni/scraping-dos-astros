import os
import time
from google import genai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- 1. CONFIGURAÇÃO DA IA (NOVO SDK) ---
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
MODELO = "gemini-3-flash-preview"

def teste_completo_isolado():
    options = webdriver.EdgeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--log-level=3")
    
    # Caminho do driver
    service = Service(r"C:\Users\Paulo\Desktop\msedgedriver.exe")
    driver = webdriver.Edge(service=service, options=options)
    wait = WebDriverWait(driver, 10)

    url = "https://www.astrology.com/horoscope/daily/aries.html"

    print("-" * 50)
    print(f"🛰️ 1. INICIANDO COLETA (EDGE)...")
    
    try:
        # Parte 1: Coleta dos dados
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.ID, "content")))
        
        paragrafos = driver.find_elements(By.CSS_SELECTOR, "div#content p")
        texto_bruto = "\n".join([p.text for p in paragrafos if len(p.text) > 40])

        # Parte 2: Processamento com IA (Verificando a identação aqui!)
        if texto_bruto:
            print("✅ 2. TEXTO CAPTURADO!")
            print(f"🤖 3. TRADUZINDO COM {MODELO}...")
            
            try:
                response = client.models.generate_content(
                    model=MODELO, 
                    contents=f"Traduza para português do Brasil de forma motivadora: {texto_bruto}"
                )
                
                print("\n✨ RESULTADO FINAL:")
                print("-" * 30)
                print(response.text)
                print("-" * 30)
            except Exception as ai_err:
                print(f"❌ Erro na tradução da IA: {ai_err}")
        else:
            print("❌ Falha: O texto capturado está vazio.")

    except Exception as e:
        print(f"💥 ERRO NO NAVEGADOR: {e}")
    
    finally:
        driver.quit()
        print("\n🏁 Processo encerrado.")

if __name__ == "__main__":
    # Limpa a tela antes de rodar (opcional)
    os.system('cls' if os.name == 'nt' else 'clear')
    teste_completo_isolado()