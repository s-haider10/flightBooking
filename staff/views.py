from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
import pymysql
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import base64
from io import BytesIO
from django.core.mail import send_mail
from Airline_Reservation import settings

conn = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'Haider110!',
    db = 'new_airline',
    )




@login_required(login_url='login')
def staffhome(request):
    email = request.user.email
    cursor = conn.cursor()
    q = "SELECT name_of_airline FROM airline_staff WHERE email = \'{}\' "
    cursor.execute(q.format(email))
    staff_airl = cursor.fetchone()
    q1 = "SELECT * FROM flight WHERE name_of_airline = \'{}\' "
    cursor.execute(q1.format(staff_airl[0]))
    upcoming_flights = cursor.fetchall()
    lst = [a for a in upcoming_flights]
    q2 = "SELECT DISTINCT departure_airport_name FROM flight"
    cursor.execute(q2)
    departure_airports = cursor.fetchall()
    dp_lst = [a[0] for a in departure_airports]
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
    query = "SELECT DISTINCT flight_num FROM flight WHERE name_of_airline = \'{}\' ".format(staff_airl[0])
    cursor.execute(query)
    flight_num = cursor.fetchall()
    flightnum = [a[0] for a in flight_num]
    return render(request, 'staff/staffhome.html', {'lst':lst, 'dp_lst':dp_lst, 'dac_list': dac_list, 'da_lst':da_lst, 'dtac_list':dtac_list, 'flightnum':flightnum, 'airline':staff_airl[0]})

@login_required(login_url='login')
def staff_search_results(request):
    if request.method == 'POST':
        email = request.user.email
        cursor = conn.cursor()
        q = "SELECT name_of_airline FROM airline_staff WHERE email = \'{}\' "
        cursor.execute(q.format(email))
        staff_airl = cursor.fetchone()
        dp_airport = request.POST['Departure Airport']
        dp_city = request.POST['Departure City']
        dt_airport = request.POST['Destination Airport']
        dt_city = request.POST['Destination City']
        airline = request.POST['Airline']
        flight_num = request.POST['Flight Number']
        date = request.POST['Date']
        check1 = bool(dp_airport!='none')
        check2 = bool(dp_city!='none')
        check3 = bool(dt_airport!='none')
        check4 = bool(dt_city!='none')
        check5 = bool(airline!='')
        if not check1 and not check2 and not check3 and not check4 and not check5 and not check6:
            message = 'Please select at least one option!'
            return render(request, 'customer/customer_search_flight.html', {'message': message})
        else:
            q1 = ' departure_airport_name IN (SELECT name FROM airport WHERE city = \"{}\")'.format(dp_city)
            q2 = ' departure_airport_name = \"{}\"'.format(dp_airport)
            q3 = ' arrival_airport_name IN (SELECT name FROM airport WHERE city = \"{}\")'.format(dt_city)
            q4 = ' arrival_airport_name = \"{}\"'.format(dt_airport)
            q5 = ' name_of_airline = \"{}\"'.format(airline)
            final_q = list(filter(None, [q1*check2, q2*check1, q3*check4, q4*check3, q5*check5]))
            query = 'SELECT * FROM flight WHERE' + 'AND'.join(final_q) + " AND status = 'Upcoming'"
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
        query = "SELECT DISTINCT flight_num FROM flight WHERE name_of_airline = \'{}\' ".format(staff_airl[0])
        cursor.execute(query)
        flight_num = cursor.fetchall()
        flightnum = [a[0] for a in flight_num]
        return render(request, 'staff/staff_search_results.html', {'results': results, 'flightnum': flightnum, 'airline':staff_airl[0]})

@login_required(login_url='login')
def staff_viewcustomers(request):
    if request.method == 'POST':
        airline = request.POST['airline']
        flightnum = request.POST['flightnum']
        cursor = conn.cursor()
        query = "SELECT c.email, c.name, c.phone_num, c.city, c.state, c.date_of_birth FROM customer c, bookings b, ticket t WHERE c.email = b.email_customer AND t.ticket_id = b.ticket_id AND t.name_of_airline = \'{}\' AND t.flight_num = \'{}\' "
        cursor.execute(query.format(airline, flightnum))
        customers = cursor.fetchall()
        lst = [a for a in customers]
        if customers:
            pass
        else:
            message = "No customers on this flight!"
            return render(request, 'staff/staff_viewcustomers.html')
        return render(request, 'staff/staff_viewcustomers.html', {'lst':lst})

@login_required(login_url='login')
def createnewflights(request):
    email = request.user.email
    cursor = conn.cursor()
    q = "SELECT admin_permission FROM airline_staff WHERE email = \'{}\' "
    cursor.execute(q.format(email))
    admin_permission = cursor.fetchone()
    if (bool(admin_permission[0])):

        email = request.user.email
        q = "SELECT name_of_airline FROM airline_staff WHERE email = \'{}\' "
        cursor.execute(q.format(email))
        staff_airl = cursor.fetchone()

        q1 = "SELECT * FROM flight WHERE name_of_airline = \'{}\' "
        cursor.execute(q1.format(staff_airl[0]))
        upcoming_flights = cursor.fetchall()
        lst = [a for a in upcoming_flights]

        q2 = "SELECT DISTINCT name FROM airport"
        cursor.execute(q2)
        departure_airports = cursor.fetchall()
        dp_lst = [a[0] for a in departure_airports]

        # query = "SELECT DISTINCT city FROM airport WHERE name IN (SELECT departure_airport_name FROM flight)"
        # cursor.execute(query)
        # departure_airports_city = cursor.fetchall()
        # dac_list = [a[0] for a in departure_airports_city]

        # getting information about all possible arrival airports in the databse system
        query = "SELECT DISTINCT name FROM airport"
        cursor.execute(query)
        destination_airports = cursor.fetchall()
        da_lst = [a[0] for a in destination_airports]

        # getting information about all possible arrival airport cities in the database system
        # query = "SELECT DISTINCT city FROM airport WHERE name IN (SELECT arrival_airport_name FROM flight)"
        # cursor.execute(query)
        # destination_airports_city = cursor.fetchall()
        # dtac_list = [a[0] for a in destination_airports_city]

        query = "SELECT DISTINCT flight_num FROM flight WHERE name_of_airline = \'{}\' ".format(staff_airl[0])
        cursor.execute(query)
        flight_num = cursor.fetchall()
        flightnum = [a[0] for a in flight_num]

        query = "SELECT DISTINCT ID_airplane from airplane WHERE name_of_airline = \'{}\' ".format(staff_airl[0])
        cursor.execute(query)
        id_airp = cursor.fetchall()
        id_airp_ls = [a[0] for a in id_airp]
        cursor.close()
        return render(request, 'staff/createnewflights.html', {'staff_airl': staff_airl[0], 'lst': lst, 'dp_lst' : dp_lst, 'da_lst': da_lst, 'flightnum':flightnum, 'id_airp_ls':id_airp_ls})

    else:
        message = "You are not authorized to create a new flight!."
        return render(request, 'staff/staffhome.html', {'message': message})

@login_required(login_url='login')
def addflight(request):
    if request.method == 'POST':
        dp_airport = request.POST['Departure Airport']
        dp_time = request.POST['Departure Time']
        dt_airport = request.POST['Destination Airport']
        dt_time = request.POST['Destination Time']
        airline = request.POST['Airline']
        flight_num = request.POST['flightnum']
        price = request.POST['price']
        status = request.POST['status']
        id_airplane = request.POST['airplaneid']

        if not dp_airport or not dp_time or not dt_airport or not dt_time or not airline or not flight_num or not price or not status or not id_airplane:
            error = 'Please enter all the details in order to the add the flight to the database'
            return render(request, 'staff/createnewflights.html', {'error': error})

        cursor = conn.cursor()
        q = "SELECT * FROM flight WHERE name_of_airline = \'{}\' AND flight_num = '{}' "
        cursor.execute(q.format(airline, flight_num))
        check = cursor.fetchone()
        if check:
            error = "The Flight already exists!"
            return render(request, 'staff/createnewflights.html', {'error': error})
        if dp_time >= dt_time:
            error = "Arrival Time cannot be earlier than departure time!"
            return render(request, 'staff/createnewflights.html', {'error': error})
        if dp_airport == dt_airport:
            error = "Depaarture and Destination Airports cannot be the same"
            return render(request, 'staff/createnewflights.html', {'error': error})

        query = "INSERT INTO flight VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\' )"
        cursor.execute(query.format(airline, flight_num, dp_airport, dp_time, dt_airport, dt_time, price, status, id_airplane))
        conn.commit()
        cursor.close()
        return render(request, 'staff/addflight.html')

@login_required(login_url='login')
def changestatus(request):
    cursor = conn.cursor()

    email = request.user.email
    cursor = conn.cursor()
    q = "SELECT operator_permission FROM airline_staff WHERE email = \'{}\' "
    cursor.execute(q.format(email))
    operator_permission = cursor.fetchone()

    if (bool(operator_permission[0])):
        email = request.user.email
        q = "SELECT name_of_airline FROM airline_staff WHERE email = \'{}\' "
        cursor.execute(q.format(email))
        staff_airl = cursor.fetchone()
        query = "SELECT DISTINCT flight_num FROM flight WHERE name_of_airline = \'{}\' ".format(staff_airl[0])
        cursor.execute(query)
        flight_num = cursor.fetchall()
        flightnum = [a[0] for a in flight_num]
        cursor.close()
        return render(request, 'staff/changestatus.html', {'staff_airl': staff_airl[0], 'flightnum': flightnum})
    else:
        message = "You are not authorized to update the status of the flight."
        return render(request, 'staff/staffhome.html', {'message': message})

@login_required(login_url='login')
def update_status(request):
    if request.method == 'POST':
        airline = request.POST['Airline']
        flightnum = request.POST['flightnum']
        new_status = request.POST['status']

        if flightnum == "" or new_status == "":
            message = 'Please Fill all the fields below!'
            return render(request, 'staff/changestatus.html', {'message':message})

        cursor = conn.cursor()
        query = "UPDATE flight SET status = \'{}\' WHERE name_of_airline = \'{}\' AND flight_num = \'{}\' "
        cursor.execute(query.format(new_status, airline, flightnum))
        conn.commit()
        cursor.close()
        return render(request, 'staff/update_status.html')

@login_required(login_url='login')
def addnewairplane(request):
    email = request.user.email
    cursor = conn.cursor()
    q = "SELECT admin_permission FROM airline_staff WHERE email = \'{}\' "
    cursor.execute(q.format(email))
    admin_permission = cursor.fetchone()
    if (bool(admin_permission[0])):
        email = request.user.email
        q = "SELECT name_of_airline FROM airline_staff WHERE email = \'{}\' "
        cursor.execute(q.format(email))
        staff_airl = cursor.fetchone()
        return render(request, 'staff/addnewairplane.html', {'staff_airl': staff_airl[0]})
    else:
        message = "You are not authorized to add new planes."
        return render(request, 'staff/staffhome.html', {'message': message})

@login_required(login_url='login')
def confirmation_new_airplane(request):
    if request.method == 'POST':
        airline = request.POST['Airline']
        seats = request.POST['seats']

        if not seats or not airline:
            message = "Please Fill all the fields"
            return redirect('addnewairplane')
        cursor = conn.cursor()
        query = "SELECT MAX(ID_airplane) FROM airplane WHERE name_of_airline = \'{}\' "
        cursor.execute(query.format(airline))
        id = cursor.fetchone()
        if not id[0]:
            newid = 1
        else:
            newid = int(id[0])+1

        cursor = conn.cursor()
        query = "INSERT INTO airplane VALUES (\'{}\', \'{}\', \'{}\') ".format(airline, newid, seats)
        cursor.execute(query)
        conn.commit()
        cursor.close()

        cursor = conn.cursor()
        query = "SELECT * FROM airplane WHERE name_of_airline = \'{}\' ".format(airline)
        cursor.execute(query)
        all_airplanes = cursor.fetchall()
        lst = [(a[1], a[2]) for a in all_airplanes]

        return render(request, 'staff/confirmation_new_airplane.html', {'lst': lst})
    else:
        return render(request, 'staff/addnewairplane.html')

@login_required(login_url='login')
def addnewairport(request):
    email = request.user.email
    cursor = conn.cursor()
    q = "SELECT admin_permission FROM airline_staff WHERE email = \'{}\' "
    cursor.execute(q.format(email))
    admin_permission = cursor.fetchone()
    if (bool(admin_permission[0])):
        return render(request, 'staff/addnewairport.html')
    else:
        message = "You are not authorized to add new airports."
        return render(request, 'staff/staffhome.html', {'message': message})

@login_required(login_url='login')
def airport_add(request):
    if request.method == 'POST':
        cursor = conn.cursor()
        name = request.POST['name']
        city = request.POST['city']
        query = "SELECT EXISTS(SELECT * FROM airport WHERE name = \'{}\' )"
        cursor.execute(query.format(name))
        check = cursor.fetchone()
        if not check:
            return redirect('addnewairport')
        cursor.close()
        cursor = conn.cursor()
        query = "INSERT INTO airport VALUES (\'{}\', \'{}\') ".format(name, city)
        cursor.execute(query)
        conn.commit()
        cursor.close()
        return render(request, 'staff/airport_add.html')

@login_required(login_url='login')
def viewbookingagents(request):
    query = "SELECT b.email, b.booking_agent_ID, COUNT(bk.ticket_id) FROM booking_agent b, bookings bk WHERE bk.booking_date >= ADDDATE(DATE(NOW()), INTERVAL -1 MONTH) AND b.booking_agent_ID = bk.booking_agent_id GROUP BY b.email, b.booking_agent_ID ORDER BY COUNT(bk.ticket_id) DESC "
    cursor = conn.cursor()
    cursor.execute(query)
    top5_agent_onem = []
    temp = cursor.fetchone()
    count = 1
    while temp and count <= 2:
        top5_agent_onem.append(list(temp))
        temp = cursor.fetchone()
        count += 1
    cursor.close()

    query = "SELECT b.email, b.booking_agent_ID, COUNT(bk.ticket_id) FROM booking_agent b, bookings bk WHERE bk.booking_date >= ADDDATE(DATE(NOW()), INTERVAL -12 MONTH) AND b.booking_agent_ID = bk.booking_agent_id GROUP BY b.email, b.booking_agent_ID ORDER BY COUNT(bk.ticket_id) DESC "
    cursor = conn.cursor()
    cursor.execute(query)
    top5_agent_oney = []
    temp = cursor.fetchone()
    count = 1
    while temp and count <= 2:
        top5_agent_oney.append(list(temp))
        temp = cursor.fetchone()
        count += 1
    cursor.close()

    query = "SELECT b.email, b.booking_agent_ID, 0.1*SUM(f.price) FROM booking_agent b, bookings bk, ticket t, flight f WHERE bk.booking_date >= ADDDATE(DATE(NOW()), INTERVAL -1 MONTH) AND bk.booking_agent_id = b.booking_agent_ID AND f.flight_num = t.flight_num AND t.name_of_airline = f.name_of_airline AND t.ticket_id = bk.ticket_id GROUP BY b.email, b.booking_agent_ID ORDER BY SUM(f.price) DESC "
    cursor = conn.cursor()
    cursor.execute(query)

    top5_agent_com = []
    temp = cursor.fetchone()
    count = 1
    while temp and count <= 2:
        top5_agent_com.append(list(temp))
        temp = cursor.fetchone()
        count += 1
    cursor.close()
    return render(request, 'staff/viewbookingagents.html', {'top5_agent_com': top5_agent_com, 'top5_agent_oney':top5_agent_oney, 'top5_agent_onem':top5_agent_onem})


@login_required(login_url='login')
def addnewbookingagent(request):
    email = request.user.email
    cursor = conn.cursor()
    q = "SELECT admin_permission FROM airline_staff WHERE email = \'{}\' "
    cursor.execute(q.format(email))
    admin_permission = cursor.fetchone()
    if (bool(admin_permission[0])):
        email = request.user.email
        q = "SELECT name_of_airline FROM airline_staff WHERE email = \'{}\' "
        cursor.execute(q.format(email))
        staff_airl = cursor.fetchone()


        query = "SELECT DISTINCT(email) FROM booking_agent"
        cursor.execute(query)
        all_agents = cursor.fetchall()
        lst = [a[0] for a in all_agents]
        return render(request, 'staff/addnewbookingagent.html', {'lst': lst, 'staff_airl': staff_airl[0]})

    else:
        message = "You are not authorized to add new agents."
        return render(request, 'staff/staffhome.html', {'message': message})


@login_required(login_url='login')
def add_agent(request):
    if request.method == 'POST':
        cursor = conn.cursor()
        email = request.POST['email']
        airline = request.POST['airline']
        query = "SELECT EXISTS(SELECT email, name_of_airline FROM agent_works_for WHERE email = \'{}\' AND name_of_airline = \'{}\' )"
        cursor.execute(query.format(email, airline))
        check = cursor.fetchone()
        if not check:
            return redirect('addnewbookingagent')
        cursor.close()
        cursor = conn.cursor()
        query = "INSERT INTO agent_works_for VALUES (\'{}\', \'{}\') "
        cursor.execute(query.format(email, airline))
        conn.commit()
        cursor.close()
        return render(request, 'staff/add_agent.html')


@login_required(login_url='login')
def viewfreqcustomers(request):
    cursor = conn.cursor()
    email = request.user.email
    q = "SELECT name_of_airline FROM airline_staff WHERE email = \'{}\' "
    cursor.execute(q.format(email))
    staff_airl = cursor.fetchone()
    temp = "CREATE VIEW cust_freq AS (SELECT b.email_customer as cust_email, COUNT(b.ticket_id) as freq FROM bookings b, ticket t WHERE t.name_of_airline = \'{}\' AND t.ticket_id = b.ticket_id GROUP BY b.email_customer)"
    cursor.execute(temp.format(staff_airl[0]))
    conn.commit()
    temp2 = "CREATE VIEW max_freq AS (SELECT MAX(freq) as max_freqency FROM cust_freq)"
    cursor.execute(temp2)
    conn.commit()
    q = "SELECT c.email, c.name, c.phone_num FROM customer c, max_freq m, cust_freq cf WHERE c.email = cf.cust_email AND cf.freq = m.max_freqency"
    cursor.execute(q)
    frequent_customers = cursor.fetchall()
    frequent_customers = [a[0] for a in frequent_customers]
    print (frequent_customers)

    cursor.execute('DROP VIEW cust_freq')
    cursor.execute('DROP VIEW max_freq')
    q = "SELECT email FROM customer"
    cursor.execute(q)
    email_cust = cursor.fetchall()
    lst = [a[0] for a in email_cust]
    cursor.close()
    return render(request, 'staff/viewfreqcustomers.html', {'email_cust':lst, 'frequent_customers': frequent_customers})


@login_required(login_url='login')
def customerhistory(request):
    if request.method == 'POST':
        cursor = conn.cursor()
        email = request.user.email
        q = "SELECT name_of_airline FROM airline_staff WHERE email = \'{}\' "
        cursor.execute(q.format(email))
        staff_airl = cursor.fetchone()
        cursor.close()
        email = request.POST['cust_email']
        cursor = conn.cursor()
        query = "SELECT f.name_of_airline, f.flight_num, f.departure_airport_name, f.departure_time, f.arrival_airport_name, f.arrival_time, f.price, f.status FROM flight f, ticket t, bookings b WHERE b.email_customer = \'{}\' AND b.ticket_id = t.ticket_id AND t.name_of_airline = f.name_of_airline AND t.flight_num = f.flight_num AND f.name_of_airline = \'{}\' "
        cursor.execute(query.format(email, staff_airl[0]))
        history = cursor.fetchall()
        print (history)
        lst = [a for a in history]
        cursor.close()
        return render(request, 'staff/customerhistory.html', {'lst': lst})

@login_required(login_url='login')
def revenue_comparison(request):
    cursor = conn.cursor()
    email = request.user.email
    q = "SELECT name_of_airline FROM airline_staff WHERE email = \'{}\' "
    cursor.execute(q.format(email))
    staff_airl = cursor.fetchone()
    cursor.close()
    cursor = conn.cursor()

    revenue_wo_ag_lm = "SELECT SUM(price) from flight NATURAL JOIN bookings NATURAL JOIN ticket WHERE name_of_airline = \'{}\' and booking_agent_ID is NULL AND (booking_date BETWEEN DATE_SUB(DATE(NOW()), INTERVAL 30 DAY) AND DATE(NOW()) )".format(staff_airl[0])
    cursor.execute(revenue_wo_ag_lm)
    wo_ag_lm = cursor.fetchone()
    if not wo_ag_lm[0]:
        wo_ag_lm = 0
    else:
        wo_ag_lm = int(wo_ag_lm[0])
    revenue_w_ag_lm = "SELECT SUM(price) from flight NATURAL JOIN bookings NATURAL JOIN ticket WHERE name_of_airline = \'{}\' and booking_agent_ID is NOT NULL AND (booking_date BETWEEN DATE_SUB(DATE(NOW()), INTERVAL 30 DAY) AND DATE(NOW()) )".format(staff_airl[0])
    cursor.execute(revenue_w_ag_lm)
    ag_lm = cursor.fetchone()
    if not ag_lm[0]:
        ag_lm = 0
    else:
        ag_lm = int(ag_lm[0])
    revenue_wo_ag_ly = "SELECT SUM(price) from flight NATURAL JOIN bookings NATURAL JOIN ticket WHERE name_of_airline = \'{}\' and booking_agent_ID is NULL AND (booking_date BETWEEN DATE_SUB(DATE(NOW()), INTERVAL 365 DAY) AND DATE(NOW()) )".format(staff_airl[0])
    cursor.execute(revenue_wo_ag_ly)
    wo_ag_ly = cursor.fetchone()
    if not wo_ag_ly[0]:
        wo_ag_ly = 0
    else:
        wo_ag_ly = int(wo_ag_ly[0])
    revenue_w_ag_ly = "SELECT SUM(price) from flight NATURAL JOIN bookings NATURAL JOIN ticket WHERE name_of_airline = \'{}\' and booking_agent_ID is NOT NULL AND (booking_date BETWEEN DATE_SUB(DATE(NOW()), INTERVAL 365 DAY) AND DATE(NOW()) )".format(staff_airl[0])
    cursor.execute(revenue_w_ag_ly)
    w_ag_ly = cursor.fetchone()
    if not w_ag_ly[0]:
        w_ag_ly = 0
    else:
        w_ag_ly = int(w_ag_ly[0])

    print (ag_lm, wo_ag_lm, w_ag_ly, wo_ag_ly)
    cursor.close()
    month_last = "SELECT DATE_SUB(DATE(NOW()), INTERVAL 30 DAY)"
    cursor = conn.cursor()
    cursor.execute(month_last)
    month_last = cursor.fetchone()[0]
    cursor.close()
    year_last = "SELECT DATE_SUB(DATE(NOW()), INTERVAL 365 DAY)"
    cursor = conn.cursor()
    cursor.execute(year_last)
    year_last = cursor.fetchone()[0]
    cursor.close()

    image = BytesIO()
    fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 10))
    fig.suptitle('Revenue(Direct) vs Revenue(Indirect)')
    lst1 = [wo_ag_lm, ag_lm]
    lst2 = [wo_ag_ly, w_ag_ly]
    ax1.set_title('last month')
    ax1.pie(lst1, labels = ['Direct','Indirect'])
    ax2.set_title('last year')
    ax2.pie(lst2, labels = ['Direct','Indirect'])
    fig.legend(loc = 'center right')
    fig.savefig(image, format='png')
    image.seek(0)
    plot_url = base64.b64encode(image.getvalue()).decode('utf8')
    return render(request, 'staff/revenue_comparison.html', {'plot_url': plot_url})

@login_required(login_url='login')
def newpermission(request):
    email = request.user.email
    cursor = conn.cursor()
    q = "SELECT admin_permission FROM airline_staff WHERE email = \'{}\' "
    cursor.execute(q.format(email))
    admin_permission = cursor.fetchone()
    email = request.user.email
    q = "SELECT name_of_airline FROM airline_staff WHERE email = \'{}\' "
    cursor.execute(q.format(email))
    staff_airl = cursor.fetchone()
    if (bool(admin_permission[0])):
        q = "SELECT email FROM airline_staff WHERE email != \'{}\' AND name_of_airline = \'{}\' AND (admin_permission = 0 OR operator_permission = 0)"
        cursor.execute(q.format(email, staff_airl[0]))
        employees = cursor.fetchall()
        employees = [a for a in employees]
        return render(request, 'staff/newpermission.html', {'employees': employees})
    else:
        redirect('staffhome')

@login_required(login_url='login')
def changepermission(request):
    if request.method == 'POST':
        email = request.user.email
        cursor = conn.cursor()
        q = "SELECT admin_permission FROM airline_staff WHERE email = \'{}\' "
        cursor.execute(q.format(email))
        admin_permission = cursor.fetchone()
        if (bool(admin_permission[0])):
            employee_email = request.POST['email']
            permission = request.POST['permission']
            if permission == "admin":
                query = "UPDATE airline_staff SET admin_permission = 1 WHERE email = \'{}\' "
                cursor.execute(query.format(employee_email))
                conn.commit()
                cursor.close()
            else:
                query = "UPDATE airline_staff SET operator_permission = 1 WHERE email = \'{}\' "
                cursor.execute(query.format(employee_email))
                conn.commit()
                cursor.close()
            return render(request, 'staff/changepermission.html')

@login_required(login_url='login')
def viewreports(request):
    cursor = conn.cursor()
    email = request.user.email
    q = "SELECT name_of_airline FROM airline_staff WHERE email = \'{}\' "
    cursor.execute(q.format(email))
    staff_airl = cursor.fetchone()[0]
    #for tickets sold last month
    today = "SELECT DATE(NOW())"
    cursor.execute(today)
    date_today = cursor.fetchone()[0]
    month_last = "SELECT DATE_SUB(DATE(NOW()), INTERVAL 30 DAY)"
    cursor.execute(month_last)
    date_last_month = cursor.fetchone()[0]
    query = "SELECT COUNT(*) FROM bookings NATURAL JOIN flight NATURAL JOIN ticket WHERE name_of_airline = \'{}\' AND DATE(booking_date) BETWEEN \'{}\' AND \'{}\' "
    cursor.execute(query.format(staff_airl, date_last_month, date_today))
    temp = cursor.fetchone()[0]
    print (temp)
    if not temp:
        ticket_sold_last_month = 0
    else:
        ticket_sold_last_month = int(temp)
    today = "SELECT DATE(NOW())"
    cursor.execute(today)
    date_today = cursor.fetchone()[0]
    year_last = "SELECT DATE_SUB(DATE(NOW()), INTERVAL 365 DAY)"
    cursor.execute(year_last)
    date_last_year = cursor.fetchone()[0]
    query = "SELECT COUNT(*) FROM bookings NATURAL JOIN flight NATURAL JOIN ticket WHERE name_of_airline = \'{}\' AND DATE(booking_date) BETWEEN \'{}\' AND \'{}\' "
    cursor.execute(query.format(staff_airl, date_last_month, date_today))
    temp = cursor.fetchone()[0]
    if not temp:
        ticket_sold_last_year = 0
    else:
        ticket_sold_last_year = int(temp)
    cursor.close()

    month_wise_query = "SELECT YEAR(date_sub(DATE(NOW()), interval {} month)) as year, MONTH(date_sub(DATE(NOW()), interval {} month)) as month, COUNT(*) FROM ticket NATURAL JOIN bookings NATURAL JOIN flight WHERE name_of_airline = \'{}\' AND YEAR(booking_date)=YEAR(date_sub(DATE(NOW()), interval {} month)) AND MONTH(booking_date) = MONTH(date_sub(DATE(NOW()), interval {} month))"
    lst = [month_wise_query.format("1","1",staff_airl, "1", "1"),month_wise_query.format("2","2",staff_airl, "2", "2"),month_wise_query.format("3","3",staff_airl, "3", "3"),month_wise_query.format("4","4",staff_airl, "4", "4"),month_wise_query.format("5","5",staff_airl, "5", "5"),month_wise_query.format("6","6",staff_airl, "6", "6"),month_wise_query.format("7","7",staff_airl, "7", "7"),month_wise_query.format("8","8",staff_airl, "8", "8"),month_wise_query.format("9","9",staff_airl, "9", "9"),month_wise_query.format("10","10",staff_airl, "10", "10"),month_wise_query.format("11","11",staff_airl, "11", "11"),month_wise_query.format("12","12",staff_airl, "12", "12")]
    index_m = []
    ticket_m = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    cursor = conn.cursor()
    for i, query in enumerate(lst):
        cursor.execute(query)
        ticket = cursor.fetchone()
        if ticket[2]:
            ticket_m[i] = int(ticket[2])
        index_m.append(str(ticket[0])+'-'+str(ticket[1]))
    cursor.close()

    index_m.reverse()
    ticket_m.reverse()
    image = BytesIO()
    plt.clf()
    ax = plt.gca()
    ax.tick_params(axis = 'both', which = 'major', labelsize = 6)
    plt.bar(index_m, height = ticket_m, width = 0.5)
    plt.xlabel('month')
    plt.ylabel('tickets sold')
    plt.title("Month Wise Tickets Sold (in the past one year)")
    image.seek(0)
    plt.savefig(image, format='png')
    plot_url = base64.b64encode(image.getvalue()).decode('utf8')

    return render(request, 'staff/viewreports.html', {'plot_url': plot_url})
