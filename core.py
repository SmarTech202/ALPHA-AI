print("INICIANDO SISTEMA...")
import commands
import coleta
import mind

from gspread.cell import Cell
from datetime import datetime
from random import randint
from time import sleep
import mysql.connector
from os import system
import pandas as pd
import warnings
import requests

learning_mode = False
thank = False
word = False

good = 0
bad = 0
comical = 0
lastInt = False
infoColecter = coleta.getInfo()

system("cls || clear")
print("SISTEMA INICIADO!")
sleep(1.5)

try:
    userInfo = pd.read_excel(".\\Storage\\userInfo.xlsx", engine="openpyxl")
    userInfo = userInfo.to_dict()
    username = userInfo["Username"][0]
    good = float(userInfo["Good"][0])
    bad = float(userInfo["Bad"][0])
    comical = float(userInfo["Comical"][0])
    lastInt = userInfo["Last Interaction"][0]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        classification = mind.HumorClassification()
        humor = classification.getHumor([good, bad, comical])

    if humor == "bom" or humor == "neutro":
        print(f"Alpha AI: Seja bem vindo de volta {username}!")
        sleep(1.5)
    print("Alpha AI:",commands.initiatingProtocol[randint(0, 4)])
except:
    print("Alpha AI: Parece que você é um usuário novo.")
    sleep(1.5)
    username = str(input("Alpha AI: Como gostaria de ser chamado? "))
    if " " in username:
        username = username.split(" ")[0]

    sleep(0.5)
    print(f"Alpha AI: Certo {username}! Tudo pronto para iniciarmos!")

    userInfo = {"Username":[username], "Good":[0], "Bad":[0], "Comical":[0], "Last Interaction":["None"]}
    userInfo = pd.DataFrame(userInfo)
    userInfo.to_excel(".\\Storage\\userInfo.xlsx", index=False)

sleep(1.5)
system("clear || cls")
print(commands.sistemTittle)

while True:
    promptBrute = str(input(f"{username}: "))
    prompt = commands.filtro(promptBrute)
    sleep(1)

    if prompt == "exit":
        if humor == "bom" or humor == "neutro":
            print("Aplha AI:",commands.shutingOffResponse["formal"][randint(0, 3)])
        if humor == "comico":
            print("Aplha AI:",commands.shutingOffResponse["coloquial"][randint(0, 3)])
        if humor == "ruim":
            print("Aplha AI:",commands.shutingOffResponse["raivoso"][randint(0, 3)])
        sleep(1.5)
        break

    if prompt.split(" ")[0] in commands.greetings:
        good += 0.05
        if lastInt == "Greetings":
            bad += 0.05
        if prompt.split(" ")[0] in commands.greetingsComical:
            good += 0.1
            comical += 0.25
        if humor == "bom" or humor == "neutro":
            print("Aplha AI:",commands.greetingsResponse["formal"][randint(0, 4)])
        if humor == "comico":
            print("Aplha AI:",commands.greetingsResponse["coloquial"][randint(0, 4)])
        if humor == "ruim":
            print("Aplha AI:",commands.greetingsResponse["raivoso"][randint(0, 5)])
        lastInt = "Greetings"

    if prompt.split(" ")[0] in commands.thanks or ("muito obrigado" in prompt):
        if thank:
            if humor == "bom" or humor == "neutro":
                print("Aplha AI:", commands.thankResponse["formal"][randint(0, 3)]) 
            if humor == "comico":
                print("Aplha AI:",commands.thankResponse["coloquial"][randint(0, 3)])
            if humor == "ruim":
                print("Aplha AI:",commands.thankResponse["raivoso"][randint(0, 3)])
            thank = False
            good += 0.07
        else:
            comical += 0.07
            bad += 0.05
            print("Aplha AI:",commands.weirdThanksResponse[randint(0, 5)])

    if prompt in commands.needHelpCall:
        if lastInt == "HelpCall":
            bad += 0.15
            if humor == "bom" or humor == "neutro":
                print("Aplha AI:",commands.helpCallRepeat["formal"][randint(0, 2)])
            if humor == "comico":
                print("Aplha AI:",commands.helpCallRepeat["coloquial"][randint(0, 2)])
            if humor == "ruim":
                print("Aplha AI:",commands.helpCallRepeat["raivoso"][randint(0, 2)])
        lastInt = "HelpCall"
        thank = True
            
        system("clear || cls")
        print(commands.helpCallResponse)
        input("[ENTER] Sair da tela de ajuda: ")
        system("clear || cls")
        print(commands.sistemTittle)
    
    if prompt.split(": ")[0] in commands.wordMeaningCall:
        if lastInt == "WordMeaning":
            print("Alpha AI:", commands.wordMeaningRepeat[randint(0, 3)])
        else:
            print("Alpha AI: Buscando...")
        response = infoColecter.dictionary(promptBrute.split(": ")[1])
        word = promptBrute.split(": ")[1]

        if response == "Não encontrada":
            if humor == "bom" or humor == "neutro":
                print("Alpha AI:", commands.wordMeaningError["formal"][randint(0, 3)])
            if humor == "comico":
                print("Alpha AI:", commands.wordMeaningError["coloquial"][randint(0, 3)])
            if humor == "ruim":
                print("Alpha AI:", commands.wordMeaningError["raivoso"][randint(0, 3)])
        else:
            print(response)
        lastInt = "WordMeaning"
        thank = True
    
    if prompt.split(": ")[0] in commands.meaningExplaining and lastInt == "WordMeaning" and word:
        if len(promptBrute.split(": ")[1]) <= 0:
            bad += 0.2
            print("Não entendi o que isso deveria significar.")
        else:
            messageResponse = pd.DataFrame({"word":[word],"meaning":[promptBrute.split(": ")[1]]})

            try:
                wordMeaning = pd.read_excel(".\\Storage\\meaningInfo.xlsx", engine="openpyxl")
                wordMeaning = pd.concat([messageResponse, wordMeaning]).drop_duplicates(subset=["word", "meaning"], keep="last").reset_index(drop=True)
                wordMeaning.to_excel(".\\Storage\\meaningInfo.xlsx", index=False)
            except:
                messageResponse.to_excel(".\\Storage\\meaningInfo.xlsx", index=False)
            print("Alpha AI:",commands.wordMeaningReacting[randint(0, 5)])

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        classification = mind.HumorClassification()
        humor = classification.getHumor([good, bad, comical])

        userInfo = {"Username":[username], "Good":[good], "Bad":[bad], "Comical":[comical], "Last Interaction":[lastInt]}
        userInfo = pd.DataFrame(userInfo)
        userInfo.to_excel(".\\Storage\\userInfo.xlsx", index=False)