import sqlite3

def istrinti_objekta():
    conn = sqlite3.connect('nt_database.db')
    cursor = conn.cursor()

    try:
        reg_numeris = input("Iveskite objekto unikalu numeri: ")

        cursor.execute('''
            SELECT id
            FROM nekilnojamas_turtas
            WHERE reg_numeris LIKE ?
        ''', (f'%{reg_numeris}%',))

        rasta_eilute = cursor.fetchall()

        if len(rasta_eilute) == 1:
            cursor.execute('''
                DELETE FROM busena
                WHERE nekilnojamas_turtas_id IN 
                (
                SELECT id
                FROM nekilnojamas_turtas
                WHERE reg_numeris LIKE ?
                )
                    ''', (f'%{reg_numeris}%',))

            cursor.execute('''
                DELETE FROM nekilnojamas_turtas
                WHERE reg_numeris LIKE ?
                ''', (f'%{reg_numeris}%',))

            conn.commit()

            print(f"Objektas su unikaliu numeriu {reg_numeris} buvo istrintas.")
        elif len(rasta_eilute) > 1:
            print(f"Rasta keleta objektu pagal {reg_numeris} paieska. Irasykite tikslesni unikalu numeri.")
        else:
            print(f"Nerasta jokiu objektu su unikaliu numeriu {reg_numeris}.")

    except Exception as e:
        print(f"Klaida: {e}")
        conn.rollback()

    finally:
        conn.close()

def istrinti_savininka():
    conn = sqlite3.connect('nt_database.db')
    cursor = conn.cursor()

    try:
        savininkas_vardas = input("Iveskite savininko varda: ")

        cursor.execute('''
            SELECT id
            FROM savininkas
            WHERE sav_vardas LIKE ?
        ''', (f'%{savininkas_vardas}%',))

        rastos_eilutes = cursor.fetchall()

        if len(rastos_eilutes) == 1:
            savininkas_id = rastos_eilutes[0][0]

            cursor.execute('''
                DELETE FROM busena
                WHERE nekilnojamas_turtas_id IN 
                (
                    SELECT id
                    FROM nekilnojamas_turtas
                    WHERE savininkas_id = ?
                )
            ''', (savininkas_id,))
            cursor.execute('''
                DELETE FROM nekilnojamas_turtas
                WHERE savininkas_id = ?
            ''', (savininkas_id,))
            cursor.execute('''
                DELETE FROM savininkas
                WHERE id = ?
            ''', (savininkas_id,))

            conn.commit()

            print(f"Savininkas {savininkas_vardas} ir susijusi informacija buvo istrinta.")
        elif len(rastos_eilutes) > 1:
            print(f"Rasta keleta savininku pagal {savininkas_vardas} paieska. Irasykite tikslesni varda.")
        else:
            print(f"Nerasta jokio savininko su vardu {savininkas_vardas}.")

    except Exception as e:
        print(f"Klaida: {e}")
        conn.rollback()

    finally:
        conn.close()

def istrinti_agentura():
    conn = sqlite3.connect('nt_database.db')
    cursor = conn.cursor()

    try:
        agentura = input("Iveskite agenturos pavadinima: ")

        cursor.execute('''
            SELECT id
            FROM nt_agentura
            WHERE pavadinimas LIKE ?
        ''', (f'%{agentura}%',))

        rastos_eilutes = cursor.fetchall()

        if len(rastos_eilutes) == 1:
            agentura_id = rastos_eilutes[0][0]

            cursor.execute('''
                DELETE FROM agenturos_mokestis
                WHERE nt_agentura_id = ?
            ''', (agentura_id,))
            cursor.execute('''
                DELETE FROM nt_agentura
                WHERE id = ?
            ''', (agentura_id,))

            conn.commit()

            print(f"Agentura {agentura} ir susijusi informacija buvo istrinta.")
        elif len(rastos_eilutes) > 1:
            print(f"Rasta keleta agenturu pagal {agentura} paieska. Irasykite tikslesni pavadinima.")
        else:
            print(f"Nerasta jokio agenturos su pavadinimu {agentura}.")

    except Exception as e:
        print(f"Klaida: {e}")
        conn.rollback()

    finally:
        conn.close()

def istrinti_pirkeja():
    conn = sqlite3.connect('nt_database.db')
    cursor = conn.cursor()

    try:
        pirkejas = input("Iveskite pirkejo varda: ")

        cursor.execute('''
            SELECT id
            FROM pirkejas
            WHERE pir_vardas LIKE ?
        ''', (f'%{pirkejas}%',))

        rastos_eilutes = cursor.fetchall()

        if len(rastos_eilutes) == 1:
            pirkejas_id = rastos_eilutes[0][0]

            cursor.execute('''
                DELETE FROM pirkejas
                WHERE id = ?
            ''', (pirkejas_id,))

            conn.commit()

            print(f"Pirkejas {pirkejas} ir susijusi informacija buvo istrinta.")
        elif len(rastos_eilutes) > 1:
            print(f"Rasta keleta pirkeju pagal {pirkejas} paieska. Irasykite tikslesni varda.")
        else:
            print(f"Nerasta jokio pirkejo su vardu {pirkejas}.")

    except Exception as e:
        print(f"Klaida: {e}")
        conn.rollback()

    finally:
        conn.close()