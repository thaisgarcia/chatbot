from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

chatbot = ChatBot("BotR2-D2")

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
    'Thank you',
    'Por nada!',
    'Sério?',
    'Sim'
]

trainer = ListTrainer(chatbot)
trainer.train(conversa)

while True:
    mensagem = input("Envie uma mensagem para o chatbot: ")
    if mensagem.lower() == "parar":
        break
    resposta = chatbot.get_response(mensagem)
    print(resposta)