from python:3.10-slim
RUN groupadd apigroup && useradd -m -g apigroup -s /bin/bash api
RUN echo "api ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN mkdir -p /home/fastapi/app/api
WORKDIR /home/fastapi/app/api
COPY requirements.txt .
COPY start.sh .
RUN pip install --no-cache-dir -r requirements.txt
RUN chown -R api:apigroup /home/fastapi
USER api
RUN chmod +x start.sh
