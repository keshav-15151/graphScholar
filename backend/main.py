from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from backend.database import get_db
from backend.models import Paper
from backend.schemas import PaperCreate, PaperResponse, PaperUpdate


app = FastAPI()


@app.get("/")
def home():
    return {"message": "GraphScholar is running!"}


@app.get("/papers", response_model=list[PaperResponse])
def get_papers(db: Session = Depends(get_db)):
    statement = select(Paper).order_by(Paper.id)
    return db.scalars(statement).all()


@app.get("/papers/{paper_id}", response_model=PaperResponse)
def get_paper(
    paper_id: int,
    db: Session = Depends(get_db),
):
    paper = db.get(Paper, paper_id)

    if paper is None:
        raise HTTPException(
            status_code=404,
            detail="Paper not found",
        )

    return paper


@app.get("/papers/year/{year}", response_model=list[PaperResponse])
def get_papers_by_year(
    year: int,
    db: Session = Depends(get_db),
):
    statement = (
        select(Paper)
        .where(Paper.year == year)
        .order_by(Paper.id)
    )
    return db.scalars(statement).all()
  
@app.post("/papers", response_model=PaperResponse, status_code=status.HTTP_201_CREATED)
def create_paper(
    paper_data: PaperCreate,
    db: Session = Depends(get_db),
):
    paper = Paper(
        title=paper_data.title,
        year=paper_data.year,
    )

    try:
        db.add(paper)
        db.commit()
        db.refresh(paper)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not save the paper",
        )

    return paper


@app.put("/papers/{paper_id}", response_model=PaperResponse)
def update_paper(
    paper_id: int,
    paper_data: PaperUpdate,
    db: Session = Depends(get_db),
):
    paper = db.get(Paper, paper_id)

    if paper is None:
        raise HTTPException(
            status_code=404,
            detail="Paper not found",
        )

    paper.title = paper_data.title
    paper.year = paper_data.year

    try:
        db.commit()
        db.refresh(paper)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not update the paper",
        )

    return paper


@app.delete("/papers/{paper_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_paper(
    paper_id: int,
    db: Session = Depends(get_db),
):
    paper = db.get(Paper, paper_id)

    if paper is None:
        raise HTTPException(
            status_code=404,
            detail="Paper not found",
        )

    try:
        db.delete(paper)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not delete the paper",
        )