from datetime import timedelta

from django.contrib.auth.views import LoginView
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,authenticate
from django.utils import timezone

from .forms import LoginForm, CustomerRegistrationForm, ProfileForm, VerifyPinForm, KidProfileForm, SearchForm
from .models import Customer, UserProfile, KidsProfile, Adult_Movie,Kids_Movie  # Corrected model name to follow PEP8 conventions
from django.views.generic import TemplateView


def login_view(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                customer = Customer.objects.get(username=username)
                if customer.password == password:
                    customer_id = customer.id
                    return redirect( 'profile_selection',customer_id = customer_id)
                else:
                    form.add_error(None, 'Invalid credentials')
            except Customer.DoesNotExist:
                form.add_error(None, 'User not found')

    return render(request, 'registration/login.html',{'form':form})

def register_view(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to a success page
    else:
        form = CustomerRegistrationForm()

    return render(request, 'register_form.html', {'form': form})


def home(request):
    return render(request,'home.html')

# views.py
def profile_selection(request, customer_id):
    customer = Customer.objects.get(id=customer_id)

    # Fetch adult profiles
    adult_profiles = UserProfile.objects.filter(user=customer)

    # Fetch kids' profiles
    kids_profiles = KidsProfile.objects.filter(user=customer)

    return render(request, 'profiles/profile_selection.html', {
        'customer': customer,
        'adult_profiles': adult_profiles,
        'kids_profiles': kids_profiles,
    })




def profile_list(request):
    profiles = UserProfile.objects.all()
    return render(request, 'welcome.html', {'profiles': profiles})

import hmac

def verify_pin(request, user_profile_id):
    template_name = 'profiles/verify_pin.html'

    user_profile = get_object_or_404(UserProfile, id=user_profile_id)

    if request.method == 'POST':
        form = VerifyPinForm(request.POST)
        if form.is_valid():
            provided_pin = form.cleaned_data['pin']
            stored_pin = user_profile.pin

            # Use constant-time comparison to mitigate timing attacks
            if hmac.compare_digest(provided_pin, stored_pin):
                print("PIN is correct. Redirecting to welcome page.")
                return redirect('welcome')
            else:
                form.add_error('pin', 'Invalid PIN')
                print(f'Invalid PIN: {form.errors}')
        else:
            print(f'Invalid form: {form.errors}')
    else:
        form = VerifyPinForm()

    return render(request, template_name, {'form': form, 'user_profile': user_profile})


class ErrorPageView(TemplateView):
    template_name = 'profiles/error.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error_message'] = "You can create a maximum of 4 profiles only."
        return context

# Your existing imports and views

def add_profile(request, customer_id):
    template_name = 'profiles/add_profile.html'

    customer = get_object_or_404(Customer, id=customer_id)

    # Check the number of existing profiles for the customer
    existing_profiles_count = UserProfile.objects.filter(user=customer).count()

    # Check if the limit has been reached
    limit_reached = existing_profiles_count >= 4

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and not limit_reached:
            # Create a UserProfile instance but don't save it yet
            profile = form.save(commit=False)

            # Associate the profile with the customer
            profile.user = customer

            # Save the profile to the database
            profile.save()

            # Fetch the list of profiles again
            profiles = UserProfile.objects.filter(user=customer)

            # Redirect to a success page or any other desired page
            return redirect('profile_selection', customer_id=customer.id)
        else:
            form.add_error('image', 'Invalid avatar choice')  # Handle invalid choice

    else:
        form = ProfileForm()

    if limit_reached:
        error_message = "You can create a maximum of 4 profiles only."
        return render(request, 'profiles/error.html', {'error_message': error_message})

    return render(request, template_name, {'form': form, 'limit_reached': limit_reached})

def store_profile_details(request, customer_id):
    customer = Customer.objects.get(id=customer_id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a UserProfile instance but don't save it yet
            profile = form.save(commit=False)

            # Associate the profile with the customer
            profile.customer = customer

            # Save the profile to the database
            profile.save()



            # Redirect to a success page or any other desired page
            return redirect('profile_selection', customer_id=customer.id)
        else:
            form.add_error('image', 'Invalid avatar choice')  # Handle invalid choice
    else:
        form = ProfileForm()

    return render(request, 'add_profile.html', {'customer': customer, 'form': form})

# views.py
# views.py
def register_kid_profile(request, customer_id):
    template_name = 'profiles/add_kids_profile.html'

    customer = Customer.objects.get(id=customer_id)

    # Check if the limit for kid profiles has been reached
    kid_profiles_limit = 2  # Set the desired limit for kid profiles
    kid_profiles_count = KidsProfile.objects.filter(user=customer).count()

    if kid_profiles_count >= kid_profiles_limit:
        error_message = f"You can create a maximum of {kid_profiles_limit} kid profiles only."
        return render(request, 'profiles/error.html', {'error_message': error_message})

    if request.method == 'POST':
        form = KidProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a KidsProfile instance but don't save it yet
            kid_profile = form.save(commit=False)

            # Associate the kid profile with the customer
            kid_profile.user = customer

            # Save the kid profile to the database
            kid_profile.save()

            # Redirect to a success page or any other desired page
            return redirect('profile_selection', customer_id=customer.id)
        else:
            form.add_error('image', 'Invalid avatar choice')  # Handle invalid choice
    else:
        form = KidProfileForm()

    return render(request, template_name, {'customer': customer, 'form': form})


def welcome2_view(request):
    adult_movies = Adult_Movie.objects.all()
    recent_movies = Adult_Movie.objects.filter(release_date__gte=(timezone.now() - timedelta(days=3))).order_by('-release_date')
    print(recent_movies)
    return render(request, 'welcome2.html', {'adult_movies': adult_movies,'recent_movies': recent_movies})


def movie_details(request, movie_id):
    movie = get_object_or_404(Adult_Movie, pk=movie_id)
    return render(request, 'movie_detail.html', {'movie': movie})

def movie_details2(request, movie_id):
    movie = get_object_or_404(Adult_Movie, pk=movie_id)
    return render(request, 'movie_detail2.html', {'movie': movie})

def play_video(request, movie_id):
    movie = get_object_or_404(Adult_Movie, pk=movie_id)
    return render(request, 'play_video.html', {'movie': movie})

def KidsWelcomeView(request, kids_profile_id):
    kids_movies = Kids_Movie.objects.all()
    recent_movies = Kids_Movie.objects.filter(release_date__gte=(timezone.now() - timedelta(days=3))).order_by('-release_date')
    print(recent_movies)
    return render(request, 'kids_welcome.html', {'kids_movies': kids_movies, 'recent_movies': recent_movies})


def kidsmovie_details(request, movie_id):
    movie = get_object_or_404(Kids_Movie, pk=movie_id)
    return render(request, 'kidsmovie_detail.html', {'movie': movie})


def kidsplay_video(request, movie_id):
    movie = get_object_or_404(Kids_Movie, pk=movie_id)
    return render(request, 'kidsplay_video.html', {'movie':movie})

def subscribe_page(request):
    return render(request, 'subscribe.html')

def subscribe_page1(request, movie_id):
    return render(request, 'subscribe.html', {'movie_id': movie_id})

def subscribe(request, plan):
    # Simulate a subscription process (replace this with your actual logic)
    print(f'Simulating subscription process for plan: {plan}')

    # Redirect to the subscription success page after a brief delay (adjust the delay as needed)
    return redirect('subscription_success')

def subscription_success(request):
    return render(request, 'subscription_successfull.html')

def welcome(request):
    # Any additional logic you want to include in the view
    adult_movies=Adult_Movie.objects.all()
    recent_movies = Adult_Movie.objects.filter(release_date__gte=(timezone.now() - timedelta(days=3))).order_by('-release_date')
    print(recent_movies)
    return render(request, 'welcome.html', {'adult_movies': adult_movies,'recent_movies': recent_movies})

def all_movies(request):
    all_movies = Adult_Movie.objects.all()
    return render(request, 'all_movies.html', {'all_movies': all_movies})

def all_kidsmovies(request):
    all_kidsmovies = Kids_Movie.objects.all()
    return render(request, 'all_kidsmovies.html', {'all_kidsmovies': all_kidsmovies})


def going_to_search(request):
    # Handle search form submission
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['search_query']
            # Add your search logic here if needed
            # For example, you can filter movies based on the search query
            search_results = Adult_Movie.objects.filter(title__icontains=query)
            # Add search results to the context
            context = {'search_results': search_results, 'form': form}
            return render(request, 'search_page.html', context)

    # If it's not a search submission or the form is not valid, display the page with placeholder data
    random_movies = Adult_Movie.objects.annotate(num_views=Count('movie_views')).order_by('?')[:6]
    recent_movies = Adult_Movie.objects.order_by('-release_date')[:6]
    all_movies = Adult_Movie.objects.all()[:10]
    all_series = Adult_Movie.objects.filter(type='series')[:6]
    form = SearchForm()

    context = {
        'recent_movies': recent_movies,
        'all_movies': all_movies,
        'all_series': all_series,
        'random_movies': random_movies,
        'form': form,
        # Add other data to the context as needed
    }

    return render(request, 'search_page.html', context)


def going_to_search_kids(request):
    # Handle search form submission
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['search_query']
            # Add your search logic here if needed
            # For example, you can filter movies based on the search query
            search_results = Kids_Movie.objects.filter(title__icontains=query)
            # Add search results to the context
            context = {'search_results': search_results, 'form': form}
            return render(request, 'search_kidspage.html', context)

    # If it's not a search submission or the form is not valid, display the page with placeholder data
    random_movies = Kids_Movie.objects.annotate(num_views=Count('movie_views')).order_by('?')[:6]
    recent_movies = Kids_Movie.objects.order_by('-release_date')[:6]
    all_movies = Kids_Movie.objects.all()[:10]
    all_series = Kids_Movie.objects.filter(type='series')[:6]
    form = SearchForm()

    context = {
        'recent_movies': recent_movies,
        'all_movies': all_movies,
        'all_series': all_series,
        'random_movies': random_movies,
        'form': form,
        # Add other data to the context as needed
    }

    return render(request, 'search_kidspage.html', context)

def edit_profile(request, profile_id):
    profile = UserProfile.objects.get(pk=profile_id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            # Extract the customer_id from the profile object
            customer_id = profile.user.id

            # Redirect to the profile selection page with the customer_id parameter
            return redirect('profile_selection', customer_id=customer_id)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profiles/edit_profile.html', {'form': form})

def delete_profile(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)

    if request.method == 'POST':
        profile.delete()

        # Extract the customer_id from the profile object
        customer_id = profile.user.id

        # Redirect to the profile selection page with the customer_id parameter
        return redirect('profile_selection', customer_id=customer_id)

    return render(request, 'profiles/delete_profile.html', {'profile': profile})