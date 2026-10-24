from sqlalchemy import select

from backend.database import SessionLocal
from backend.models import Paper


with SessionLocal() as session:
    statement = select(Paper).order_by(Paper.id)
    papers = session.scalars(statement).all()

    for paper in papers:
        print(paper.id, paper.title, paper.year)