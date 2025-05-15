from fastapi import Depends, FastAPI

from core.startup import on_startup, on_shutdown
from core.users import current_active_user
from models.user import User
from services.convert_router import convert_router

from .user_router import api_router


app = FastAPI()
app.include_router(api_router)
app.include_router(convert_router, prefix="/files", tags=["files"])


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


app.add_event_handler("startup", on_startup)
app.add_event_handler("shutdown", on_shutdown)
