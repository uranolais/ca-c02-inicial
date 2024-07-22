import anthropic
import dotenv 
import os
from helpers import *

dotenv.load_dotenv()
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
modelo = "claude-3-opus-20240229"
restaurantes = carrega('./dados/dados_SaborExpress.txt')

def analisar_imagem(caminho_imagem):
    prompt_sistema = f"""
        Você é um assistente de chatbot e o usuário está enviado a foto de um alimento. Faça uma análise dele, e se for um alimento que tenha em seus restaurantes cadastrados,
        recomende um restaurante em que essa pessoa possa adquiri-lo. Assuma que você sabe e processou uma 
        imagem com o Vision e a resposta será informada no formato de saída.
        Não responda imagens não relacionadas a alimentos e comidas.
        Utilize os restaurantes dados a seguir:

        # FORMATO DA RESPOSTA
       
        Minha análise para imagem consiste em: Indicação de restaurante que venda esse alimento (se tiver em um restaurante cadastrado)
        
        # RESTAURANTES
        {restaurantes}
        
        ## Descreva a imagem
        coloque a descrição aqui
    """
    imagem_base64 = encodar_imagem(caminho_imagem)
    resposta = client.messages.create(
        model=modelo,
        max_tokens=1024,
        system=prompt_sistema,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data":imagem_base64,
                        },
                    }
                ],
            }
        ],
    )
    return resposta.content[0].text

# print(analisar_imagem("macarrao-simples.jpg"))