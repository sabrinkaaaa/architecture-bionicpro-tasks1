from fastapi import FastAPI
app = FastAPI()

@app.post("/auth/exchange")
async def exchange_code(payload: dict):
    # получаем code и code_verifier
    # отправляем запрос в Keycloak
    # получаем access и refresh токен
    # сохраняем токен на сервере, фронту возвращаем только cookie
    return {"status": "ok"}
