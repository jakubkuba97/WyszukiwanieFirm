import requests
from bs4 import BeautifulSoup


class Firm:
    def __init__(self, strona_internet, nazwa):
        self.strona_baza_firm = strona_internet
        self.nazwa_firmy = nazwa
        self.adres_firmy = "Adres firmy"
        self.numer_nip = "0000000000"
        self.numer_telefonu = " "

        self.strona_krs = " "
        self.osoby_reprezentujace = "Brak osob w danych"

        self.operator = "---"
        self.ile_sim = "-"
        self.data_umowy = "00.00.0000"
        self.uwagi = " "

        agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
        req = requests.get(self.strona_baza_firm, headers=agent)
        soup = BeautifulSoup(req.content, "html.parser")
        soup = soup.find('body')
        check = False
        while not check:
            try:
                for header in soup.find_all(class_="firstBox txtDataBox lineHeight26"):
                    text_temp = str(header.contents)
                    self.numer_telefonu = ""
                    if "tel./" in text_temp:
                        self.numer_telefonu += text_temp[text_temp.index("tel./"):text_temp.index("tel./") + 23]
                    elif "tel. " in text_temp:
                        self.numer_telefonu = text_temp[text_temp.index("tel."):text_temp.index("tel.") + 19]
                    if "fax " in text_temp:
                        if self.numer_telefonu != "":
                            self.numer_telefonu += "  \n"
                        self.numer_telefonu += text_temp[text_temp.index("fax "):text_temp.index("fax ") + 18]
                    if self.numer_telefonu == "":
                        self.numer_telefonu = " "
                    break
                for header in soup.find_all(class_="addrNipBox"):
                    text_temp = str(header.contents)
                    text = ""
                    if "</span><br/><span" in text_temp and "streetAddress\">" in text_temp:
                        text += text_temp[text_temp.index("streetAddress\">") + 15:text_temp.index("</span><br/><span")] + " \n"
                    if "</span> <span itemprop=\"addr" in text_temp and "postalCode\">" in text_temp:
                        text += text_temp[text_temp.index("postalCode\">") + 12:text_temp.index("</span> <span itemprop=\"addr")] + " \n"
                    elif "postalCode\">" in text_temp and "</span>" in text_temp[text_temp.index("postalCode\">"):]:
                        text += text_temp[text_temp.index("postalCode\">") + 12:text_temp.index("postalCode\">") + 12 + 6] + " \n"
                    if "</span> - <span class=\"dar" in text_temp and "addressLocality\">" in text_temp:
                        text += text_temp[text_temp.index("addressLocality\">") + 17:text_temp.index("</span> - <span class=\"dar")] + " "
                    elif "addressLocality\">" in text_temp and "</span> </a> - " in text_temp[text_temp.index("addressLocality\">"):]:
                        text += text_temp[text_temp.index("addressLocality\">") + 17:(
                                text_temp.index("addressLocality\">") + 17 + text_temp[text_temp.index("addressLocality\">"):].index("</span> </a> - "))] + " "
                    if "</span></div>, ' ', <di" in text_temp and "darkGrayColor\">" in text_temp:
                        text += text_temp[text_temp.index("darkGrayColor\">") + 15:text_temp.index("</span></div>, ' ', <di")] + " "
                    elif "darkGrayColor br_link\"> <span>" in text_temp and "</span> </a>" in text_temp[text_temp.index("darkGrayColor br_link\"> <span>"):]:
                        text += text_temp[text_temp.index("darkGrayColor br_link\"> <span>") + 15:(
                            text_temp.index("darkGrayColor br_link\"> <span>") + 15 + text_temp[text_temp.index("darkGrayColor br_link\"> <span>"):].index("</span> </a>"))] + " "
                    if "pozna" not in text.lower()[int(len(text) / 2):]:
                        text += "Poznan"
                    self.adres_firmy = text
                    if "NIP:" in text_temp:
                        self.numer_nip = text_temp[text_temp.index("NIP:") + 12:text_temp.index("NIP:") + 22]
                    break
                check = True
            except ValueError:
                print("Strona: " + self.strona_baza_firm)
                input("Wejdz na strone i zaznacz ze nie jestes robotem po czym wroc tutaj i nacisnij \"enter\"!")
                req = requests.get(self.strona_baza_firm, headers=agent)
                soup = BeautifulSoup(req.content, "html.parser")
                soup = soup.find('body')
        if self.numer_nip != "0000000000" and len(self.numer_nip) == 10:
            self.osoby_reprezentujace = "Nie mozna wyszukac reprezentacji!"
