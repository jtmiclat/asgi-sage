FROM python:3.7-slim
WORKDIR /app
RUN pip install --no-cache starlette uvicorn gunicorn asgi-sage==0.1.1
COPY app.py /app/.
CMD gunicorn -k uvicorn.workers.UvicornWorker --bind :$PORT --workers 1 --threads 3 app:app --timeout 60
