FROM python:3.10-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install python-dotenv
COPY . .
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5001"]
