🩸 Blood Bank & Donor Management System

A web-based application built using Django & SQLite to digitalize the process of blood donor registration, blood requests, stock management, and report generation.
This system aims to connect donors and recipients while helping administrators manage blood availability efficiently.

🔥 Features
👥 User Features

Register as blood donor

Request blood online

Check blood stock availability

View blood request status

Generate reports with date filtering

Built-in FAQ Chatbot for instant guidance

🛡️ Admin Features

Login authentication (admin protected)

Approve / Reject blood requests

Manage donor and request records

Generate filtered PDF reports with charts & summaries

🏗️ Tech Stack
Component	Technology
Frontend	HTML, CSS, Bootstrap, JavaScript
Backend	Django (Python)
Database	SQLite
Report Export	ReportLab
Hosting (Local)	Django Development Server
🗂️ Project Modules
Module	Description
Donor Module	Register donor & display donor list
Blood Stock Module	Maintains available blood units
Request Module	Users request blood online
Admin Module	Login + Approve/Reject requests
Reports Module	Export filtered PDF reports with charts
Chatbot	Answer frequently asked questions
🖥️ Screenshots (Optional)

Add screenshots here if needed later

/static/screenshots/homepage.png
/static/screenshots/manage_requests.png
/static/screenshots/reports.png

🚀 Installation & Setup
git clone <repository_url>
cd bloodbank
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


Now open the browser and run:

http://localhost:8000/

🔑 Admin Login

To create a superuser:

python manage.py createsuperuser

📊 Database Design (Entities)

Donor (id, name, blood_group, city, contact)

BloodRequest (id, name, blood_group, city, contact, status)

BloodStock (id, blood_group, units)

ERD available in documentation.

📄 PDF Report Features

✔ Charts included
✔ Date range filter
✔ Summary of total donors, stocks & requests
✔ Structured report header and footer

🗣️ Chatbot (FAQ)

How to register as donor

How to request blood

Who approves requests

Where to check status

Technologies used in project

🏁 Future Enhancements

SMS / Email notification to donors and recipients

Online blood donor booking system

Multi-branch blood bank support

Live blood stock update from hospitals

📜 License

This project is developed for academic and learning purposes.
