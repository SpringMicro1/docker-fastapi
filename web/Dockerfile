from python:3.10.5-slim
# RUN groupadd apigroup && useradd -m -g apigroup -s /bin/bash api
# RUN echo "api ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN mkdir -p /home/fastapi/app/web
WORKDIR /home/fastapi/app/web
COPY requirements.txt .
# COPY start.sh .
# COPY main.py .
RUN pip install --no-cache-dir -r requirements.txt
# RUN chown -R api:apigroup /home/fastapi
# USER api
# RUN chmod +x start.sh
# RUN ls -l

# main.py:app
# https://fastapi.tiangolo.com/deployment/server-workers/
ENTRYPOINT ["/usr/local/bin/gunicorn", "main:app", "--workers", "8", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", ":8000", "--reload"]
