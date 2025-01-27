# Área para a coleta de dados da internet.
# Conteúdo: Significado de palavras, Valores de Cryptomoedas.
# Significado: Ele buscará os significado da palavra enviada pelo usuário em uma página de dicionário.
# Podendo ser corrigido pelo usuário quando o Learning Mode estiver ativado.
# Crypto: Ele enviará, armazenará e fará uma comparação com o valor já armazenado da moéda.

# Site do Dicionário: https://www.dicio.com.br/palavra/
# Site do Crypto: https://coinmarketcap.com/currencies/bitcoin/
from bs4 import BeautifulSoup
import pandas as pd
import requests
import commands

class getInfo():
    def dictionary(self, word: str):
        try:
            wordMeaning = pd.read_excel(".\\Storage\\meaningInfo.xlsx", engine="openpyxl")
            wordMeaning = wordMeaning.to_dict()
        except:
            wordMeaning = False

        if wordMeaning and len(wordMeaning["word"]) > 0:
            count = 0
            for wordM in wordMeaning["word"]:
                if str(wordMeaning["word"][wordM]).lower() == word.lower():
                    return wordMeaning["meaning"][count]
                count += 1
        
        response = requests.get(f"https://www.dicio.com.br/{word}/")
        content = BeautifulSoup(response.content, "html.parser")

        dictionaryResponse = content.find("div", attrs={"class":"title-header"})
        dictionaryResponse = dictionaryResponse.find("h1")
        dictionaryResponse = dictionaryResponse.text

        if str(dictionaryResponse) == "Não encontrada":
            return "Não encontrada"
        else:
            wordMeaning = content.find("p", attrs={"class":"significado textonovo"})
            messageResponse = str(commands.filtroDicionario(wordMeaning))
            response = messageResponse.replace(r"%br%", "\n").replace("**", "\n")
            messageResponse = pd.DataFrame({"word":[word],"meaning":[messageResponse]})

            try:
                wordMeaning = pd.read_excel(".\\Storage\\meaningInfo.xlsx", engine="openpyxl")
                wordMeaning = pd.concat([messageResponse, wordMeaning]).drop_duplicates(subset=["word", "meaning"], keep="last").reset_index(drop=True)
                wordMeaning.to_excel(".\\Storage\\meaningInfo.xlsx", index=False)
            except:
                messageResponse.to_excel(".\\Storage\\meaningInfo.xlsx", index=False)
        return response