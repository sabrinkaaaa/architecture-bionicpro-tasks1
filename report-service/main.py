from fastapi import FastAPI, Request, HTTPException, Query
from clickhouse_driver import Client
import os
from datetime import datetime

app = FastAPI(title="BionicPRO Report Service")

# Подключение к ClickHouse (имя сервиса в docker-compose)
CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "clickhouse-server")
CLICKHOUSE_DB = os.getenv("CLICKHOUSE_DB", "default")

client = Client(host=CLICKHOUSE_HOST, database=CLICKHOUSE_DB)

@app.get("/reports/me")
def get_my_report(
    request: Request,
    from_date: str = Query(..., description="Дата начала периода YYYY-MM-DD"),
    to_date: str = Query(..., description="Дата конца периода YYYY-MM-DD")
):
    """
    Возвращает отчёт для текущего пользователя
    """
    # Получаем user_id из заголовка (BFF должен подставлять)
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Не авторизован")

    # Проверка формата даты
    try:
        start = datetime.strptime(from_date, "%Y-%m-%d")
        end = datetime.strptime(to_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат даты")

    # Запрос к ClickHouse
    query = """
        SELECT user_id, steps, battery, name, event_date
        FROM user_reports
        WHERE user_id = %(user_id)s
        AND event_date BETWEEN %(from_date)s AND %(to_date)s
        ORDER BY event_date
    """
    rows = client.execute(query, {"user_id": int(user_id), "from_date": start, "to_date": end})

    # Формируем ответ
    reports = [
        {"user_id": r[0], "steps": r[1], "battery": r[2], "name": r[3], "event_date": r[4].isoformat()}
        for r in rows
    ]

    return {"reports": reports}
