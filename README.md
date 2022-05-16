# Cs50 clinic management system

#### Video Demo: <URL https://youtu.be/XNyGb9QmXGY>

#### Description:

my project is a web app using flask, sql and bootstrap

##### 1.app.py:

1.  login route
2.  log out route
3.  sign-up route
4.  the index route which is the main page after logging in to show today's appointments
5.  finance routes
6.  pass route to change the password
7.  search route to search patients
8.  staff route to show and add staff
9.  add_new route to add new appointments
10. date route to show certain dates' appointments
11. pro route to show procedures
12. delete route to delete certain appointments
13. contact route shows contact info

##### templates: all using bootstrap and extending layout.html
1. layout.html:  i created a nav-bar which is collapsible. in the login page it shows only contact us link. after u log in it shows all the possible routs. 

2. login.html: it extends layout.html plus a login box with options to login or sign-up.

3. register.html: after clicking sign-up it goes to a page with a form for registration with all fields required.

4. appointments.html: after logging in the first page shows appoimtments on current date and u can also select a certain date

6. certainDate.html: after selecting a certain date in the appoimtments page it quiries the database for the date and shows appointments on that date 

7. new.html: when u click on add new appointment from the nav-bar it shows a form to add a new appointment and register it in the database.

8. contact.html: it only shows the email of the developer for contact.

9. finance.html: this page utilizes multiple routes to perform all its functions to show procedures and income on certain dates.

10. apology.html: it gives erroe messages when input is invalis or incorrect using the error function in help.py.

11. staff.html: it shows the staff registered to a certain clinic utilizing the username in the sign up form as a unique input.

12. search.html: it shows the patients searched with all procedures performed on the patient.

13. procedure.html: it shows all procedures in the database related to the current clinic logged in.

##### database:
clinic.db: this file contains:
1. appointments table: showing name, day, hour, procedure, user(to defferentiate different clinics) and id 

2. procedures table: showing patient's name, doctor, procedure, comments, price, user(to defferentiate different clinics), and date

3. staff table: showing name, Role, age, salary, user(to defferentiate different clinics) and id 

4. users table: showing username(unique), password(hashed), clinic name and owner
