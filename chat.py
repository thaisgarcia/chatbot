from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

app = Flask(__name__)

chatbot = ChatBot("Chatbot")

conversa = [
    'Oi',
    'Olá',
    'Tudo bem?',
    'Tudo ótimo',
    'Você gosta de programar?',
    'Sim, eu programo em Python',
    'Qual o seu nome?',
    'R2-D2',
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

@app.route("/get_response", methods=["POST"])
def get_response():
    try:
        user_message = request.form["user_message"]
        app.logger.info(f"Received user message: {user_message}")
        response = str(chatbot.get_response(user_message))
        app.logger.info(f"Generated response: {response}")
        return response
    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return "Error"


if __name__ == "__main__":
    app.run(debug=True)
