from fastapi import FastAPI
import uvicorn
from fastapi.responses import RedirectResponse
from config.environment import Settings
from mail_core.adapter.inbound.api.routers import (
    create_mail,
    get_expire,
    refill,
    delete_mail,
    create_quota,
    update_quota,
    get_quota,
    get_emails,
    deactivate_email,
    activate_email,
    get_email
)

app = FastAPI(title="Mail Core Service")

app.include_router(get_email.router, prefix="/api/v1")
app.include_router(get_emails.router, prefix="/api/v1")
app.include_router(create_mail.router, prefix="/api/v1")
app.include_router(get_expire.router, prefix="/api/v1")
app.include_router(refill.router, prefix="/api/v1")
app.include_router(delete_mail.router, prefix="/api/v1")

app.include_router(create_quota.router, prefix="/api/v1")
app.include_router(update_quota.router, prefix="/api/v1")
app.include_router(get_quota.router, prefix="/api/v1")

app.include_router(deactivate_email.router, prefix="/api/v1")
app.include_router(activate_email.router, prefix="/api/v1")


@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=Settings.API_HOST,
        port=Settings.API_PORT,
        reload=True,
        debug=True,
    )
