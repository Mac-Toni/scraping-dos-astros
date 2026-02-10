import os
import time
import smtplib
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from google import genai
from email.message import EmailMessage

# --- CONFIGURAÇÕES ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMAIL_USUARIO = "SEU E-MAIL AQUI"
# A senha abaixo vem da variável de ambiente que configuramos
SENHA_APP = os.getenv("SUA CHAVE AQUI")

def coletar_horoscopo(id_signo):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service("msedgedriver.exe") 
    driver = webdriver.Edge(service=service, options=options)
    
    url = f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign={id_signo}"
    
    try:
        driver.get(url)
        time.sleep(5) # Aumentamos o tempo para garantir que a página carregue

        # Buscamos o texto da previsão de forma mais segura
        texto = driver.find_element(By.CSS_SELECTOR, ".main-horoscope p").text
        
        # Como o ID do signo deu erro, vamos usar o nome fixo baseado no ID que enviamos
        signos = {1: "Aries", 2: "Taurus", 3: "Gemini", 4: "Cancer", 5: "Leo", 6: "Virgo", 
                  7: "Libra", 8: "Scorpio", 9: "Sagittarius", 10: "Capricorn", 11: "Aquarius", 12: "Pisces"}
        
        signo_nome = signos.get(id_signo, "Seu Signo")
        
        return signo_nome, texto
    finally:
        driver.quit()

def processar_com_gemini(signo, texto_ingles):
    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = f"""
    Você é um astrólogo moderno e motivador. 
    Traduza e adapte o horóscopo abaixo para o signo de {signo}.
    O tom deve ser realista e inspirador para o dia de hoje em português do Brasil.
    
    Texto original: {texto_ingles}
    """
    
    for tentativa in range(3): # Tenta até 3 vezes se houver erro de servidor ou limite
        try:
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt
            )
            return response.text
        except Exception as e:
            # Se o erro for de limite de cota (429) ou servidor instável (503)
            if "429" in str(e) or "503" in str(e):
                tempo_espera = 60  # Espera 60 segundos para a cota resetar ou o servidor respirar
                print(f"⏳ Limite ou instabilidade em {signo}. Aguardando {tempo_espera}s (Tentativa {tentativa + 1}/3)...")
                time.sleep(tempo_espera)
            else:
                # Se for um erro diferente (como chave de API inválida), ele para o código
                raise e
                
    return f"\n[Aviso: Não foi possível obter a previsão para {signo} devido ao limite de requisições do Google.]\n"

def enviar_email(corpo_mensagem):
    msg = EmailMessage()
    msg['Subject'] = f"✨ Seu Oráculo Diário - {time.strftime('%d/%m/%Y')}"
    msg['From'] = EMAIL_USUARIO
    msg['To'] = EMAIL_USUARIO 
    msg.set_content(corpo_mensagem)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        # Usamos a variável SENHA_APP que já carrega o os.getenv
        smtp.login(EMAIL_USUARIO, SENHA_APP)
        smtp.send_message(msg)

# --- EXECUÇÃO ---
# --- EXECUÇÃO COM LOOP ---
if __name__ == "__main__":
    try:
        print("🔮 O Oráculo está consultando as estrelas para todos os signos...")
        
        signos = {
            1: "Áries", 2: "Touro", 3: "Gêmeos", 4: "Câncer", 
            5: "Leão", 6: "Virgem", 7: "Libra", 8: "Escorpião", 
            9: "Sagitário", 10: "Capricórnio", 11: "Aquário", 12: "Peixes"
        }
        
        relatorio_completo = "✨ PREVISÕES DO ORÁCULO DIGITAL ✨\n\n"

        for id_sig, nome_sig in signos.items():
            print(f"⏳ Coletando {nome_sig}...")
            nome, raw_text = coletar_horoscopo(id_sig)
            
            print(f"🤖 IA processando {nome_sig}...")
            previsao = processar_com_gemini(nome, raw_text)
            
            relatorio_completo += f"--- {nome_sig.upper()} ---\n{previsao}\n\n"
            time.sleep(1) # Pequena pausa para estabilidade

        print("📧 Enviando relatório completo para o seu celular...")
        enviar_email(relatorio_completo)
        
        print("🚀 SUCESSO TOTAL! Todos os signos foram enviados.")

    except Exception as e:
        print(f"❌ Ocorreu um erro no loop: {e}")