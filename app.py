from flask import Flask,render_template, request, Response
from chatbot import bot
import os
from helpers import *
from resumidor import criando_resumo
import uuid

app = Flask(__name__)
app.secret_key = 'alura'

caminho_imagem_enviada = None #sem upload
UPLOAD_FOLDER = 'dados' 

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
    global caminho_imagem_enviada
    prompt = request.json["msg"]
    nome_do_arquivo = 'historico_sabor_express'
    historico = ''
    if os.path.exists(nome_do_arquivo):
        historico = carrega(nome_do_arquivo)
    historico_resumido = criando_resumo(historico)

    resposta = bot(prompt,historico_resumido,caminho_imagem_enviada)
    texto_resposta = resposta.content[0].text

    conteudo = f"""
    Historico: {historico_resumido}
    Usuário: {prompt}
    IA: {texto_resposta}    
    """
    salva(nome_do_arquivo,conteudo)

    return texto_resposta

@app.route('/limpar_historico', methods = ['POST'])
def limpar_historico():
    nome_do_arquivo = 'historico_sabor_express'
    if os.path.exists(nome_do_arquivo):
        os.remove(nome_do_arquivo)
        print("Arquivo removido!")
    else: 
        print("Não foi possivel remover esse arquivo")
    return {}

# @app.route('/upload_imagem', methods=['POST'])
# def upload_imagem():
#     if 'imagem' in request.files:
#         imagem_enviada = request.files['imagem']
#         print(imagem_enviada)
#         return 'Imagem recebida com sucesso!', 200
#     return 'Nenhum arquivo foi enviado', 400

@app.route('/upload_imagem', methods=['POST'])
def upload_imagem():
    global caminho_imagem_enviada
    if 'imagem' in request.files:
        imagem_enviada = request.files['imagem']
        nome_arquivo = str(uuid.uuid4()) + os.path.splitext(imagem_enviada.filename)[1]
        caminho_arquivo = os.path.join(UPLOAD_FOLDER, nome_arquivo)
        print(caminho_arquivo)
        imagem_enviada.save(caminho_arquivo)
        caminho_imagem_enviada = caminho_arquivo
        print(caminho_imagem_enviada)
        return 'Imagem recebida com sucesso!', 200
    return 'Nenhum arquivo foi enviado', 400

if __name__ == "__main__":
    app.run(debug = True)