# Campus SkillSwap

A Django web app where college students can post skills or services they offer
(tutoring, design, music lessons, ride shares, you name it) and discover what
their classmates can do. Includes search, ratings & reviews, and per-user
dashboards.

## Features

- **User accounts** — sign up, log in, log out, edit profile
- **Skill CRUD** — post a skill, edit your own listings, delete them
- **Browse & search** — full-text search across title / description / owner,
  combined with category filtering on a single form
- **Skill detail pages** — full description, pricing, contact preference,
  and an instructor card with avatar
- **Reviews & ratings** — leave a 1–5 star rating and comment on any skill
  you didn't post yourself; one review per user per skill; average rating
  shown on every skill page
- **Personal dashboard** — see your stats and manage your own posts
- **Django admin** — manage users, skills, and reviews from `/admin/`

## Tech Stack

- **Django 6.x** (Python web framework)
- **SQLite** (default dev database)
- **Bootstrap 5** + **Bootstrap Icons** (via CDN)
- **Inter** font from Google Fonts
- Function-based views, Django ModelForms, server-rendered templates

## Setup

### Prerequisites

- Python 3.10+
- `git`

### 1. Clone and enter the project

```bash
git clone https://github.com/cer-apple/skillswap_project.git
cd skillswap_project
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate          # macOS / Linux
# venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. (Optional) Seed dummy data

A management command is included that creates 10 dummy users and ~16 sample
skill listings so you can explore the app without starting from an empty DB:

```bash
python manage.py seed_dummy_data
```

### 6. Run the dev server

```bash
python manage.py runserver
```

Open <http://127.0.0.1:8000/> in your browser.

## Test Accounts

> These accounts only exist after you run `python manage.py seed_dummy_data`
> (and create the admin user yourself with `createsuperuser`).

### Admin

| Username | Password   |
| -------- | ---------- |
| `admin`  | `admin123` |

Create with:

```bash
python manage.py createsuperuser
```

### Regular Users

All of the seeded users below share the password **`password123`**:

`alice`, `bob`, `carol`, `david`, `emma`, `frank`, `grace`, `henry`,
`iris`, `jack`, `tatsuki`

## Project Structure

```
campus_skillswap/
├── MainApp/                    # Main Django app
│   ├── management/commands/    # seed_dummy_data
│   ├── migrations/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py               # Skill, Review
│   ├── urls.py
│   └── views.py
├── campus_skillswap/           # Project settings package
├── templates/MainApp/          # All HTML templates
├── manage.py
├── requirements.txt
└── README.md
```

## Screenshots

> Add screenshots here once you've taken them. Suggested shots:

- **Home / Browse** — `docs/screenshots/home.png`
- **Skill detail with reviews** — `docs/screenshots/skill_detail.png`
- **Dashboard** — `docs/screenshots/dashboard.png`
- **Post a skill form** — `docs/screenshots/skill_form.png`

```markdown
![Home](docs/screenshots/home.png)
![Skill detail](docs/screenshots/skill_detail.png)
```

## License

Built as a student project. Use freely for learning purposes.
