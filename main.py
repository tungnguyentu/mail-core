from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from mail_core.adapter.inbound.api.routers import mail

app = FastAPI()

app.include_router(mail.router, prefix="/api/v1")


@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")
