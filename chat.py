from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from flask_mysqldb import MySQL
import re
import logging
from datetime import datetime

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'barbearia'
mysql = MySQL(app)

app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.INFO)

chatbot = ChatBot("Chatbot")

conversa = [
    'Oi',
    'Olá',
    'Tudo bem?',
    'Tudo ótimo',
    'Tudo',
    'Que bom',
    'Qual o valor?',
    'R$ 30,00',
    'Quem é você?',
    'Eu sou um assistente virtual',
    'Obrigada',
    'Por nada!',
]

trainer = ListTrainer(chatbot)
trainer.train(conversa)

@app.route("/")
def home():
    return render_template("index.html")

# Funções CRUD
def agendar(nome_cliente, data, hora):
    try:
        # Converter data e hora
        data_formatada = datetime.strptime(data, "%Y-%m-%d").date()
        hora_formatada = datetime.strptime(hora, "%H:%M:%S").time()

        conn = mysql.connect # Obter a conexão com o banco de dados
        cur = conn.cursor()
        cur.execute("INSERT INTO agendamentos (nome_cliente, data, hora) VALUES (%s, %s, %s)",
                    [nome_cliente, data_formatada, hora_formatada])
        conn.commit()
        return "Agendamento realizado com sucesso!"
    except Exception as e:
        return f"Erro ao agendar: {str(e)}"

def cancelar(agendamento_id):
    try:
        cur = mysql.get_db().cursor()
        cur.execute("DELETE FROM agendamentos WHERE id = %s", [agendamento_id])
        mysql.get_db().commit()
        return "Cancelamento realizado com sucesso!"
    except Exception as e:
        return f"Erro ao cancelar: {str(e)}"

def consultar(nome_cliente):
    try:
        cur = mysql.get_db().cursor()
        cur.execute("SELECT * FROM agendamentos WHERE nome_cliente = %s", [nome_cliente])
        result = cur.fetchall()
        return jsonify(result)
    except Exception as e:
        return f"Erro ao consultar: {str(e)}"

# Rota para processar a mensagem do usuário
@app.route("/get_response", methods=["POST"])
def get_response():
    try:
        user_message = request.form["user_message"]
        app.logger.info(f"Received user message: {user_message}")

        # Processa operações CRUD
        resultado_operacao = processa_agendamento(user_message)

        if resultado_operacao:
            resposta = resultado_operacao
        else:
            resposta = str(chatbot.get_response(user_message))

        return resposta

    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return "Error"


def processa_agendamento(user_message):
    # Lista de palavras-chave relacionadas a operações CRUD
    palavras_chave_agendar = ["agendamento", "agendar", "marcar", "data", "hora", "dia"]
    palavras_chave_cancelar = ["cancelar", "desmarcar", "remover", "cancelamento"]
    palavras_chave_consultar = ["consultar", "verificar", "meus agendamentos"]
    palavras_chave_alterar = ["alterar", "alteração", "mudar"]

    # Construir expressões regulares para encontrar palavras-chave
    padrao_agendar = re.compile(r"\b(?:{})\b".format("|".join(palavras_chave_agendar)), re.IGNORECASE)
    padrao_cancelar = re.compile(r"\b(?:{})\b".format("|".join(palavras_chave_cancelar)), re.IGNORECASE)
    padrao_consultar = re.compile(r"\b(?:{})\b".format("|".join(palavras_chave_consultar)), re.IGNORECASE)
    padrao_alterar = re.compile(r"\b(?:{})\b".format("|".join(palavras_chave_alterar)), re.IGNORECASE)

    # Verificar se as expressões regulares encontram correspondências na mensagem do usuário
    if padrao_agendar.search(user_message):
        # Tentar extrair informações sobre agendamento da mensagem do usuário
        informacoes_agendamento = extrai_informacoes_agendamento(user_message)

        if informacoes_agendamento:
            # Aqui você pode processar as informações extraídas (nome, data, hora)
            nome_cliente = informacoes_agendamento.get("nome")
            data = informacoes_agendamento.get("data")
            hora = informacoes_agendamento.get("hora")

            # Chama a função de agendamento
            return agendar(nome_cliente, data, hora)
        else:
            return "Não foi possível extrair informações de agendamento."

    elif padrao_cancelar.search(user_message):
        # Executar a operação de cancelamento
        # A lógica de cancelamento deve ser implementada aqui
        return "Operação: Cancelar"

    elif padrao_consultar.search(user_message):
        # Executar a operação de consulta
        # A lógica de consulta deve ser implementada aqui
        return "Operação: Consultar"

    else:
        # Nenhuma operação correspondente identificada
        return None


def extrai_informacoes_agendamento(user_message):
    # Construir uma expressão regular para extrair nome, data e hora da mensagem
    padrao = re.compile(r"\b(?:nome|data|hora)\b.*?(\b\w+\b)", re.IGNORECASE)
    correspondencia = padrao.findall(user_message)

    if correspondencia:
        # Retorna um dicionário com as informações extraídas
        return {"nome": correspondencia[0], "data": correspondencia[1], "hora": correspondencia[2]}
    else:
        return None


if __name__ == "__main__":
    app.run()