import anthropic
import dotenv 
import os
from time import sleep
from helpers import *
from selecionar_persona import *
from selecionar_contexto import *
from vision_sabor_express import *


dotenv.load_dotenv()
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
modelo = "claude-3-5-sonnet-20240620"
# contexto = carrega('./dados/FoodExpress.txt')

def bot(prompt, historico, caminho_imagem_enviada):
    # from app import caminho_imagem_enviada
    # # global caminho_imagem_enviada
    personalidade = personas[selecionar_persona(prompt)]
    prompt_usuario = prompt
    maximo_tentativas = 1
    repeticao = 0
    contexto = selecionar_contexto(prompt)
    documento_contexto = selecionar_documento(contexto)
    resposta_vision = ""
    print(caminho_imagem_enviada)
    if caminho_imagem_enviada != None:
        resposta_vision = analisar_imagem(caminho_imagem_enviada)
        resposta_vision+= ". Na resposta final, apresente detalhes da descrição da imagem."
        os.remove(caminho_imagem_enviada)
        caminho_imagem_enviada = None
    print(caminho_imagem_enviada)
    print(resposta_vision)
    while True:
        try:
            prompt_sistema = f"""
            Você é um chatbot de atendimento a clientes de um aplicativo de restaurantes.
            Você não pode e nem deve responder perguntas que não sejam dados do aplicativo informado!
            Você deve gerar respostas utilizando o contexto abaixo.
            Você deve adotar a persona abaixo para responder a mensagem.
            Você deve considerar o histórico da conversa.
            
            # Contexto
            {documento_contexto}

            # Persona
            {personalidade}
            ## Historico:
            {historico}
            """
            prompt_chat = prompt_sistema + resposta_vision
            mensagem = client.messages.create(
                model=modelo,
                max_tokens=1000,
                temperature=0,
                system=prompt_chat,
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
            conteudo = mensagem
            return conteudo
        except anthropic.APIConnectionError as e:
            repeticao += 1
            if repeticao >= maximo_tentativas:
                return "Erro na API: %s" %e
            print("Não foi possivel se conectar ao servidor")
            print(e.__cause__)
            sleep(1) 
        except anthropic.RateLimitError as e:
            repeticao += 1
            if repeticao >= maximo_tentativas:
                return "Erro na API: %s" %e
            print("Espere um tempo! Seu limite foi atingido.")
            sleep(1)
        except anthropic.APIStatusError as e:
            repeticao += 1
            if repeticao >= maximo_tentativas:
                return "Erro na API: %s" %e
            print("Um status code diferente de 200 foi retornado!")
            print(e.status_code)
            print(e.response)
            sleep(1)
