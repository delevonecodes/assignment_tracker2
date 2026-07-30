# Stracker

Stracker is a full-stack assignment management web application built with Flask that helps students organize coursework, track deadlines, and manage assignments through an intuitive dashboard. Users can create an account, securely log in, and manage their own assignments with a responsive, modern interface.

## Live Demo

Coming Soon

## Screenshots

### Landing Page
<img width="1920" height="1079" alt="image" src="https://github.com/user-attachments/assets/386de661-d45f-4a04-9cb2-44b0e004bd86" />

### Dashboard
<img width="1920" height="1079" alt="image" src="https://github.com/user-attachments/assets/3c7b561b-5ba4-4981-8bcd-165b9ebb7117" />

### Assignment Management
<img width="1920" height="1079" alt="image" src="https://github.com/user-attachments/assets/598b503b-3cef-41a4-a481-46adfbd2fb87" />

---

## Features

- Secure user authentication (Register/Login/Logout)
- Password hashing for account security
- Personalized dashboard for every user
- Create, edit, and delete assignments
- Assignment due dates
- Calendar view for upcoming assignments
- Responsive design for desktop and mobile devices
- User-specific data isolation
- Flash messages for user feedback
- Clean and intuitive user interface

---

## Built With

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Werkzeug

### Frontend

- HTML5
- CSS3
- Jinja2 Templates
- JavaScript

### Database

- SQLite

---

## Project Structure

```
assignment_tracker2/
│
├── website/
│   ├── auth.py
│   ├── dashboard.py
│   ├── models.py
│   ├── __init__.py
│   ├── templates/
│   └── static/
│
├── instance/
├── requirements.txt
├── main.py
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/delevonecodes/assignment_tracker2.git
```

Navigate into the project

```bash
cd assignment_tracker2
```

Create a virtual environment

Windows

```bash
python -m venv .venv
```

Mac/Linux

```bash
python3 -m venv .venv
```

Activate the virtual environment

Windows

```bash
.venv\Scripts\activate
```

Mac/Linux

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python main.py
```

Open your browser and visit

```
http://127.0.0.1:5000
```

---

## Technologies Demonstrated

This project demonstrates practical experience with:

- Full-stack web development
- Flask application architecture
- SQL databases
- CRUD operations
- User authentication
- Session management
- Template inheritance
- Responsive web design
- Database relationships
- Form validation
- Version control with Git
- GitHub project management

---

## Future Improvements

Potential future enhancements include:

- Assignment reminders
- Email notifications
- Dark mode
- Assignment categories
- File attachments
- Search and filtering
- Progress tracking
- Recurring assignments
- Course management
- Calendar synchronization

---

## What I Learned

Through building Stracker, I gained experience with:

- Structuring medium-sized Flask applications
- Building secure authentication systems
- Designing relational databases using SQLAlchemy
- Managing user sessions
- Creating reusable HTML templates with Jinja2
- Implementing CRUD functionality
- Improving responsive web design
- Deploying and maintaining a full-stack web application
- Using Git and GitHub for version control

---

## License

This project is licensed under the MIT License.

---

## Author

**Raji Ross**

Computer Science Student

Interested in:

- Software Engineering
- Machine Learning
- Full Stack Development
- Roblox Development

GitHub: https://github.com/delevonecodes

---

## Acknowledgements

This project was built independently as part of my software engineering portfolio while learning full-stack web development with Flask.
