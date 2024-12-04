from django.shortcuts import render,redirect,get_object_or_404
from Manager.models import Tour
from .forms import UserBookingForm
from .models import UserBooking
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def Contact(request):
    return render(request,'Tour/contact.html')

def tour_list(request):
    tours = Tour.objects.all()  # Fetch all tours
    return render(request, 'Tour/tour_list.html', {'tours': tours})

#def user_tour_detail(request, pk):
    #tour = get_object_or_404(Tour, pk=pk)
    #return render(request, 'Tour/tour_detail.html', {'tour': tour})



# List all bookings for the logged-in user
@login_required
def user_booking_list(request):
    bookings = UserBooking.objects.filter(user=request.user)
    return render(request, 'tour/user_booking_list.html', {'bookings': bookings})



@login_required
def tour_detail(request, tour_id):
    """
    View to display detailed information about a specific tour.
    """
    tour = get_object_or_404(Tour, id=tour_id)
    return render(request, 'tour/tour_detail.html', {'tour': tour})



def create_booking(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)

    if request.method == "POST":
        form = UserBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tour = tour  # Assign the selected tour
            booking.user = request.user  # Assign the current user
            booking.save()  # This will automatically calculate and save total_price
            return redirect('Tour:booking_success')  # Use the correct namespace
    else:
        form = UserBookingForm()

    return render(request, 'tour/create_booking.html', {'form': form, 'tour': tour})

def booking_success(request):
    # Display a success message
    messages.success(request, 'Your booking was successful!')

    # Get the user's bookings ordered by booking date
    user_bookings = UserBooking.objects.filter(user=request.user).order_by('date')

    # Pass the bookings to the template
    return render(request, 'tour/booking_success.html', {'user_bookings': user_bookings})

def user_bookings(request):
    # Function to list the bookings of a user.
    user_bookings = UserBooking.objects.filter(user=request.user).order_by('date')

    return render(request, 'tour/user_bookings.html', {'user_bookings': user_bookings})