FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && python -m nltk.downloader -d /usr/local/share/nltk_data punkt punkt_tab

COPY . .

RUN python manage.py collectstatic --noinput

ENV DEBUG=False
EXPOSE 8000
CMD sh -c "python manage.py migrate --noinput && python manage.py seed_demo && exec gunicorn CodeCloneDetector.wsgi --bind 0.0.0.0:${PORT:-8000}"
