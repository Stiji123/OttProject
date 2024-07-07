from django.urls import path
from .views import home, login_view, register_view, add_profile, profile_selection, profile_list, verify_pin, \
    store_profile_details, ErrorPageView, register_kid_profile, welcome, movie_details, play_video, subscribe_page, \
    subscribe, subscription_success, welcome2_view, going_to_search, KidsWelcomeView, kidsmovie_details, kidsplay_video, \
    subscribe_page1, movie_details2, all_movies, all_kidsmovies, going_to_search_kids, edit_profile, delete_profile

urlpatterns = [
    path('', home, name='home'),  # Updated URL pattern to include 'signup/'
    path('login/',login_view, name='login'),
    path('register_form/', register_view, name='register_form'),
    path('profile_selection/<int:customer_id>/', profile_selection, name='profile_selection'),
    path('add_profile/<int:customer_id>/', add_profile, name='add_profile'),
    path('add_kids_profile/<int:customer_id>/', register_kid_profile, name='add_kids_profile'),
    path('profiles/', profile_list, name='profile_list'),
    path('verify_pin/<int:user_profile_id>/', verify_pin, name='verify_pin'),
    path('store_profile_details/<int:customer_id>/', store_profile_details, name='store_profile_details'),
    path('error/', ErrorPageView.as_view(), name='error_page'),
    path('welcome/', welcome, name='welcome'),
    path('subscribe/', subscribe_page, name='subscribe'),
    path('subscribe/<str:plan>/', subscribe, name='subscribe'),
    path('subscription_success/', subscription_success, name='subscription_success'),
    path('subscribe_page1/<int:movie_id>/', subscribe_page1, name='subscribe_page1'),
    path('welcome2/', welcome2_view, name='welcome2'),
    path('movie_details/<int:movie_id>/', movie_details, name='movie_details'),
    path('movie_details2/<int:movie_id>/', movie_details2, name='movie_details2'),
    path('play_video/<int:movie_id>/', play_video, name='play_video'),
    path('going_to_search/', going_to_search, name='going_to_search'),
    path('going_to_search_kids/', going_to_search_kids, name='going_to_search_kids'),
    path('kids_welcome/<int:kids_profile_id>/', KidsWelcomeView, name='kids_welcome'),
    path('kidsmovie_detail/<int:movie_id>/', kidsmovie_details, name='kidsmovie_details'),
    path('kidsplay_video/<int:movie_id>/', kidsplay_video, name='kidsplay_video'),
    path('all_movies/', all_movies, name='all_movies'),
    path('all_kidsmovies/', all_kidsmovies, name='all_kidsmovies'),
    path('edit_profile/<int:profile_id>/', edit_profile, name='edit_profile'),
    path('delete_profile/<int:profile_id>/', delete_profile, name='delete_profile'),


]