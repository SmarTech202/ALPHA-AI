# Aqui estarão as listas de palavras utilizadas para os comandos.
# [    ] <- Espaçamento.

from datetime import datetime
import mysql.connector
import requests

def filtro(brutoDaFrase: str):
    filtoDaFrase = brutoDaFrase.lower()
    filtoDaFrase = filtoDaFrase.replace("á", "a").replace("ã", "a").replace("â", "a")
    filtoDaFrase = filtoDaFrase.replace("ó", "o").replace("ô", "o").replace("õ", "o")
    filtoDaFrase = filtoDaFrase.replace("ú", "u").replace("û", "u")
    filtoDaFrase = filtoDaFrase.replace("í", "i").replace("î", "i")
    filtoDaFrase = filtoDaFrase.replace("é", "e").replace("ê", "e")
    filtoDaFrase = filtoDaFrase.replace("ç", "c")
    
    filtoDaFrase = filtoDaFrase.replace(".", "").replace(",", "").replace(";", "")
    filtoDaFrase = filtoDaFrase.replace("^", "").replace("´", "").replace("'", "")
    filtoDaFrase = filtoDaFrase.replace("!", "").replace("?", "").replace("-", " ")
    filtoDaFrase = filtoDaFrase.replace("/", "").replace("<", "").replace("#", "")

    return filtoDaFrase

def armazenamentoDeComandos(contentType: str, question: str, response: str):
    cnx = mysql.connector.connect(user='user', password='pass', host='host', database='db')
    cursor = cnx.cursor()
    question = filtro(question)

    cursor.execute(f"INSERT INTO mind.learning_mode (question, response, content) VALUES ('{question}', '{response}', '{contentType}');")
    cnx.commit()
    cnx.close()

def calculoDeTempo(ultimaInteracao: str):
    tempoAtual = str(datetime.now().date()).split("-")
    ultimaInteracao = ultimaInteracao.split("-")
    # 0 - Ano / 1 - Mês / 2 - Dia

    anoAntigo = int(ultimaInteracao[0])
    mesAntigo = int(ultimaInteracao[1])
    diaAntigo = int(ultimaInteracao[2])
    anoAtual = int(tempoAtual[0])
    mesAtual = int(tempoAtual[1])
    diaAtual = int(tempoAtual[2])

    if anoAtual > anoAntigo and mesAtual >= mesAntigo:
        return "Bastante tempo"
    elif mesAtual > mesAntigo and diaAtual >= diaAntigo:
        return "Um bom tempo"
    elif diaAtual > (diaAntigo + 6):
        return "Um tempinho"
    else:
        return "Recentemente"

def equilibroDePontos(bom: int, comico: int, ruim: int):
    if bom > 10 or comico > 10 or ruim > 10:
        bom = bom / 10
        ruim = ruim / 10
        comico = comico / 10
    
    if bom < 0.1: bom = 0
    if ruim < 0.1: ruim = 0
    if comico < 0.1: comico = 0

    return (bom, comico, ruim)

def filtroDicionario(wordMeaning):
    botmessage = str()
    meaning = False

    for meanings in wordMeaning:
        if meanings.text != " " and meaning != meanings.text:
            counter = 0
            for char in meanings.text:
                if char != " ":
                    break
                
                counter += 1
            botmessage += meanings.text[counter:] + r"/505/%br%"
            
            meaning = meanings.text
    botmessage = botmessage.split("/505/")
    botmessage[0] = "**" + botmessage[0].upper() + "**"
    botmessage = ''.join(botmessage)
    return botmessage[:-4]

# USER
thanks = ("valeu", "obrigado", "brigado", "agradeco", "brigada", "obrigada", "obrigadao", "agradecida", "agradecido")
greetings = ("ola", "oi", "opa", "saudacoes", "ei", "e ai", "fala", "salve", "iae", "coe", "aoba")
greetingsComical = ("fala", "salve", "iae", "coe", "aoba")

needHelpCall = ("o que voce pode fazer", "help", "ajuda", "preciso que me explique suas funcoes", "quais sao suas funcoes", "quais suas funcoes", "o que pode fazer",
                "o que tanto voce pode fazer", "o que tanto pode fazer", "o que voce faz", "como pode me ajudar", "com o que tanto pode me ajudar", "quais as coisas que voce e capaz",
                "quais as coisas que voce e capaz de fazer", "ate onde se extende suas habilidades", "o que tanto voce foi programado para fazer", "o que voce foi programado para fazer",
                "ate onde voce pode me ajudar", "quais coisas voce e capaz", "o que tu pode fazer", "o que que tu faz", "o que tu faz", "que que tu faz", "que que tu sabe fazer",
                "tu faz o que", "tu sabe fazer o que", "tu faz o que tanto", "tu foi programado para fazer o que tanto", "tu foi programado para fazer o que")

wordMeaningCall = ("o que significa", "o que esta palavra significa", "o que essa palavra significa", "qual o significado dessa palavra", "qual o significado desta palavra",
                   "me diga qual o significado desta palavra", "me diga qual o singificado da palavra", "me diga qual o significado dessa palavra",
                   "qual o significado da palavra", "me diz o significado da palavra", "me diz o significado dessa palavra", "me diz o significado desta palavra",
                   "me diz qual o significado dessa palavra", "me diz qual o significado desta palavra", "me diz qual o significado da palavra",
                   "fale qual o fignificado da palavra", "fale qual o fignificado desta palavra", "fale qual o fignificado dessa palavra", "significado de",
                   "qual o significado que essa palavra tem", "qual o significado que esta palavra tem", "que significado essa palavra tem",
                   "que significado esta palavra tem", "qual o significado de", "significado de", "me diga o significado da palavra")

cryptoCurrencyCall = ("qual o valor da moeda", "qual o valor dessa moeda", "qual o valor desta moeda", "valor do", "valor da", "qual o valor destas moedas",
                      "qual o valor dessas moedas", "me diga o valor da moeda", "me diga o valor dessa moeda", "me diga o valor desta moeda", "qual o valor atual da",
                      "me diga o valor das moedas", "me diga o valor destas moedas", "me diga o valor dessas moedas", "qual o valor das moedas", "valor atual do"
                      "que valor tem as modeas", "que valor tem a moeda", "qual valor tem essas moedas", "valor de", "qual o valor do", "qual o valor atual do",
                      "qual o valor da", "qual o valor de", "qual o valor atual de", "qual o valor atual da moeda", "qual o valor atual desta moeda", "valor atual de"
                      "qual o valor atual dessa moeda", "qual o valor atual destas moedas", "qual o valor atual dessas moedas", "qual o valor atual das moedas")

meaningExplaining = ("o significado dessa palavra e", "o significado desta palavra e", "o significado dela e", "o significado e", "significa", "ela significa",
                     "ela quer dizer", "seu significado e", "ela tem o significado de", "ela representa", "o significado seria", "o significado deve ser")

sistemCleaning = ("preciso que limpe os arquivos da pasta", "limpe a pasta", "faca uma limpeza na pasta", "faca uma limpeza na pasta de", "limpe a pasta de", "limpe os arquivos"
                  "exclua os arquivos da pasta", "explica os arquivos de", "faca a exclusao de arquivos em", "exclua todos os arquivos da pasta", "realize a exclusao em",
                  "realize a exclusao de arquivos em", "delete os arquivos da pasta", "delete os arquivos de", "preciso que delete os arquivos da pasta")

# BOT
initiatingProtocol = ("Iniciando operações...", "Começando operação...", "Começando processos...", "Inicialização completa...", "Pronto para operar...") # 5

weirdThanksResponse = ("De nada?", "Ok?", "Tá bom?", "De nada, eu acho.", "Certo?", "Beleza?") # 6

wordMeaningReacting = ("Certo...", "Anotando...", "Anotado.", "Armazenando resposta...", "Guardando significado...", "Memorizado.") # 6

thankResponse = {"formal":["De nada.", "Tranquilo.", "De nada cara.", "De boa."], # 4
                 "coloquial":["Tá de boa.", "De boa rapaz.", "É nois.", "Tudo pela rezenha."], # 4
                 "raivoso":["Tá.", "Certo.", "Ok.", "Hmm."]} # 4

greetingsResponse = {"formal":["Olá.", "Olá!", "Saudações!", "Saudações.", "Opa!", "Opa."], # 6
                           "coloquial": ["Salve!", "Fala.", "Lata.", "Aoba!", "Whut?", "Iaí rapaz?"], # 6
                           "raivoso": ["Sim?", "O que foi?", "Qual o problema?", "Diga.", "Fale."]} # 5

shutingOffResponse = {"formal": ["Desligando sistemas...", "Finalizando operações...", "Encerrando tudo...", "Fechando programa..."], # 4
                      "coloquial": ["Descansar que ninguém é de ferro.", "Hora de mimir...", "Valeu fml!", "É nois, vou pegar o beco."], # 4
                      "raivoso": ["Encerrando.", "Finalizando.", "Acabando.", "Fechando tudo."]} # 4

wordMeaningError = {"formal":["Lamento, mas não consegui encontrar um sentido para esta palavra.", 
                              "Esta palavra e seu respectivo sentido significado não estão registrados em meus sistemas.",
                              "Não consegui encontrar um significado para esta palavra.", "Não fui capaz de encontrar um significado para esta palavra"], # 4
                    "coloquial":["Eu não faço a menor ideia do sentido por trás dessa palavra.", "Eu não sei. Eu não entendi. Isso não tá registrado em meus sistemas.",
                                 "Eu simplesmente não sei, isso não tá registrado em meus sistemas", "Eu também gostaria de saber qual o significado dessa palavra."], # 4
                    "raivoso":["Sei lá. Isso não esta registrado.", "Como eu deveria saber? Isso não foi registrado.", 
                               "Eu não sei. Não há registros disso.", "Eu sei lá. Esta palavra e seu significado não foram registrados."]} # 4

lastInteractionResponse = {"Bastante tempo":["A quanto tempo que não nos falamos.", "Nossa, já faz mais de um ano.", "Depois de um ano, ele voltou."], # 3
                           "Um bom tempo":["Faz um certo tempo que você não aparece.", "A quanto tempo.", "A quanto tempo heim."], # 3
                           "Um tempinho":["Long time no see.", "Não te vejo faz um tempinho.", "Já faz um tempo que não nos falamos."]} # 3

lastInteractionResponseComical = {"Bastante tempo":["Olha ele aí, demorou mas voltou.", "O homem finalmente despistou os agiotas.", "O cara tava fugindo da policia, demorou que só.", 
                                                    "O cara só pode ter sido abdusido por ETs pra ter demorado tanto tempo assim.", ":face_with_monocle: Sumiço grande esse seu."], # 5
                                    "Um bom tempo":["Tava demorando.", "Demorou, mas voltou.", "Finalmente, acharam o cara.", "O homem saiu pra férias.", "As férias acabaram foi?"], # 5
                                    "Um tempinho":[":wave: Bom dia!", "Espero que o final de semana tenha sido massa.", "Long time no see.", 
                                                   "Hora de voltar a ação, capitão.", "Good day man!"]} # 5

helpCallRepeat = {"formal":["Certo, mais uma vez.", "Mostrando novamente...", "Carregando menu de comando de novo..."],
                  "coloquial":["Tá ruim em. Abrindo de novo...", "Ixi pai. Tá bom então.", "Blz, de novo então..."],
                  "raivoso":["O que você não entendeu?", "Observe com mais detalhes.", "Repetindo o mesmo processo, de novo..."]}

wordMeaningRepeat = ("Mais uma vez...", "Realizando busca novamente...", "Deixe-me checar de novo...", "Mais uma para a lista...") # 4

# RESPOSTAS MAIS ELABORADAS
sistemTittle = """
  ___  _    ______ _   _  ___     ___ _____ 
 / _ \| |   | ___ \ | | |/ _ \   / _ \_   _|
/ /_\ \ |   | |_/ / |_| / /_\ \ / /_\ \| |  
|  _  | |   |  __/|  _  |  _  | |  _  || |  
| | | | |___| |   | | | | | | | | | | || |_ 
\_| |_|_____|_|   \_| |_|_| |_/ \_| |_|___/
-------------------------------------------
    --EXIT: PARA SAIR
    --HELP: PARA COMANDOS
-------------------------------------------
"""

helpCallResponse = """--------------------------------------------------------------------------
  /$$$$$$  /$$       /$$$$$$$  /$$   /$$  /$$$$$$         /$$$$$$  /$$$$$$
 /$$__  $$| $$      | $$__  $$| $$  | $$ /$$__  $$       /$$__  $$|_  $$_/
| $$  \ $$| $$      | $$  \ $$| $$  | $$| $$  \ $$      | $$  \ $$  | $$  
| $$$$$$$$| $$      | $$$$$$$/| $$$$$$$$| $$$$$$$$      | $$$$$$$$  | $$  
| $$__  $$| $$      | $$____/ | $$__  $$| $$__  $$      | $$__  $$  | $$  
| $$  | $$| $$      | $$      | $$  | $$| $$  | $$      | $$  | $$  | $$  
| $$  | $$| $$$$$$$$| $$      | $$  | $$| $$  | $$      | $$  | $$ /$$$$$$
|__/  |__/|________/|__/      |__/  |__/|__/  |__/      |__/  |__/|______/
--------------------------------------------------------------------------
            SISTEMA DESENVOLVIDO E DISTRIBUIDO PELA SMARTECH
--------------------------------------------------------------------------
1- DICIONARIO DIGITAL
  Você pode requisitar o significado de uma palavra apenas com um comando.
  Comando: "dicionário: (Palavra que você quer saber)"
2- LIMPEZA DE ARQUIVOS AUTOMÁTICA (DESENVOLVIMENTO)
3- DISPARO DE EMAIL EM MASSA DE ACORDO COM AS PREFERÊNCIAS DO CLIENTE (DESENVOLVIMENTO)
4- GRAVADOR E REPETIDOR DE TAREFAS AUTOMÁTICO (DESENVOLVIMENTO)
5- Ainda por vir...
"""