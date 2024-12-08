from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView
from .models import Blog, Tour, Booking, Review
from .forms import BookingForm, ReviewForm, CreateTourForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from Tour.models import UserBooking

from user.models import ClientDetails


#from Tour import tour_list


# Booking List View


@login_required
def manager_home(request):
    user = get_object_or_404(ClientDetails, email=request.user)
    if user.is_manager:
        return render(request, 'manager/home.html')
    return render(request, 'user/no_access.html')

# Review Create View
@login_required
def create_review(request, tour_id):
    user = get_object_or_404(ClientDetails, email=request.user)
    if user.is_manager:
        tour = get_object_or_404(Tour, id=tour_id)
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.tour = tour
                review.save()
                return redirect('manager:tour_detail', pk=tour.id)
        else:
            form = ReviewForm()
        return render(request, 'manager/review_form.html', {'form': form, 'tour': tour})
    return render(request, 'user/no_access.html')

@login_required
def tour_list(request):
    user = get_object_or_404(ClientDetails, email=request.user)
    if user.is_manager:
        tours = Tour.objects.all()
        return render(request, 'manager/tour_list.html', {'tours': tours})
    return render(request, 'user/no_access.html')

@login_required
# Tour Detail View (to show details and associated reviews)
def tour_detail(request, pk):
    user = get_object_or_404(ClientDetails, email=request.user)
    if user.is_manager:
        tour = get_object_or_404(Tour, pk=pk)
        reviews = tour.reviews.all()
        return render(request, 'manager/tour_detail.html', {'tour': tour, 'reviews': reviews})
    return render(request, 'user/no_access.html')

@login_required
def create_tour(request):
    user = get_object_or_404(ClientDetails, email=request.user)
    if user.is_manager:
        try:
            if request.method == 'POST':
                title = request.POST.get('title', '')
                description = request.POST.get('description', '')
                location = request.POST.get('location', '')
                adventure_type = request.POST.get('adventure_type', '')
                price = request.POST.get('price', '')
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                max_group_size = request.POST.get('max_group_size', '')
                itinerary = request.POST.get('itinerary', '')
                image = request.FILES.get('image')

                # Validate required fields and save the tour
                if title and description and location and price and start_date and end_date:
                    tour = Tour(
                        title=title,
                        description=description,
                        location=location,
                        adventure_type=adventure_type,
                        price=price,
                        start_date=start_date,
                        end_date=end_date,
                        max_group_size=max_group_size,
                        itinerary=itinerary,
                        image=image,
                        created_by=request.user
                    )
                    tour.save()
                    return redirect('manager:tour_list')
            else:
                return render(request, 'manager/create_tour.html', {'location_choices': Tour.LOCATION_CHOICES, 'adventure_choices': Tour.ADVENTURE_CHOICES})
        except Exception as e:
            return render(request, 'manager/create_tour.html', {'error': e, 'location_choices': Tour.LOCATION_CHOICES, 'adventure_choices': Tour.ADVENTURE_CHOICES})
    return render(request, 'user/no_access.html')

@login_required
def edit_tour(request, pk):
    user = get_object_or_404(ClientDetails, email=request.user)
    if user.is_manager:
        tour = get_object_or_404(Tour, pk=pk)
        if request.method == 'POST':
            # Get the updated values from the POST request
            tour.title = request.POST.get('title', tour.title)
            tour.description = request.POST.get('description', tour.description)
            tour.location = request.POST.get('location', tour.location)
            tour.adventure_type = request.POST.get('adventure_type', tour.adventure_type)
            tour.price = request.POST.get('price', tour.price)
            tour.start_date = request.POST.get('start_date', tour.start_date)
            tour.end_date = request.POST.get('end_date', tour.end_date)
            tour.max_group_size = request.POST.get('max_group_size', tour.max_group_size)
            tour.itinerary = request.POST.get('itinerary', tour.itinerary)

            # Handle image update
            if 'image' in request.FILES:
                tour.image = request.FILES['image']

            # Save the updated tour object
            tour.save()

            # Redirect to the tour list after saving
            return redirect('manager:tour_list')
        return render(request, 'manager/edit_tour.html', {'tour': tour, 'location_choices': Tour.LOCATION_CHOICES, 'adventure_choices': Tour.ADVENTURE_CHOICES})
    return render(request, 'user/no_access.html')

@login_required
def delete_tour(request, pk):
    user = get_object_or_404(ClientDetails, email=request.user)
    if user.is_manager:
        tour = get_object_or_404(Tour, pk=pk)
        tour.delete()
        return redirect('manager:tour_list')
    return render(request, 'user/no_access.html')

class BookingListView(ListView):
    model = UserBooking
    template_name = 'manager/booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return UserBooking.objects.all()

# Booking Create View
@login_required
def create_booking(request, tour_id):
    user = get_object_or_404(ClientDetails, email=request.user)
    if user.is_manager:
        tour = get_object_or_404(Tour, id=tour_id)
        status_choices = UserBooking._meta.get_field('status').choices
        users = ClientDetails.objects.filter(is_manager=False)
        if request.method == 'POST':
            form = BookingForm(request.POST)
            user = ClientDetails.objects.get(email=request.POST.get('user'))
            if form.is_valid():
                booking = form.save(commit=False)
                booking.user = user.id
                booking.tour = tour
                booking.total_price = booking.calculate_total_price()
                booking.save()
                return redirect('manager:booking_list')
        else:
            form = BookingForm()
        return render(request, 'manager/booking_form.html', {
            'form': form, 'tour': tour, 'users':users, 'status_choices': status_choices
        })
    return render(request, 'user/no_access.html')

@login_required
def edit_booking(request, pk):
    user = get_object_or_404(ClientDetails, email=request.user)
    if user.is_manager:
        booking = get_object_or_404(UserBooking, id=pk)
        status_choices = UserBooking._meta.get_field('status').choices  # Fetch status choices dynamically
        users = ClientDetails.objects.filter(is_manager=False) # Fetch all users

        if request.method == 'POST':
            user = User.objects.get(username=request.POST['user'])
            # Update booking data with POST values
            booking.user = user  # Get selected user
            booking.date = request.POST['date']
            booking.num_people = request.POST['num_people']
            booking.status = request.POST['status']
            booking.total_price = int(booking.num_people) * booking.tour.price  # Recalculate total price
            booking.save()

            return redirect('manager:booking_list')

        return render(request, 'manager/edit_booking.html', {
            'booking': booking,
            'users': users,
            'status_choices': status_choices,
        })
    return render(request, 'user/no_access.html')

@login_required
def delete_booking(request, pk):
    user = get_object_or_404(ClientDetails, email=request.user)
    if user.is_manager:
        booking = get_object_or_404(UserBooking, pk=pk)
        booking.delete()
        return redirect('manager:booking_list')
    return render(request, 'user/no_access.html')

@login_required
def users_list(request):
    user = get_object_or_404(ClientDetails, email=request.user)
    if user.is_manager:
        Users = ClientDetails.objects.all()
        return render(request, 'manager/users_list.html', {'Users': Users})
    return render(request, 'user/no_access.html')

@login_required
def add_user(request):
    user = get_object_or_404(ClientDetails, email=request.user)
    if user.is_manager:
        try:
            if request.method=='POST':
                f_name = request.POST.get('c_fname')
                l_name = request.POST.get('c_lname')
                mail = request.POST.get('c_email')
                contact = request.POST.get('c_phone')
                password = request.POST.get('c_password')
                cpassword = request.POST.get('c_repassword')
                address = request.POST.get('c_address')
                photo = request.FILES.get('c_image')
                is_manager = request.POST.get('is_manager', 'false')

                if password==cpassword:
                    if User.objects.filter(username=mail).exists():
                        messages.info(request,'email already exists')

                    else:
                        user=User.objects.create_user(username=mail,password=password)
                        customer=ClientDetails(id=user,first_name=f_name,last_name=l_name,phone=contact,
                                                email=mail,address=address, photo=photo)
                        if is_manager=='true':
                            customer.is_manager=True

                        user.save()
                        customer.save()
                        return redirect('manager:users_list')
                else:
                    messages.info(request,'password mismatch')
            return render(request, 'manager/add_user.html', {})
        except Exception as e:
            return render(request, 'manager/add_user.html', {})
    return render(request, 'user/no_access.html')


@login_required
def delete_user(request, pk):
    user = get_object_or_404(ClientDetails, email=request.user)
    if user.is_manager:
        user = get_object_or_404(User, pk=pk)
        client_user = get_object_or_404(ClientDetails, id=user)
        client_user.delete()
        return redirect('manager:users_list')
    return render(request, 'user/no_access.html')

@login_required
def blog_list(request):
    user = get_object_or_404(ClientDetails, email=request.user)
    if user.is_manager:
        blogs = Blog.objects.all()
        return render(request, 'manager/blogs_list.html', {'blogs': blogs})
    return render(request, 'user/no_access.html')

@login_required
def create_blog(request):
    user = get_object_or_404(ClientDetails, email=request.user)
    if user.is_manager:
        if request.method=='POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            author = request.POST.get('author')
            image = request.FILES.get('image')

            Blog.objects.create(
                title=title,
                content=content,
                author_name=author,
                image=image
            )
            return redirect('manager:blog_list')
        else:
            return render(request, 'manager/create_blog.html')
    return render(request, 'user/no_access.html')

@login_required
def edit_blog(request, pk):
    user = get_object_or_404(ClientDetails, email=request.user)
    if user.is_manager:
        blog = get_object_or_404(Blog, pk=pk)

        if request.method == 'POST':
            # Update the blog details
            blog.title = request.POST.get('title')
            blog.content = request.POST.get('content')
            blog.author_name = request.POST.get('author')

            # Update the image only if a new one is uploaded
            image = request.FILES.get('image')
            if image:
                blog.image = image

            blog.save()
            return redirect('manager:blog_list')  # Redirect to the blog list or another page

        # Pass the blog object to pre-fill the form
        return render(request, 'manager/edit_blog.html', {'blog': blog})
    return render(request, 'user/no_access.html')

@login_required
def delete_blog(request, pk):
    user = get_object_or_404(ClientDetails, email=request.user)
    if user.is_manager:
        blog = get_object_or_404(Blog, pk=pk)
        blog.delete()
        return redirect('manager:blog_list')
    return render(request, 'user/no_access.html')
