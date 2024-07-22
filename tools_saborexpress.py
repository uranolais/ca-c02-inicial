import anthropic
import dotenv 
import os
from helpers import *

dotenv.load_dotenv()
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
MODEL_NAME = "claude-3-opus-20240229"

tools = [
    {
        "name": "pega_dados_sabor_express",
        "description": "Pega os dados referentes ao Sabor Express",
        "input_schema": {
            "type": "object",
            "properties": {
                "caminho_do_arquivo": {
                    "type": "string",
                    "description": "Caminho do arquivo que contém os Dados e Informações do Sabor Express"
                }
            },
            "required": ["caminho_do_arquivo"]
        }
    },
    {
        "name": "pega_politicas_sabor_express",
        "description": "Pega os dados de políticas referentes ao Sabor Express",
        "input_schema": {
            "type": "object",
            "properties": {
                "caminho_do_arquivo": {
                    "type": "string",
                    "description": "Caminho do arquivo que contém as Politicas do Sabor Express"
                }
            },
            "required": ["caminho_do_arquivo"]
        }
    },
    {
        "name": "pega_cadastro_sabor_express",
        "description": "Pega as informações de cadastro do Sabor Express",
        "input_schema": {
            "type": "object",
            "properties": {
                "caminho_do_arquivo": {
                    "type": "string",
                    "description": "Caminho do arquivo que contém as informações de Cadastro do Sabor Express"
                }
            },
            "required": ["caminho_do_arquivo"]
        }
    }
]

def pega_dados_sabor_express(caminho_do_arquivo):
    dados_sabor_express = carrega(caminho_do_arquivo)
    return dados_sabor_express

def pega_politicas_sabor_express(caminho_do_arquivo):
    politicas_sabor_express = carrega(caminho_do_arquivo)
    return politicas_sabor_express

def pega_cadastro_sabor_express(caminho_do_arquivo):
    cadastro_sabor_express = carrega(caminho_do_arquivo)
    return cadastro_sabor_express
    
def processa_chamada_tool(tool_name, tool_input):
    if tool_name == "pega_dados_sabor_express":
        return pega_dados_sabor_express(tool_input["caminho_do_arquivo"])
    elif tool_name == "pega_politicas_sabor_express":
        return pega_politicas_sabor_express(tool_input["caminho_do_arquivo"])
    elif tool_name == "pega_cadastro_sabor_express":
        return pega_cadastro_sabor_express(tool_input["caminho_do_arquivo"])