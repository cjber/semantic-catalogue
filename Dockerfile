FROM python:3.10.9

WORKDIR /
COPY . .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["fastapi", "run", "src/search_api/api.py", "--port", "7860"]
