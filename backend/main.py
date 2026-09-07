from fastapi import FastAPI

app = FastAPI()

papers = [
    {
        "id": 1,
        "title": "Attention Is All You Need",
        "year": 2017,
        "authors": ["Vaswani", "Shazeer", "Parmar"]
    },
    {
        "id": 2,
        "title": "BERT: Pre-training of Deep Bidirectional Transformers",
        "year": 2018,
        "authors": ["Devlin", "Chang", "Lee"]
    }
]


@app.get("/")
def home():
    return {"message": "GraphScholar is running!"}


@app.get("/papers")
def get_papers():
    return papers

@app.get("/papers/{paper_id}")
def get_paper(paper_id: int):
    for paper in papers:
        if paper["id"] == paper_id:
            return paper

    return {"error": "Paper not found"}

@app.get("/papers/year/{year}")
def get_papers_by_year(year: int):
    return [paper for paper in papers if paper["year"] == year]
    return {"error": "Paper not found"}