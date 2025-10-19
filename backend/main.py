from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Score
from fastapi.middleware.cors import CORSMiddleware # so it can recieve requests from html5 in my itch.io page

app = FastAPI()

origins = [
    "https://html-classic.itch.zone",
    "https://victorcg50.itch.io/myfirstgodot2dgame" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        #yield and finally ensure that it always closes the Session
        db.close()

@app.get('/')
def root():
    return {'message': 'Escape The Creeps API running!'}

@app.post('/submit_score/')
def submit_score(player_name:str, score:int, db:Session = Depends(get_db)):
    if len(player_name) > 20:
        raise HTTPException(
            status_code= 400,
            detail='Player name too long (max 20 characters)'
        )
    new_score = Score(player_name=player_name,score=score)
    db.add(new_score)
    db.commit()
    return {'status': 'success', 'player_name': player_name, 'score': score}

@app.get('/leaderboard/')
def leaderboard(limit:int = 10, db:Session = Depends(get_db)):
    scores = db.query(Score).order_by(Score.score.desc()).limit(limit).all()
    return [{'player_name': s.player_name, 'player_score': s.score} for s in scores]