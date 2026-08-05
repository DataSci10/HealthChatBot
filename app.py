import logging

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from config import settings
from langchain_openai import OpenAIEmbeddings

from rag_retriever.retriever import build_retriever
from rag.rag_chain import build_chain
from cache.redis_cache import get_cached_answer, cache_answer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Healthcare Chatbot")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


logger.info("Loading retriever...")

embedding_model = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)

retriever = build_retriever(embedding_model)

chain = build_chain(retriever)

logger.info("Healthcare chatbot is ready.")


class ChatRequest(BaseModel):
    question: str


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


@app.post("/chat")
async def chat(req: ChatRequest):

    logger.info(
        "Received chat request (question length: %d)",
        len(req.question)
    )

    cached = get_cached_answer(req.question)

    if cached:
        logger.info("Redis Cache HIT")
        return {
            "answer": cached,
            "cache": True
        }

    logger.info("Redis Cache MISS")

    try:

        logger.info("Invoking RAG pipeline")

        response = chain.invoke(req.question)

        cache_answer(
            req.question,
            str(response)
        )

        logger.info("Response cached successfully")

        return {
            "answer": str(response.content),
            "cache": False
        }

    except Exception as e:
        logger.exception(f"Error while processing chat request: {e}")
        raise