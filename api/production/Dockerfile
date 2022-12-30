from python:3.10-slim
RUN groupadd apigroup && useradd -m -g apigroup -s /bin/bash api
RUN echo "api ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN mkdir -p /home/fastapi/app/api
WORKDIR /home/fastapi/app/api
RUN mkdir project
ADD project/* ./project/
ADD requirements/* ./
ADD start.sh ./
ADD pytest.ini ./
RUN pip install --no-cache-dir -r prod.txt
RUN pip list
RUN chown -R api:apigroup /home/fastapi
USER api
RUN chmod +x start.sh
