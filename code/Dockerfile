FROM python:3.13-alpine
WORKDIR /app
COPY  requirements.txt .
RUN pip install -r requirements.txt --break-system-packages
COPY . /app/ 
CMD [ "python3","controller.py" ]


