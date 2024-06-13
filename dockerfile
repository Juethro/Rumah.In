FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install NPM tailwindcss
RUN apt-get update && apt-get install -y npm

# Set working directory di dalam kontainer
WORKDIR /app

# Salin file requirements.txt ke dalam kontainer
COPY requirements.txt .

# Install dependensi
RUN pip install -r requirements.txt

# Salin semua file ke workdir
COPY . .

# Pindah ke folder theme/static_src dan install npm dependencies
WORKDIR /app/web/theme/static_src
RUN npm install

# Pindah ke folder web
WORKDIR /app/web
RUN python manage.py tailwind build

# Membuka akses ke port 8000
EXPOSE 8000

# Run cron + django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]






