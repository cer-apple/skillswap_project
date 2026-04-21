from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# STATUS CHOICES for availability
STATUS_CHOICES = [
    ('available', 'Available'),
    ('unavailable', 'Unavailable'),
    ('pending', 'Pending'),
]

# CONTACT PREFERENCE CHOICES
CONTACT_CHOICES = [
    ('email', 'Email'),
    ('phone', 'Phone'),
    ('instagram', 'Instagram'),
    ('whatsapp', 'WhatsApp'),
]

# PRICE TYPE CHOICES
PRICE_TYPE_CHOICES = [
    ('free', 'Free'),
    ('paid', 'Paid'),
    ('negotiable', 'Negotiable'),
]

# CATEGORY CHOICES
CATEGORY_CHOICES = [
    ('tutoring', 'Tutoring'),
    ('design', 'Design'),
    ('tech', 'Technology'),
    ('sports', 'Sports'),
    ('music', 'Music'),
    ('language', 'Language'),
    ('fitness', 'Fitness'),
    ('business', 'Business'),
    ('creative', 'Creative'),
    ('other', 'Other'),
]


class Skill(models.Model):
    """
    Model to represent a skill/service that a user offers.
    Connected to Django User model for ownership.
    """
    # Basic Information
    title = models.CharField(
        max_length=200,
        help_text="Name of your skill or service (e.g., 'Python Tutoring')"
    )
    
    description = models.TextField(
        help_text="Detailed description of what you're offering"
    )
    
    # Category of skill
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='other',
        help_text="What category does your skill fall into?"
    )
    
    # Pricing information
    price_type = models.CharField(
        max_length=20,
        choices=PRICE_TYPE_CHOICES,
        default='negotiable',
        help_text="Is your skill free or paid?"
    )
    
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Price (leave blank if free)"
    )
    
    # Contact preferences
    contact_preference = models.CharField(
        max_length=20,
        choices=CONTACT_CHOICES,
        default='email',
        help_text="How should people contact you?"
    )
    
    # Availability
    availability_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        help_text="Are you currently available?"
    )
    
    # Foreign key to User (the person offering the skill)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='skills',
        help_text="The user offering this skill"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']  # Newest skills first
        verbose_name_plural = 'Skills'
    
    def __str__(self):
        """String representation of the skill"""
        return f"{self.title} by {self.owner.username}"


class Review(models.Model):
    """A 1-5 star rating + comment left by a user on a skill."""

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews_written',
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rate from 1 (worst) to 5 (best)",
    )
    comment = models.TextField(
        blank=True,
        help_text="Optional comment about your experience",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        # One review per (skill, author) pair
        constraints = [
            models.UniqueConstraint(
                fields=['skill', 'author'],
                name='unique_review_per_user_per_skill',
            )
        ]

    def __str__(self):
        return f"{self.author.username} → {self.skill.title} ({self.rating}/5)"
