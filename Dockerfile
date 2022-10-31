FROM python:bullseye
COPY . .
RUN apt update
RUN apt install openjdk-11-jdk -y
RUN pip install -r requirements.txt
EXPOSE 8050
CMD ["python", "dashboard.py"]
