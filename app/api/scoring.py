from fastapi import APIRouter
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from app.utils.complexity.squad_score import squad_score, scaler
from app.api.models import ScoringRequest

# global variables and services
router = APIRouter()
load_dotenv()


@router.post("/scoring/text")
async def submission_text(body: ScoringRequest):
    """
    Takes a pre-transcribed text string, then passes the transcription to the 
    SquadScore method.
    """
    # score the transcription using SquadScore algorithm
    score = await squad_score(body.transcription, scaler)

    # return the complexity score
    return JSONResponse(
        status_code=200,
        content={
            "complexity": score,
        },
    )
