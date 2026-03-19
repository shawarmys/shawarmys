FROM python:3.12-slim

WORKDIR /app

# Copy dataset into the image
COPY data /app/data

# Install Python deps
COPY server/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt \
    && pip install --no-cache-dir uvicorn

# Copy application source and install editable
COPY server /app/server

WORKDIR /app/server
RUN pip install --no-cache-dir -e .

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--log-level", "debug"]
