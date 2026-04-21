from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from .models import Skill, Review, CATEGORY_CHOICES
from .forms import CustomUserCreationForm, SkillForm, UserProfileForm, ReviewForm


# ==================== AUTHENTICATION VIEWS ====================

def register(request):
    """
    View for user registration.
    GET: Display registration form
    POST: Create new user account
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('MainApp:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'MainApp/register.html', context)


def login_view(request):
    """
    View for user login.
    GET: Display login form
    POST: Authenticate user
    """
    if request.user.is_authenticated:
        return redirect('MainApp:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('MainApp:home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'MainApp/login.html')


def logout_view(request):
    """
    View for user logout.
    POST: Log out user and redirect to home
    """
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('MainApp:home')


# ==================== SKILL LIST & DETAIL VIEWS ====================

def home(request):
    """
    Home page - display all available skills.
    GET: Show all skills with optional search/filter
    """
    skills = Skill.objects.filter(availability_status='available').select_related('owner')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        skills = skills.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(owner__username__icontains=search_query)
        )
    
    # Filter by category
    category = request.GET.get('category', '')
    if category:
        skills = skills.filter(category=category)
    
    # Use the canonical CATEGORY_CHOICES so the dropdown shows full labels
    # (e.g. "Technology" instead of just "Tech") and stays consistent with the model.
    context = {
        'skills': skills,
        'search_query': search_query,
        'selected_category': category,
        'categories': CATEGORY_CHOICES,
    }
    return render(request, 'MainApp/home.html', context)


def skill_detail(request, pk):
    """
    View to display detailed information about a specific skill,
    plus its reviews and a form for the current user to leave one.
    """
    skill = get_object_or_404(Skill, pk=pk)
    reviews = skill.reviews.select_related('author').all()

    # Aggregate rating stats
    stats = reviews.aggregate(avg=Avg('rating'))
    avg_rating = stats['avg']
    review_count = reviews.count()

    # Has the current user already reviewed this skill?
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(author=request.user).first()

    # Owners cannot review their own skill; everyone else (logged in) can
    can_review = (
        request.user.is_authenticated
        and request.user != skill.owner
        and user_review is None
    )
    review_form = ReviewForm() if can_review else None

    context = {
        'skill': skill,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_count': review_count,
        'review_form': review_form,
        'user_review': user_review,
        'can_review': can_review,
    }
    return render(request, 'MainApp/skill_detail.html', context)


@login_required(login_url='MainApp:login')
def add_review(request, pk):
    """Handle POST of a review form on a skill detail page."""
    skill = get_object_or_404(Skill, pk=pk)

    if skill.owner == request.user:
        messages.error(request, "You can't review your own skill.")
        return redirect('MainApp:skill_detail', pk=pk)

    if Review.objects.filter(skill=skill, author=request.user).exists():
        messages.error(request, "You've already reviewed this skill.")
        return redirect('MainApp:skill_detail', pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.skill = skill
            review.author = request.user
            review.save()
            messages.success(request, 'Thanks for your review!')
        else:
            messages.error(request, 'Please fix the errors in your review.')

    return redirect('MainApp:skill_detail', pk=pk)


@login_required(login_url='MainApp:login')
def delete_review(request, pk):
    """Allow the review's author to delete their own review."""
    review = get_object_or_404(Review, pk=pk)

    if review.author != request.user:
        messages.error(request, 'You can only delete your own review.')
        return redirect('MainApp:skill_detail', pk=review.skill.pk)

    if request.method == 'POST':
        skill_pk = review.skill.pk
        review.delete()
        messages.success(request, 'Review deleted.')
        return redirect('MainApp:skill_detail', pk=skill_pk)

    return redirect('MainApp:skill_detail', pk=review.skill.pk)


# ==================== SKILL CRUD VIEWS ====================

@login_required(login_url='MainApp:login')
def create_skill(request):
    """
    View for creating a new skill post.
    Only logged-in users can create skills.
    GET: Display skill creation form
    POST: Save new skill to database
    """
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = request.user  # Set the current user as owner
            skill.save()
            messages.success(request, 'Skill posted successfully!')
            return redirect('MainApp:skill_detail', pk=skill.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = SkillForm()
    
    context = {'form': form, 'title': 'Post a New Skill'}
    return render(request, 'MainApp/skill_form.html', context)


@login_required(login_url='MainApp:login')
def update_skill(request, pk):
    """
    View for editing an existing skill post.
    Only the skill owner can edit their own skill.
    GET: Display edit form with current data
    POST: Update skill in database
    """
    skill = get_object_or_404(Skill, pk=pk)
    
    # Check if user owns the skill
    if skill.owner != request.user:
        messages.error(request, 'You can only edit your own skills.')
        return redirect('MainApp:skill_detail', pk=pk)
    
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated successfully!')
            return redirect('MainApp:skill_detail', pk=skill.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = SkillForm(instance=skill)
    
    context = {'form': form, 'skill': skill, 'title': 'Edit Skill'}
    return render(request, 'MainApp/skill_form.html', context)


@login_required(login_url='MainApp:login')
def delete_skill(request, pk):
    """
    View for deleting a skill post.
    Only the skill owner can delete their own skill.
    GET: Show confirmation page
    POST: Delete skill from database
    """
    skill = get_object_or_404(Skill, pk=pk)
    
    # Check if user owns the skill
    if skill.owner != request.user:
        messages.error(request, 'You can only delete your own skills.')
        return redirect('MainApp:skill_detail', pk=pk)
    
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted successfully.')
        return redirect('MainApp:dashboard')
    
    context = {'skill': skill}
    return render(request, 'MainApp/skill_confirm_delete.html', context)


# ==================== USER DASHBOARD ====================

@login_required(login_url='MainApp:login')
def dashboard(request):
    """
    User dashboard - displays user's own skills and account info.
    Only accessible to logged-in users.
    """
    user_skills = Skill.objects.filter(owner=request.user).select_related('owner')
    
    # Statistics for dashboard
    total_skills = user_skills.count()
    available_skills = user_skills.filter(availability_status='available').count()
    
    context = {
        'skills': user_skills,
        'total_skills': total_skills,
        'available_skills': available_skills,
    }
    return render(request, 'MainApp/dashboard.html', context)


@login_required(login_url='MainApp:login')
def profile(request):
    """
    View for users to update their profile information.
    GET: Display current profile info
    POST: Update user information
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('MainApp:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {'form': form}
    return render(request, 'MainApp/profile.html', context)