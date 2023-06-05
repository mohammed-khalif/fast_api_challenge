from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel



# Create the FastAPI instance
app = FastAPI()


# Create the database connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./my_database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Define the database model
class MyData(Base):
    __tablename__ = "mydata"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)


# Create the database tables
Base.metadata.create_all(bind=engine)


# Pydantic model for POST and PUT requests
class MyDataCreateUpdate(BaseModel):
    name: str
    description: str


# Pydantic model for GET responses
class MyDataResponse(BaseModel):
    id: int
    name: str
    description: str


# Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET all data
@app.get("/get_all_endpoint/")
def get_all_data(db: Session = Depends(get_db)):
    data = db.query(MyData).all()
    return data


# GET single data
@app.get("/get_one_endpoint/{id}")
def get_single_data(id: int, db: Session = Depends(get_db)):
    data = db.query(MyData).filter(MyData.id == id).first()
    if data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    return data


# POST new data
@app.post("/post_endpoint/")
def create_data(item: MyDataCreateUpdate, db: Session = Depends(get_db)):
    data = MyData(name=item.name, description=item.description)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


# PUT full update of data
@app.put("/put_endpoint/{id}")
def update_data(id: int, item: MyDataCreateUpdate, db: Session = Depends(get_db)):
    data = db.query(MyData).filter(MyData.id == id).first()
    if data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    data.name = item.name
    data.description = item.description
    db.commit()
    db.refresh(data)
    return data


# PATCH partial update of data
@app.patch("/patch_endpoint/{id}")
def partial_update_data(id: int, item: MyDataCreateUpdate, db: Session = Depends(get_db)):
    data = db.query(MyData).filter(MyData.id == id).first()
    if data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    if item.name:
        data.name = item.name
    if item.description:
        data.description = item.description
    db.commit()
    db.refresh(data)
    return data


# DELETE a piece of data
@app.delete("/delete_endpoint/{id}")
def delete_data(id: int, db: Session = Depends(get_db)):
    data = db.query(MyData).filter(MyData.id == id).first()
    if data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    db.delete(data)
    db.commit()
    return {"message": "Data deleted"}