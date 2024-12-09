from django.shortcuts import render,redirect,get_object_or_404
from Manager.models import Tour, Blog
from .forms import UserBookingForm
from .models import UserBooking
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings  # Add this import statement


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

def tour_detail(request, tour_id):
    """
    View to display detailed information about a specific tour.
    """
    tour = get_object_or_404(Tour, id=tour_id)
    return render(request, 'tour/tour_detail.html', {'tour': tour})

def send_booking_confirmation_email(user, tour, booking):
    """
    Sends a booking confirmation email to the user.

    :param user: The user object.
    :param tour: The tour object.
    :param booking: The booking object.
    """
    subject = "Booking Confirmation: Your Tour is Confirmed!"
    message = f"""
    Dear {user.first_name},

    Thank you for booking your tour with Adventure Tourism! We're thrilled to have you join us.

    Here are the details of your booking:

    - Tour Name: {tour.title}
    - From: {booking.date}
    - Number of Travelers: {booking.num_people}
    - Total Amount Paid: ₹{booking.total_price}

    We've received your payment successfully, and your booking is confirmed. Our team will contact you soon with further details.

    If you have any questions, feel free to contact us at support@adventuretourism.com or +91-XXXX-XXXXXX.

    Safe travels,
    The Adventure Tourism Team
    🌍 Explore the world with us
    """
    recipient_email = user.username

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,  # Sender email
        [recipient_email],         # Recipient email
        fail_silently=False,
    )

from django.http import JsonResponse

@login_required
def new_booking(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    user = get_object_or_404(User, username=request.user)

    if request.method == "POST":
        form = UserBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tour = tour  # Assign the selected tour
            booking.user = user  # Assign the current user
            booking.status = 'Confirmed'
            booking.save()  # Save the booking

            # Send confirmation email
            # try:
            #     send_booking_confirmation_email(user, tour, booking)
            # except Exception as e:
            #     # Log the error (optional)
            #     print(f"Failed to send confirmation email: {e}")

            # Handle AJAX requests
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": True, "message": "Booking saved successfully", "id": booking.id})

            # Standard form submission
            return redirect('Tour:booking_success')

        else:
            # Handle AJAX requests for invalid form
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "errors": form.errors}, status=400)

    # Handle GET request
    else:
        form = UserBookingForm()

    return render(request, 'tour/create_booking.html', {'form': form, 'tour': tour, 'user': user})

@login_required
def booking_success(request):
    # Display a success message
    messages.success(request, 'Your booking was successful!')

    # Get the user's bookings ordered by booking date
    user_bookings = UserBooking.objects.filter(user=request.user).order_by('date')

    # Pass the bookings to the template
    return render(request, 'tour/booking_success.html', {'user_bookings': user_bookings})

@login_required
def user_bookings(request):
    # Function to list the bookings of a user.
    user_bookings = UserBooking.objects.filter(user=request.user).order_by('date')

    return render(request, 'tour/user_bookings.html', {'user_bookings': user_bookings})

def blogs(request):
    blogs = Blog.objects.all().order_by('created_at')
    return render(request, 'tour/blogs_list.html', {'blogs': blogs})

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'tour/blog_detail.html', {'blog': blog})