from fastapi import FastAPI, HTTPException
from httpx import AsyncClient
from bot.dca_bot.signer import sign_payload
from bot.config.config import THREE_COMMAS_API_KEY, THREE_COMMAS_BASE_URL

from .dca_bot.schemas import CreateDCABotPayload

app = FastAPI()

@app.post("/create-dca-bot")
async def create_dca_bot(payload: CreateDCABotPayload):
    try:
        url = f"{THREE_COMMAS_BASE_URL}/ver1/bots/create_bot"
        signature = sign_payload(payload.dict())

        headers = {
            "APIKEY": THREE_COMMAS_API_KEY,
            "Signature": signature,
            "Content-Type": "application/json"
        }

        async with AsyncClient(timeout=10.0) as client:
            response = await client.post(url, headers=headers, json=payload.dict())
            print("Response:", response.status_code, response.text)

        if response.status_code == 201:
            return response.json()
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

    except Exception as e:
        print("Exception occurred:", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")
