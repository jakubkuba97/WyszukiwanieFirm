import requests
from bs4 import BeautifulSoup
from math import ceil
from FirmObject import Firm


class BazaFirm:
    def __init__(self, max_sites_saved):
        self.current_site = 1
        self.firms_all = []
        self.website_adress = "https://www.baza-firm.com.pl/?vn=Sp.%20z%20o.o.&vm=pozna%C5%84&vw=15&vwn=wielkopolskie&pg=" + str(self.current_site) + "&b_szukaj=szukaj"
        self.site_size = 20
        self.number_of_sites = 1
        self.max_sites_saved = max_sites_saved
        try:
            agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
            req = requests.get(self.website_adress, headers=agent)
            soup = BeautifulSoup(req.content, "html.parser")
            soup = soup.find('body')
            while soup is None:
                print("Strona: " + self.website_adress)
                input("Wejdz na strone i zaznacz ze nie jestes robotem po czym wroc tutaj i nacisnij \"enter\"!")
                req = requests.get(self.website_adress, headers=agent)
                soup = BeautifulSoup(req.content, "html.parser")
                soup = soup.find('body')
            for header in soup.find_all(class_="navLeft"):
                for small_id in header.find_all(class_="boldTxt"):
                    self.number_of_sites = ceil(float(small_id.contents[0]) / self.site_size)
                    break
                break
            first = True
            while self.current_site <= self.max_sites_saved and self.current_site <= self.number_of_sites:
                if not first:
                    self.website_adress = "https://www.baza-firm.com.pl/?vn=Sp.%20z%20o.o.&vm=pozna%C5%84&vw=15&vwn=wielkopolskie&pg=" + str(self.current_site) + "&b_szukaj=szukaj"
                    req = requests.get(self.website_adress, headers=agent)
                    soup = BeautifulSoup(req.content, "html.parser")
                    soup = soup.find('body')
                check = False
                while not check:
                    try:
                        for header in soup.find_all(class_="wizLnk"):
                            tempo_name = header.text[:-2]
                            self.firms_all.append(Firm(str(header)[str(header).index("http"):str(header).index("\" rel=")], tempo_name))
                        check = True
                    except ValueError:
                        print("Strona: " + self.website_adress)
                        input("Wejdz na strone i zaznacz ze nie jestes robotem po czym wroc tutaj i nacisnij \"enter\"!")
                        req = requests.get(self.website_adress, headers=agent)
                        soup = BeautifulSoup(req.content, "html.parser")
                        soup = soup.find('body')
                first = False
                if self.max_sites_saved >= self.number_of_sites:
                    print("\tZaladowano 1 strone! " + str(self.current_site) + " / " + str(self.number_of_sites) + ".")
                else:
                    print("\tZaladowano 1 strone! " + str(self.current_site) + " / " + str(self.max_sites_saved) + ".")
                self.current_site += 1
        except requests.exceptions.ConnectionError:
            print("Brak polaczenia z internetem!")
