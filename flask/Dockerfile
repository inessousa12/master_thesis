FROM ubuntu:latest
WORKDIR /src
RUN apt -y update
RUN apt -y upgrade
RUN apt install -y python3
RUN apt install -y python3-pip
COPY . .
RUN chmod +x -R .
RUN pip install -r requirements.txt --no-cache-dir
CMD ["python3","app.py"]
