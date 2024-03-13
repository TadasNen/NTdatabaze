from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'sqlite:///nt_database.db'
engine = create_engine(DATABASE_URL)

Base = declarative_base()


class Savininkas(Base):
    __tablename__ = 'savininkas'
    id = Column(Integer, primary_key=True)
    sav_vardas = Column(String, nullable=False)
    sav_tel_numeris = Column(Integer, nullable=False)
    sav_el_pastas = Column(String, nullable=False)
    sav_saskaita = Column(String, nullable=False)
    nekilnojamas_turtas = relationship('NekilnojamasTurtas', back_populates='savininkas')


class Pirkejas(Base):
    __tablename__ = 'pirkejas'
    id = Column(Integer, primary_key=True)
    pir_vardas = Column(String, nullable=False)
    pir_tel_numeris = Column(Integer, nullable=False)
    pir_el_pastas = Column(String, nullable=False)
    pir_saskaita = Column(String, nullable=False)


class Busena(Base):
    __tablename__ = 'busena'
    id = Column(Integer, primary_key=True)
    nekilnojamas_turtas_id = Column(Integer, ForeignKey('nekilnojamas_turtas.id'))
    nekilnojamas_turtas = relationship("NekilnojamasTurtas", back_populates="busena")


class NekilnojamasTurtas(Base):
    __tablename__ = 'nekilnojamas_turtas'
    id = Column(Integer, primary_key=True)
    savininkas_id = Column(Integer, ForeignKey('savininkas.id'))
    busena = relationship("Busena", back_populates="nekilnojamas_turtas")
    savininkas = relationship("Savininkas", back_populates="nekilnojamas_turtas")


class Pavedimas(Base):
    __tablename__ = 'pavedimas'
    id = Column(Integer, primary_key=True)
    busena_id = Column(Integer, ForeignKey('busena.id'), nullable=False)
    pirkejas_id = Column(Integer, ForeignKey('pirkejas.id'), nullable=False)
    data_pardavimo = Column(Date, nullable=False)
    agenturos_mokestis_eur = Column(Integer, nullable=False)
    savininko_gavimas_eur = Column(Integer, nullable=False)
    busena = relationship("Busena")


Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

result = (
    session.query(Pavedimas, Savininkas, Pirkejas, Busena, NekilnojamasTurtas)
    .join(Busena, Busena.id == Pavedimas.busena_id)
    .join(NekilnojamasTurtas, NekilnojamasTurtas.id == Busena.nekilnojamas_turtas_id)
    .join(Savininkas, Savininkas.id == NekilnojamasTurtas.savininkas_id)
    .join(Pirkejas, Pirkejas.id == Pavedimas.pirkejas_id)
    .all()
)

for pavedimas, savininkas, pirkejas, busena, nekilnojamas_turtas in result:
    print(f"Pavedimo ID: {pavedimas.id}, Savininko Vardas: {savininkas.sav_vardas}, "
          f"Pirkejo Vardas: {pirkejas.pir_vardas}, Busenos ID: {busena.id}, Data: {pavedimas.data_pardavimo}")