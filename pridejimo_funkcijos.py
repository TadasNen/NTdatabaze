import sqlite3
import datetime

def id_pridejimas(lentele, cursor):
    cursor.execute(f'SELECT MAX(id) FROM {lentele}')
    max_id = cursor.fetchone()[0]
    return max_id + 1 if max_id is not None else 1

def prideti_objekta():
    conn = sqlite3.connect('nt_database.db')
    cursor = conn.cursor()

    try:
        print("Informacija apie savininka")
        savininkas_vardas = input("Vardas ir pavarde: ")
        savininkas_tel_numeris = input("Telefono numeris: ")
        savininkas_el_pastas = input("El. pastas: ")
        savininkas_saskaita = input("Banko saskaita: ")
        savininkas_id = id_pridejimas('savininkas', cursor)

        cursor.execute('''
            INSERT INTO savininkas (id, sav_vardas, sav_tel_numeris, sav_el_pastas, sav_saskaita)
            VALUES (?, ?, ?, ?, ?)
        ''', (savininkas_id, savininkas_vardas, savininkas_tel_numeris, savininkas_el_pastas, savininkas_saskaita))

        print("\nInformacija apie nekilnojama turta")
        nekilinojamas_turtas_tipas = input("Nekilnojamo turto tipas\n"
                                           "1 - Gyvenamoji patalpa\n"
                                           "2 - Garažas\n"
                                           "3 - Pramonine patalpa\n"
                                           "4 - Ofisas\n"
                                           "Jusu pasirinkimas: ")
        nekilnojamas_turtas_adresas = input("Adresas: ")
        nekilnojamas_turtas_miestas = input("Miestas: ")
        nekilnojamas_turtas_plotas_kvm = input("Plotas, kvm: ")
        nekilnojamas_turtas_reg_numeris = input("Unikalus numeris: ")
        nekilnojamas_turtas_id = id_pridejimas('nekilnojamas_turtas', cursor)

        cursor.execute('''
            INSERT INTO nekilnojamas_turtas (id, savininkas_id, nt_tipas_id, adresas, miestas, plotas_kvm, reg_numeris)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nekilnojamas_turtas_id, savininkas_id, nekilinojamas_turtas_tipas,nekilnojamas_turtas_adresas,
              nekilnojamas_turtas_miestas, nekilnojamas_turtas_plotas_kvm, nekilnojamas_turtas_reg_numeris))

        nekilnojamas_turtas_id = cursor.lastrowid

        busena_tipas = '2'
        busena_data_pridejimo = datetime.date.today()
        busena_id = id_pridejimas('busena', cursor)

        cursor.execute('''
            INSERT INTO busena (id, nekilnojamas_turtas_id, busena_tipas_id, data_pridejimo)
            VALUES (?, ?, ?, ?)
        ''', (busena_id, nekilnojamas_turtas_id, busena_tipas, busena_data_pridejimo))

        conn.commit()

        print("Nauja informacija issaugota duomenu bazeje.")

    except Exception as error:
        print(f"Klaida: {error}")
        conn.rollback()

    finally:
        conn.close()

def prideti_nt():
    conn = sqlite3.connect('nt_database.db')
    cursor = conn.cursor()

    try:
        print("Informacija apie Nekilnojamo Turto agentura")
        pavadinimas = input("Pavadinimas: ")
        imones_kodas = input("Imones kodas: ")
        tel_numeris = input("Telefono numeris: ")
        el_pastas = input("El. pastas: ")
        nt_id = id_pridejimas('nt_agentura', cursor)

        cursor.execute('''
            INSERT INTO nt_agentura (id, pavadinimas, imones_kodas, tel_numeris, el_pastas)
            VALUES (?, ?, ?, ?, ?)
        ''', (nt_id, pavadinimas, imones_kodas, tel_numeris, el_pastas))

        print("\nInformacija apie NT mokescius")
        mokescio_id_pardavimas = id_pridejimas('agenturos_mokestis', cursor)
        id_pardavimas = 1
        pardavimo_procentas = input("Objekto pardavimo mokestis, %: ")
        pardavimo_min = input("Minimali pardavimo mokescio suma, EUR: ")
        pardavimo_max = input("Maksimali pardavimo mokescio suma, EUR: ")

        cursor.execute('''
            INSERT INTO agenturos_mokestis (id, nt_agentura_id, pardavimo_tipas_id, procentas, min_mokestis, max_mokestis)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (mokescio_id_pardavimas, nt_id, id_pardavimas, pardavimo_procentas, pardavimo_min, pardavimo_max))

        mokescio_id_nuoma = mokescio_id_pardavimas + 1
        id_nuoma = 2
        nuomos_procentas = input("Objekto nuomos mokestis, %: ")
        nuomos_min = input("Minimali nuomos mokescio suma, EUR: ")
        nuomos_max = input("Maksimali nuomos mokescio suma, EUR: ")

        cursor.execute('''
            INSERT INTO agenturos_mokestis (id, nt_agentura_id, pardavimo_tipas_id, procentas, min_mokestis, max_mokestis)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (mokescio_id_nuoma, nt_id, id_nuoma, nuomos_procentas,nuomos_min, nuomos_max))

        conn.commit()

        print("Nauja informacija issaugota duomenu bazeje.")

    except Exception as error:
        print(f"Klaida: {error}")
        conn.rollback()

    finally:
        conn.close()

def prideti_pirkeja():
    conn = sqlite3.connect('nt_database.db')
    cursor = conn.cursor()

    try:
        print("Informacija apie pirkeja")
        id = id_pridejimas('pirkejas', cursor)
        vardas = input("Pilnas vardas: ")
        tel_nr = input("Telefono numeris: ")
        el_pastas = input("Elektroninis pastas: ")
        saskaita = input("Banko saskaita: ")

        cursor.execute('''
            INSERT INTO pirkejas (id, pir_vardas, pir_tel_numeris, pir_el_pastas, pir_saskaita)
            VALUES (?, ?, ?, ?, ?)
        ''', (id, vardas, tel_nr, el_pastas, saskaita))

        conn.commit()

        print("Nauja informacija issaugota duomenu bazeje.")

    except Exception as error:
        print(f"Klaida: {error}")
        conn.rollback()

    finally:
        conn.close()