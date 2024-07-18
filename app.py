from flask import Flask,render_template, request, Response
from chatbot import bot
import os
from helpers import *
from resumidor import criando_resumo

app = Flask(__name__)
app.secret_key = 'alura'

@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/chat",methods=['POST'])
# def chat():
#     prompt = request.json["msg"]
#     resposta = bot(prompt)
#     texto_resposta = resposta.content[0].text
#     return texto_resposta 

@app.route("/chat",methods=['POST'])
def chat():
    prompt = request.json["msg"]
    nome_do_arquivo = 'historico_sabor_express'
    historico = ''
    if os.path.exists(nome_do_arquivo):
        historico = carrega(nome_do_arquivo)
    historico_resumido = criando_resumo(historico)

    resposta = bot(prompt,historico_resumido)
    texto_resposta = resposta.content[0].text

    conteudo = f"""
    Historico: {historico_resumido}
    Usuário: {prompt}
    IA: {texto_resposta}    
    """
    salva(nome_do_arquivo,conteudo)

    return texto_resposta

@app.route('/limparhistorico', methods = ['POST'])
def limpar_historico():
    nome_do_arquivo = 'historico_sabor_express'
    if os.path.exists(nome_do_arquivo):
        os.remove(nome_do_arquivo)
        print("Arquivo removido!")
    else: 
        print("Não foi possivel remover esse arquivo")
    return {}

if __name__ == "__main__":
    app.run(debug = True)