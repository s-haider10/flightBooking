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



conn = pymysql.connect(   
    host = 'localhost',
    user = 'root',
    password = 'Haider110!',
    db = 'new_airline',
    )



@login_required(login_url='login')
def agenthome(request):
    upcoming_flights = []
    final_d = []
    email = request.user.email
    cursor = conn.cursor()
    query = "SELECT booking_agent_ID from booking_agent WHERE email = \"{}\" ".format(email)
    cursor.execute(query)
    id_agent = cursor.fetchone()
    cursor.close()
    your_flights = "SELECT f.name_of_airline, f.flight_num, f.departure_airport_name, f.departure_time, f.arrival_airport_name, f.arrival_time, f.price, b.email_customer FROM bookings b, ticket t, flight f WHERE b.booking_agent_id = \"{}\" AND b.ticket_id = t.ticket_id AND f.name_of_airline = t.name_of_airline AND t.flight_num = f.flight_num AND status = 'Upcoming'".format(id_agent[0])
    cursor = conn.cursor()
    cursor.execute(your_flights)
    info = cursor.fetchall()
    for x in range(len(info)):
        temp = list(info[x])
        final = tuple(temp)
        upcoming_flights.append(final)
    cursor.close()
    your_flights_delayed = "SELECT f.name_of_airline, f.flight_num, f.departure_airport_name, f.departure_time, f.arrival_airport_name, f.arrival_time, f.price, b.email_customer FROM bookings b, ticket t, flight f WHERE b.booking_agent_id = \"{}\" AND b.ticket_id = t.ticket_id AND f.name_of_airline = t.name_of_airline AND t.flight_num = f.flight_num AND status = 'Delayed'".format(id_agent[0])
    cursor = conn.cursor()
    cursor.execute(your_flights_delayed)
    info_delayed = cursor.fetchall()
    # info = [a for a in info]
    #info_delayed = [a for a in info_delayed]
    for i in range(len(info_delayed)):
        temp = list(info_delayed[i])
        final_delayed = tuple(temp)
        final_d.append(final_delayed)
    cursor.close()
    return render(request, 'agent/agenthome.html', {'info': upcoming_flights, 'info_delayed': final_d})

@login_required(login_url='login')
def agentsearchflights(request):
    cursor = conn.cursor()
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
    return render(request, 'agent/agentsearchflights.html', {'departure_airports':dp_lst,
                                                           'departure_airports_city': dac_list,
                                                           'destination_airports': da_lst,
                                                           'destination_airports_city': dtac_list})
@login_required(login_url='login')
def agent_search_results(request):
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
                print (f[-1])
                if int(f[-1]) <= 0:
                    final_results.remove(f)
            print (final_results)
            cursor.close()
            flight_nums = [int(a[1]) for a in final_results]
            return render (request, 'agent/agent_search_results.html', {'final_results': final_results, 'flight_nums':flight_nums})


@login_required(login_url='login')
def agentpurchaseticket(request):
    if request.method == 'POST':
        cursor = conn.cursor()
        choice = (request.POST['choice'])
        x = choice.split(',')
        print (choice)
        name_of_airline = (x[0][2:-1]) #TO REMOOVE ALL THE COMMAS AND UNNECCARY ELEMENTS
        print (name_of_airline)
        
        flight_num = x[1][1:]
        print (flight_num)
        email = request.POST['email']
        query = "SELECT * FROM bookings b NATURAL JOIN ticket t WHERE b.email_customer = \"{}\" AND t.name_of_airline = \"{}\" AND t.flight_num = \"{}\" "
        print ("--------------------------------")
        cursor.execute(query.format(email, name_of_airline, flight_num))
        previous_purchased = cursor.fetchall()
        if previous_purchased:
            message = 'Customer is only allowed to buy one ticket! You customer has already purchased one ticket.'
            return render(request, 'agent/agentsearchflights.html', {'message': message})
        query = "SELECT MAX(ticket_id) FROM ticket"
        cursor.execute(query)
        temp = cursor.fetchone()
        if temp:
            id = int(temp[0]) + 1
        else:
            id = 1
        print(id)
        query = "SELECT email, name_of_airline FROM agent_works_for WHERE email = \'{}\' AND name_of_airline = \'{}\' ".format(request.user.email, name_of_airline)
        # checking if the user works for the airline or no
        cursor.execute(query)
        verification = cursor.fetchone()
        if not verification:
            message = 'You do not work for this airline, hence you cannot purchase the ticket!'
            return render(request, 'agent/agentsearchflights.html', {'message': message})
        ticket_q = "INSERT INTO ticket (ticket_id, name_of_airline, flight_num) VALUES (\'{}\', \'{}\', \'{}\') ".format(id, name_of_airline, flight_num)
        cursor.execute(ticket_q)
        conn.commit()
        cursor.close()
        agent = request.user.email
        cursor = conn.cursor()
        query = "SELECT booking_agent_ID from booking_agent WHERE email = \"{}\" ".format(agent)
        cursor.execute(query)
        id_agent = cursor.fetchone()
        bookings_q = "INSERT INTO bookings VALUES (\'{}\', \'{}\', \'{}\', DATE(NOW()))".format(id, email, id_agent[0])
        cursor.execute(bookings_q)
        conn.commit()
        cursor.close()
        return render(request, 'agent/agentpurchaseticket.html')

@login_required(login_url='login')
def viewcommission(request):
    agent = request.user.email
    cursor = conn.cursor()
    query = "SELECT booking_agent_ID from booking_agent WHERE email = \"{}\" ".format(agent)
    cursor.execute(query)
    id_agent = cursor.fetchone()

    query = "SELECT 0.1*SUM(f.price) FROM bookings b, flight f, ticket t WHERE b.booking_agent_id = \"{}\" AND b.ticket_id = t.ticket_id AND t.name_of_airline = f.name_of_airline AND t.flight_num = f.flight_num"
    cursor.execute(query.format(id_agent[0]))
    agentcommission = list(cursor.fetchone())


    query = "SELECT COUNT(*) FROM bookings WHERE booking_agent_id = \"{}\" AND booking_date >= ADDDATE(DATE(NOW()), INTERVAL -30 DAY) "
    cursor.execute(query.format(id_agent[0]))
    tot_ticket_30 = cursor.fetchone()

    query = "SELECT COUNT(*) FROM bookings WHERE booking_agent_id = \"{}\" "
    cursor.execute(query.format(id_agent[0]))
    tot_ticket = list(cursor.fetchone())
    cursor.close()
    # average_commision = round(int(agentcommission[0]) / int(tot_ticket[0]), 1)
    return render(request, 'agent/viewcommission.html', {'tot_ticket_30': list(tot_ticket_30), 'tot_ticket':tot_ticket, 'agentcommission':agentcommission})

@login_required(login_url='login')
def viewtopcustomers(request):
    agent = request.user.email
    cursor = conn.cursor()
    query = "SELECT booking_agent_ID from booking_agent WHERE email = \"{}\" ".format(agent)
    cursor.execute(query)
    id_agent = cursor.fetchone()

    query = "SELECT b.email_customer, COUNT(b.email_customer), c.name, c.phone_num, c.city, c.state, c.date_of_birth FROM bookings b, customer c WHERE b.booking_agent_id = \"{}\" AND b.booking_date >= ADDDATE(DATE(NOW()), INTERVAL -6 MONTH) AND b.email_customer = c.email GROUP BY b.email_customer ORDER BY COUNT(b.email_customer) DESC"
    cursor.execute(query.format(id_agent[0]))
    list_customer = []
    temp = cursor.fetchone()
    count = 1
    while temp and count <=5:
        list_customer.append(list(temp))
        temp = cursor.fetchone()
        count += 1
    cursor.close()
    top5cust = tuple(list_customer)


    cursor = conn.cursor()
    query = "SELECT b.email_customer, 0.1 * SUM(f.price), c.name, c.phone_num, c.city, c.state, c.date_of_birth FROM bookings b, customer c, flight f, ticket t WHERE b.booking_agent_id = \"{}\" AND b.booking_date >= ADDDATE(DATE(NOW()), INTERVAL -6 MONTH) AND  b.ticket_id = t.ticket_id AND t.name_of_airline = f.name_of_airline AND t.flight_num = f.flight_num AND b.email_customer = c.email GROUP BY b.email_customer ORDER BY SUM(f.price) DESC"
    cursor.execute(query.format(id_agent[0]))

    list_customer = []
    temp = cursor.fetchone()
    count = 1
    while temp and count <=5:
        list_customer.append(list(temp))
        temp = cursor.fetchone()
        count += 1
    cursor.close()
    top5cust_commision = tuple(list_customer)

    x1 = [row[2] for row in top5cust]
    y1 = [int(row[1]) for row in top5cust]

    x2 = [row[2] for row in top5cust_commision]
    y2 = [float(row[1]) for row in top5cust_commision]

    img = BytesIO()
    fig, (ax1, ax2) = plt.subplots(2, figsize=(10,10))
    ax1.bar(x1, height=y1, width=0.2, color='red', edgecolor='yellow')
    ax1.set_xlabel('Customer')
    ax1.set_ylabel('Ticket Number Sold')
    ax1.set_title('Top 5 Customers -  Ticket Sold')
    ax2.bar(x2, height=y2, width=0.3, color='blue', edgecolor='green')
    ax2.set_xlabel('Customer')
    ax2.set_ylabel('Commission Earned ($ USD)')
    ax2.set_title('Top 5 Customers - Commission Earned')
    fig.legend(loc='center right')
    fig.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return render(request, 'agent/viewtopcustomers.html', {'top5cust_commision': top5cust_commision, 'top5cust': top5cust, 'plot_url': plot_url})
