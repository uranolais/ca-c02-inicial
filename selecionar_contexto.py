import anthropic
import dotenv 
import os
from helpers import *

dotenv.load_dotenv()
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
modelo = "claude-3-5-sonnet-20240620"
dados_SaborExpress = carrega('./dados/dados_SaborExpress.txt')
politicas_SaborExpress = carrega('./dados/politicas_SaborExpress.txt')
cadastro_SaborExpress = carrega('./dados/cadastro_SaborExpress.txt')

def selecionar_documento(contexto):
    if "políticas" in contexto:
        return dados_SaborExpress + "\n" + politicas_SaborExpress
    elif "cadastro" in contexto:
        return dados_SaborExpress + "\n" + cadastro_SaborExpress
    else:
        return dados_SaborExpress

def selecionar_contexto(prompt):
    prompt_usuario = prompt
    try:
        prompt_sistema = f"""
        A empresa Sabor Express possui três documentos principais que detalham diferentes aspectos do negócio:

        #Documento 1 "\n {dados_SaborExpress} "\n"
        #Documento 2 "\n" {politicas_SaborExpress} "\n"
        #Documento 3 "\n" {cadastro_SaborExpress} "\n"

        Avalie o prompt do usuário e retorne o documento mais indicado para ser usado no contexto da resposta. Retorne 'dados' se for o Documento 1, 'políticas' se for o Documento 2 e 'cadastro' se for o Documento 3. 

        """
        mensagem = client.messages.create(
            model=modelo,
            max_tokens=1000,
            temperature=0,
            system=prompt_sistema,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_usuario
                        }
                    ]
                }
            ]
        )
        contexto = mensagem.content[0].text.lower()
        return contexto
    except anthropic.APIConnectionError as e:
        return "Erro na API: %s" %e
    except anthropic.RateLimitError as e:
        print("Espere um tempo! Seu limite foi atingido.")
        return "Erro na API: %s" %e
    except anthropic.APIStatusError as e:
        print("Um status code diferente de 200 foi retornado!")
        print(e.status_code)
        print(e.response)
        return "Erro na API: %s" %e

