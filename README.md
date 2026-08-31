# SafetyFund Management System

## Overview

SafetyFund Management System is a web-based cooperative and savings management platform built with Django and PostgreSQL. The system helps members save money, purchase shares, request loans, make loan repayments, and stay informed through announcements. It also provides administrators and finance officers with tools to manage members, deposits, loans, repayments, and organizational activities.

The goal of the project is to digitize the management of a member-based financial organization while improving transparency, accountability, and communication among members.

---

## Features

### Public Features
- Home Page
- About Page
- Contact Page
- Announcements Page
- Meet The Team Page
- User Registration
- User Login

### Member Features
- Personal Dashboard
- Membership Application
- Deposit Requests
- Upload Deposit Proof
- Loan Requests
- Loan Repayment Requests
- Upload Repayment Proof
- View Personal Loans
- View Deposit History
- View Shares Information
- View Announcements

### Finance Officer Features
- Finance Dashboard
- Review Deposit Requests
- Approve Deposits
- Review Loan Requests
- Approve Loans
- Review Loan Repayments
- Approve Repayments
- Manage Financial Transactions

### Administrator Features
- Admin Dashboard
- Manage Members
- Manage Users
- Assign User Roles
- Activate/Deactivate Users
- Review Membership Applications
- Create Announcements
- Upload Announcement Images
- View Member Profiles
- Monitor Loans and Deposits

---

## Technology Stack

### Backend
- Python
- Django

### Database
- PostgreSQL

### Frontend
- HTML
- CSS
- Bootstrap 5
- JavaScript

### Authentication
- Django Authentication System
- Custom User Model

---

## User Roles

| Role | Description |
|--------|------------|
| USER | Registered User |
| MEMBER | Approved Member |
| FINANCE | Finance Officer |
| ADMINISTRATOR | System Administrator |
| DEVELOPER | Developer Account |

---

## Project Structure

```text
SafetyFund/
│
├── accounts/
├── finance/
├── membership/
├── templates/
├── static/
│   ├── css/
│   └── images/
├── media/
├── config/
├── manage.py
└── requirements.txt
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/kwisanga7/SafetyFund.git
cd SafetyFund
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure PostgreSQL

Update your database settings in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'safetyfund_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Run Development Server

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---

## Current Modules

### Accounts Module
- Authentication
- Registration
- Login
- User Roles
- Member Profiles

### Membership Module
- Membership Applications
- Membership Approval

### Finance Module
- Share Transactions
- Deposit Requests
- Loan Requests
- Loan Repayments
- Financial Reviews

### Announcement Module
- Create Announcements
- Upload Images
- Display Public Announcements

---

## Future Enhancements

- Notification System
- Email Notifications
- PDF Statements
- Financial Reports
- Analytics Dashboard
- Dividend Calculations
- Online Payment Integration
- Mobile Application
- Audit Logs
- Document Management

---

## Screenshots

Add screenshots of:
- Home Page
- Member Dashboard
- Finance Dashboard
- Admin Dashboard
- Announcements Page

---

## Author

**Elie Kwisanga**

- Software Developer
- AI & Machine Learning Enthusiast
- Safety Professional

GitHub: https://github.com/kwisanga7

---

## License

This project is developed for educational and organizational purposes. Feel free to modify and extend it according to your needs.

---

## Project Status

🚧 Active Development

Current Version: **v1.0.0**

Completed Features:
- User Authentication
- Membership Applications
- Deposits Management
- Loan Management
- Loan Repayments
- Role-Based Dashboards
- Announcements System

Upcoming Features:
- Notifications
- Reports
- Analytics
- Email Integration
- Payment Gateway Integration
