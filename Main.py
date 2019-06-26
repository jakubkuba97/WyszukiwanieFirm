from SiteObject import BazaFirm
import ExcelWorks

if __name__ == '__main__':
    nazwa_pliku_excel = "Zapisane strony"
    print()
    entered = ""
    while len(entered) < 1:
        entered = input("Wpisz ile stron chcesz zapisac: ")
        try:
            if int(entered) <= 0:
                print("Podano zla liczbe!")
                entered = ""
        except (ValueError, TypeError):
            print("Nie podano liczby!")
            entered = ""

    print("\tRozpoczecie wyszukiwania!\n")
    baza_danych = BazaFirm(int(entered))

    print("\n\tWyszukiwanie danych zakonczone poprawnie!")
    print("\tRozpoczecie zapisywania!\n")
    while True:
        try:
            ExcelWorks.set_first(nazwa_pliku_excel)
            length = baza_danych.max_sites_saved
            if baza_danych.max_sites_saved >= baza_danych.number_of_sites:
                length = baza_danych.number_of_sites
            ExcelWorks.write_to_file(nazwa_pliku_excel, baza_danych.firms_all, length, baza_danych.site_size)
            ExcelWorks.adjust(nazwa_pliku_excel)
            break
        except PermissionError:
            input("Zamknij plik i nacisnij \"enter\"!")

    print("\n\tZapisywanie danych zakonczone poprawnie!")
    user_input = ""
    while user_input != 'e':
        user_input = input('\tWpisz "e" aby zakonczyc!  ')
