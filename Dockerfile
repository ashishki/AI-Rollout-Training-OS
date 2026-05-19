FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

COPY requirements.txt pyproject.toml README.md ./
COPY ai_rollout_os ./ai_rollout_os
COPY migrations ./migrations

RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt -e .

USER app

EXPOSE 8000

CMD ["uvicorn", "ai_rollout_os.main:app", "--host", "0.0.0.0", "--port", "8000"]
