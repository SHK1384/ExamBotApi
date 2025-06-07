## ⚙️ Setup Instructions (for local testing)

### 1. Clone the repository

```bash
git clone https://github.com/SHK1384/ExamBotApi.git
cd ExamBotApi
```

### 2. Create a virtual environment

```bash
pip -m venv .venv
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Make the migrations

```bash
python manage.py migrate
```

### 5. Run the project

```bash
python manage.py runserver
```

## ⚙️ Setup Instructions (for production)

### 1. Setup the postgresql in the .env file
```
DB_PORT: "database port"
DB_HOST: "database address"
DB_PASSWORD: "database password"
DB_USER: "database username"
DB_NAME: "database name"
DB: "just put postgres"
```

### 2. Setup the minIO for storage in the .env file
```
ENDPOINT_URL: "minIO address"
SECRET_KEY_ACCESS: "minIO secret key"
ACCESS_KEY_ID: "minIO access key id"
```

### 3. Other .env file setup
```
DEBUG: "False in production"
APP_HOST: "https://<appName>.darkube.app"
ALLOWED_HOSTS: "<appName>.darkube.app"
```
