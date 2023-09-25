import hashlib
import time
from flask import Flask, render_template, request, url_for, redirect, session, jsonify
from pymysql.converters import escape_string
import mysql.connector
import pymysql
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

app = Flask(__name__, static_url_path="/", static_folder="static")

conn = pymysql.connect(host='localhost',user='root', password='password', database='projectpart3')



@app.route('/')
def hello():
	if 'username1' in session:
		return redirect('/CustomerViewMyFlights')
	elif 'username2' in session:
		return redirect('/BookingAgentViewMyFlights')
	elif 'username3' in session:
		return redirect('/StaffViewMyFlights')
	else:
		return render_template('index.html')


@app.route('/index')
def index():
	return render_template('index.html')


@app.route('/login')
def login():
	return render_template('login.html')


@app.route('/register')
def register():
	return render_template('register.html')

# -------------------------------------------------Public Function --------------------------------------------

# Search Flight Page using date
@app.route('/SearchFlightThroughDateAuth', methods=['GET', 'POST'])
def SearchFlightThroughDateAuth():
	date = request.form['date']
	departure = request.form['departure']
	arrival = request.form['arrival']
	cursor = conn.cursor()
	query = """SELECT *\
			FROM flight, airport\
			WHERE flight.departure_airport = airport.name And (departure_airport = %s OR city = %s)\
            AND datediff(flight.departure_date, %s)=0\
			AND flight.flight_num in\
			(SELECT flight.flight_num \
			FROM flight, airport\
			WHERE flight.arrival_airport = airport.name and (arrival_airport = %s OR city = %s))"""
	cursor.execute(query, (departure, departure,  date, arrival, arrival))
	rows = cursor.fetchall()
	print("Show the info", rows)
	cursor.close()
	return render_template('Public_Flight_Info.html', rows=rows)


# Search Flight Status using flight number
@app.route('/SearchFlightThroughFlightNumberAuth', methods=['GET', 'POST'])
def SearchFlightThroughFlightNumberAuth():
	FlightNumber = request.form['FlightNumber']
	DepartureDate = request.form['DepartureDate']
	ArrivalDate = request.form['ArrivalDate']
	cursor = conn.cursor()
	query = "SELECT *\
			FROM flight\
			WHERE flight_num = %s AND datediff(flight.departure_date, %s)=0 AND datediff(flight.arrival_date, %s)=0"
	cursor.execute(query, (FlightNumber,DepartureDate,ArrivalDate))
	rows = cursor.fetchall()
	cursor.close()
	return render_template('Public_Flight_Info.html', rows=rows)


# ----------------------------------------Log in-----------------------------------------------
@app.route('/CustomerLoginAuth', methods=['GET', 'POST'])
def CustomerLoginAuth():
	email = request.form['email']
	password = request.form['password']
	cursor = conn.cursor()
	query = "SELECT * FROM customer WHERE email = %s and password = %s"
	cursor.execute(query, (email, password)) #!!!
	data = cursor.fetchone()
	cursor.close()
	error = None
	if(data):
		session['username1'] = email
		return redirect("/CustomerViewMyFlights")
	else:
		error = 'Invalid login or username'
		return render_template('login.html', error=True)


@app.route('/AgentLoginAuth', methods=['GET', 'POST'])
def AgentLoginAuth():
	email = request.form['email']
	password = request.form['password']
	cursor = conn.cursor()
	query = "SELECT * FROM booking_agent WHERE email = %s and password = %s"
	cursor.execute(query,(email, hashlib.md5(password.encode()).hexdigest()))
	data = cursor.fetchone()
	cursor.close()
	error = None
	if(data):
		session['username2'] = email
		return redirect("/BookingAgentViewMyFlights")
	else:
		error = 'Invalid login or username'
		return render_template('login.html', error=True)


@app.route('/StaffLoginAuth', methods=['GET', 'POST'])
def StaffLoginAuth():
	username = request.form['username']
	password = request.form['password']
	cursor = conn.cursor()
	query = "SELECT * FROM airline_staff WHERE username = %s and password = %s"
	cursor.execute(query, (username, hashlib.md5(password.encode()).hexdigest()))
	data = cursor.fetchone()
	cursor.close()
	error = None
	if(data):
		session['username3'] = [username,data[-1],data[-2]]
		return redirect('/StaffViewMyFlights')
	else:
		error = 'Invalid login or username'
		return render_template('login.html', error=True)


# -------------------------------------Register---------------------------------------------------------
# Authenticates the register for customer
@app.route('/CustomerRegisterAuth', methods=['GET', 'POST'])
def CustomerRegisterAuth():
	email = request.form['email']
	name = request.form['name']
	password = request.form['password']
	building_number = request.form['building_number']
	street = request.form['street']
	city = request.form['city']
	state = request.form['state']
	phone_number = request.form['phone_number']
	passport_number = request.form['passport_number']
	passport_expiration = request.form['passport_expiration']
	passport_country =request.form['passport_country']
	date_of_birth =request.form['date_of_birth']
	cursor = conn.cursor()
	query = "SELECT * FROM customer WHERE email = %s"
	cursor.execute(query, (email))
	data = cursor.fetchone()
	error = None
	if(data):
		error = "This user already exists!"
		return render_template('register.html', error = error)
	else:
		try:
			ins = "INSERT INTO customer VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			cursor.execute(ins, (email, name, hashlib.md5(password.encode()).hexdigest(), building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth))
			conn.commit()
			cursor.close()
		except:
			return render_template('register.html', error='Failed to register user.')
		return redirect('/login')

@app.route('/AgentRegisterAuth', methods=['GET', 'POST'])
def AgentRegisterAuth():
	email = request.form['email']
	password = request.form['password']
	booking_agent_id = request.form['booking_agent_id']
	cursor = conn.cursor()
	query = "SELECT * FROM booking_agent WHERE email = %s"
	cursor.execute(query, (email))
	data = cursor.fetchone()
	error = None
	if(data):
		error = "This user already exists!"
		return render_template('register.html', error = error)
	else:
		ins = "INSERT INTO booking_agent VALUES(%s,%s,%s)"
		cursor.execute(ins,(email, hashlib.md5(password.encode()).hexdigest(), booking_agent_id))
		conn.commit()
		cursor.close()
		return redirect('/login')

# Authenticates the register for airline staff
@app.route('/AirlineStaffRegisterAuth', methods=['GET', 'POST'])
def AirlineStaffRegisterAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	date_of_birth = request.form['date_of_birth']
	permission = 'Normal'
	airline_name = request.form['airline_name']
	cursor = conn.cursor()
	query = "SELECT * FROM airline_staff WHERE username = %s"
	cursor.execute(query, (username))
	data = cursor.fetchone()
	error = None
	if(data):
		error = "This user already exists!"
		return render_template('register.html', error = True)
	else:
		try:
			ins = "INSERT INTO airline_staff VALUES(%s,%s,%s,%s,%s,%s,%s)"
			cursor.execute(ins, (username, hashlib.md5(password.encode()).hexdigest(), first_name, last_name, date_of_birth, permission, airline_name))
			conn.commit()
			cursor.close()
			return render_template('login.html', message = True)
		except:
			return render_template('register.html', error = True)


# --------------------------------------------------------Log out--------------------------------------------
@app.route('/CustomerLogout')
def CustomerLogout():
	session.pop('username1')
	return redirect('/')
@app.route('/BookingAgentLogout')
def BookingAgentLogout():
	session.pop('username2')
	return redirect('/')
@app.route('/AirlineStaffLogout')
def AirlineStaffLogout():
	session.pop('username3')
	return redirect('/')
#--------------------------------------------------------Customer Function----------------------------------------------

# Customer view their booked flights
@app.route('/CustomerViewMyFlights', methods=['GET', 'POST'])
def CustomerViewMyFlights():
	if session.get('username1'):
		email = session['username1']
		cursor = conn.cursor()
		if request.method == 'GET':
			cursor = conn.cursor()
			query = "select flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_date, flight.departure_time, flight.arrival_airport, flight.arrival_date, flight.arrival_time, flight.price, flight.status, flight.airplane_id\
					from flight, ticket, purchase, customer\
					where status = 'upcoming' and flight.flight_num = ticket.flight_num and flight.airline_name = ticket.airline_name and purchase.ticket_id = ticket.ticket_id and purchase.customer_email = customer.email and customer.email = %s;"
			cursor.execute(query, (email))
			rows = cursor.fetchall()
			cursor.close()
			return render_template('Customer_View_My_Flights.html', rows = rows)
		if request.method == 'POST':
			departure = request.form['departure']
			destination = request.form['destination']
			DepartureDate = request.form['DepartureDate']
			ArrivalDate = request.form['ArrivalDate']
			para_dept = [email]
			para_arr = [email]
			query_dept = "select flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_date, flight.departure_time, flight.arrival_airport, flight.arrival_date, flight.arrival_time, flight.price, flight.status, flight.airplane_id\
					from purchase, ticket, flight, airport\
					where  purchase.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND flight.departure_airport = airport.name and purchase.customer_email = %s "
			query_arr = "AND (flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_date, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id) IN\
					(select flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_date, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id\
					from purchase, ticket, flight, airport\
					where  purchase.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND flight.arrival_airport = airport.name and purchase.customer_email = %s "
			if departure != "":
				query_dept += " AND (flight.departure_airport = %s OR airport.city = %s)"
				para_dept.append(pymysql.converters.escape_string(departure))
				para_dept.append(pymysql.converters.escape_string(departure))
			if destination != "":
				query_arr += " AND (flight.arrival_airport = %s OR airport.city = %s)"
				para_arr.append(pymysql.converters.escape_string(destination))
				para_arr.append(pymysql.converters.escape_string(destination))
			if DepartureDate != "":
				query_dept += " AND flight.departure_date >= %s"
				query_arr += " AND flight.departure_date >= %s"
				para_arr.append(DepartureDate)
				para_dept.append(DepartureDate)
			if ArrivalDate != "":
				query_dept += " AND flight.arrival_date <= %s"
				query_arr += " AND flight.arrival_date <= %s"
				para_arr.append(ArrivalDate)
				para_dept.append(ArrivalDate)
			query = query_dept +query_arr + ")"
			para = para_dept + para_arr
			cursor.execute(query, (para))
			rows = cursor.fetchall()
			cursor.close()
			return render_template('Customer_View_My_Flights.html', rows=rows,message=True)
		elif request.method == 'GET':
			new_query = "SELECT flight.airline_name,flight.flight_num,flight.departure_airport, flight.departure_date, flight.departure_time, flight.arrival_airport, flight.arrival_date, flight.arrival_time,flight.price,flight.status,flight.airplane_id FROM purchase, ticket, flight  WHERE purchase.ticket_id = ticket.ticket_id and flight.flight_num = ticket.flight_num and customer_email = %s"
			cursor.execute(new_query, (email))
			rows = cursor.fetchall()
			return render_template('Customer_View_My_Flights.html', rows=rows)
	else:
		return redirect('/login')

@app.route('/CustomerSearchTickets')
def customerSearchTickets():
	if session.get('username1'):
		return render_template('Customer_Search_Tickets.html')
	else:
		return redirect('/login')

# Customer purchase new tickets
@app.route('/CustomerPurchaseTickets', methods=['GET', 'POST'])
def CustomerPurchaseTickets():
	if session.get('username1'):
		email = session['username1']
		if request.method == "GET":
			return render_template("Customer_Purchase_Tickets.html")
		else:
			try:
				cursor = conn.cursor()
				AirlineCompany = request.form['AirlineCompany']
				FlightNumber = request.form['FlightNumber']
				query_seats_total = "select seats from flight, airplane where flight.airline_name = %s and flight.flight_num = %s and flight.airplane_id = airplane.id"
				cursor.execute(query_seats_total,(AirlineCompany,FlightNumber))
				seats_total = cursor.fetchall()
				query_purchased = "SELECT COUNT(ticket_id),flight.flight_num FROM ticket,flight WHERE flight.airline_name = %s and flight.flight_num = %s and ticket.flight_num = flight.flight_num"
				cursor.execute(query_purchased,(AirlineCompany, FlightNumber))
				purchased = cursor.fetchall()
				query_ticket_id = "SELECT MAX(ticket_id) + 1 FROM ticket;"
				cursor.execute(query_ticket_id)
				ticket_id = cursor.fetchall()
				ticket_id = ticket_id[0][0]

				# stores the results in a variable
			except:
				return render_template('Customer_Purchase_Tickets.html', error=True)
			if seats_total <= purchased:
				conn.commit()
				cursor.close()
				return render_template('Customer_Purchase_Tickets.html',error = True)
			else:
				try:
					query_insert_ticket = "INSERT INTO ticket (ticket_id, airline_name, flight_num) VALUES (%s, %s, %s)"
					query_insert_purchase = "INSERT INTO purchase (ticket_id, customer_email, booking_agent_email, purchase_date) VALUES (%s, %s,null, %s)"
					t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
					t = t[:10]
					print(ticket_id, AirlineCompany, FlightNumber,email,t)
					cursor.execute(query_insert_ticket,(ticket_id, AirlineCompany, FlightNumber))
					cursor.execute(query_insert_purchase,(ticket_id,email,t))
					conn.commit()
					cursor.close()
					return render_template('Customer_Purchase_Tickets.html',message = True)
				except:
					return render_template('Customer_Purchase_Tickets.html',error = True)
	else:
		return redirect('/login')

# Customer Search Flight Page thorugh date
@app.route('/CustomerSearchFlight', methods=['GET', 'POST'])
def CustomerSearchFlight():
	date = request.form['date']
	departure = request.form['departure']
	arrival = request.form['arrival']
	cursor = conn.cursor()
	query = "SELECT *\
			FROM flight, airport\
			WHERE flight.departure_airport = airport.name and (departure_airport = %s OR city = %s) AND\
			datediff(flight.departure_date, %s)=0\
			AND flight.flight_num in\
			(SELECT flight.flight_num \
			FROM flight, airport\
			WHERE flight.arrival_airport = airport.name and (arrival_airport = %s OR city = %s))"
	cursor.execute(query, (departure, departure, date, arrival, arrival))
	rows = cursor.fetchall()
	cursor.close()
	return render_template('Customer_Search_Tickets.html', rows=rows)


@app.route('/CustomerTrackMySpending', methods=['GET', 'POST'])
def CustomerTrackMySpending():
	if session.get('username1'):
		if request.method == 'GET':
			return render_template("Customer_Track_My_Spending.html")
		email = session['username1']
		cursor = conn.cursor()
		if request.form.get('StartMonth') is None:
			StartMonth_1 = str(date.today()- relativedelta(months = 12))
			StartMonth = str(date.today()- relativedelta(months = 6))
			EndMonth = str(date.today())
		else:
			StartMonth_1 = request.form['StartMonth']
			StartMonth = request.form['StartMonth']
			EndMonth = request.form['EndMonth']
		query_1 = "select sum(flight.price)\
					from purchase, ticket, flight\
					where purchase.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND purchase.customer_email = %s AND purchase_date >= %s AND purchase_date <= %s"
		query = "select sum(flight.price), YEAR(purchase_date), MONTH(purchase_date)\
				from purchase, ticket, flight\
				where purchase.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND purchase.customer_email = %s AND purchase_date >= %s AND purchase_date <= %s\
				group by YEAR(purchase_date), MONTH(purchase_date);"
		cursor.execute(query_1, (email,StartMonth_1, EndMonth))
		result_1 = cursor.fetchone()
		result_1 = int(result_1[0]) if result_1[0] else 0
		cursor.execute(query, (email, StartMonth, EndMonth))
		result = cursor.fetchall()
		rows = {}
		startDate = datetime.strptime(StartMonth,'%Y-%m-%d')
		endDate = datetime.strptime(EndMonth, '%Y-%m-%d')
		year = startDate.year
		month = startDate.month
		while year <= endDate.year:
			if year == endDate.year and month == endDate.month+1:
				break
			if month <= 12:
				temp = str(year)+"-"+str(month)
				rows[temp] = 0
				month += 1
			else:
				year += 1
				month = 1
		for i in result:
			rows[str(i[1])+"-"+str(i[2])] = int(i[0])
		array_1 = []
		for (key,value) in rows.items():
			array_1.append([key, value])
		cursor.close()
		dic = {}
		dic["data1"] = result_1
		dic["data2"] = array_1
		print(dic)
		return jsonify(dic)
	else:
		return redirect ('/login')

# ------------------------------------------------------Booking agent Function----------------------------------------------
@app.route('/BookingAgentViewMyFlights', methods=['GET', 'POST'])
def BookingAgentViewMyFlights():
	if session.get('username2'):
		email = session['username2']
		if request.method == 'GET':
			cursor = conn.cursor()
			query = "select flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_date, flight.departure_time, flight.arrival_airport, flight.arrival_date, flight.arrival_time, flight.price, flight.status, flight.airplane_id\
					from flight, ticket, purchase, booking_agent\
					where status = 'upcoming' and flight.flight_num = ticket.flight_num and flight.airline_name = ticket.airline_name and purchase.ticket_id = ticket.ticket_id and purchase.booking_agent_email = booking_agent.email and booking_agent.email = %s;"
			cursor.execute(query, (email))
			rows = cursor.fetchall()
			cursor.close()
			return render_template('Booking_Agent_View_My_Flights.html', rows = rows)
		if request.method == 'POST':
			cursor = conn.cursor()
			departure = request.form['departure']
			destination = request.form['destination']
			DepartureDate = request.form['DepartureDate']
			ArrivalDate = request.form['ArrivalDate']
			para_dept = [email]
			para_arr = [email]
			query_dept = "select flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_date, flight.departure_time, flight.arrival_airport, flight.arrival_date, flight.arrival_time, flight.price, flight.status, flight.airplane_id\
					from purchase, ticket, flight, airport, booking_agent\
					where booking_agent.email = purchase.booking_agent_email AND purchase.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND flight.departure_airport = airport.name and booking_agent.email = %s "
			query_arr = "AND (flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_date, flight.arrival_airport, flight.arrival_date, flight.price, flight.status, flight.airplane_id) IN\
					(select flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_date, flight.arrival_airport, flight.arrival_date, flight.price, flight.status, flight.airplane_id\
					from purchase, ticket, flight, airport, booking_agent\
					where booking_agent.email = purchase.booking_agent_email AND purchase.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND flight.arrival_airport = airport.name and booking_agent.email = %s "
			if departure != "":
				query_dept += " AND (flight.departure_airport = %s OR airport.city = %s)"
				para_dept.append(pymysql.converters.escape_string(departure))
				para_dept.append(pymysql.converters.escape_string(departure))
			if destination != "":
				query_arr += " AND (flight.arrival_airport = %s OR airport.city = %s)"
				para_arr.append(pymysql.converters.escape_string(destination))
				para_arr.append(pymysql.converters.escape_string(destination))
			if DepartureDate != "":
				query_dept += " AND flight.departure_date >= %s"
				query_arr += " AND flight.departure_date >= %s"
				para_arr.append(DepartureDate)
				para_dept.append(DepartureDate)
			if ArrivalDate != "":
				query_dept += " AND flight.arrival_date <=%s"
				query_arr += " AND flight.arrival_date <= %s"
				para_arr.append(ArrivalDate)
				para_dept.append(ArrivalDate)
			query = query_dept +query_arr + ")"
			para = para_dept + para_arr
			cursor.execute(query, (para))
			rows = cursor.fetchall()
			cursor.close()
			return render_template('Booking_Agent_View_My_Flights.html', rows=rows)
	else:
		return redirect('/login')


@app.route('/BookingAgentSearchTickets')
def BookingAgentSearchTickets():
	if session.get('username2'):
		return render_template('Booking_Agent_Search_Tickets.html')
	else:
		return redirect('/login')


@app.route('/BookingAgentSearchFlight', methods=['GET', 'POST'])
def BookingAgentSearchFlight():
	date = request.form['date']
	departure = request.form['departure']
	arrival = request.form['arrival']
	cursor = conn.cursor()
	query = "SELECT *\
			FROM flight, airport\
			WHERE flight.departure_airport = airport.name and (departure_airport = %s OR city = %s) AND\
			datediff(flight.departure_date, %s)=0\
			AND flight.flight_num in\
			(SELECT flight.flight_num \
			FROM flight, airport\
			WHERE flight.arrival_airport = airport.name and (arrival_airport = %s OR city = %s))"
	cursor.execute(query, (departure, departure, date, arrival, arrival))
	rows = cursor.fetchall()
	cursor.close()
	return render_template('Booking_Agent_Search_Tickets.html', rows=rows)


@app.route('/BookingAgentPurchaseTickets', methods=['GET', 'POST'])
def BookingAgentPurchaseTickets():
	if session.get('username2'):
		if request.method == "POST":
			try:
				email = session['username2']
				# cursor used to send queries
				cursor = conn.cursor()
				customer_email = request.form['customer_email']
				AirlineCompany = request.form['AirlineCompany']
				FlightNumber = request.form['FlightNumber']
				# executes query
				query_seats_total = "select seats from flight, airplane where flight.airline_name = %s and flight.flight_num = %s and flight.airplane_id = airplane.id"
				cursor.execute(query_seats_total, (AirlineCompany,FlightNumber))
				seats_total = cursor.fetchall()
				query_purchased = "SELECT COUNT(ticket_id),flight.flight_num FROM ticket,flight WHERE flight.airline_name = %s and flight.flight_num = %s and ticket.flight_num = flight.flight_num"
				cursor.execute(query_purchased, (AirlineCompany, FlightNumber))
				purchased = cursor.fetchall()
				query_ticket_id = "SELECT MAX(ticket_id) + 1 FROM ticket"
				cursor.execute(query_ticket_id)
				ticket_id = cursor.fetchall()
				ticket_id = ticket_id[0][0]
				booking_agent_id_query = "SELECT booking_agent_id FROM booking_agent WHERE email = %s"
				cursor.execute(booking_agent_id_query, (email))
				booking_agent_id = cursor.fetchall()
				booking_agent_id = booking_agent_id[0][0]
				query_permission = "select airline_name from work_for where booking_agent_email = %s"
				cursor.execute(query_permission,(email))
				permission = cursor.fetchall()
				p=list(permission)
				airline = (AirlineCompany,)
				if airline not in p:
					return render_template('Booking_Agent_Purchase_Tickets.html', error = True)
			except:
				return render_template('Booking_Agent_Purchase_Tickets.html', error = True)
			# stores the results in a variable
			if seats_total <= purchased:
				conn.commit()
				cursor.close()
				return render_template('Booking_Agent_Purchase_Tickets.html',error = True)
			else:
				try:
					query_insert_ticket = "INSERT INTO ticket (ticket_id, airline_name, flight_num) VALUES (%s, %s, %s)"
					query_insert_purchase = "INSERT INTO purchase (ticket_id, customer_email, booking_agent_email, purchase_date) VALUES (%s, %s, %s, %s)"
					t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
					t = t[:10]
					print(ticket_id, AirlineCompany, FlightNumber,customer_email,t)
					cursor.execute(query_insert_ticket, (ticket_id, AirlineCompany, FlightNumber))
					cursor.execute(query_insert_purchase, (ticket_id,customer_email,email,t))
					conn.commit()
					cursor.close()
					return render_template('Booking_Agent_Purchase_Tickets.html',message = True)
				except:
					return render_template('Booking_Agent_Purchase_Tickets.html', error = True)
		else:
			return render_template('Booking_Agent_Purchase_Tickets.html')
	else:
		return redirect('/login')


@app.route('/BookingAgentViewMyCommission', methods=['GET', 'POST'])
def BookingAgentViewMyCommission():
	if session.get('username2'):
		username = session['username2']
		if request.method == 'GET':
			cursor = conn.cursor()
			DateAfter = str(date.today()- relativedelta(months = 6))
			DateBefore = str(date.today())
			query = "select sum(price * 0.1), avg(price * 0.1), count(*)\
				from flight, ticket, purchase, booking_agent\
				where booking_agent.email = purchase.booking_agent_email AND purchase.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num \
				AND booking_agent.email = %s AND purchase_date >= %s and purchase_date <= %s"
			cursor.execute(query, (username, DateAfter, DateBefore))
			rows = cursor.fetchall()
			cursor.close()
			return render_template('Booking_Agent_View_My_Commission.html', rows=rows)
		elif request.method == 'POST':
			DateAfter = request.form['DateAfter']
			DateBefore = request.form['DateBefore']
			cursor = conn.cursor()
			query = "select sum(price * 0.1), avg(price * 0.1), count(*)\
				from flight, ticket, purchase, booking_agent\
				where booking_agent.email = purchase.booking_agent_email AND purchase.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num \
				AND booking_agent.email = %s AND purchase_date >= %s and purchase_date <= %s"
			cursor.execute(query, (username, DateAfter, DateBefore))
			rows = cursor.fetchall()
			cursor.close()
			return render_template('Booking_Agent_View_My_Commission.html', rows = rows)
	else:
		return redirect('/login')


@app.route('/BookingAgentViewTopCustomers', methods = ["GET", "POST"])
def BookingAgentViewTopCustomers():
	if session.get('username2'):
		username = session['username2']
		cursor = conn.cursor()
		query_1 = "select customer_email, count(ticket_id) as count\
			from purchase, booking_agent where purchase_date >= date_sub(now(),INTERVAL 6 MONTH) and booking_agent.email = purchase.booking_agent_email and booking_agent.email = %s \
			group by customer_email \
			ORDER BY count DESC\
			limit 5;"
		cursor.execute(query_1, (username))
		rows1 = cursor.fetchall()
		query_2 = "select customer_email, sum(price*0.1) as sum\
					from purchase, ticket, flight, booking_agent\
					where purchase_date >= date_sub(now(),INTERVAL 12 MONTH) and purchase.ticket_id = ticket.ticket_id and ticket.airline_name=flight.airline_name and ticket.flight_num = flight.flight_num\
					and booking_agent.email = purchase.booking_agent_email and booking_agent.email = %s\
					group by customer_email\
					ORDER BY sum DESC\
					limit 5;"
		cursor.execute(query_2, (username))
		rows2 = cursor.fetchall()
		cursor.close()

		# BEGIN
		my_array1 = "["
		for email, y in rows1:
			my_array1 += "{name: \"%s\", y: %s}," % (email, y)
		my_array1.rstrip(",")
		my_array1 += "]"

		my_array2 = "["
		for email, y in rows2:
			my_array2 += "{name: \"%s\", y: %s}," % (email, y)
		my_array2.rstrip(",")
		my_array2 += "]"
		# END
		return render_template("Booking_Agent_View_Top_Customers.html",my_array1 = my_array1, my_array2 = my_array2)
	else:
		return redirect('/login')

# -----------------------------------------------------Airline Staff Function-------------------------------------
@app.route('/StaffViewMyFlights', methods=['GET', 'POST'])
def StaffViewMyFlights():
	if session.get('username3'):
		if request.method == "GET":
			airline = session['username3'][1]
			status = "upcoming"
			cursor = conn.cursor()
			query = "select *\
					from flight\
					where airline_name = %s  and status = %s and departure_date <=  date_add(now(),INTERVAL 30 DAY)"
			cursor.execute(query, (airline, status))

			rows1 = cursor.fetchall()
			cursor.close()

			return render_template('Staff_View_My_Flights.html', rows1 = rows1)
	else:
		return redirect('/login')

@app.route('/StaffViewMyFlights_search', methods = ['GET', 'POST'])
def StaffViewMyFlights_search():
	airline = session['username3'][1]
	cursor = conn.cursor()
	departure = request.form['departure']
	destination = request.form['destination']
	DepartureDate = request.form['DepartureDate']
	ArrivalDate = request.form['ArrivalDate']
	para_dept = [airline]
	para_arr = [airline]
	query_dept = "select flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_date, flight.departure_time, flight.arrival_airport, flight.arrival_date, flight.arrival_time, flight.price, flight.status, flight.airplane_id\
			from flight, airport\
			where flight.airline_name = %s AND flight.departure_airport = airport.name "
	query_arr = "AND (flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id) IN\
			(select flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id\
			from flight, airport\
			where flight.airline_name = %s AND flight.arrival_airport = airport.name "
	if departure != "":
		query_dept += " AND (flight.departure_airport = %s OR airport.city = %s)"
		para_dept.append(pymysql.converters.escape_string(departure))
		para_dept.append(pymysql.converters.escape_string(departure))
	if destination != "":
		query_arr += " AND (flight.arrival_airport = %s OR airport.city = %s)"
		para_arr.append(pymysql.converters.escape_string(destination))
		para_arr.append(pymysql.converters.escape_string(destination))
	if DepartureDate != "":
		query_dept += " AND flight.departure_date >= %s"
		query_arr += " AND flight.departure_date >= %s"
		para_arr.append(DepartureDate)
		para_dept.append(DepartureDate)
	if ArrivalDate != "":
		query_dept += " AND flight.arrival_date <= %s"
		query_arr += " AND flight.arrival_date <= %s"
		para_arr.append(ArrivalDate)
		para_dept.append(ArrivalDate)
	query = query_dept +query_arr + ")"
	para = para_dept + para_arr
	cursor.execute(query, para)
	rows1 = cursor.fetchall()
	cursor.close()
	return render_template('Staff_View_My_Flights.html', rows1 = rows1)

@app.route('/StaffViewMyFlights_flightNumber', methods =['GET', 'POST'])
def StaffViewMyFlights_flightNumber():
	airline = session['username3'][1]
	cursor = conn.cursor()
	status = "upcoming"
	query_1 = "select *\
			from flight\
			where airline_name = %s  and status = %s and departure_time <=  date_add(now(),INTERVAL 30 DAY)"
	cursor.execute(query_1, (airline, status))
	rows1 = cursor.fetchall()
	flight_num = request.form['flight_number']
	query = "select purchase.customer_email, customer.name, customer.phone_number\
			from flight, ticket, purchase, customer\
			where flight.flight_num = ticket.flight_num and flight.airline_name = %s and flight.airline_name = ticket.airline_name \
			and purchase.ticket_id = ticket.ticket_id and flight.flight_num = %s and customer.email = purchase.customer_email;"
	cursor.execute(query, (airline, flight_num))
	rows2 = cursor.fetchall()
	cursor.close()
	return render_template("Staff_View_My_Flights.html", rows1 = rows1, rows2 = rows2)

@app.route('/StaffCreateNewFlights', methods=['GET', 'POST'])
def StaffCreateNewFlights():
	if session['username3'][-1] == 'Normal' or session['username3'][-1] == 'Operator':
		return redirect('/StaffViewMyFlights')
	if session.get('username3'):
		airline = session['username3'][1]
		cursor = conn.cursor()
		query = "select * from flight where airline_name = %s"
		cursor.execute(query, (airline))
		rows = cursor.fetchall()
		cursor.close()
		if request.method == "GET":
			airline = session['username3'][1]
			cursor = conn.cursor()
			query = "select * from flight where airline_name = %s"
			cursor.execute(query, (airline))
			rows = cursor.fetchall()
			cursor.close()
			return render_template('Staff_Create_New_Flights.html',rows = rows)
		else:
			try:
				airline = session['username3'][1]
				cursor = conn.cursor()
				flight_num = request.form['flight_num']
				DepartureAirport = request.form['DepartureAirport']
				DepartureDate = request.form['DepartureDate']
				DepartureTime = request.form['DepartureTime']
				ArrivalAirport = request.form['ArrivalAirport']
				ArrivalDate = request.form['ArrivalDate']
				ArrivalTime = request.form['ArrivalTime']
				TicketPrice = request.form['TicketPrice']
				FlightStatus = request.form['FlightStatus']
				airplane_id = request.form['airplane_id']
				query = "insert into flight values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
				cursor.execute(query,(airline, flight_num, pymysql.converters.escape_string(DepartureAirport),DepartureDate, DepartureTime, pymysql.converters.escape_string(ArrivalAirport), ArrivalDate, ArrivalTime, TicketPrice, FlightStatus, airplane_id))
				conn.commit()
				cursor.close()
				return render_template("Staff_Create_New_Flights.html", rows=rows, message=True) 
			except Exception as e:
				print(e)
				return render_template('Staff_Create_New_Flights.html', rows = rows, error = True)


	else:
		return redirect('/login')

@app.route('/StaffChangePermissionOfStaff', methods=['GET', 'POST'])
def StaffChangePermissionOfStaff():
	if session['username3'][-1] == 'Normal' or session['username3'][-1] == 'Operator':
		return redirect('/StaffViewMyFlights')
	if session.get('username3'):
		if request.method == "GET":
			return render_template('Staff_Change_Permission_Of_Staff.html')
		if request.method == "POST":
			
			cursor = conn.cursor()
			username = request.form['username']
			permission = request.form['permission']
			query = "update airline_staff\
					set permission = %s\
					where username = %s"
			try:
				cursor.execute(query, (permission, username))
				conn.commit()
				cursor.close()
				return render_template("Staff_Change_Permission_Of_Staff.html",message = True)
			except:
				return render_template("Staff_Change_Permission_Of_Staff.html",error = True)
	else:
		return redirect('/login')

@app.route('/StaffChangeStatusofFlights', methods=['GET', 'POST'])
def StaffChangeStatusofFlights():
	if session['username3'][-1] == 'Normal' or session['username3'][-1] == 'Admin':
		return redirect('/StaffViewMyFlights')
	if session.get('username3'):
		if request.method == "GET":
			return render_template('Staff_Change_Status_of_Flights.html')
		if request.method == "POST":
			airline = session['username3'][1]
			cursor = conn.cursor()
			flight_num = request.form['flight_num']
			status = request.form['status']
			query = "update flight\
					set status = %s\
					where flight_num = %s and airline_name = %s"
			try:
				cursor.execute(query, (status, flight_num, airline))
				conn.commit()
				cursor.close()
				return render_template("Staff_Change_Status_of_Flights.html",message = True)
			except:
				return render_template("Staff_Change_Status_of_Flights.html",error = True)
	else:
		return redirect('/login')

@app.route('/StaffAddAirplane', methods = ['GET','POST'])
def StaffAddAirplane():
	if session['username3'][-1] == 'Normal' or session['username3'][-1] == 'Operator':
		return redirect('/StaffViewMyFlights')
	if session.get('username3'):
		airline = session['username3'][1]
		cursor = conn.cursor()
		query = "select * from airplane where airline_name = %s"
		cursor.execute(query, (airline))
		rows1 = cursor.fetchall()
		cursor.close()
		if request.method == "GET":
			return render_template('Staff_Add_Airplane.html',rows1 = rows1)
		else:
			airline = session['username3'][1]
			cursor = conn.cursor()
			airplane_id = request.form['airplane_id']
			seats = request.form['seats']
			query = "insert into airplane values (%s, %s, %s); "
			try:
				cursor.execute(query,(airplane_id, airline, seats))
				conn.commit()
				cursor.close()
				return render_template("Staff_Add_Airplane.html",rows1 = rows1,message = True)
			except:
				return render_template("Staff_Add_Airplane.html",rows1 = rows1,error = True)
	else:
		return redirect('/login')

@app.route('/StaffAddNewAirport', methods=['GET', 'POST'])
def StaffAddNewAirport():
	if session['username3'][-1] == 'Normal' or session['username3'][-1] == 'Operator':
		return redirect('/StaffViewMyFlights')
	if request.method == 'POST':
		try:
			cursor = conn.cursor()
			airport_city = request.form['airport_city']
			airport_name = request.form['airport_name']
			query = "insert into airport values (%s, %s)"
			cursor.execute(query, (pymysql.converters.escape_string(airport_name),pymysql.converters.escape_string(airport_city)))
			conn.commit()
			cursor.close()
			return render_template("Staff_Add_New_Airport.html",message = True)
		except:
			return render_template("Staff_Add_New_Airport.html",error = True)
	elif request.method == 'GET':
		return render_template("Staff_Add_New_Airport.html")

@app.route('/StaffAddAgent', methods=['GET', 'POST'])
def StaffAddAgent():
	if session['username3'][-1] == 'Normal' or session['username3'][-1] == 'Operator':
		return redirect('/StaffViewMyFlights')
	if request.method == 'POST':
		try:
			cursor = conn.cursor()
			agent_email = request.form['agent_email']
			airline = session['username3'][1]
			query = "insert into work_for values (%s, %s)"
			print(query,  (agent_email,airline))
			cursor.execute(query, (agent_email,airline))
			conn.commit()
			cursor.close()
			return render_template("Staff_Add_Agent.html",message = True)
		except:
			return render_template("Staff_Add_Agent.html",error = True)
	elif request.method == 'GET':
		return render_template("Staff_Add_Agent.html")

@app.route('/StaffViewFrequentCustomers', methods = ['GET','POST'])
def StaffViewFrequentCustomers():
	if session.get("username3"):
		if request.method == "POST":
			airline = session['username3'][1]
			cursor = conn.cursor()
			query = "select customer.email, customer.name, count(purchase.ticket_id) as count\
					from purchase,ticket, customer\
					where ticket.airline_name = %s AND purchase.ticket_id = ticket.ticket_id and customer.email = purchase.customer_email and purchase.purchase_date >= date_sub(now(),INTERVAL 12 MONTH)\
					group by customer.email\
					ORDER BY count DESC\
					limit 1;"
			cursor.execute(query, (airline))
			rows1 = cursor.fetchall()
			email = request.form['email']
			query_2 = "select flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id\
						from purchase, ticket, flight\
						where purchase.ticket_id = ticket.ticket_id AND flight.flight_num = ticket.flight_num AND flight.airline_name = ticket.airline_name AND flight.airline_name = %s AND purchase.customer_email = %s"
			cursor.execute(query_2,(airline, email))
			rows2 = cursor.fetchall()
			cursor.close()
			return render_template("Staff_View_Frequent_Customers.html", rows1= rows1, rows2=rows2)
		else:
			airline = session['username3'][1]
			cursor = conn.cursor()
			query = "select customer.email, customer.name, count(purchase.ticket_id) as count\
					from purchase,ticket, customer\
					where ticket.airline_name = %s AND purchase.ticket_id = ticket.ticket_id and customer.email = purchase.customer_email and purchase.purchase_date >= date_sub(now(),INTERVAL 12 MONTH)\
					group by customer.email\
					ORDER BY count DESC\
					limit 1;"
			cursor.execute(query, (airline))
			rows1 = cursor.fetchall()
			cursor.close()
			return render_template("Staff_View_Frequent_Customers.html", rows1 = rows1)
	else:
		return redirect('/login')

@app.route('/StaffViewBookingAgent', methods = ['GET','POST'])
def StaffViewBookingAgent():
	if session.get("username3"):
		airline = session['username3'][1]
		cursor = conn.cursor()
		query_1 = "select booking_agent.email, purchase.booking_agent_email, count(purchase.ticket_id) AS count\
					from purchase,ticket, booking_agent\
					where ticket.airline_name  = %s AND booking_agent.email = purchase.booking_agent_email AND purchase.ticket_id = ticket.ticket_id and purchase.purchase_date >= date_sub(now(),INTERVAL 1 MONTH) and purchase.booking_agent_email is not null\
					group by booking_agent.email\
					ORDER BY count DESC\
					limit 5;"
		cursor.execute(query_1, (airline))
		rows1 = cursor.fetchall()
		query_2 = "select booking_agent.email, purchase.booking_agent_email, count(purchase.ticket_id) AS count\
					from purchase,ticket, booking_agent\
					where  ticket.airline_name  = %s AND booking_agent.email = purchase.booking_agent_email AND purchase.ticket_id = ticket.ticket_id and purchase.purchase_date >= date_sub(now(),INTERVAL 12 MONTH) and purchase.booking_agent_email is not null\
					group by booking_agent.email\
					ORDER BY count DESC\
					limit 5;"
		cursor.execute(query_2, (airline))
		rows2 = cursor.fetchall()
		query_3 = "select booking_agent.email, purchase.booking_agent_email, sum(flight.price * 0.1) as commission\
				from purchase,ticket, flight, booking_agent\
				where booking_agent.email = purchase.booking_agent_email AND flight.airline_name  = %s AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num  AND \
				purchase.ticket_id = ticket.ticket_id and purchase.purchase_date >= date_sub(now(),INTERVAL 12 MONTH) and purchase.booking_agent_email is not null \
				group by booking_agent.email\
				ORDER BY commission DESC\
				limit 5"
		cursor.execute(query_3, (airline))
		rows3 = cursor.fetchall()
		cursor.close()
		return render_template("Staff_View_Booking_Agent.html", rows1 = rows1, rows2 = rows2, rows3 = rows3)
	else:
		return redirect('/login')

@app.route('/StaffReports', methods = ['GET','POST'])
def StaffReports():
	if session.get('username3'):
		if request.method == 'GET':
			return render_template('Staff_Reports.html')
		airline = session['username3'][1]
		cursor = conn.cursor()	
		StartTime = request.form['StartTime']
		EndTime = request.form['EndTime']
		query = "select count(purchase.ticket_id),YEAR(purchase_date),MONTH(purchase_date)\
				from purchase, flight, ticket\
				where purchase.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name and ticket.flight_num = flight.flight_num and flight.airline_name = %s and purchase_date >= %s and purchase_date <= %s\
				group by YEAR(purchase_date),MONTH(purchase_date);"
		cursor.execute(query,(airline, StartTime, EndTime))
		result = cursor.fetchall()
		rows = {}
		startDate = datetime.strptime(StartTime,'%Y-%m-%d')
		endDate = datetime.strptime(EndTime, '%Y-%m-%d')
		year = startDate.year
		month = startDate.month
		while year <= endDate.year:
			if year == endDate.year and month == endDate.month+1:
				break
			if month <= 12:
				temp = str(year)+"-"+str(month)
				rows[temp] = 0
				month += 1
			else:
				year += 1
				month = 1
		for i in result:
			rows[str(i[1])+"-"+str(i[2])] = i[0]
		array_1 = []
		for (key,value) in rows.items():
			array_1.append([key, value])
		cursor.close()
		return jsonify(array_1)
	else:
		return redirect('/login')

@app.route('/StaffComparisonOfRevenueEarned', methods = ['GET','POST'])
def StaffComparisonOfRevenueEarned():
	# in the last month
	if session.get('username3'):
		airline = session['username3'][1]
		cursor = conn.cursor()
		query_indirect_1 = "select sum(flight.price)\
					from purchase,ticket, flight\
					where flight.airline_name  = %s AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num  AND \
					purchase.ticket_id = ticket.ticket_id and purchase.purchase_date >= date_sub(now(),INTERVAL 1 MONTH) AND purchase.booking_agent_email is not null"
		cursor.execute(query_indirect_1, (airline))
		rows3 = cursor.fetchall()
		query_direct_1 = "select sum(flight.price)\
					from purchase,ticket, flight\
					where flight.airline_name  = %s AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num  AND \
					purchase.ticket_id = ticket.ticket_id and purchase.purchase_date >= date_sub(now(),INTERVAL 1 MONTH) AND purchase.booking_agent_email is null"
		cursor.execute(query_direct_1, (airline))
		rows4 = cursor.fetchall() 
		rows3_dic = {}
		rows4_dic = {}
		rows3_dic["name"] = "Indirect sale"
		rows3_dic["y"] = rows3[0][0]
		rows4_dic["name"] = "Direct sale"
		rows4_dic["y"] = rows4[0][0]
		cursor.close()
		# in the last year
		cursor = conn.cursor()
		query_indirect = "select sum(flight.price)\
					from purchase,ticket, flight\
					where flight.airline_name  = %s AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num  AND \
					purchase.ticket_id = ticket.ticket_id and purchase.purchase_date >= date_sub(now(),INTERVAL 12 MONTH) AND purchase.booking_agent_email is not null"
		cursor.execute(query_indirect, (airline))
		rows1 = cursor.fetchall()
		query_direct = "select sum(flight.price)\
					from purchase,ticket, flight\
					where flight.airline_name  = %s AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num  AND \
					purchase.ticket_id = ticket.ticket_id and purchase.purchase_date >= date_sub(now(),INTERVAL 12 MONTH) AND purchase.booking_agent_email is null"
		cursor.execute(query_direct,(airline))
		rows2 = cursor.fetchall() 
		rows1_dic = {}
		rows2_dic = {}
		rows1_dic["name"] = "Indirect sale"
		rows1_dic["y"] = rows1[0][0]
		rows2_dic["name"] = "Direct sale"
		rows2_dic["y"] = rows2[0][0]
		cursor.close()
		print(rows1,rows2,rows3,rows4)
		if rows1[0][0] is not None and rows2[0][0] is not None and rows3[0][0] is not None and rows4[0][0] is not None:
			return render_template("staff_Comparison_Of_Revenue_Earned.html", my_array=r'[{"name":"Indirect sale", "y":%f}, {"name":"Direct sale", "y": %f}]' % (rows3[0][0], rows4[0][0]), my_array2=r'[{"name":"Indirect sale", "y":%f}, {"name":"Direct sale", "y": %f}]' % (rows1[0][0], rows2[0][0]))
		else:
			return render_template("staff_Comparison_Of_Revenue_Earned.html", my_array=r'[{"name":"Indirect sale", "y":%f}, {"name":"Direct sale", "y": %f}]' % (0, 0), my_array2=r'[{"name":"Indirect sale", "y":%f}, {"name":"Direct sale", "y": %f}]' % (0, 0))

	else:
		return redirect('/login')

@app.route('/StaffViewTopDestinations', methods = ['GET','POST'])
def StaffViewTopDestinations():
	if session.get('username3'):
		airline = session['username3'][1]
		cursor = conn.cursor()
		query_1 = "select airport.city, count(ticket.ticket_id) as count from purchase,ticket, flight, airport\
				where flight.airline_name  = %s AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND flight.arrival_airport = airport.name AND \
				purchase.ticket_id = ticket.ticket_id AND purchase_date >= date_sub(now(),INTERVAL 3 MONTH)\
				group by airport.city\
				ORDER BY count DESC\
				limit 5;"
		cursor.execute(query_1,(airline))
		rows1 = cursor.fetchall()

		query_2 = "select airport.city, count(ticket.ticket_id) as count from purchase,ticket, flight, airport\
				where flight.airline_name  = %s AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND flight.arrival_airport = airport.name AND \
				purchase.ticket_id = ticket.ticket_id AND purchase_date >= date_sub(now(),INTERVAL 12 MONTH)\
				group by airport.city\
				ORDER BY count DESC\
				limit 5;"
		cursor.execute(query_2,(airline))
		rows2 = cursor.fetchall()
		cursor.close()
		return render_template("Staff_View_Top_Destinations.html", rows1 = rows1, rows2 = rows2)
	else:
		return redirect('/login')
	
app.secret_key = 'some key that you will never guess'
if __name__ == "__main__":
	app.run('127.0.0.1', 9000, debug = True)
