**🗺️ Travel Guide

A Django-based travel guide application where users can explore tourist destinations, view maps, create personal itineraries, book hotels, add activities, and share reviews.

🚀 Features

User authentication & profiles

Add and explore tourist destinations

Google Maps integration (city/location based)

Personal itineraries with hotels and activities

Reviews and ratings system

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/Mostakim15/Travel-Guide.git
cd Travel-Guide

2️⃣ Create & activate virtual environment
python -m venv env
# On Windows
env\Scripts\activate
# On Mac/Linux
source env/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Apply migrations
python manage.py migrate

5️⃣ Create superuser (admin)
python manage.py createsuperuser

6️⃣ Run development server
python manage.py runserver


Now open 👉 http://127.0.0.1:8000

🌍 Environment Variables

Create a .env file in the root folder and add:

SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Google Maps API Key
GOOGLE_MAPS_API_KEY=your_api_key_here

📂 Project Structure
Travel-Guide/
│── core/                # Main app (models, views, urls, admin)
│── templates/           # HTML templates
│── static/              # CSS, JS, images
│── manage.py
│── requirements.txt
│── README.md

🛠️ Tech Stack

Backend: Django, Python

Frontend: HTML, CSS, Bootstrap, JS

Database: SQLite (default) / PostgreSQL (production)

APIs: Google Maps API

🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

📜 License

This project is licensed under the MIT License.**
