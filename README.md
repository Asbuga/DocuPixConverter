# 🖼️📄 DocuPixConverter

## 📌 Description  
This is a **web application for converting images and documents**,  
built with **FastAPI**. It supports **user authentication** (powered  
by `fastapi-users`) and runs inside a **Docker container** using  
**Nginx** and **PostgreSQL**.  

## 🚀 Features  
✔️ Convert images and documents to different formats  
✔️ User registration & authentication via `fastapi-users`  
✔️ API for file processing  
✔️ Deployment via **Docker**  

## 🏗️ Technologies  
- **FastAPI** – Backend framework  
- **PostgreSQL** – Database  
- **FastAPI-Users** – User authentication  
- **Nginx** – Reverse proxy  
- **Docker** – Containerization  

## 🛠️ Getting Started  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/Asbuga/DocuPixConverter.git
cd web_app
```

### 2️⃣ Configure .env
Create a `.env` file (or check if it exists) with the following content:
```.env
ENVIRONMENT=production
```
and `database.env`with the following content:
```database.env
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=app_db
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_pass
```

### 3️⃣ Run with Docker
```bash
docker compose up --build
```

### 4️⃣ Check if it's Running
Once the app is running, access the API at:
```web
http://localhost:8080/
```

### 📖 API Documentation
After starting the project, you can access the API documentation at:
```web
http://localhost:8080/docs/
```
This is an automatically generated Swagger UI for interacting with the API.

### 📜 License
This project is licensed under GNU GPL 3.0.
