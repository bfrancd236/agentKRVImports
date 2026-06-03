from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from agent import run_agent
from whatsapp import send_message

app = FastAPI(title="KRV Imports — Agente de Vendas WhatsApp")


@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()

    if body.get("event") != "messages.upsert":
        return JSONResponse({"status": "ignored"})

    data = body.get("data", {})
    key = data.get("key", {})

    if key.get("fromMe", False):
        return JSONResponse({"status": "ignored"})

    remote_jid: str = key.get("remoteJid", "")
    message = data.get("message", {})
    text = (
        message.get("conversation")
        or (message.get("extendedTextMessage") or {}).get("text")
    )

    if not text or not remote_jid:
        return JSONResponse({"status": "no_text"})

    reply = run_agent(remote_jid, text)
    send_message(remote_jid, reply)

    return JSONResponse({"status": "ok"})


@app.get("/health")
async def health():
    return {"status": "online", "agent": "KRV Imports"}
