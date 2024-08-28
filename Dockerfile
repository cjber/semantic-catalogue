FROM python:3.12

WORKDIR /
COPY . .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["fastapi", "run", "src/search_api/api.py", "--port", "7860"]
