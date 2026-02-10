import os
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def testar_sistema_completo():
    print("🛠️ Iniciando Diagnóstico do Oráculo...")
    
    # 1. Verificação da Senha de App
    remetente = "p8823661@gmail.com"
    senha = os.environ.get('ORACULO_APP_PASS')
    
    if not senha:
        print("❌ ERRO: Variável 'ORACULO_APP_PASS' não encontrada no sistema.")
        return

    # 2. Montagem do E-mail de Teste Unificado
    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = remetente
    msg["Subject"] = f"🧪 TESTE DE CONEXÃO - 5 FONTES - {time.strftime('%H:%M:%S')}"

    corpo = (
        "✅ Conexão Python -> Gmail: OK\n"
        "✅ Variáveis de Ambiente: OK\n"
        "✅ Status das 5 Fontes: Verificando...\n\n"
        "Se você recebeu este e-mail, o motor de envio está pronto para unificar os 5 sites."
    )
    msg.attach(MIMEText(corpo, "plain"))

    # 3. Tentativa de Envio com Debug Ativo
    try:
        print(f"📧 Tentando enviar para {remetente}...")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.set_debuglevel(1)  # Isso mostra a conversa real com o Google
            server.starttls()
            server.login(remetente, senha)
            server.sendmail(remetente, remetente, msg.as_string())
        
        print("\n🚀 SUCESSO! O motor de envio está funcionando perfeitamente.")
        print("Verifique seu celular (e a pasta de SPAM).")
        
    except Exception as e:
        print(f"\n❌ FALHA NO TESTE: {e}")
        print("\nDICA: Se o erro for 'Authentication Failed', sua senha de app expirou ou foi digitada errada.")

if __name__ == "__main__":
    testar_sistema_completo()