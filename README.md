![Eclíptica](C:\Users\Paulo\variosprojetos\zodiaco-digital\imagens\images.png)

# 🔮 Oráculo Digital: Web Scraping & AI 2026

Este projeto é um sistema automatizado de astrologia que utiliza **Web Scraping** para coletar horóscopos diários, **Inteligência Artificial (Gemini 3)** para tradução e resumo motivacional, e um sistema de **notificação por e-mail**.

zodiaco-digital/
├── .gitignore           # Filtro para evitar o envio de arquivos desnecessários (drivers/caches).
├── main.py              # Script principal: Fluxo completo (Scraping + Gemini 3 + E-mail).
├── README.md            # Documentação, guia de instalação e jornada técnica.
├── teste_isolado.py     # Homologação: Validação da tradução com Gemini 3.
├── teste_email.py       # Utilitário: Teste de envio e autenticação SMTP.
├── teste_selenium.py    # Utilitário: Verificação do motor de busca Edge/Selenium.
└── teste_schedule.py    # Experimento: Rotina de agendamento automático.

## 🚀 Funcionalidades

* **Coleta Dinâmica:** Captura previsões do site *astrology.com* usando Selenium com Microsoft Edge.
* **IA de Ponta:** Utiliza o modelo `gemini-3-flash-preview` para transformar textos brutos em mensagens inspiradoras em português.
* **Notificação Automática:** Envia o relatório final diretamente para o e-mail configurado.
* **Resiliência:** Tratamento de erros para limites de cota (429) e modelos obsoletos.

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **Selenium:** Automação de navegador.
* **Google GenAI SDK:** Integração com a API do Gemini.
* **Microsoft Edge Driver:** Navegação em modo *headless* (invisível).

## 📋 Pré-requisitos

1.  **Chave de API do Gemini:** Obtenha em [Google AI Studio](https://aistudio.google.com/).
2.  **Microsoft Edge Driver:** Certifique-se de ter o `msedgedriver.exe` compatível com sua versão do navegador.
3.  **Variáveis de Ambiente:** Por segurança, o projeto utiliza variáveis de ambiente:
    * `GEMINI_API_KEY`: Sua chave secreta do Google.
    * `ORACULO_APP_PASS`: Senha de aplicativo do Gmail (para envio de e-mail).

## 🔧 Instalação

1. Clone o repositório:
   ```bash
   git clone [https://github.com/SEU_USUARIO/zodiaco-digital.git](https://github.com/SEU_USUARIO/zodiaco-digital.git)

   ## 🧠 Desafios Técnicos & Soluções (Jornada do Herói)

Durante o desenvolvimento deste projeto em fevereiro de 2026, enfrentamos desafios que exigiram adaptações rápidas:

* **Obsolescência de Modelos:** Tentativas iniciais com o `gemini-1.5-flash` retornaram erro 404, revelando que o modelo já não estava disponível para a API v1beta na nossa região. 
    * **Solução:** Implementação de um log de debug para listar modelos ativos, resultando na migração para o **Gemini 3 Flash Preview**.
* **Gestão de Cotas (Rate Limiting):** O modelo 2.0 apresentou erro `429 RESOURCE_EXHAUSTED` (limite de tokens/minuto).
    * **Solução:** Mudança estratégica para o modelo Gemini 3, que possui uma cota independente para desenvolvedores, garantindo a continuidade do serviço.
* **Antidetecção no Scraping:** O site alvo bloqueava automações padrão.
    * **Solução:** Configuração do Edge em modo *headless* com a flag `AutomationControlled` desativada e uso de User-Agents específicos para simular navegação humana.