# EasyRide

This Django web application facilitates a ride-sharing service that allows users to assume the roles of ride owners, drivers, or sharers. Users can request rides, drive for them, and join rides, managing multiple roles across various rides.

## Features

### Accounts
- **Create Account**: Users can create a new account if they do not already have one.
- **Login/Logout**: Secure login and logout functionality.

### Ride Management
- **Ride Requesting**: Users can request rides by specifying destination, required arrival time, number of passengers, optional vehicle type, and special requests.
- **Ride Editing**: As long as a ride is open and not confirmed, the ride owner can modify the ride details.
- **Ride Status Viewing**: Both ride owners and sharers can view the status of their non-complete rides, seeing updates and driver details for confirmed rides.

### Driver Functions
- **Driver Registration**: Users can register as a driver, providing personal and vehicle information.
- **Ride Searching**: Drivers can search for open ride requests that fit their vehicle’s capacity and special equipment.
- **Claiming and Starting Rides**: Drivers can claim rides and mark them as complete after reaching the destination.

### Ride Sharing
- **Searching for Rides**: Users can search for rides by specifying a destination and arrival window, and join available rides.

## Technology Stack
- **Backend**: Django
- **Database**: PostgreSQL
- **Frontend**: Use of CSS/JavaScript libraries is encouraged, with Bootstrap recommended.

## Installation

1. Clone the repository.
2. Install dependicies: `pip install -r requirements.txt`
3. Set up database in `settings.py`
4. Run `python manage.py migrate`
5. Run `python manage.py runserver`
6. If you would like to start it with docker, run `sudo docker-compose up`
