# Skill Mentor AI Interview

Skill Mentor is a Flask-based interview preparation platform that uses AI-powered question generation, answer feedback, resume-based interview creation, and user analytics.

## Features

- User registration and login with email/password
- Google OAuth login support
- Email OTP verification for registration and password reset
- Interview tracks for HR, Technical, Behavioral, and Resume-based interview modes
- AI-generated interview questions using Google Gemini
- AI feedback and scoring for submitted answers
- Resume upload support to generate custom interview questions
- User dashboard with recent interviews and performance metrics
- Interview history, detailed results, analytics, leaderboard, and batch summary
- Certificate generation for completed interview performance
- SQLite database persistence and secure environment-based configuration

## Tech Stack

- Python 3
- Flask
- SQLite
- Authlib (Google OAuth)
- google-generativeai (Gemini)
- PyPDF2, python-docx for resume parsing
- ReportLab for PDF certificate generation
- Flask-Talisman for optional security headers
- python-dotenv for environment configuration

## Repository Structure

- `app.py` – Main Flask application and business logic
- `requirements.txt` – Python dependencies
- `README.md` – Project documentation
- `.gitignore` – Files and folders excluded from git
- `.env.example` – Example environment variables file
- `interview.db` – SQLite database (ignored)
- `static/` – CSS, JavaScript, images, certificates, and fonts
- `templates/` – Flask HTML templates
- `uploads/` – Uploaded resumes and files (ignored)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/kajaresahil05/Skill-Mentor-AI-Interview.git
cd Skill_Mentor
```

### 2. Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create and configure `.env`

Copy the example file and provide your own settings:

```bash
copy .env.example .env
```

Update `.env` with your values:

- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `FLASK_SECRET_KEY`
- `API_KEY` (Gemini / Google Generative AI)
- `EMAIL_USERNAME`
- `EMAIL_PASSWORD`

### 5. Run the application

```bash
python app.py
```

Open the app at:

```
http://127.0.0.1:5000
```

## Environment Variables

Example values are provided in `.env.example`.

- `GOOGLE_CLIENT_ID` – Google OAuth client ID
- `GOOGLE_CLIENT_SECRET` – Google OAuth client secret
- `FLASK_SECRET_KEY` – Secret key for Flask sessions
- `API_KEY` – Gemini AI API key
- `EMAIL_USERNAME` – Email account for OTP delivery
- `EMAIL_PASSWORD` – Email app password or SMTP credentials

## Database

The app uses `interview.db` to store:

- Registered users
- Interview sessions
- Answers and feedback
- Scores and history

The database is initialized automatically when the app starts.

## Important Notes

- Do not commit `.env` or any secret keys to GitHub.
- `.gitignore` already excludes `.env`, `.db`, `uploads/`, `.idea/`, and generated Python files.
- If you do not have a Gemini API key, the app may still fallback to built-in sample questions, but the full AI experience requires `API_KEY`.
- `Flask-Talisman` is optional; the app will still run if it is not installed.

## Usage

1. Register using a Gmail or APSIT email address
2. Verify your account using the OTP sent to your email
3. Log in and choose an interview category
4. Select difficulty or upload a resume for custom questions
5. Answer questions and receive AI-generated feedback
6. View analytics, history, leaderboard, and certificate options

## Security

- Passwords are hashed using Werkzeug
- Session cookies are configured with `HttpOnly` and `SameSite=Lax`
- Google OAuth is available for a faster sign-in flow

## Optional Enhancements

- Add a real SMTP email provider for OTP delivery
- Add SSL configuration for production use
- Remove sample or personal files before publishing
- Secure generated certificates and badge images

## License

This repository has no license specified. Add a `LICENSE` file if you want to publish under a specific open source license.
