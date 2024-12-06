from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
from .models import Tour, Booking, Review
from .forms import BookingForm, ReviewForm, CreateTourForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from Tour.models import UserBooking
#from Tour import tour_list


# Booking List View


@login_required
def manager_home(request):
    return render(request, 'manager/home.html')

class BookingListView(ListView):
    model = UserBooking
    template_name = 'manager/booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return UserBooking.objects.all()

# Booking Create View
@login_required
def create_booking(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.tour = tour
            booking.total_price = booking.num_of_people * tour.price
            booking.save()
            return redirect('manager:booking_list')
    else:
        form = BookingForm()
    return render(request, 'manager/booking_form.html', {'form': form, 'tour': tour})

# Review Create View
@login_required
def create_review(request, tour_id):
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

@login_required
def tour_list(request):
    tours = Tour.objects.all()
    return render(request, 'manager/tour_list.html', {'tours': tours})

@login_required
# Tour Detail View (to show details and associated reviews)
def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    reviews = tour.reviews.all()
    return render(request, 'manager/tour_detail.html', {'tour': tour, 'reviews': reviews})

@login_required
def create_tour(request):
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

@login_required
def edit_tour(request, pk):
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

@login_required
def delete_tour(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    tour.delete()
    return redirect('manager:tour_list')

@login_required
def delete_booking(request, pk):
    booking = get_object_or_404(UserBooking, pk=pk)
    booking.delete()
    return redirect('manager:booking_list')