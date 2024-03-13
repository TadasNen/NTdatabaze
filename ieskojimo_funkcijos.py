import sqlite3

def pagal_savininka():
    con = sqlite3.connect('nt_database.db')
    cursor = con.cursor()

    paieska = input("Iveskite pilna arba dali vardo: ")

    query = '''
    SELECT savininkas.sav_vardas, savininkas.sav_tel_numeris, savininkas.sav_el_pastas, nekilnojamas_turtas.adresas, 
    nekilnojamas_turtas.miestas, nekilnojamas_turtas.plotas_kvm, nekilnojamas_turtas.reg_numeris
    FROM savininkas
    JOIN nekilnojamas_turtas ON savininkas.id = nekilnojamas_turtas.savininkas_id
    WHERE sav_vardas LIKE ?
    '''

    cursor.execute(query, ('%' + paieska + '%',))

    res = cursor.fetchall()
    if res:
        print("\nPaieskos rezulatai:")
        for el in res:
            print(el)
    else:
        print("Jokiu rezultatu nerasta.")

    con.close()

def pagal_objekta():
    con = sqlite3.connect('nt_database.db')
    cursor = con.cursor()

    paieska = input("Iveskite pilna arba dali adreso, miesto ar unikalaus numerio: ")

    query = '''
    SELECT savininkas.sav_vardas, savininkas.sav_tel_numeris, savininkas.sav_el_pastas,
           nekilnojamas_turtas.adresas, nekilnojamas_turtas.miestas,
           nekilnojamas_turtas.plotas_kvm, nekilnojamas_turtas.reg_numeris
    FROM savininkas
    JOIN nekilnojamas_turtas ON savininkas.id = nekilnojamas_turtas.savininkas_id
    WHERE nekilnojamas_turtas.adresas LIKE ? OR
          nekilnojamas_turtas.miestas LIKE ? OR
          nekilnojamas_turtas.reg_numeris LIKE ?
    '''

    cursor.execute(query, (f'%{paieska}%', f'%{paieska}%', f'%{paieska}%'))

    res = cursor.fetchall()
    if res:
        print("\nPaieskos rezulatai:")
        for el in res:
            print(el)
    else:
        print("Jokiu rezultatu nerasta.")

    con.close()

def pagal_busena():
    con = sqlite3.connect('nt_database.db')
    cursor = con.cursor()

    paieska = input("Iveskite 1 - Aktyvus, 2 - Pasyvus, 3 - Parduota: ")

    query = f'''
    SELECT savininkas.sav_vardas, savininkas.sav_tel_numeris, savininkas.sav_el_pastas,
           nekilnojamas_turtas.adresas, nekilnojamas_turtas.miestas,
           nekilnojamas_turtas.plotas_kvm, nekilnojamas_turtas.reg_numeris, busena_tipas.tipas
    from busena
    JOIN nekilnojamas_turtas ON busena.nekilnojamas_turtas_id = nekilnojamas_turtas.id
    JOIN busena_tipas ON busena.busena_tipas_id = busena_tipas.id
    JOIN savininkas on nekilnojamas_turtas.savininkas_id = savininkas.id
    WHERE busena.busena_tipas_id = {paieska}
    '''

    cursor.execute(query)

    res = cursor.fetchall()
    if res:
        print("\nPaieskos rezulatai:")
        for el in res:
            print(el)
    else:
        print("Jokiu rezultatu nerasta.")

    con.close()
