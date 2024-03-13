import sqlite3
import pandas as pd

con = sqlite3.connect('nt_database.db')
cursor = con.cursor()

sql_script = """
CREATE TABLE IF NOT EXISTS savininkas(
  id INTEGER NOT NULL,
  sav_vardas TEXT NOT NULL,
  sav_tel_numeris INTEGER NOT NULL,
  sav_el_pastas TEXT NOT NULL,
  sav_saskaita TEXT NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS busena(
  id INTEGER NOT NULL,
  nekilnojamas_turtas_id INTEGER NOT NULL,
  nt_agentura_id INTEGER NOT NULL,
  pardavimo_tipas_id INTEGER NOT NULL,
  busena_tipas_id INTEGER NOT NULL,
  data_pridejimo DATE NOT NULL,
  kaina_eur INTEGER,
  PRIMARY KEY(id),
  CONSTRAINT nt_agentura_busena
    FOREIGN KEY (nt_agentura_id) REFERENCES nt_agentura (id),
  CONSTRAINT nekilnojamas_turtas_busena
    FOREIGN KEY (nekilnojamas_turtas_id) REFERENCES nekilnojamas_turtas (id),
  CONSTRAINT pardavimo_tipas_busena
    FOREIGN KEY (pardavimo_tipas_id) REFERENCES pardavimo_tipas (id),
  CONSTRAINT busena_tipas_busena
    FOREIGN KEY (busena_tipas_id) REFERENCES busena_tipas (id)
);

CREATE TABLE IF NOT EXISTS nt_agentura(
  id INTEGER NOT NULL,
  pavadinimas TEXT NOT NULL,
  imones_kodas INTEGER NOT NULL UNIQUE,
  tel_numeris INTEGER,
  el_pastas TEXT,
  PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS nekilnojamas_turtas(
  id INTEGER NOT NULL,
  savininkas_id INTEGER NOT NULL,
  nt_tipas_id INTEGER NOT NULL,
  adresas TEXT NOT NULL,
  plotas_kvm INTEGER NOT NULL,
  reg_numeris TEXT NOT NULL UNIQUE,
  PRIMARY KEY(id),
  CONSTRAINT savininkas_nekilnojamas_turtas
    FOREIGN KEY (savininkas_id) REFERENCES savininkas (id),
  CONSTRAINT nt_tipas_nekilnojamas_turtas
    FOREIGN KEY (nt_tipas_id) REFERENCES nt_tipas (id)
);

CREATE TABLE IF NOT EXISTS agenturos_mokestis(
  id INTEGER NOT NULL,
  nt_agentura_id INTEGER NOT NULL,
  pardavimo_tipas_id INTEGER NOT NULL,
  procentas INTEGER,
  min_mokestis INTEGER,
  max_mokestis INTEGER,
  PRIMARY KEY(id),
  CONSTRAINT nt_agentura_agenturos_mokestis
    FOREIGN KEY (nt_agentura_id) REFERENCES nt_agentura (id),
  CONSTRAINT mokscio_tipas_agenturos_mokestis
    FOREIGN KEY (pardavimo_tipas_id) REFERENCES pardavimo_tipas (id)
);

CREATE TABLE IF NOT EXISTS pirkejas(
  id INTEGER NOT NULL,
  pir_vardas TEXT NOT NULL,
  pir_tel_numeris INTEGER NOT NULL,
  pir_el_pastas TEXT NOT NULL,
  pir_saskaita TEXT NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS pardavimo_tipas(id INTEGER NOT NULL, tipas TEXT, PRIMARY KEY(id));

CREATE TABLE IF NOT EXISTS pavedimas(
  id INTEGER NOT NULL,
  busena_id INTEGER NOT NULL,
  pirkejas_id INTEGER NOT NULL,
  data_pardavimo DATE NOT NULL,
  agenturos_mokestis_eur INTEGER,
  savininko_gavimas_eur INTEGER,
  PRIMARY KEY(id),
  CONSTRAINT pirkejas_pavedimas FOREIGN KEY (pirkejas_id) REFERENCES pirkejas (id),
  CONSTRAINT busena_pavedimas FOREIGN KEY (busena_id) REFERENCES busena (id)
);

CREATE TABLE IF NOT EXISTS nt_tipas(id INTEGER NOT NULL, tipas TEXT NOT NULL, PRIMARY KEY(id))
  ;

CREATE TABLE IF NOT EXISTS busena_tipas
  (id INTEGER NOT NULL, tipas TEXT NOT NULL, PRIMARY KEY(id));
"""

cursor.executescript(sql_script)

df1 = pd.read_excel('pirkejas.xlsx')
df1.to_sql('pirkejas', con, if_exists='replace', index=False)

df2 = pd.read_excel('savininkas.xlsx')
df2.to_sql('savininkas', con, if_exists='replace', index=False)

df3 = pd.read_excel('nekilnojamas_turtas.xlsx')
df3.to_sql('nekilnojamas_turtas', con, if_exists='replace', index=False)

df4 = pd.read_excel('nt_tipas.xlsx')
df4.to_sql('nt_tipas', con, if_exists='replace', index=False)

df5 = pd.read_excel('nt_agentura.xlsx')
df5.to_sql('nt_agentura', con, if_exists='replace', index=False)

df6 = pd.read_excel('agenturos_mokestis.xlsx')
df6.to_sql('agenturos_mokestis', con, if_exists='replace', index=False)

df7 = pd.read_excel('pardavimo_tipas.xlsx')
df7.to_sql('pardavimo_tipas', con, if_exists='replace', index=False)

df8 = pd.read_excel('pavedimas.xlsx')
df8.to_sql('pavedimas', con, if_exists='replace', index=False)

df9 = pd.read_excel('busena.xlsx')
df9.to_sql('busena', con, if_exists='replace', index=False)

df10 = pd.read_excel('busena_tipas.xlsx')
df10.to_sql('busena_tipas', con, if_exists='replace', index=False)

con.commit()
con.close()
