✅ ToDoZen – Connecting the Goals

ToDoZen is a comprehensive task management web application designed to help users stay organized, track progress, and stay motivated. Built with Flask, MySQL, and Twilio SMS API, the system enables users to create tasks with deadlines and priorities, view them on a dynamic calendar, receive SMS reminders, and earn rewards for completion.

🚀 Features

📝 Task Management – Create, categorize, and prioritize tasks.

📅 Calendar Integration – Interactive task calendar (FullCalendar.js).

🔔 Deadline Reminders – Automated SMS notifications using Twilio API.

📊 Progress Visualization – Charts & graphs to track task completion.

🎯 Rewards System – Earn points and rewards for finishing tasks.

👤 Profile Page – Track achievements, rewards, and learn productivity tips.

📱 Responsive UI – Accessible across desktop and mobile devices.

🛠️ Tech Stack

Frontend: HTML, CSS, JavaScript, FullCalendar.js, AJAX

Backend: Flask (Python)

Database: MySQL

Notifications: Twilio SMS API

⚙️ Installation

Clone the repository:

git clone https://github.com/your-username/todozen.git
cd todozen


Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt


Set up the MySQL database:

Import schema.sql from the /database folder.

Update credentials in config.py.

Configure Twilio API for SMS notifications:

Add your TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER in config.py.

Run the application:

flask run


Open in browser:

http://127.0.0.1:5000/

🧪 Testing

✅ Unit tests (task creation, reminders)

✅ Integration tests (Flask + MySQL + Twilio)

✅ End-to-end flow (task creation → calendar view → reminder → completion)

✅ Performance tests under multiple concurrent users

📌 Future Enhancements

📱 Mobile app integration (Flutter/React Native)

📤 Email + Push notifications

⏱️ Advanced scheduling with recurring tasks

🎮 Gamification with badges & levels

 A requirements.txt file for your ToDoZen – Connecting the Goals project (based on your report

ToDoZen-Connecting_the_Goals_Re…

 and the tech stack mentioned):

Flask==2.3.3
Flask-MySQLdb==1.0.1
mysqlclient==2.2.0
twilio==8.5.0
numpy==1.24.3
Pillow==10.0.0
requests==2.31.0
gunicorn==21.2.0

🔑 Why these packages?

Flask → backend framework.

Flask-MySQLdb + mysqlclient → connect Flask with MySQL.

Twilio → SMS reminders.

NumPy → used for backend data handling (if task analytics expands).

Pillow → for handling images (profile pictures, avatars).

Requests → API calls (useful for external integrations).

Gunicorn → deployment (Heroku/AWS).

📌 Since FullCalendar.js runs on the frontend, it doesn’t go into requirements.txt (it will be included via CDN or static/js).

#Folder Structure

A professional folder structure for your ToDoZen – Connecting the Goals GitHub repo. It mirrors the design & tech stack described in your report
ToDoZen-Connecting_the_Goals
and keeps things modular:

todozen/
│── README.md
│── requirements.txt
│── config.py               # Database + Twilio config
│── run.py                  # Flask entry point
│── .gitignore
│── LICENSE
│
├── backend/
│   ├── __init__.py         # Flask app factory
│   ├── models.py           # DB models: Task, User, Rewards
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py  # User login/registration
│   │   ├── task_routes.py  # CRUD for tasks
│   │   ├── calendar_routes.py # Task calendar API
│   │   ├── reminder_routes.py # SMS reminders
│   │   └── profile_routes.py  # User profile & rewards
│   ├── services/
│   │   ├── db_service.py   # MySQL queries
│   │   ├── sms_service.py  # Twilio integration
│   │   └── reward_service.py # Rewards system logic
│   └── utils/
│       ├── validators.py
│       └── helpers.py
│
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   ├── main.js
│   │   │   ├── calendar.js      # FullCalendar.js integration
│   │   │   └── charts.js        # Task progress visualization
│   │   └── images/
│   └── templates/
│       ├── base.html
│       ├── index.html           # Dashboard
│       ├── login.html
│       ├── register.html
│       ├── calendar.html
│       ├── profile.html
│       └── rewards.html
│
├── database/
│   ├── schema.sql          # MySQL schema
│   └── seed_data.sql       # Sample tasks/users
│
├── tests/
│   ├── test_auth.py
│   ├── test_tasks.py
│   ├── test_calendar.py
│   ├── test_reminders.py
│   └── test_rewards.py
│
└── docs/
    ├── System_Architecture.png
    ├── MySQL_Diagram.png
    ├── UseCaseDiagram.png
    ├── Wireframes.png
    └── ToDoZen_Report.pdf

✨ With this setup:

backend/ → Handles routes, services, database models.

frontend/ → Templates (Jinja2) + static assets (CSS, JS, images).

database/ → Schema + sample data for testing.

tests/ → Unit & integration tests.

docs/ → Diagrams, report, documentation.

👨‍💻 Author
Sourav Paul – GitHub
Guided by Dr. Nabanita Choudhury (Assam down town University).

📜 License
This project is licensed under the MIT License – see the LICENSE
 file for details.
