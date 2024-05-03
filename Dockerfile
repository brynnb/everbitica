# syntax=docker/dockerfile:1

# Stage 1: Build the React application
FROM node:14 as react-build
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json ./
COPY frontend/ ./
RUN npm run build

FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

COPY --from=react-build /app/build /code/frontend/build

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]