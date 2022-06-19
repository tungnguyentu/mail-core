from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from mail_core.adapter.inbound.api.routers import (
    create_mail,
    get_expire,
    refill,
)

app = FastAPI()

app.include_router(create_mail.router, prefix="/api/v1")
app.include_router(get_expire.router, prefix="/api/v1")
app.include_router(refill.router, prefix="/api/v1")


@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")
