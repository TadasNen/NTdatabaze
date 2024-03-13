from ieskojimo_funkcijos import *
from pridejimo_funkcijos import *
from istrinimo_funkcijos import *
from pakeitimo_funkcijos import *

def pagr_menu():
    print("\nPagrindinis menu:")
    print("1. Ieskoti")
    print("2. Prideti")
    print("3. Istrinti")
    print("4. Pakeisti")
    print("q - Iseiti")

def ieskoti_menu():
    print("\nIeskoti pagal:")
    print("1. Savininka")
    print("2. Nekilnojama turta")
    print("3. Busena")
    print("b - Atgal i pagrindini menu")

def prideti_menu():
    # Prideti funkcionaluma, kad ieskotu egzistuojancio savininho ties 1 punktu
    print("\nPrideti nauja:")
    print("1. Objekta")
    print("2. NT agentura")
    print("3. Pirkeja")
    print("b - Atgal i pagrindini menu")

def istrinti_menu():
    print("\nIstrinti:")
    print("1. Objekta")
    print("2. Savininka")
    print("3. NT agentura")
    print("4. Pirkeja")
    print("b - Atgal i pagrindini menu")

def pakeisti_menu():
    print("\nKa pakeisti:")
    # pataisyti, kad jei rasta ne viena agentura
    print("1. Is pasyvaus i aktyvu")
    print("2. Is aktyvaus i parduota")
    print("3. Is aktyvaus i pasyvu")
    print("b - Atgal i pagrindini menu")

def menu():
    while True:
        pagr_menu()
        pasirinkimas = input("Iveskite pasirinkima: ")

        if pasirinkimas == '1':
            while True:
                ieskoti_menu()
                ieskoti_pasirinkimas = input("Iveskite ieskojimo pasirinkima: ")

                if ieskoti_pasirinkimas == '1':
                    pagal_savininka()
                if ieskoti_pasirinkimas == '2':
                    pagal_objekta()
                if ieskoti_pasirinkimas == '3':
                    pagal_busena()
                if ieskoti_pasirinkimas == 'b':
                    break

        if pasirinkimas == '2':
            while True:
                prideti_menu()
                prideti_pasirinkimas = input("Iveskite ka norite prideti: ")
                if prideti_pasirinkimas == '1':
                    prideti_objekta()
                if prideti_pasirinkimas == '2':
                    prideti_nt()
                if prideti_pasirinkimas == '3':
                    prideti_pirkeja()
                if prideti_pasirinkimas == 'b':
                    break

        if pasirinkimas == '3':
            while True:
                istrinti_menu()
                istrinti_pasirinkimas = input("Iveskite ka norite istrinti: ")
                if istrinti_pasirinkimas == '1':
                    istrinti_objekta()
                if istrinti_pasirinkimas == '2':
                    istrinti_savininka()
                if istrinti_pasirinkimas == '3':
                    istrinti_agentura()
                if istrinti_pasirinkimas == '4':
                    istrinti_pirkeja()
                if istrinti_pasirinkimas == 'b':
                    break

        if pasirinkimas == '4':
            while True:
                pakeisti_menu()
                pakeisti_pasirinkimas = input("Iveskite pakeitimo pasirinkima: ")
                if pakeisti_pasirinkimas == '1':
                    pasyvus_i_aktyvu()
                if pakeisti_pasirinkimas == '2':
                    aktyvus_i_parduota()
                if pakeisti_pasirinkimas == '3':
                    aktyvus_i_pasyvu()
                if pakeisti_pasirinkimas == 'b':
                    break

        if pasirinkimas == 'q':
            break

menu()