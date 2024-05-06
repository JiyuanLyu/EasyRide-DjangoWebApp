from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

from .models import Ride, User, Vehicle, RideSharer
from django.db.models import Sum
from .forms import RideRequestForm, UserFrom, VehicleForm, LoginForm, SharerRequestForm, SharerEditForm, EditUserForm, EditDriverForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def main_page(request):
    is_driver = False
    if request.user.is_authenticated:
        is_driver = User.objects.filter(user_name=request.user).values_list('is_driver')[0][0]
    return render(request, 'main_page.html', {'is_driver': is_driver})
    # is_driver = User.objects.filter(user_name=request.user).values_list('is_driver')[0][0]
    # return render(request, 'main_page.html', {'is_driver': is_driver})

def profile_page(request):
    is_driver = False
    vehicle_info = None  
    if request.user.is_authenticated:
        is_driver = request.user.is_driver
        if is_driver:
            try:
                vehicle_info = Vehicle.objects.get(driver=request.user)
            except Vehicle.DoesNotExist:
                vehicle_info = None
    
    return render(request, 'profile.html', {
        'is_driver': is_driver,
        'vehicle_info': vehicle_info,
    })
@csrf_exempt
def Login(request):
    error_message = None  # Initialize error message
    if request.method == 'POST':
        user_login_form = LoginForm(request.POST)
        if user_login_form.is_valid():
            user_name = user_login_form.cleaned_data['user_name']  # Make sure your form has a field for this
            password = user_login_form.cleaned_data['password']
            if not User.objects.exclude(pk=request.user.pk).filter(user_name=user_name).exists():
                messages.error(request, 'Username does not exist.')
                return redirect('main_page')
            test_user = User.objects.get(user_name=user_name)
            if test_user.password == password:
                login(request, test_user)  # Log the user in
                return redirect('main_page')
            else:
                error_message = 'Invalid account'  # Either username or password is incorrect

    else:
        user_login_form = LoginForm()

    return render(request, 'login.html', {'form': user_login_form, 'error_message': error_message})




def logout_view(request):
    logout(request)
    return redirect('main_page')

    # # Retrieve the user_id from the current session
    # id = request.session['user_id']
    # print("user id: ", id)
    # # Check if user_id exists in the session
    # if id is not None:
    #     # Print or use the user_id as needed
    #     print(f"Logging out user_id: {id}")
        
    #     # Delete the user_id from the session
    #     del request.session['id']
        
    #     # Mark the session as modified to make sure it gets saved
    #     request.session.modified = True
    
    # # Redirect to a page (e.g., main_page) after logout
    # return redirect('main_page')


# def user_request(request):
#     if request.method == 'POST':
#         user_request_form = UserFrom(request.POST)
#         if user_request_form.is_valid():
#             user = User(
#                 email_address=user_request_form.cleaned_data['email_address'],
#                 user_name=user_request_form.cleaned_data['user_name'],
#                 password=user_request_form.cleaned_data['password'],

#             )
#             # user.set_password(password)
#             user.save()
#             messages.info(request, 'Your profile has been uploaded successfully!')
#             ##new page
#             return redirect('main_page')
        
#     else:
#         user_request_form = UserFrom()

#     context = {'user_request_form': user_request_form}
#     return render(request, 'user_request.html', context)

@csrf_exempt
def user_request(request):
    if request.method == 'POST':
        user_request_form = UserFrom(request.POST)
        if user_request_form.is_valid():
            email_address = user_request_form.cleaned_data['email_address']
            user_name = user_request_form.cleaned_data['user_name']
            
            # Check if the email address is already in use
            if User.objects.exclude(pk=request.user.pk).filter(email_address=email_address).exists():
                messages.error(request, 'Email address already in use.')
                return render(request, 'user_request.html', {'user_request_form': user_request_form})

            # Check if the username already exists
            if User.objects.exclude(pk=request.user.pk).filter(user_name=user_name).exists():
                messages.error(request, 'Username already in use.')
                return render(request, 'user_request.html', {'user_request_form': user_request_form})
            
            # Create and save the new user
            user = User(email_address=email_address, user_name=user_name)
            # messages.info(request, user_request_form.cleaned_data['password'])
            print(user_request_form.cleaned_data['password'])
            user.set_password(user_request_form.cleaned_data['password'])  # Properly handle password
            user.password = user_request_form.cleaned_data['password']
            # print(user.password)
            user.save()
            
            messages.info(request, 'Your profile has been updated successfully!')
            return redirect('main_page')
    else:
        user_request_form = UserFrom()

    context = {'user_request_form': user_request_form}
    return render(request, 'user_request.html', context)

@csrf_exempt
@login_required
def edit_user_request(request):
    # Assuming 'user_name' is the correct field on your User model and is unique
    user = User.objects.get(user_name=request.user)  # You can use request.user directly if it's the User model instance
    if request.method == 'POST':
        edit_user_request_form = EditUserForm(request.POST, instance=request.user)
        if edit_user_request_form.is_valid():
            
            new_email_address = edit_user_request_form.cleaned_data['email_address']
            # user.email_address = email_address
            new_user_name = edit_user_request_form.cleaned_data['user_name']
            # user.user_name = user_name


            # Check if the email already exists and belongs to another user
            if User.objects.exclude(pk=user.pk).filter(email_address=new_email_address).exists():
                messages.error(request, 'Email address already in use.')
                return render(request, 'edit_user.html', {'edit_user_request_form': edit_user_request_form})

            # Check if the username already exists and belongs to another user
            if User.objects.exclude(pk=request.user.pk).filter(user_name=new_user_name).exists():
                messages.error(request, 'Username already in use.')
                return render(request, 'edit_user.html', {'edit_user_request_form': edit_user_request_form})
            # user.save()

            User.objects.filter(user_name=request.user).update(user_name=new_user_name, email_address=new_email_address)
            messages.info(request, 'Your profile has been edited successfully!')
            return redirect('profile')  # Redirect to the 'profile' page after saving
    else:
        # Prepopulate the form with the user's current data
        edit_user_request_form = EditUserForm(instance=user)

    context = {'edit_user_request_form': edit_user_request_form}
    return render(request, 'edit_user.html', context)

@csrf_exempt
@login_required
def edit_driver_request(request):
    # Assuming 'user_name' is the correct field on your User model and is unique
    # driver = Vehicle.objects.get(driver__user_name=request.user)  # You can use request.user directly if it's the User model instance
    driver = Vehicle.objects.filter(driver__user_name=request.user).first()
    if request.method == 'POST':
        edit_driver_request_form = EditDriverForm(request.POST, instance=driver)
        if edit_driver_request_form.is_valid():
            driver.driver_name = edit_driver_request_form.cleaned_data['driver_name'],
            driver.vehicle_type = edit_driver_request_form.cleaned_data['vehicle_type'],
            driver.license_plate = edit_driver_request_form.cleaned_data['license_plate'],
            driver.max_passengers = edit_driver_request_form.cleaned_data['max_passengers']
            driver.special_vehicle_info = edit_driver_request_form.cleaned_data['special_vehicle_info'],

            driver.save()
            messages.info(request, 'Your driver profile has been edited successfully!')
            return redirect('profile')  # Redirect to the 'profile' page after saving
    else:
        # Prepopulate the form with the user's current data
        edit_driver_request_form = EditDriverForm(instance=driver)

    context = {'edit_driver_request_form': edit_driver_request_form}
    return render(request, 'edit_driver.html', context)

## owner require a ride
@csrf_exempt
@login_required
def ride_request(request):
    if request.method == 'POST':
        #messages.info(request, 'post successfully!')
        ride_request_form = RideRequestForm(request.POST)
        if ride_request_form.is_valid():
            #messages.info(request, 'form valid!')
            ride = Ride(
                destination=ride_request_form.cleaned_data['destination'],
                required_arrival_date_time=ride_request_form.cleaned_data['required_arrival_date_time'],
                vehicle_type=ride_request_form.cleaned_data.get('vehicle_type', ''),
                special_request=ride_request_form.cleaned_data.get('special_request', ''),
                shared=ride_request_form.cleaned_data['shared'],
                owner_passenger_num=ride_request_form.cleaned_data['owner_passenger_num'],
                ownerID= User.objects.filter(user_name=request.user).values_list('user_id'),
                #ownerID=request.user.id,
                status='open'
            )
            ride.save()
            messages.info(request, 'Your ride request has been submitted successfully!')
            return redirect('main_page')
        else:
            messages.error(request, f'Form invalid: {ride_request_form.errors}')
    else:
        ride_request_form = RideRequestForm()

    context = {'ride_request_form': ride_request_form}
    return render(request, 'ride-request.html', context)

## sharer want to find open rides
@csrf_exempt
@login_required
def sharer_request(request):
    if request.method == 'POST':
        sharer_request_form = SharerRequestForm(request.POST)
        if sharer_request_form.is_valid():
            sharer_data = sharer_request_form.cleaned_data
            sharer_data['earliest_arrival_date_time'] = sharer_data['earliest_arrival_date_time'].isoformat()
            sharer_data['latest_arrival_date_time'] = sharer_data['latest_arrival_date_time'].isoformat()
            
            request.session['sharer_data'] = sharer_request_form.cleaned_data
            return redirect('valid_rides')
    else:
        sharer_request_form = SharerRequestForm()
        
    context = {'sharer_request_form': sharer_request_form}
    return render(request, 'sharer_request.html', context)

@login_required
def search_valid_rides(request):
    sharer_data = request.session.get('sharer_data')
    if not sharer_data:
        return redirect('sharer_request')

    destination = sharer_data['destination']
    earliest_arrival = datetime.fromisoformat(sharer_data['earliest_arrival_date_time'])
    latest_arrival = datetime.fromisoformat(sharer_data['latest_arrival_date_time'])
    passenger_num = sharer_data['sharer_passenger_num']
 
    valid_rides = Ride.objects.filter(destination=destination,
                                      required_arrival_date_time__gte=earliest_arrival,
                                      required_arrival_date_time__lte=latest_arrival,
                                      status='open',
                                      shared=True).exclude(ownerID=User.objects.get(user_name=request.user).user_id)
    #.exclude(ownerID=User.objects.filter(user_name=request.user).values_list('user_id')[0][0])
    # print("len of valid rides: ", len(valid_rides))

    return render(request, 'valid_rides.html', {'valid_rides': valid_rides.order_by('required_arrival_date_time')})

# @login_required
# def search_valid_rides(request):
#     sharer_data = request.session.get('sharer_data')
#     if not sharer_data:
#         return redirect('sharer_request')

#     destination = sharer_data['destination']
#     earliest_arrival = datetime.fromisoformat(sharer_data['earliest_arrival_date_time'])
#     latest_arrival = datetime.fromisoformat(sharer_data['latest_arrival_date_time'])
#     passenger_num = sharer_data['sharer_passenger_num']

#     valid_rides = Ride.objects.filter(destination=destination,
#                                       required_arrival_date_time__gte=earliest_arrival,
#                                       required_arrival_date_time__lte=latest_arrival,
#                                       status='open',
#                                       shared=True)#.exclude(ownerID=User.objects.filter(user_name=request.user).values_list('user_id')[0][0])


#     return render(request, 'valid_rides.html', {'valid_rides': valid_rides.order_by('required_arrival_date_time')})


@csrf_exempt
@login_required
def driver_request(request):
    if User.objects.filter(user_name=request.user).values_list('is_driver')[0][0]:
        messages.info(request, 'You are already a driver!')
        return redirect('main_page')
    
    if request.method == 'POST':
        driver_request_form = VehicleForm(request.POST)
        if driver_request_form.is_valid():
            driver = Vehicle(
                driver_id=User.objects.filter(user_name=request.user).values_list('user_id')[0][0],
                #driver_id=request.user__user_id,
                driver_name=driver_request_form.cleaned_data['driver_name'],
                vehicle_type=driver_request_form.cleaned_data['vehicle_type'],
                license_plate=driver_request_form.cleaned_data['license_plate'],
                max_passengers = driver_request_form.cleaned_data['max_passengers'],
                special_vehicle_info = driver_request_form.cleaned_data.get('special_vehicle_info', '')
            )
            User.objects.filter(user_name=request.user).update(is_driver=True)
            ## request.user.update(is_driver=True)
            request.user.save()
            driver.save()
            messages.info(request, 'You are a driver now! Well Done!')
            return redirect('main_page')
        
    else:
        driver_request_form = VehicleForm()

    context = {'driver_request_form': driver_request_form}
    return render(request, 'driver_request.html', context)


@login_required
def search_driver_rides(request):
    # vehicle = Vehicle.objects.filter(driver__user_name=request.user).first()
    # if not vehicle:
    
    if not User.objects.filter(user_name=request.user).values_list('is_driver')[0][0]:
        messages.warning(request, 'You are not a driver yet!')
        return render(request, 'driver_request.html')
    
    # vehicle = Vehicle.objects.filter(driver__user_name=request.user).first()
    # potential_rides = Ride.objects.filter(status='open',owner_passenger_num__lte=vehicle.max_passengers).filter(
    #     Q(vehicle_type__isnull=True) | Q(vehicle_type='') | Q(vehicle_type=vehicle.vehicle_type),
    #     Q(special_request__isnull=True) | Q(special_request='') | Q(special_request__icontains=vehicle.special_vehicle_info)
    # )

    curr_drives = Ride.objects.filter(driver__user_name=request.user, status='confirmed')
    curr_drives_times = curr_drives.values_list('required_arrival_date_time', flat=True).distinct()
    vehicle = Vehicle.objects.filter(driver__user_name=request.user).first()
    # print("cur_drive_time: ", len(curr_drives_times))
    potential_rides = Ride.objects.filter(
        status='open',
        owner_passenger_num__lte=vehicle.max_passengers
    ).exclude(
        required_arrival_date_time__in=curr_drives_times  # Exclude rides with matching required_arrival_date_time
    ).filter(
        Q(vehicle_type__isnull=True) | Q(vehicle_type='') | Q(vehicle_type=vehicle.vehicle_type),
        Q(special_request__isnull=True) | Q(special_request='') | Q(special_request__icontains=vehicle.special_vehicle_info)
    ).exclude(ownerID=User.objects.get(user_name=request.user).user_id)

    matching_rides = []
    for ride in potential_rides:
        sharer_passenger_count = RideSharer.objects.filter(share_ride=ride).aggregate(Sum('passenger_num'))['passenger_num__sum'] or 0
        total_passenger_count = ride.owner_passenger_num + sharer_passenger_count

        if total_passenger_count <= vehicle.max_passengers:# and ride.ownerID != User.objects.filter(user_name=request.user).values_list('user_id')[0][0]:
            matching_rides.append(ride)
            
    matching_rides = sorted(matching_rides, key=lambda x: x.required_arrival_date_time)

    return render(request, 'search_driver_rides.html', {'matching_rides': matching_rides})

@login_required
def ride_info(request, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    user = User.objects.get(user_name=request.user)
    
    isOwner = False
    isDriver = False
    hasSharer = False
    
    owner = User.objects.get(user_id=ride.ownerID)
    if user.user_id == ride.ownerID:
        isOwner = True
    
    driver = False
    vehicle = False
    if ride.status != 'open':
        driver = ride.driver
        vehicle = Vehicle.objects.get(driver=ride.driver)
        # if user.user_id == vehicle.driver.user_id:
        if ride in Ride.objects.filter(driver__user_name=request.user, status='confirmed'):
            isDriver = True
    
    sharers = False
    if ride.shared:
        sharers = RideSharer.objects.filter(share_ride=ride)
        sharer_user_ids = list(RideSharer.objects.filter(share_ride=ride).values_list('share_user_id', flat=True))
        share_users = User.objects.filter(user_id__in=sharer_user_ids)
        
        # if user.user_id in sharer_user_ids:
        #     hasSharer = True
        
    return render(request, 'ride_info.html', {'ride': ride,
                                              'isOwner': isOwner,
                                              'isDriver': isDriver,
                                              'owner': owner,
                                              'vehicle': vehicle,
                                              'sharers': sharers})

@login_required
def sharer_join(request, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    sharer_data = request.session.get('sharer_data', {})
    passenger_num = sharer_data.get('sharer_passenger_num', sharer_data['sharer_passenger_num'])
    
    if ride.ownerID == User.objects.filter(user_name=request.user).values_list('user_id')[0][0]:
        messages.error(request, "You cannot join your own ride!")
        return redirect('valid_rides')
        
    if ride.shared and ride.status == 'open':
        RideSharer.objects.create(
            share_ride=ride,
            share_user= request.user,
            passenger_num=passenger_num
        )
        
        emails = [ User.objects.filter(user_id=ride.ownerID).values_list('email_address')[0][0] ]
        if ride.shared:
            for sharer in RideSharer.objects.filter(share_ride=ride).values():
                if sharer['share_user_id'] == User.objects.get(user_name=request.user).user_id:
                    messages.error(request, "You've already join this ride!")
                    return redirect('valid_rides')
                sharer_id = sharer['share_user_id']
                emails.append(User.objects.filter(user_id=sharer_id).values_list('email_address')[0][0])
        
        send_mail(
            'Ride Confirmation',
            f'{request.user} join the ride to {ride.destination} on {ride.required_arrival_date_time}.',
            settings.EMAIL_HOST_USER,
            emails,
            fail_silently=False,
        )
        
        messages.success(request, "You've successfully joined the ride!")
    else:
        messages.error(request, "This ride cannot be joined.")
        return redirect('valid_rides')

    return redirect('ride_info', ride_id=ride_id)


@login_required
def driver_join(request, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    
    if not User.objects.filter(user_name=request.user).values_list('is_driver')[0][0]:
        messages.error(request, "You're not a driver yet'!")
        return redirect('create_driver_success')
        
    if ride.ownerID == User.objects.filter(user_name=request.user).values_list('user_id')[0][0]:
        messages.error(request, "You cannot drive your own ride!")
        return redirect('search_driver_rides')
    
    if ride.status == 'open':
        # ride.objects.update(driver=User.objects.get(user_name=request.user),
        #                     status="comfirmed")
        ride.driver = User.objects.get(user_name=request.user)
        ride.status = 'confirmed'
        
        # Send email when ride is confirmed
        emails = [ User.objects.filter(user_id=ride.ownerID).values_list('email_address')[0][0] ]
        if ride.shared:
            for sharer in RideSharer.objects.filter(share_ride=ride).values():
                sharer_id = sharer['share_user_id']
                emails.append(User.objects.filter(user_id=sharer_id).values_list('email_address')[0][0])
        
        send_mail(
            'Ride Confirmation',
            f'Your ride to {ride.destination} on {ride.required_arrival_date_time} has been confirmed.',
            settings.EMAIL_HOST_USER,
            emails,
            fail_silently=False,
        )
        ride.save()
        messages.success(request, "You've successfully became the driver of this ride!")
    else:
        messages.error(request, "This ride is not open.")
        return redirect('search_driver_rides')

    return redirect('ride_info', ride_id=ride_id)

@login_required
def my_rides(request):
    owner_rides = Ride.objects.filter(ownerID=User.objects.filter(user_name=request.user).values_list('user_id')[0][0]).exclude(status='completed')
    sharer_ride_ids = RideSharer.objects.filter(share_user=request.user).values_list('share_ride', flat=True).values_list('share_ride_id', flat=True)
    
    my_rides = owner_rides
    for share_id in sharer_ride_ids:
        my_rides = owner_rides | Ride.objects.filter(ride_id=share_id)
        owner_rides = my_rides
    return render(request, 'my_rides.html', {'my_rides': my_rides.order_by('required_arrival_date_time')})

@login_required
def my_drives(request):
    if not User.objects.filter(user_name=request.user).values_list('is_driver')[0][0]:
        messages.error(request, 'You are not a driver yet!')
        return redirect('main_page')
    
    my_drives = Ride.objects.filter(driver__user_name=request.user, status='confirmed')

    return render(request, 'my_drives.html', {'my_drives': my_drives.order_by('required_arrival_date_time')})

@csrf_exempt
@login_required
def owner_edit(request, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    user = User.objects.get(user_name=request.user)
    
    if user.user_id != ride.ownerID:
        messages.error(request, "You are not authorized to edit this ride.")
        return redirect('ride_info', ride_id=ride_id)
    
    if ride.status != 'open':
        messages.info(request, 'The ride status is not open, you cannot edit the ride now.')
        return redirect('ride_info', ride_id=ride_id)
    
    if request.method == 'POST':
        if 'quit' in request.POST:
            emails = []
            if ride.shared:
                for sharer in RideSharer.objects.filter(share_ride=ride):
                    #sharer_id = sharer.share_user.user_id
                    #emails.append(User.objects.filter(user_id=sharer_id).values_list('email_address')[0][0])
                    emails.append(sharer.share_user.email_address)
                    sharer.delete()
            
            send_mail(
                'Ride Canceled',
                f'Your sharing ride to {ride.destination} on {ride.required_arrival_date_time} is canceled by owner.',
                settings.EMAIL_HOST_USER,
                emails,
                fail_silently=False,
            )
            ride.delete()
            
            messages.success(request, "You have successfully cancel the ride plan.")
            return redirect('my_rides')
        
        
        form = RideRequestForm(request.POST)
        if form.is_valid():
            ride.destination = form.cleaned_data['destination']
            ride.required_arrival_date_time = form.cleaned_data['required_arrival_date_time']
            ride.vehicle_type = form.cleaned_data.get('vehicle_type', '')
            ride.special_request = form.cleaned_data.get('special_request', '')
            ride.shared = form.cleaned_data['shared'] == 'True'
            ride.owner_passenger_num = form.cleaned_data['owner_passenger_num']
            ride.save()

            messages.success(request, 'Ride information updated successfully.')
            return redirect('ride_info', ride_id=ride_id)
    else:
        initial_data = {
            'destination': ride.destination,
            'required_arrival_date_time': ride.required_arrival_date_time,
            'vehicle_type': ride.vehicle_type,
            'special_request': ride.special_request,
            'shared': ride.shared,
            'owner_passenger_num': ride.owner_passenger_num,
        }
        form = RideRequestForm(initial=initial_data)

    return render(request, 'owner_edit.html', {'form': form, 'ride': ride})

@csrf_exempt
@login_required
def sharer_edit(request, sharer_id, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    user = User.objects.get(user_name=request.user)
    
    if ride.status != 'open':
        messages.info(request, 'The ride status is not open, you cannot edit the ride now.')
        return redirect('ride_info', ride_id=ride_id)
    
    #ride_sharer = get_object_or_404(RideSharer, fk__id=share_id, share_user=user)
    ride_sharer = RideSharer.objects.get(share_ride=ride, share_user_id=sharer_id)
    
    if user != ride_sharer.share_user:
        messages.error(request, "You are not authorized to edit this ride.")
        return redirect('ride_info', ride_id=ride_id)

    if request.method == 'POST':
        if 'quit' in request.POST:
            send_mail(
                'Ride Sharer Quit',
                f'Your ride sharer {ride_sharer} to {ride.destination} on {ride.required_arrival_date_time} quit the trip.',
                settings.EMAIL_HOST_USER,
                [ User.objects.filter(user_id=ride.ownerID).values_list('email_address')[0][0] ],
                fail_silently=False,
            )
            #print(ride.required_arrival_date_time)
            ride_sharer.delete()
            messages.success(request, "You have successfully quit the ride.")
            return redirect('my_rides')

        form = SharerEditForm(request.POST)
        if form.is_valid():
            ride_sharer.passenger_num = form.cleaned_data['sharer_passenger_num']
            ride_sharer.save()
            messages.success(request, "Ride information updated successfully.")
            return redirect('ride_info', ride_id=ride_id)
        
    else:
        form = SharerEditForm(initial={'sharer_passenger_num': ride_sharer.passenger_num})

    return render(request, 'sharer_edit.html', {'form': form,
                                                'ride': ride})
    
@login_required
def driver_complete(request, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    user = User.objects.get(user_name=request.user)
    
    if user != ride.driver:
        messages.error(request, "You are not authorized to finish this ride.")
        return redirect('ride_info', ride_id=ride_id)
    
    if ride.status != 'confirmed':
        messages.info(request, 'The ride status is not confirmed yet, you cannot complete this ride.')
        return redirect('ride_info', ride_id=ride_id)
    
    ride.status = 'completed'
    
    # Send email when ride is completed
    emails = [ User.objects.filter(user_id=ride.ownerID).values_list('email_address')[0][0] ]
    if ride.shared:
        for sharer in RideSharer.objects.filter(share_ride=ride).values():
            sharer_id = sharer['share_user_id']
            emails.append(User.objects.filter(user_id=sharer_id).values_list('email_address')[0][0])
    
    send_mail(
        'Ride Completed',
        f'Your ride to {ride.destination} on {ride.required_arrival_date_time} has been completed.',
        settings.EMAIL_HOST_USER,
        emails,
        fail_silently=False,
    )
    ride.save()
    messages.success(request, "You've successfully completed this drive!")
    
    return redirect('ride_info', ride_id=ride_id)
