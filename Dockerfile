FROM python:3.12

RUN apt-get update && apt-get install -y 
RUN mkdir /home/app

COPY . /home/app

WORKDIR /home/app

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.address" ,"0.0.0.0"]


## docker run -d -p8501:8501 --name app app
## docker build -t app -f Dockerfile .

