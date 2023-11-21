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
import ssl
import smtplib
import os

# Create your views here.
conn = pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'Haider110!',
    db = 'new_airline',
    )

@login_required(login_url='login')
def customerhome(request):
    final_results = []
    # accessing the current session information
    email = request.user.email
    cursor = conn.cursor()
    query = "SELECT name_of_airline, flight_num, departure_airport_name, departure_time, arrival_airport_name, arrival_time, status FROM bookings NATURAL JOIN (ticket NATURAL JOIN flight) WHERE email_customer = \'{}\' AND status = 'Upcoming' "
    query = query.format(email)
    cursor.execute(query)
    data = cursor.fetchall()
    for x in range(len(data)):
        temp = list(data[x])
        final = tuple(temp)
        final_results.append(final)
    cursor.close()
    return render(request, 'customer/customerhome.html', {'data': final_results})


@login_required(login_url='login')
def customer_search_flight(request):
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
    return render(request, 'customer/customer_search_flight.html', {'departure_airports':dp_lst,
                                                           'departure_airports_city': dac_list,
                                                           'destination_airports': da_lst,
                                                           'destination_airports_city': dtac_list})
@login_required(login_url='login')
def customer_search_results(request):
    final_results = []
    if request.method == 'POST':
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
            return render(request, 'customer/customer_search_flight.html', {'message': message})
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
            # we also have to check how many available seats are left for customers to purchase.
            seats_available = []
            for fl in results:
                # here we retrieve information about all the flights the user is interested in
                name_of_airline = fl[0]
                flight_num = fl[1]
                # now we check how many seats are avaiable
                q = "SELECT ID_airplane FROM flight WHERE name_of_airline = \"{}\" AND flight_num = \"{}\" ".format(name_of_airline,flight_num)
                cursor.execute(q)
                id = cursor.fetchone()[0]
                q1 = "SELECT num_of_seats FROM airplane WHERE ID_airplane = \"{}\" AND name_of_airline = \"{}\" ".format(id, name_of_airline)
                cursor.execute(q1)
                seats_tot = cursor.fetchone()[0]
                # now we can add a query to see my how many tickets are presently there
                q2 = "SELECT COUNT(*) FROM ticket WHERE name_of_airline = \"{}\" AND flight_num = \"{}\" ".format(name_of_airline,flight_num)
                cursor.execute(q2)
                seats_sold = cursor.fetchone()[0]
                seats_left = int(seats_tot) - int(seats_sold)
                seats_available.append((seats_left))
            for x in range(len(results)):
                temp = list(results[x])
                temp.append(seats_available[x])
                final = tuple(temp)
                final_results.append(final)
            for f in final_results:
                if f[-1] == 0:
                    final_results.remove(f)
            cursor.close()
            flight_nums = [int(a[1]) for a in final_results]
            return render (request, 'customer/customer_search_results.html', {'final_results': final_results, 'flight_nums':flight_nums})


@login_required(login_url='login')
def purchaseticket(request):
    if request.method == 'POST':
        cursor = conn.cursor()
        choice = request.POST['choice']
        x = choice.split(',')
        name_of_airline = (x[0][2:-1])
        flight_num = x[1][1:]
        customer_email = request.user.email
        query = "SELECT * FROM bookings b NATURAL JOIN ticket t WHERE b.email_customer = \"{}\" AND t.name_of_airline = \"{}\" AND t.flight_num = \"{}\" "
        cursor.execute(query.format(customer_email, name_of_airline, flight_num))
        previous_purchased = cursor.fetchall()
        if previous_purchased:
            message = 'Ticket already purchased! Can only buy one ticket per flight!'
            return render(request, 'customer/purchaseticket.html', {'message': message})
        query = "SELECT MAX(ticket_id) FROM ticket"
        cursor.execute(query)
        temp = cursor.fetchone()
        if temp:
            id = int(temp[0]) + 1
        else:
            id = 1
        ticket_q = "INSERT INTO ticket (ticket_id, name_of_airline, flight_num) VALUES (\'{}\', \'{}\', \'{}\') ".format(id, name_of_airline, flight_num)
        cursor.execute(ticket_q)
        conn.commit()
        cursor.close()
        cursor = conn.cursor()
        bookings_q = "INSERT INTO bookings VALUES (\'{}\', \'{}\', NULL, DATE(NOW()))".format(id, customer_email)
        cursor.execute(bookings_q)
        conn.commit()
        cursor.close()
        subject = "Booking Confirmation"
        msg = "This message is your booking confirmation for flight number \'{}\ of \'{}\'.".format(flight_num, name_of_airline)
        print (msg)
        return render(request, 'customer/purchaseticket.html')

@login_required(login_url='login')
def trackmyspending(request):
    username = request.user.email
    cursor = conn.cursor()
    past_year = "SELECT SUM(price) FROM bookings NATURAL JOIN ticket NATURAL JOIN flight where email_customer = \"{}\" AND booking_date BETWEEN date_sub(DATE(NOW()), interval 1 year) AND DATE(NOW())".format(username)
    cursor.execute(past_year)
    expenditure = cursor.fetchone()
    cursor.close()
    if not past_year:
        past_year = '0'
    else:
        past_year = past_year[0]
    # it is also mentioned taht we have to check past months data as well for up to 6 months
    qm = "SELECT YEAR(date_sub(DATE(NOW()), interval {} month)) as year , MONTH(date_sub(DATE(NOW()), interval {} month)) as month, SUM(price) FROM ticket NATURAL JOIN bookings NATURAL JOIN flight WHERE email_customer=\'{}\' AND YEAR(booking_date)=YEAR(date_sub(DATE(NOW()), interval {} month))  AND MONTH(booking_date)= MONTH(date_sub(DATE(NOW()), interval {} month))"
    # We can represent months by numbers 0, 1, 2, 3, 4, 5
    qm_list = [qm.format("0","0",username, "0", "0"),
               qm.format("1","1",username, "1", "1"),
               qm.format("2","2",username, "2", "2"),
               qm.format("3","3",username, "3", "3"),
               qm.format("4","4",username, "4", "4"),
               qm.format("5","5",username, "5", "5")]
    index_m = []
    m_spending_customer = [0, 0, 0, 0, 0, 0]
    cursor = conn.cursor()
    for x, spending_query in enumerate(qm_list):
        cursor.execute(spending_query)
        cust_spending = cursor.fetchone()
        if cust_spending[2]: #this is bascially sum(price)
            m_spending_customer[x] = int(cust_spending[2])
        index_m.append(str(cust_spending[0])+'-'+str(cust_spending[1])) #to show the months
    cursor.close()

    img = BytesIO()
    fig, (ax1, ax2) = plt.subplots(2, figsize=(10,10))
    fig.suptitle('Past 6 Months Spending Track')
    ax1.bar(index_m, height=m_spending_customer)
    ax1.set_xlabel('month')
    ax1.set_ylabel('amount of spending')
    ax2.pie(m_spending_customer, labels=index_m)
    fig.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return render(request, 'customer/trackmyspending.html', {'past_year':past_year, 'm_spending_customer': m_spending_customer, 'index_m': index_m, 'plot_url': plot_url})
