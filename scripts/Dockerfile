FROM python:3.11-slim

# Install Firefox ESR and geckodriver
RUN apt-get update && apt-get install -y --no-install-recommends \
    firefox-esr \
    geckodriver \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "scrape_x.py"]
