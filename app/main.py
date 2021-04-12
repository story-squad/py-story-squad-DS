from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv

from app.api import submission, visualization, clustering
from app.utils.security.header_checking import get_api_key

app = FastAPI(
    title="Story Squad DS API",
    description="A RESTful API for the Story Squad Project",
    version="0.2",
    docs_url="/"
)

load_dotenv()

app.include_router(
    submission.router,
    tags=['Submission'],
    dependencies=[Security(get_api_key)],
)
app.include_router(
    visualization.router,
    tags=['Visualization'],
    dependencies=[Security(get_api_key)],
)
app.include_router(
    clustering.router,
    tags=['Clustering'],
    dependencies=[Security(get_api_key)],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app)
