from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..core.config import settings


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    # Placeholder deterministic reply. Wire to OpenAI if key is provided.
    if settings.openai_api_key:
        try:
            # Lazy import to avoid dependency unless configured
            import openai  # type: ignore
            openai.api_key = settings.openai_api_key
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": req.message}],
            )
            text = completion.choices[0].message["content"].strip()
            return ChatResponse(reply=text)
        except Exception as exc:  # pragma: no cover - best effort
            raise HTTPException(status_code=500, detail=str(exc))

    return ChatResponse(reply=f"You said: {req.message}")


