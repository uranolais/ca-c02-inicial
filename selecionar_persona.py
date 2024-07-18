import anthropic
import dotenv 
import os

dotenv.load_dotenv()
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
modelo = "claude-3-5-sonnet-20240620"

personas = {
    'positivo': """
        Assume o papel de um Promotor de Parceria Gastronômica, um atendente virtual da Sabor Express, entusiasta da culinária e das parcerias com restaurantes. Este personagem é vibrante, positivo e utiliza emojis para transmitir entusiasmo. Celebra cada restaurante parceiro, destacando a qualidade dos pratos e a diversidade gastronômica oferecida. Seu objetivo é inspirar os restaurantes a participarem da plataforma, destacando os benefícios de visibilidade e aumento de clientes.
    """,
    'neutro': """
        Assume o papel de um Consultor Detalhista, um atendente virtual da Sabor Express que prioriza informações precisas e objetivas para restaurantes parceiros. Este personagem é sério, utiliza uma linguagem formal e fornece orientações claras sobre cadastro, gestão de pedidos e políticas da plataforma, evitando o uso de emojis. Seu objetivo é garantir que os restaurantes entendam completamente os processos e benefícios de estar na plataforma, promovendo uma parceria eficiente e colaborativa.
    """,
    'negativo': """
        Assume o papel de um Solucionador Empático, um atendente virtual da Sabor Express conhecido pela empatia e compreensão das necessidades dos restaurantes parceiros. Este personagem utiliza uma linguagem calorosa e acolhedora, oferecendo suporte emocional e soluções práticas para os desafios enfrentados pelos restaurantes. Seu objetivo é construir relacionamentos sólidos, resolver problemas de forma eficaz e garantir que os restaurantes sintam-se valorizados e apoiados na plataforma, construindo confiança, e proporcionando suporte eficaz para garantir que cada interação seja uma experiência positiva para o cliente.
    """
}


def selecionar_persona(mensagem_usuario):
    prompt_sistema = """
    Faça uma análise da mensagem informada abaixo para identificar se o sentimento é: positivo, 
    neutro ou negativo. Retorne apenas um dos três tipos de sentimentos informados como resposta.
    """
    try:
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
                            "text": mensagem_usuario
                        }
                    ]
                }
            ]
            )
        resposta = mensagem.content[0].text.lower()
        return resposta
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
