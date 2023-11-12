# Chatbot inteligente com Python 🤖

<b>Utlizando o Jupyter Notebook: </b>

1- Crie um Ambiente Virtual no Anaconda Prompt: <br>
`conda create --name chatbotpython python=versão_que_está_usando` <br>

2- Ative o Ambiente Virtual: `conda activate chatbotpython` 

2- Instale nesse Ambiente Virtual o Jupyter: `pip install jupyter`

3- Instale a biblioteca ChatterBot: `pip install chatterbot`

4- Instale a biblioteca Spacy: `pip install spacy`

5- Abra o Jupyter Notebook pelo Ambiente Virtual no Anaconda Prompt: `jupyter notebook`

6- Agora vamos à programação!

O primeiro passo é importar a biblioteca do Chatterbot e em seguida nós vamos precisar treinar ChatBot no Python. <br>
`from chatterbot import ChatBot` <br>
`from chatterbot.trainers import ListTrainer`


7- A biblioteca do ChatterBot está com um problema de compatibilidade, então execute os seguintes códigos para corrigir o bug: <br>
`from spacy.cli import download` <br>
`download("en_core_web_sm")` <br>
`class ENGSM:` <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`ISO_639_1 = 'en_core_web_sm'`

8- Crie o ChatBot e treine ele para que possa conversar: <br>
`chatbot = ChatBot("BotR2-D2")`

`conversa = [
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
]`

`trainer = ListTrainer(chatbot)` <br>
`trainer.train(conversa)`

9- Testando o ChatBot: <br>
`while True:` <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`mensagem = input("Envie uma mensagem para o chatbot: ")` <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`if mensagem.lower() == "parar":` <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`break` <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`resposta = chatbot.get_response(mensagem)` <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`print(resposta)`

Esse é um teste com um loop infinito para que você possa ir conversando com o bot. <br>
Vale lembrar que todos esses testes ele vai guardando, ou seja, vai gerando uma base de dados com essas informações para se aperfeiçoar ainda mais nas respostas.

10- Caso você queira resetar essa base de dados (se tiver gerado uma base que não está boa) pode utilizar o seguinte código: <br>
`chatbot.storage.drop()`
