FROM python:3.11-alpine

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"

ENTRYPOINT ["pytest"]
CMD ["--alluredir", "allure-results"]