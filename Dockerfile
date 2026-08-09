FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends nginx supervisor && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN rm -f /etc/nginx/sites-enabled/default

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 10000

CMD ["supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]