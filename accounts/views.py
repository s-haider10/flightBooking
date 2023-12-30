from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.validators import validate_email
import pymysql

# Create your views here.
conn = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    db = 'new_airline',
    )

def home(request):
    final_results = []
    query = 'SELECT * FROM airline'
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    for x in range(len(results)):
        temp = list(results[x])
        final = tuple(temp)
        final_results.append((final))
    cursor.close()

    return render(request, 'accounts/home.html', {'airline_results':final_results})

def aagenthome(request):
    return redirect('agenthome')
def astaffhome(request):
    return redirect('staffhome')
def acustomerhome(request):
    return redirect('customerhome')
def login(request):
    cursor = conn.cursor()
    if request.method == 'POST':
        if request.POST['type'] == '' or not request.POST['username'] or not request.POST['password']:
            message = 'Please fill all the fields!'
            return render(request, 'accounts/login.html', {'message': message})
        if request.POST['type'] == 'customer':
            q = "SELECT * FROM customer WHERE email = \'{}\' and password = \'{}\'"
        elif request.POST['type'] == 'agent':
            q = "SELECT * FROM booking_agent WHERE email = \'{}\' and password = \'{}\'"
        else:
            q = "SELECT * FROM airline_staff WHERE email = \'{}\' and password = \'{}\'"
        query = q.format(request.POST['username'], request.POST['password'])
        cursor.execute(query)
        data = cursor.fetchone()
        cursor.close()
        user = auth.authenticate(username = request.POST['username'], password = request.POST['password'])
        if not data:
            message = "Invalid Credentials! Please Try Again."
            return render(request, 'accounts/login.html', {'message': message})
        if user is not None and data:
            auth.login(request, user)
            if request.POST['type'] == 'customer':
                return redirect('customerhome')
            elif request.POST['type'] == 'agent':
                return redirect('agenthome')
            else:
                return redirect('staffhome')
        else:
            user = User.objects.create_user(request.POST['username'], password=request.POST['password'], first_name = 'a', last_name = 'y', email = request.POST['username'])
            user.save()
            auth.login(request, user)
            if request.POST['type'] == 'customer':
                return redirect('customerhome')
            elif request.POST['type'] == 'agent':
                return redirect('agenthome')
            else:
                return redirect('home')
    else:
        return render(request, 'accounts/login.html')

def signup(request):
    return render(request, 'accounts/signup.html')

def customersignup(request):
    cursor = conn.cursor()
    if request.method == 'POST':
        if request.POST['email'] and request.POST['name'] and request.POST['date_of_birth'] and request.POST['password'] and request.POST['building_number'] and request.POST['street_address'] and request.POST['city'] and request.POST['state'] and request.POST['phone_num'] and request.POST['passport_num'] and request.POST['passport_expiration'] and request.POST['passport_country']:
            verification = "SELECT * FROM customer WHERE email = \'{}\'".format(request.POST['email'])
            cursor.execute(verification)
            data = cursor.fetchone()
            if data:
                message = 'This email address is already in use!'
                return render(request, 'accounts/customersignup.html', {'message': message})
            else:
                query = "INSERT INTO customer VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\' )"
                cursor.execute(query.format(request.POST['email'],
                                            request.POST['name'],
                                            request.POST['password'],
                                            request.POST['building_number'],
                                            request.POST['street_address'],
                                            request.POST['city'],
                                            request.POST['state'],
                                            request.POST['phone_num'],
                                            request.POST['passport_num'],
                                            request.POST['passport_expiration'],
                                            request.POST['passport_country'],
                                            request.POST['date_of_birth']))
                conn.commit()
                user = User.objects.create_user(request.POST['email'], password=request.POST['password'], first_name = request.POST['name'], last_name = '', email = request.POST['email'])
                user.save()
                cursor.close()
                auth.login(request, user)
                return redirect('customerhome')
        else:
            message = 'Please fill all fields below!'
            return render(request, 'accounts/customersignup.html', {'message': message})
    else:
        return render(request, 'accounts/customersignup.html')

def staffsignup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        date_of_birth = request.POST['date_of_birth']
        airline = request.POST['airline']
        if email and password and firstname and lastname and date_of_birth and airline:
            verification = "SELECT * FROM airline_staff WHERE email = \'{}\' "
            cursor = conn.cursor()
            cursor.execute(verification.format(email))
            result = cursor.fetchone()
            if result:
                message = 'This email address is already in use!'
                return render(request, 'accounts/staffsignup.html', {'message': message})
            else:
                query = "INSERT INTO airline_staff VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', 0, 0)"
                cursor.execute(query.format(email, password, firstname, lastname, date_of_birth, airline))
                conn.commit()
                user = User.objects.create_user(request.POST['email'], password=request.POST['password'], first_name = request.POST['firstname'], last_name = '', email = request.POST['email'])
                user.save()
                cursor.close()
                auth.login(request, user)
                return redirect('staffhome')
        else:
            message = 'Please fill all fields below!'
            return render(request, 'accounts/staffsignup.html', {'message': message})
    else:
        cursor = conn.cursor()
        query = 'SELECT DISTINCT(name_of_airline) FROM airline'
        cursor.execute(query)
        data = cursor.fetchall()
        lst = [a[0] for a in data]
    return render(request, 'accounts/staffsignup.html', {'lst': lst})

def agentsignup(request):
    if request.method == 'POST':
        if request.POST['email'] and request.POST['password']:
            verification = "SELECT * FROM booking_agent WHERE email = \'{}\' ".format(request.POST['email'])
            cursor = conn.cursor()
            cursor.execute(verification)
            result = cursor.fetchone()
            if result:
                message = 'This email address is already in use!'
                return render(request, 'accounts/agentsignup.html', {'message': message})
            else:
                query = "SELECT MAX(booking_agent_ID) FROM booking_agent"
                cursor.execute(query)
                result = cursor.fetchone()[0]
                if not result:
                    id = 1
                else:
                    id = int(result) + 1
                query = "INSERT INTO booking_agent VALUES (\'{}\', \'{}\', \'{}\')".format(request.POST['email'],request.POST['password'], id)
                cursor.execute(query)
                conn.commit()
                cursor.close()
                user = User.objects.create_user(request.POST['email'], password=request.POST['password'], first_name = 'agent', last_name = '', email = request.POST['email'])
                user.save()
                cursor.close()
                auth.login(request, user)
                return redirect('agenthome')
        else:
            return render(request, 'accounts/agentsignup.html')
    else:
        return render(request, 'accounts/agentsignup.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

def search_flight(request):
    cursor = conn.cursor()
    # getting information about all possible departure airports in the database system
    query = "SELECT DISTINCT departure_airport_name FROM flight"
    cursor.execute(query)
    departure_airports = cursor.fetchall()
    dp_lst = [a[0] for a in departure_airports]
    # getting information about all possible departure airport cities in the database system
    query = "SELECT DISTINCT city FROM airport WHERE name IN (SELECT departure_airport_name FROM flight)"
    cursor.execute(query)
    departure_airports_city = cursor.fetchall()
    dac_list = [a[0] for a in departure_airports_city]
    # getting information about all possible arrival airports in the databse system
    query = "SELECT DISTINCT arrival_airport_name FROM flight"
    cursor.execute(query)
    destination_airports = cursor.fetchall()
    da_lst = [a[0] for a in destination_airports]
    # getting information about all possible arrival airport cities in the database system
    query = "SELECT DISTINCT city FROM airport WHERE name IN (SELECT arrival_airport_name FROM flight)"
    cursor.execute(query)
    destination_airports_city = cursor.fetchall()
    dtac_list = [a[0] for a in destination_airports_city]

    cursor.close()
    return render(request, 'accounts/search_flight.html', {'departure_airports':dp_lst,
                                                           'departure_airports_city': dac_list,
                                                           'destination_airports': da_lst,
                                                           'destination_airports_city': dtac_list})

def search_for_flight(request):
    if request.method == 'POST':
        final_results = []
        dp_airport = request.POST['Departure Airport']
        dp_city = request.POST['Departure City']
        dt_airport = request.POST['Destination Airport']
        dt_city = request.POST['Destination City']
        date = request.POST['Date']
        check1 = bool(dp_airport!='none')
        check2 = bool(dp_city!='none')
        check3 = bool(dt_airport!='none')
        check4 = bool(dt_city!='none')
        check5 = bool(date!='')
        if not check1 and not check2 and not check3 and not check4 and not check5:
            message = 'Please select at least one option!'
            return render(request, 'accounts/home.html', {'message': message})
        else:
            q1 = ' departure_airport_name IN (SELECT name FROM airport WHERE city = \"{}\")'.format(dp_city)
            q2 = ' departure_airport_name = \"{}\"'.format(dp_airport)
            q3 = ' arrival_airport_name IN (SELECT name FROM airport WHERE city = \"{}\")'.format(dt_city)
            q4 = ' arrival_airport_name = \"{}\"'.format(dt_airport)
            q5 = ' DATE(departure_time) = DATE(\"{}\")'.format(date)
            final_q = list(filter(None, [q1*check2, q2*check1, q3*check4, q4*check3, q5*check5]))
            query = 'SELECT * FROM flight WHERE' + 'AND'.join(final_q) + " AND status = 'Upcoming'"
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            for x in range(len(results)):
                temp = list(results[x])
                final = tuple(temp)
                final_results.append((final))
            cursor.close()
            return render(request, 'accounts/search_results.html', {'results':final_results})
    else:
        # Ensuring that no one reaches this page unless they have filled out their preferences.
        return render(request, 'accounts/search_flight.html')

def flightstatus(request):
    return render(request, 'accounts/flightstatus.html')


def checkstatus(request):
    if request.method == 'POST':
        flight_num = request.POST['flight_num']
        dp_date = request.POST['dp_date']
        ar_date = request.POST['ar_date']

        check1 = bool(flight_num != '')
        check2 = bool(dp_date != '')
        check3 = bool(ar_date != '')

        if not check1 and not check2 and not check3:
            message = 'You need to atleast fill in one option'
            return render(request, 'accounts/checkstatus.html', {'message': message})
        else:
            q1 = 'flight_num = \"{}\"'.format(flight_num)
            q2 = 'DATE(departure_time) = DATE(\"{}\")'.format(dp_date)
            q3 = 'DATE(arrival_time) = DATE(\"{}\")'.format(ar_date)
            final_q = list(filter(None, [q1*check1, q2*check2, q3*check3]))
            query = 'SELECT * FROM flight WHERE ' + ' AND '.join(final_q)
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()[0]
            cursor.close()
            return render(request, 'accounts/flightstatus.html', {'result': result})
    else:
        return render(request, 'accounts/checkstatus.html')
