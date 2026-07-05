from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.schemas.chat_management import CreateChatRequest, RenameChatRequest
from backend.app.services.chat_service import ChatService
from backend.app.services.chat_management_service import ChatManagementService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

chat_service = ChatService()
manager = ChatManagementService()


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        return chat_service.generate_reply(
            chat_id=request.chat_id,
            user_id=request.user_id,
            question=request.question,
            provider=request.provider,
            model=request.model,
            source_id=request.source_id,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/stream")
def chat_stream(request: ChatRequest):
    def stream_generator():
        try:
            yield "data: Searching selected knowledge source...\n\n"

            for token in chat_service.generate_reply_stream(
                chat_id=request.chat_id,
                user_id=request.user_id,
                question=request.question,
                provider=request.provider,
                model=request.model,
                source_id=request.source_id,
            ):
                safe_token = token.replace("\n", "\\n")
                yield f"data: {safe_token}\n\n"

            yield "data: [DONE]\n\n"

        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_generator(),
        media_type="text/event-stream",
    )


@router.post("/create")
def create_chat(request: CreateChatRequest):
    return manager.create_chat(request.user_id)


@router.get("/list/{user_id}")
def list_chats(user_id: int):
    return manager.get_chats(user_id)


@router.get("/history/{chat_id}")
def history(chat_id: int):
    return manager.get_history(chat_id)


@router.put("/rename/{chat_id}")
def rename(chat_id: int, request: RenameChatRequest):
    return manager.rename_chat(chat_id, request.title)


@router.delete("/delete/{chat_id}")
def delete(chat_id: int):
    return manager.delete_chat(chat_id)