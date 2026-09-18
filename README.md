# ProCRM — Full-Featured Portfolio CRM MVP

## Included
- Authentication: login/logout
- Dashboard analytics
- Customer CRUD
- Lead CRUD
- Sales pipeline by lead stage
- Invoice CRUD
- Search and status filters
- Responsive glassmorphism UI
- WhatsApp click-to-chat links
- Django admin support

## Setup

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

This is a portfolio-ready MVP. For production, add payment gateway integration, audit logs, API authentication, automated tests, deployment configuration, and real WhatsApp Business API credentials.
