from typing import Optional

from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Sequence(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    seq: int  = Field(default=None, primary_key=False)
    name: str = Field(index=True)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    try :
        SequenceRecord = Sequence(id=1, seq= 1, name="Sequence Record")
        session = Session(engine)
        session.add(SequenceRecord)
        session.commit()
    except:
        pass


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/sequence/increment")
def increment(seqNumbersRequired : int = 1):
    with Session(engine) as session:
        results = session.exec(select(Sequence)).first()
        print('#############')
        response = { "sequenceNumbers" : [], "sequnceLength" : seqNumbersRequired }
        response['sequenceNumbers'].extend([results.seq + x for x in range(0,seqNumbersRequired)])
        print(response)
        print('#############')        
        results.seq = results.seq + seqNumbersRequired
        session.add(results)
        session.commit()
        return response


@app.get("/sequence/no-increment")
def no_increment():
    with Session(engine) as session:
        response = session.exec(select(Sequence)).all()
        return response
    
