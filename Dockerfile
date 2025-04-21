FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0


WORKDIR /app

COPY app.py auth.py kanban.py news.py models.py requirements.txt /app/
COPY templates /app/templates
COPY static /app/static

# Install dependencies
RUN apt-get update && apt-get install -y gcc libffi-dev build-essential && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc build-essential && apt-get autoremove -y && apt-get clean

# Expose the Flask port
EXPOSE 5000

# Default command
CMD ["flask", "run"]
