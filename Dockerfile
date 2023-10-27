FROM python:3-slim AS base

WORKDIR /app
ADD . .

RUN pip install -r requirements.txt

WORKDIR /app/src

EXPOSE 3000
ENTRYPOINT ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "3000"]

FROM base AS dev
ENTRYPOINT ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]
