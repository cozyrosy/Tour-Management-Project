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
            form = CreateTourForm(request.POST, request.FILES)
            if form.is_valid():
                tour = form.save(commit=False)
                import pdb; pdb.set_trace()
                tour.created_by = request.user
                # tour.image = request./FILES.get('image', None)
                tour.save()
                return redirect('manager:tour_list')
        else:
            form = CreateTourForm()
        return render(request, 'manager/create_tour.html', {'form': form})
    except Exception as e:
        return render(request, 'manager/create_tour.html', {'error': e})

@login_required
def edit_tour(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    if request.method == 'POST':
        return redirect('manager:tour_list')

@login_required
def delete_tour(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    tour.delete()
    return redirect('manager:tour_list')