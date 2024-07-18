import anthropic
import dotenv 
import os

dotenv.load_dotenv()
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
modelo = "claude-3-opus-20240229"

def criando_resumo(historico):
    prompt_sistema = f"""
        Resumir progressivamente as linhas de conversa fornecidas, 
        acrescentando ao resumo anterior e retornando um novo resumo. 
        Não apague nenhum assunto da conversa. 
        Se não houver resumo, apenas continue a conversa normalmente.

        ## EXEMPLO:
        O usuario pergunta o que a IA pensa sobre a inteligência artificial. 
        A IA acredita que a inteligência artificial é uma força para o bem.
        Usuário: Por que você acha que a inteligência artificial é uma força para o bem?
        IA: Porque a inteligência artificial ajudará os humanos a alcançarem seu pleno 
        potencial.

        ### Novo resumo:
        O usuario questiona a razão pela qual a IA considera a inteligência artificial 
        uma força para o bem, e a IA responde que é porque a inteligência artificial 
        ajudará os humanos a atingirem seu pleno potencial.

        ## FIM DO EXEMPLO
        
        Resumo atual:
        {historico}

        Novo resumo:"""
    try:
        mensagem = client.messages.create(
            model=modelo,
            max_tokens=4000,
            temperature=0,
            system=prompt_sistema,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": historico
                        }
                    ]
                }
            ]
            )
        resumo = mensagem.content[0].text
        return resumo
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

# def criando_resumo(historico):
#     resposta = resumidor_de_historico(historico=historico)
#     resumo = resposta.choices[0].message.content
#     return resumo