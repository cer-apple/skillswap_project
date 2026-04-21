from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from MainApp.models import Skill


DUMMY_USERS = [
    {"username": "alice",  "first_name": "Alice",  "last_name": "Anderson", "email": "alice@example.com"},
    {"username": "bob",    "first_name": "Bob",    "last_name": "Brown",    "email": "bob@example.com"},
    {"username": "carol",  "first_name": "Carol",  "last_name": "Clark",    "email": "carol@example.com"},
    {"username": "david",  "first_name": "David",  "last_name": "Davis",    "email": "david@example.com"},
    {"username": "emma",   "first_name": "Emma",   "last_name": "Evans",    "email": "emma@example.com"},
    {"username": "frank",  "first_name": "Frank",  "last_name": "Foster",   "email": "frank@example.com"},
    {"username": "grace",  "first_name": "Grace",  "last_name": "Green",    "email": "grace@example.com"},
    {"username": "henry",  "first_name": "Henry",  "last_name": "Hill",     "email": "henry@example.com"},
    {"username": "iris",   "first_name": "Iris",   "last_name": "Irving",   "email": "iris@example.com"},
    {"username": "jack",   "first_name": "Jack",   "last_name": "Johnson",  "email": "jack@example.com"},
]

DEFAULT_PASSWORD = "password123"

# (owner_username, title, description, category, price_type, price, contact_preference)
DUMMY_SKILLS = [
    (
        "alice",
        "Calculus I & II Tutoring",
        "Struggling with limits, derivatives, or integrals? I'm a math major who has TA'd Calc I for two semesters. "
        "I can walk you through problem sets and help you prep for midterms. Weekday evenings in the library work best.",
        "tutoring", "paid", Decimal("25.00"), "email",
    ),
    (
        "alice",
        "Japanese <-> English Language Exchange",
        "Native English speaker studying Japanese (JLPT N3). Looking to swap 30 min of English conversation for 30 min of Japanese. "
        "Casual coffee-shop vibe, no textbooks required.",
        "language", "free", None, "instagram",
    ),
    (
        "bob",
        "Acoustic Guitar Lessons for Beginners",
        "Been playing guitar for 8 years and gig at open mics around campus. Can teach you basic chords, strumming, and your first full song "
        "in about a month. I have a spare acoustic you can borrow for lessons.",
        "music", "paid", Decimal("20.00"), "whatsapp",
    ),
    (
        "carol",
        "Logo & Poster Design for Student Orgs",
        "Graphic design minor with 3 years of Adobe Illustrator experience. I've made flyers for the film club and the a cappella group. "
        "Turnaround usually 3-5 days. Show me your org and I'll send past work.",
        "design", "paid", Decimal("35.00"), "email",
    ),
    (
        "carol",
        "Portrait & Event Photography",
        "I shoot senior portraits, LinkedIn headshots, and small campus events. Sony A7III, natural light preferred. "
        "Editing included. Portfolio available on request.",
        "creative", "paid", Decimal("50.00"), "instagram",
    ),
    (
        "david",
        "Intro to Python / Data Structures Help",
        "CS junior, comfortable with Python, Java, and a bit of C++. Happy to pair-program through assignments or review your code before submission. "
        "Won't write it for you - but I'll make sure you actually get it.",
        "tech", "paid", Decimal("30.00"), "email",
    ),
    (
        "emma",
        "Home-Cooked Meal Prep (Asian cuisine)",
        "I love cooking and always make too much. Weekly meal prep for 5 containers - stir fry, curry, dumplings, bento-style. "
        "Great for exam weeks when you don't want dining hall food. Bring your own containers to save $5.",
        "other", "paid", Decimal("40.00"), "whatsapp",
    ),
    (
        "emma",
        "Baking Basics: Cookies & Bread",
        "Free baking session in the dorm kitchen! I teach, you help, we split whatever we make. Fun way to kill a Sunday afternoon. "
        "DM me your availability.",
        "creative", "free", None, "instagram",
    ),
    (
        "frank",
        "Personal Training & Gym Buddy",
        "Exercise Science major, certified personal trainer. I can put together a 4-week program for you or just be your accountability partner "
        "at the rec center. Free first session so we can see if we're a good fit.",
        "fitness", "paid", Decimal("15.00"), "phone",
    ),
    (
        "grace",
        "Pickup Basketball / Skills Clinic",
        "Played varsity in high school. Running casual skills sessions Sat mornings at the outdoor courts - ball handling, shooting form, defense. "
        "All skill levels welcome, totally free.",
        "sports", "free", None, "instagram",
    ),
    (
        "grace",
        "Lecture Notes: Intro Econ & Stats",
        "Detailed handwritten-to-typed notes for ECON 101 and STAT 201 (Prof. Miller's sections). PDFs delivered weekly. "
        "Saved me last semester, might save you too.",
        "tutoring", "paid", Decimal("10.00"), "email",
    ),
    (
        "henry",
        "Resume & Internship Application Review",
        "Finance senior with offers from 2 bulge-bracket banks. I'll review your resume and cover letter, and do a mock behavioral interview. "
        "Have helped 6 friends land interviews this recruiting cycle.",
        "business", "paid", Decimal("25.00"), "email",
    ),
    (
        "iris",
        "Spanish Conversation Practice",
        "Heritage Spanish speaker, studied abroad in Madrid. Happy to chat in Spanish for an hour a week - great if you have an oral exam coming up "
        "or just want to stop forgetting what you learned in high school.",
        "language", "free", None, "whatsapp",
    ),
    (
        "iris",
        "Watercolor Painting Workshop",
        "Chill 2-hour watercolor session, supplies included. I guide you through one small piece you can actually take home. "
        "Perfect study break. Groups of 2-4 work best.",
        "creative", "paid", Decimal("20.00"), "instagram",
    ),
    (
        "jack",
        "Dorm Move-In / Move-Out Help",
        "Got a pickup truck and strong arms. Can help you haul stuff to/from storage, IKEA runs, or just lift the heavy boxes up to the 4th floor "
        "when the elevator's broken. Hourly rate, negotiable for longer jobs.",
        "other", "paid", Decimal("30.00"), "phone",
    ),
    (
        "jack",
        "Bike Repair & Tune-ups",
        "Flat tire? Squeaky brakes? I've been fixing my own bikes for years. Basic tune-up is free if you supply parts, "
        "more involved repairs we can work out. Meet at the bike racks behind the union.",
        "other", "free", None, "phone",
    ),
]


class Command(BaseCommand):
    help = "Seed the database with dummy users and skill listings for development."

    @transaction.atomic
    def handle(self, *args, **options):
        created_users = 0
        skipped_users = 0
        user_map = {}

        for data in DUMMY_USERS:
            username = data["username"]
            existing = User.objects.filter(username=username).first()
            if existing:
                user_map[username] = existing
                skipped_users += 1
                self.stdout.write(f"  - user '{username}' already exists, skipping")
                continue

            user = User.objects.create_user(
                username=username,
                email=data["email"],
                password=DEFAULT_PASSWORD,
                first_name=data["first_name"],
                last_name=data["last_name"],
            )
            user_map[username] = user
            created_users += 1
            self.stdout.write(self.style.SUCCESS(f"  + created user '{username}'"))

        created_skills = 0
        skipped_skills = 0

        for owner_username, title, description, category, price_type, price, contact in DUMMY_SKILLS:
            owner = user_map.get(owner_username)
            if owner is None:
                self.stdout.write(self.style.WARNING(f"  ! no user for skill '{title}', skipping"))
                skipped_skills += 1
                continue

            if Skill.objects.filter(owner=owner, title=title).exists():
                skipped_skills += 1
                self.stdout.write(f"  - skill '{title}' for '{owner_username}' already exists, skipping")
                continue

            Skill.objects.create(
                title=title,
                description=description,
                category=category,
                price_type=price_type,
                price=price,
                contact_preference=contact,
                availability_status="available",
                owner=owner,
            )
            created_skills += 1
            self.stdout.write(self.style.SUCCESS(f"  + created skill '{title}' for '{owner_username}'"))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Done. Users: {created_users} created, {skipped_users} skipped. "
            f"Skills: {created_skills} created, {skipped_skills} skipped."
        ))
