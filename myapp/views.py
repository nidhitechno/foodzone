from django.shortcuts import render,get_object_or_404,reverse
from myapp.models import Contact, Team, Dish, Category,Order ,TableBooking,Newslettersubmit
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect,HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.shortcuts import redirect,render
from .models import Profile
from .models import Order 
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render
from django.core.mail import send_mail
from .models import Contact
from django.conf import settings  # Needed for sending email
from django.utils import timezone


# from django.contrib.auth.decorators import login_required


def custom_logout_view(request):
    logout(request)
    return redirect('login')  

def cancel_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        order.status = False  # assuming True = completed, False = cancelled
        order.save()
    return redirect('dashboard') # Replace with your desired redirect




def index(request):
    return render(request,'index.html')

     
def about(request):
    return render(request, 'about.html')

def signin(request):
    context={}
    if request.method=="POST":
        email = request.POST.get('email')
        passw = request.POST.get('password')

        check_user = authenticate(username=email, password=passw)
        if check_user:
            login(request, check_user)
            if check_user.is_superuser or check_user.is_staff:
                return HttpResponseRedirect('/admin')
            return HttpResponseRedirect('/dashboard')
        else:
            context.update({'message':'Invalid Login Details!','class':'alert-danger'})

    return render(request,'login.html', context)

def team_members(request):
    context={}
    members = Team.objects.all().order_by('name')
    context['team_members'] = members
    return render(request,'team.html', context)

def all_dishes(request):
    context={}
    dishes = Dish.objects.all()
    if "q" in request.GET:
        id = request.GET.get("q")
        dishes = Dish.objects.filter(category__id=id)
        context['dish_category'] = Category.objects.get(id=id).name 

    context['dishes'] = dishes
    return render(request,'all_dishes.html', context)
 

def register(request):
    context = {}

    if request.method == "POST":
        # Fetch data from the HTML form
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        contact = request.POST.get('number')

        # Check if a user with this email already exists
        check = User.objects.filter(username=email)

        if len(check) == 0:
            # Create the user
            usr = User.objects.create_user(username=email, email=email, password=password)
            usr.first_name = name
            usr.save()

            # Create the profile associated with the user
            profile, created = Profile.objects.get_or_create(user=usr)
            profile.contact_number = contact
            profile.save()

            context['status'] = f"User {name} Registered Successfully!"
        else:
            context['status'] = "A User with this email already exists"

    return render(request, 'register.html', context)
    
def contact_view(request):
    return render(request, 'contact.html')


def check_user_exists(request):
    email = request.GET.get('usern')
    check = User.objects.filter(username=email)
    if len(check)==0:
        return JsonResponse({'status':0,'message':'Not Exist'})
    else:
        return JsonResponse({'status':1,'message':'A user with this email already exists!'})


# @login_required
def dashboard(request):
    context = {}
    login_user = get_object_or_404(User, id=request.user.id)
    profile = Profile.objects.get_or_create(user=request.user)
    profile = Profile.objects.get(user__id=request.user.id)
    context['profile'] = profile


    #update profile
    if "update_profile" in request.POST:
        print("file=",request.FILES)
        name = request.POST.get('name')
        contact = request.POST.get('contact_number')
        add = request.POST.get('address')
       
        # profile = request.user
        # profile.user.first_name = name 
        # profile.user.save()
        # profile.contact_number = contact 
        # profile.address = add 
          

        user = request.user
        user.first_name = name
        user.save()

        profile = user.profile
        profile.contact_number = contact
        profile.address = add
        profile.save()
  

        if "profile_pic" in request.FILES:
            pic = request.FILES['profile_pic']
            profile.profile_picture = pic
        profile.save()
        context['status'] = 'Profile updated successfully!'
    
    #Change Password 
    if "change_pass" in request.POST:
        c_password = request.POST.get('current_password')
        n_password = request.POST.get('new_password')

        check = login_user.check_password(c_password)
        if check==True:
            login_user.set_password(n_password)
            login_user.save()
            login(request, login_user)
            context['status'] = 'Password Updated Successfully!' 
        else:
            context['status'] = 'Current Password Incorrect!'

    #My Orders 
    orders = Order.objects.filter(customer__user__id=request.user.id,status=True).order_by('-id')
    context['orders']=orders    
    return render(request, 'dashboard.html', context)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('login')

def user_logout(request):
    if request.method in ['GET', 'POST']:
        logout(request)
        return redirect('home')
    return HttpResponseNotAllowed(['GET', 'POST'])

def custom_logout_view(request):
    logout(request)
    return redirect('login')  

def single_dish(request, id):
    context={}
    dish = get_object_or_404(Dish, id=id)

    if request.user.is_authenticated:
        cust = get_object_or_404(Profile, user__id = request.user.id)
        order = Order(customer=cust, item=dish, status=True)
        order.save()
        inv = f'INV0000-{order.id}'

        paypal_dict = {
            'business':settings.PAYPAL_RECEIVER_EMAIL,
            'amount':dish.discount_price,
            'item_name':dish.name,
            'user_id':request.user.id,
            'invoice':inv,
            'notify_url':'http://{}{}'.format(settings.HOST, reverse('paypal-ipn')),
            'return_url':'http://{}{}'.format(settings.HOST,reverse('payment_done')),
            'cancel_url':'http://{}{}'.format(settings.HOST,reverse('payment_cancel')),
        }

        order.invoice_id = inv 
        order.save()
        request.session['order_id'] = order.id

        form = PayPalPaymentsForm(initial=paypal_dict)
        context.update({'dish':dish, 'form':form})

    return render(request,'dish.html', context)

def payment_done(request):
#     pid = request.GET.get('PayerID')
#     order_id = request.session.get('order_id')
#     order_obj = Order.objects.get(id=order_id)
#     order_obj.status=True 
#     order_obj.payer_id = pid
#     order_obj.save()

    return render(request, 'payment_successfull.html') 

def payment_cancel(request):
    return render(request, 'payment_faield.html') 

def menu_view(request):
    return render(request, 'menu.html')  # assuming you have a template named menu.html

def booking(request):
    return render(request, 'booking.html')

def booking_blog(request):
    return render(request, 'booking/blog.html')

def feature(request):
    return render(request, 'feature.html')



def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        date_str = request.POST.get('date')  # e.g., '04/16/2025'
        time_str = request.POST.get('time')  # e.g., '3:50 PM'
        guests = request.POST.get('guests')

        try:
            # Convert to Python date object
            date = datetime.strptime(date_str, '%m/%d/%Y').date()
            # Convert to Python time object
            time = datetime.strptime(time_str, '%I:%M %p').time()  # 12-hour format with AM/PM
        except ValueError:
            return render(request, 'index.html', {'error': 'Invalid date or time format.'})

        TableBooking.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            date=date,
            time=time,
            guests=guests
        )

        return render(request, 'index.html')

    return render(request, 'index.html') # redirect to a success URL or page



def sendInuery(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if not message:
            return render(request, 'index.html', {'error': 'Please enter a message.'})

        # Save to database
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        try:
            # Send email
            send_mail(
                subject,
                f"Message from {name} ({email}):\n\n{message}",
                settings.DEFAULT_FROM_EMAIL,  # From email (configured in settings.py)
                ['receiver@example.com'],     # Replace with your recipient
                fail_silently=False,
            )
            return render(request, 'index.html', {'success': 'Thanks for contacting us! We\'ve received your message.'})
        except Exception as e:
            return render(request, 'index.html', {'error': f'Sorry {name}, we couldn’t send your message. Please try again later.'})

    return render(request, 'index.html')

def Contact_us(request):
    if request.method == "POST":
        name = request.POST.get("name")
        em = request.POST.get("email")
        sub = request.POST.get("subject")
        msz = request.POST.get("message", "")  # Default to an empty string if no message is provided
       
        # Ensure that the message is not None or empty
        if not msz:
            return HttpResponse("Please provide a message.")

        obj = Contact(name=name, email=em, subject=sub, message=msz)
        obj.save()
        return HttpResponse(f"Dear {name}, Thanks For Your Time!")
    print("test")
    return render(request, 'contact.html')
 

def success_page(request):
    return render(request, 'success.html')



def buy_now(request, id):
    dish = get_object_or_404(Dish, id=id)

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    cust = get_object_or_404(Profile, user=request.user)
    order = Order(customer=cust, item=dish)
    order.save()

    inv = f'INV0000-{order.id}'
    paypal_dict = {
    'business': 'sb-iqthi27171988@business.example.com',
    'amount': '10.00',
    'item_name': dish.name,
    'invoice': inv,
    "currency_code": "USD",
    'notify_url': 'https://3361-103-76-141-163.ngrok-free.app/paypal/ipn/',
    'return_url': 'https://3361-103-76-141-163.ngrok-free.app/payment-done/',
    'cancel_return': 'https://3361-103-76-141-163.ngrok-free.app/payment-cancelled/',
    'custom': str(request.user.id),
}

    order.invoice_id = inv
    order.save()

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'redirect_to_paypal.html', {'form': form})

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def Terms_conditions(request):
    return render(request,'Terms_conditions.html')

def help_center(request):
    return render(request,'help_center.html')

def submit_newsletter(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if Newslettersubmit.objects.filter(email=email).exists():
            messages.warning(request, "You're already subscribed with this email!")
        else:
            Newslettersubmit.objects.create(
                email=email,
                submit_at=timezone.now()
            )
            messages.success(request, "Thanks for subscribing!")
        return render(request, 'index.html')
    
