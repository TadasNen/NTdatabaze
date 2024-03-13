import sqlite3
from datetime import date

def pasyvus_i_aktyvu():
    conn = sqlite3.connect('nt_database.db')
    cursor = conn.cursor()

    try:
        reg_numeris = input("Iveskite objekto unikalu numeri: ")

        cursor.execute('''
            SELECT id
            FROM nekilnojamas_turtas
            WHERE reg_numeris LIKE ?
        ''', (f'%{reg_numeris}%',))

        rastos_eilutes = cursor.fetchall()

        if len(rastos_eilutes) == 1:
            nekilnojamas_turtas_id = rastos_eilutes[0][0]
            cursor.execute('''
                UPDATE busena
                SET busena_tipas_id = 1
                WHERE nekilnojamas_turtas_id = ?
            ''', (nekilnojamas_turtas_id,))

            nt_agentura = input("Iveskite agenturos pavadinima: ")

            cursor.execute('''
                SELECT id
                FROM nt_agentura
                WHERE pavadinimas LIKE ?
            ''', (f'%{nt_agentura}%',))

            rastos_eilutes_agentura = cursor.fetchone()

            if rastos_eilutes_agentura:
                nt_agentura_id = rastos_eilutes_agentura[0]

                pardavimo_tipas_input = input("Iveskite pardavimo tipa (1 - pardavimas, 2 - nuoma): ")
                if pardavimo_tipas_input in ['1', '2']:
                    pardavimo_tipas_id = int(pardavimo_tipas_input)

                    kaina_eur_input = input("Iveskite kaina EUR: ")
                    kaina_eur = int(kaina_eur_input)

                    cursor.execute('''
                        UPDATE busena
                        SET nt_agentura_id = ?, pardavimo_tipas_id = ?, kaina_eur = ?
                        WHERE nekilnojamas_turtas_id = ?
                    ''', (nt_agentura_id, pardavimo_tipas_id, kaina_eur, nekilnojamas_turtas_id))

                    conn.commit()
                    print("Informacija atnaujinta.")
                else:
                    print("Neteisingai ivestas pardavimo tipo ID.")
            else:
                print("Nerasta nt_agentura pagal ivesta pavadinima.")
        elif len(rastos_eilutes) > 1:
            print(f"Rasta keleta objektu pagal {reg_numeris} paieska. Irasykite tikslesni unikalu numeri.")
        else:
            print(f"Nerasta jokio objekto su unikalu numeriu {reg_numeris}.")

    except Exception as e:
        print(f"Klaida: {e}")
        conn.rollback()

    finally:
        conn.close()

def aktyvus_i_pasyvu():
    conn = sqlite3.connect('nt_database.db')
    cursor = conn.cursor()

    try:
        reg_numeris = input("Iveskite unikalu numeri: ")

        cursor.execute('''
            SELECT nekilnojamas_turtas.id, busena.busena_tipas_id
            FROM nekilnojamas_turtas
            JOIN busena ON nekilnojamas_turtas.id = busena.nekilnojamas_turtas_id
            WHERE reg_numeris LIKE ?
        ''', (f'%{reg_numeris}%',))

        rastos_eilutes = cursor.fetchall()

        if len(rastos_eilutes) == 1:
            nekilnojamas_turtas_id, busena_tipas_id = rastos_eilutes[0]

            if busena_tipas_id == 1:
                cursor.execute('''
                    UPDATE busena
                    SET busena_tipas_id = 2,
                        nt_agentura_id = NULL,
                        pardavimo_tipas_id = NULL,
                        kaina_eur = NULL
                    WHERE nekilnojamas_turtas_id = ?
                ''', (nekilnojamas_turtas_id,))

                conn.commit()
                print("Informacija atnaujinta.")
            else:
                print("Objektas nera aktyvus.")
        elif len(rastos_eilutes) > 1:
            print(f"Rasta keleta objektu pagal {reg_numeris} paieska. Irasykite tikslesni unikalu numeri.")
        else:
            print(f"Nerasta jokio objekto su unikalu numeriu {reg_numeris}.")

    except Exception as e:
        print(f"Klaida: {e}")
        conn.rollback()

    finally:
        conn.close()

def aktyvus_i_parduota():
    conn = sqlite3.connect('nt_database.db')
    cursor = conn.cursor()

    try:
        reg_numeris = input("Iveskite unikalu objekto numeri: ")

        cursor.execute('''
            SELECT nekilnojamas_turtas.id nt_id, busena_tipas_id, kaina_eur, nt_agentura_id
            FROM nekilnojamas_turtas
            JOIN busena ON nekilnojamas_turtas.id = busena.nekilnojamas_turtas_id
            WHERE reg_numeris LIKE ?
        ''', (f'%{reg_numeris}%',))

        rastos_eilutes = cursor.fetchall()

        if len(rastos_eilutes) == 1:
            nt_id, busena_tipas_id, kaina_eur, nt_agentura_id = rastos_eilutes[0]

            if busena_tipas_id == 1:
                cursor.execute('''
                    UPDATE busena
                    SET busena_tipas_id = 3
                    WHERE nekilnojamas_turtas_id = ?
                ''', (nt_id,))

                pir_vardas = input("Iveskite pirkejo varda: ")

                cursor.execute('''
                    SELECT id
                    FROM pirkejas
                    WHERE pir_vardas LIKE ?
                ''', (f'%{pir_vardas}%',))

                rastos_eilutes_pirkejas = cursor.fetchall()

                if len(rastos_eilutes_pirkejas) == 1:
                    pirkejas_id = rastos_eilutes_pirkejas[0][0]

                    cursor.execute('SELECT MAX(id) FROM pavedimas')
                    max_id = cursor.fetchone()[0]
                    naujas_id = max_id + 1 if max_id is not None else 1
                    busena_id = nt_id
                    today_date = date.today().strftime('%Y-%m-%d')
                    cursor.execute('''
                        SELECT procentas, min_mokestis, max_mokestis
                        FROM agenturos_mokestis
                        WHERE nt_agentura_id = ? AND pardavimo_tipas_id = ?
                    ''', (nt_agentura_id, busena_tipas_id))

                    agenturos_mokestis_info = cursor.fetchone()

                    if agenturos_mokestis_info:
                        procentas, min_mokestis, max_mokestis = agenturos_mokestis_info

                        agenturos_mokestis_eur = kaina_eur * procentas / 100
                        if agenturos_mokestis_eur > max_mokestis:
                            agenturos_mokestis_eur = max_mokestis
                        elif agenturos_mokestis_eur < min_mokestis:
                            agenturos_mokestis_eur = min_mokestis

                        savininko_gavimas = kaina_eur - agenturos_mokestis_eur

                        cursor.execute('''
                            INSERT INTO pavedimas (id, busena_id, pirkejas_id, data_pardavimo, agenturos_mokestis_eur, 
                            savininko_gavimas_eur)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (naujas_id, busena_id, pirkejas_id, today_date, agenturos_mokestis_eur, savininko_gavimas))

                        conn.commit()
                        print("Pavedimas pridetas.")
                    else:
                        print("Nerasta informacijos apie agenturos mokesti.")
                elif len(rastos_eilutes_pirkejas) > 1:
                    print("Rasta keleta pirkeju pagal paieska. Irasykite tikslesni varda.")
                else:
                    print(f"Nerasta jokio pirkejo su vardu {pir_vardas}.")
            else:
                print("Objektas nera aktyvus.")
        else:
            print(f"Nerasta jokio objekto su unikalu numeriu {reg_numeris}.")
    except Exception as e:
        print(f"Klaida: {e}")
        conn.rollback()
    finally:
        conn.close()