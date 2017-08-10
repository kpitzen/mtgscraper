FROM python:3-slim
WORKDIR /mtgscraper
ADD . /mtgscraper
RUN pip install -r requirements.txt
CMD ["python", "main.py", "extract", "-gf"]
CMD ["python", "main.py", "load", "-d"]