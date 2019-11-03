import sqlite3
import getpass
import re
import datetime
import random

def main():
    global conn, c 
    # path = sysargv[1] 
    # conn = sqlite3.connect(path)
    conn = sqlite3.connect('./database_test.db')
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON; ')
    conn.commit()
    login_screen = False
    
   
    # LOGIN SCREEN
    """
    while login_screen == False:
        login_screen, username = login()
    """
    
    #USER MENU
    print("To register a birth, type in 1")
    print("To register a marriage, type in 2")
    print("To renew a vehicle registration, type in 3")
    print("To process a bill of sale, type in 4")
    print("To process a payment, type in 5")
    print("To get a driver abstract,type in 6")
    print("To issue a ticket, type in 7")
    print("To find a car owner, type in 8")
    action = input("Choose a task: ")
    
    if int(action) == 1: one('amanda6')
    elif int(action) == 2: two('amanda6')
    elif int(action) == 3: three()
    elif int(action) == 4: four()
    elif int(action) == 5: five()
    elif int(action) == 6: six()
    elif int(action) == 7: seven()
    elif int(action) == 8: eight()
    


def login():
    print("Login Here!")
    username = input("Enter username: ")
    password = getpass.getpass("Enter Password: ")
    
    # re.match is checking if our username and password contains alphabet, numbers and underscores ONLY
    if re.match("^[A-Za-z0-9_]*$", username) and re.match("^[A-Za-z0-9_]*$", password):
        c.execute('SELECT uid FROM users WHERE uid=? and pwd=?;', (username, password))
        if c.fetchone() != None:
            print("Login Success.")
            return True, username
        else:
            print("Login failed. Try again")
            return False, username
    else:
        print("Login failed. Try again")
        return False, username
    
# YOU NEED TO CHECK IF THE PERSON ALREADY IS IN THE BIRTH TABLE    
def one(user):
    print("You have chosen to register a birth")
    print('Note that first and last names are a maximum of 12 characters')
    
    # Receive information about birth information
    # Most of the validation is checking the length restricted to whatever it is in the database
    # or checking that a name only consists of letters and is not empty
    while True:
        fname = input("Please provide a first name: ")
        if fname != '' and len (fname) <= 12 and re.match("^[A-Za-z0-9-]*$", fname):
            break
        else:
            print("Incorrect format")
    
    while True:
        lname = input("Please provide a last name: ")
        if lname != '' and re.match("^[A-Za-z0-9-]*$", lname) and len(lname) <= 12 :
            break 
        else:
            print("Incorrect format")
    
    # check to see if this name already exists in the database
    # if they exist, deny the birth registration
    if find_person(fname, lname) != None:
        print('There is already a {} {} that exists in the database'.format(fname,lname))
        print('Birth registration rejected')
        return;
    
    while True:
        gender = input("Please provide the gender (M/F): ")
        if gender.upper() == 'F' or gender.upper() == 'M':
            break
        else:
            print('Incorrect format')
    
    # Using datetime module to validate date
    # datetime does not account for months (1-9) having a 0 at the front ex. 01 - January
    # if our input passes the datetime function and the length is one, then concatenate a 0 at the front
    while True:
        bdate = input("Please provide a birth date (YYYY-MM-DD): ")
        try:
            year, month, day = bdate.split('-')
            datetime.datetime(int(year),int(month),int(day))
            if len(month) == 1:
                month = "0" + month
            bdate = year +'-' + month +'-'+ day
            break
        except ValueError:
            print("Invalid Date")
    
    while True:
        bplace = input("Please provide a birth place (max character length is 20): ")
        if bplace != '' and bplace.isalpha() and len(bplace) <= 20:
            break    
        else:
            print('Incorrect format')
            
       
    while True:
        mot_fname = input("Please provide mother's first name: ")
        if mot_fname != '' and re.match("^[A-Za-z0-9-]*$", mot_fname) and len(mot_fname) <= 12:
            break
        else:
            print("Incorrect format")
        
    while True:
        mot_lname = input("Please provide mother's last name: ")
        if mot_lname != '' and re.match("^[A-Za-z0-9-]*$", mot_lname) and len(mot_lname) <= 12:
            break
        else:
            print("Incorrect format")
    
    # checking to see if mom already exists in the database
    mom_name = find_person(mot_fname, mot_lname)       
    if mom_name == None:
        mom_name = missing_person_info(mot_fname, mot_lname)    
    
    while True:
        fat_fname = input("Please provide father's first name: ")
        if fat_fname != '' and re.match("^[A-Za-z0-9-]*$", fat_fname) and len(fat_fname) <= 12:
            break 
        else:
            print("Incorrect format")
        
    while True:
        fat_lname = input("Please provide father's last name: ")
        if fat_lname != '' and re.match("^[A-Za-z0-9-]*$", fat_lname) and len(fat_lname) <= 12:
            break
        else:
            print("Incorrect format")
    
    # this is checking if the dad is in the database
    dad_name = find_person(fat_fname, fat_lname)
    if dad_name == None:
        dad_name = missing_person_info(fat_fname, fat_lname)
     
     
    
    # REGISTERING FOR BIRTH
    # use datetime function for registration date and use a query to find the regplace
    regdate = datetime.date.today()
    c.execute('SELECT city FROM users where uid = ?;', (user,))
    regplace = c.fetchone()[0]
    
    # creating unique registration number
    # we find the current highest registration number and add 1 
    c.execute('SELECT regno FROM births ORDER BY regno DESC')
    reg_num = c.fetchone()
    if reg_num == None:
        reg_num = 1
    else:
        reg_num = reg_num[0] + 1
    
    # REGISTER A PERSON FIRST
    # We need to grab address and phone number from mom
    # note that address and phone number is in an indexed list called result
    c.execute('SELECT address, phone FROM persons where fname LIKE ? and lname LIKE ?;', (mom_name[0], mom_name[1]))
    result = c.fetchone()
    c.execute(''' INSERT INTO persons(fname, lname, bdate, bplace, address, phone)
                  VALUES
                  (?,?,?,?,?,?)''', (fname, lname, bdate, bplace, result[0], result[1]))
    conn.commit()
    
    # THIS IS REGISTERING A BIRTH
    
    c.execute(''' INSERT INTO births(regno, fname, lname, regdate, regplace, gender, f_fname, f_lname, m_fname, m_lname)
                  VALUES (?,?,?,?,?,?,?,?,?,?)''', 
                (reg_num, fname, lname, regdate, regplace, gender, dad_name[0], dad_name[1], mom_name[0], mom_name[1]))
    conn.commit()
    
# this function checks if this person exists in the database already
def find_person(fname, lname):
    c.execute('SELECT fname, lname FROM persons WHERE fname LIKE ? and lname LIKE ?;', (fname, lname))
    return c.fetchone()

# we need first name, last name, birth date, birth place, address and phone. for each parent any column other than first and last can be null
# we know the user has hit enter if our input is an empty string, if it is set the variable to NULL
def missing_person_info(fname, lname):
    print('\n')
    print("There seems to be no record of {} {} in our database".format(fname,lname))
    print("Please fill out the information down below. \nHit enter if you do not want to fill this out.\n")  
    while True:
        bdate = input("Please provide a birth date (YYYY-MM-DD): ")
        if bdate == '':
            bdate =  'NULL'
            break
        else:
            try:
                year, month, day = bdate.split('-')
                datetime.datetime(int(year),int(month),int(day))
                if len(month) == 1:
                    month = "0" + month   
                bdate = year +'-' + month +'-'+ day                    
                break
            except ValueError:
                print("Invalid Date")
    
    while True:
        bplace = input("Please provide a birth place: ")
        if bplace == '':
            bplace = 'NULL'
            break
        else:
            if bplace.isalpha() and len(bplace) <= 20:
                break      
            else:
                print("Invalid input")
                
    while True:
        address = input("Please provide an address: ")
        if address == '':
            address = 'NULL'
            break
        else:
            if address.isalpha() and len(address) <= 30:
                break      
            else:
                print("Invalid input")        
    
    while True:
        phone_number = input("Please provide a phone number (123-456-7890): ")
        if phone_number == '':
            phone_number = 'NULL'
            break
        else:
            #if validNumber(phone_number) == True:
            if len(phone_number) <= 12 and re.match("^[0-9]{3}-[0-9]{3}-[0-9]{4}$", phone_number):
                break      
            else:
                print("Invalid input")
                      
                
    # at the very end we want to insert this into our database
    c.execute(''' INSERT INTO persons(fname, lname, bdate, bplace, address, phone)
                  VALUES
                  (?,?,?,?,?,?)''', (fname, lname, bdate, bplace, address, phone_number))
    conn.commit()
    
    return fname, lname

    
    
def two(username):
    print("You have chosen to register a marriage")
    
    # Receiving information about partner 1
    while True:
        prt1_fname = input("Please provide Partner 1's first name: ")
        if prt1_fname != '' and len(prt1_fname) <= 12 and re.match("^[A-Za-z0-9-]*$", prt1_fname):
            break
        else:
            print("Incorrect format")
    
    while True:
        prt1_lname = input("Please provide Partner 1's last name: ")
        if prt1_lname != '' and len(prt1_lname) <= 12 and re.match("^[A-Za-z0-9-]*$", prt1_lname):
            break 
        else:
            print("Incorrect format")
            
    # check to see if partner_one exists in the database        
    partner_one = find_person(prt1_fname, prt1_lname)
    if partner_one == None:
        partner_one = missing_person_info(prt1_fname, prt1_lname)
    
    # grabbing information about partner 2         
    while True:
        prt2_fname = input("Please provide Partner 2's first name: ")
        if prt2_fname != '' and len(prt2_fname) <= 12 and re.match("^[A-Za-z0-9-]*$", prt2_fname):
            break
        else:
            print("Incorrect format")
    
    while True:
        prt2_lname = input("Please provide Partner 2's last name: ")
        if prt2_lname != '' and len(prt2_lname) <= 12 and re.match("^[A-Za-z0-9-]*$", prt2_lname):
            break 
        else:
            print("Incorrect format")
            
    # check to see if partner two exists in the database
    partner_two = find_person(prt2_fname, prt2_lname)    
    if partner_two == None:
        partner_two = missing_person_info(prt2_fname, prt2_lname)
        
    # REGISTERING FOR MARRIAGE
    # use datetime function for registration date and use a query to find the registration place
    registdate = datetime.date.today()
    c.execute('SELECT city FROM users where uid = ?;', (username,))
    registplace = c.fetchone()[0]
    
    # grabbing a random and unique registration
    c.execute('SELECT regno FROM marriages ORDER BY regno DESC')
    regno = c.fetchone()
    if regno == None:
        regno = 1
    else:
        regno = regno[0] + 1
    
    c.execute(''' INSERT INTO marriages(regno, regdate, regplace, p1_fname, p1_lname, p2_fname, p2_lname)
                  VALUES (?,?,?,?,?,?,?)''', 
                (regno, registdate, registplace, partner_one[0], partner_one[1], partner_two[0], partner_two[1]))
    conn.commit()

    c.execute('SELECT * FROM marriages')
    print(c.fetchall())

def three():
 # Provide existing registration number, and renew the registration.
    # If the current registration has expired or expires today set the new expiry date to one year from today's date
    # Otherwise, set the new expiry to one year after the current expiry date.

    entry_exists = False
    while not entry_exists:
        current_regno = input('Enter an existing registration number. To go back to menu press enter: ')
        current_regno = current_regno.strip()
        if current_regno == '':
            return
        c.execute('SELECT regdate FROM registrations WHERE regno = ?;', (current_regno,))
        db_regdate = c.fetchone()
        if db_regdate == None:
            print('This registration number is not registered in the database')
        else:
            db_regdate = db_regdate[0]
            db_regdate = datetime.datetime.strptime(db_regdate, "%Y-%m-%d")
            entry_exists = True


    if datetime.datetime.today() >= db_regdate:
        # Registration has expired or expires today, set new expiry date to one year from today
        print("Current registration has expired, system is setting new expiry date to one year from today")
        today = datetime.date.today()
        today_string = today.strftime("%Y-%m-%d")
        set_db_regyear = datetime.date.today().year + 1
        year, month, day = today_string.split('-')
        new_expiry = str(set_db_regyear) + '-' + month + '-' + day
        c.execute("UPDATE registrations SET regdate = ? WHERE regno = ?;", (new_expiry, current_regno))
        # TESTING
        # c.execute("SELECT regdate FROM registrations WHERE regno = ?;", (current_regno,))
        # print(c.fetchone()[0])
    
    else:
        print("Setting the new expiry date to a year from current expiry date")
        c.execute("SELECT expiry FROM registrations WHERE regno = ?;", (current_regno,))
        old_expiry_str = c.fetchone()[0]
        exp_year, exp_month, exp_day = old_expiry_str.split('-')
        exp_year = int(exp_year) + 1
        new_exp = str(exp_year) + '-' + exp_month + '-' + exp_day
        c.execute("UPDATE registrations SET regdate = ? WHERE regno = ?;", (new_exp, current_regno))
        #TESTING
        # c.execute("SELECT regdate FROM registrations WHERE regno = ?;", (current_regno,))
        # print(c.fetchone()[0])
        
# process a bill of sale
# need: vin of a car, name of current owner, name of new owner and plate # for new reg
# if the name of current owner does not match most recent owner of car in system REJECT TRANSACTION
# if it can be made, the expiry date of current registration is set to today's date
# a new registration: new owners name, registration date = today, expiry = a year from now, unique reg number, vin will be copied from current reg to the new on e
def four():
    print('\n')
    print('You have chosen to process a bill of sale')
    
    # grab and validate information
    # grabbing vin
    while True:
        vin = input('What is the vehicle identification number (vin)? ')
        if vin != '' and len(vin) <= 5:
            break
        else:
            print('Invalid input')
            
    # grabbing current owner
    while True:
        current_fname = input('What is the first name of the current owner? ')
        if current_fname != '' and current_fname.isalpha() and len(current_fname) <= 12:
            break
        else:
            print('Invalid input')
            
    while True:
        current_lname = input('What is the last name of the current owner? ')
        if current_lname != '' and current_lname.isalpha() and len(current_lname) <= 12:
            break
        else:
            print('Invalid input')      
            
    # getting new owner
    while True:
        new_fname = input('What is the first name of the new owner? ')
        if new_fname != '' and new_fname.isalpha() and len(new_fname) <= 12:
            break
        else:
            print('Invalid input')
            
    while True:
        new_lname = input('What is the last name of the new owner? ')
        if new_lname != '' and new_lname.isalpha() and len(new_lname) <= 12:
            break
        else:
            print('Invalid input')    
            
    while True:
        plate = input('What is the plate number? ')
        if plate != '' and len(plate) <= 7:
            break
        else:
            print('Invalid input')
            
    # check to see if there is a person that exists for both people
    if find_person(current_fname, current_lname) == None:
        print('There is no {} {} in the database'.format(current_fname, current_lname))
        print('New sale rejected.')
        return;        
    
    new_person = find_person(new_fname, new_lname)
    if new_person == None:
        print('There is no {} {} in the database'.format(current_fname, current_lname))
        print('New sale rejected.')
        return;
    
    # checking to see if there is such a registration with the vin and plate
    # if there is no registration that exists, reject the sale
    # we are also grabbing the name of the most recent registration of that vin and plate number
    c.execute('SELECT fname, lname, regno, vin FROM registrations WHERE vin LIKE ? and plate LIKE ? ORDER BY regdate DESC;', (vin, plate))
    result = c.fetchone()
    if result == None:
        print('There is no registration under that vin and plate number')
        print('New sale rejected.')
        return;
    
    vin = result[3]
    # we need to check if the recent person registered to the car matches the name given to us
    if result[0].lower() != current_fname.lower() and result[1].lower() != current_lname.lower():
        print('That is not the most recent person registered to that vehicle')
        print('New sale rejected.')
        return;
    
    # change expiry date of old owner's car to today's date
    # today is a datetime object so do you need to convert it to a string???
    regno = result[2]
    today = datetime.date.today()
    c.execute('UPDATE registrations SET expiry = ? WHERE regno = ?;', (today, regno))
    
    # a new registration: new owners name, registration date = today, expiry = a year from now, unique reg number, vin will be copied from current reg to the new on 
    today_string = today.strftime("%Y-%m-%d")
    set_db_regyear = datetime.date.today().year + 1
    year, month, day = today_string.split('-')
    new_expiry = str(set_db_regyear) + '-' + month + '-' + day    
    
    c.execute('SELECT regno FROM registrations ORDER BY regno DESC')
    regno = c.fetchone()[0] + 1
    
    c.execute('INSERT INTO registrations(regno, regdate, expiry, plate, vin, fname, lname) VALUES (?,?,?,?,?,?,?);', (regno, today, new_expiry, plate, vin, new_person[0], new_person[1]))
    
    
def five():
    print("You have chosen to process a payment")
    
    while True:
        ticket_no = input("Please provide the ticket number you'd like to make a payment to: ")
        if ticket_no != '' and ticket_no.isdigit() == True:
            break
        else:
            print("Invalid ticket number")
            
    if find_ticket(ticket_no) != None:
        find_fine(ticket_no)

def find_ticket(tno):
    c.execute('SELECT tno FROM tickets WHERE tno =?;', (tno,))
    return c.fetchone()[0]

def find_fine(tno):
    c.execute('SELECT fine FROM tickets WHERE tno =?;', (tno,))
    fine_leftover = int(c.fetchone()[0])
    print("The fine amount outstanding for this ticket number is ${}".format(fine_leftover))
    
    # # use datetime function for registration date and use a query to find the registration place
    # pay_date = datetime.date.today()
    # c.execute('SELECT pdate FROM payments WHERE tno = ?;', (tno,))
    # old_paydate = str(c.fetchone()[0])
    
    # if old_paydate == str(pay_date):
        # print("You cannot make multiple payments on ticket {} today".format(tno))
        # payment_invalid()
    
    while True:
        pay_amount = input("Please provide the amount you would like to pay: ")
        
        if pay_amount != '' and pay_amount.isdigit() == True:
            pay_amount = int(pay_amount)
            payment_balance = int(fine_leftover - pay_amount)
            if payment_balance <= 0: 
                print("Invalid amount")
            else:
                print("You are making a payment of ${} to ticket number {}".format(pay_amount, tno))
                print("Your new balance of the ticket fine is {}".format(payment_balance))
            break
        else:
            print("Invalid amount")
    
    # use datetime function for registration date and use a query to find the registration place
    pay_date = datetime.date.today()
    
    # c.execute('SELECT pdate FROM marriages WHERE tno = ?;', (tno,))
    # old_pay_date = c.fetchone[0]
    
    # if old_pay_date != pay_date:
        # update_tickets(tno, pay_date, pay_amount, payment_balance)
    # else:
        # print("You cannot make multiple payments on ticket {} today".format(tno))
    
    
    # return tno, pay_date, pay_amount, payment_balance
    # conn.commit()
    
# def update_tickets(tno, pay_date, pay_amount, payment_balance):

    payment_register = 'INSERT INTO payments(tno, pdate, amount) VALUES (?,?,?)'
    c.execute(payment_register, (tno, pay_date, pay_amount))
    conn.commit()
    
    update_tickets = 'UPDATE tickets SET fine=? WHERE tno=?;'
    c.execute(update_tickets, (payment_balance, tno))
    conn.commit()
    
    return
    conn.commit()
    
# def payment_invalid():
    # print("Please try payment on this ticket again another day")
    
    # conn.commit()
    
    
    
def six():
    # Enter a first name and a last name to get a driver abstract
    # Driver abstract contains number of tickets, number of demerit notices, total number of demerit points received both within the past 2 years and within the lifetime. 
    # Given the option to see the tickets ordered from the latest to the oldest. 
    # For each ticket, you will report the ticket number, the violation date, the violation description, the fine, the registration number and the make and model of the car for which the ticket is issued. 
    # If there are more than 5 tickets, at most 5 tickets will be shown at a time, and the user can select to see more.
    f_name = input("Enter first name: ")
    l_name = input("Enter last name: ")
    
    
# ISSUE A TICKET
# given a regnum
# print out persons fname and lname, make model year and color registered to the car
# can add a ticket (INSERT into tickets) by giving violation date, violation text and fine amount
# unique ticket number is assigned automatically and ticket should be recorded
# violation date is set to today's date if not provided
def seven():
    print("You have chosen to issue a ticket:")
    
    # receive a registration number from the officer 
    # first we check that it is not empty and that the input is all digits
    # convert our variable into an int type then check to see if there is a registration number in the database
    while True:
        regno = input("Please provide a valid registration number: ")
        if regno != '' and regno.isdigit():
            regno = int(regno)
            c.execute('SELECT regno FROM registrations WHERE regno = ?;', (regno,))
            regno = c.fetchone()
            if regno == None:
                print('That registration number does not exist in the database')
            else:
                regno = regno[0]
                break
        else:
            print("Invalid input format")
            
    c.execute('SELECT r.fname, r.lname, v.make, v.model, v.year, v.color FROM registrations r, vehicles v WHERE r.vin = v.vin')
    result = c.fetchone()
    print('Persons Name: {} {}\nMake: {}\nModel: {}\nYear: {}\nColor: {}\n'.format(result[0],result[1],result[2], result[3],result[4],result[5]))
    
    # Grabbing information for the ticket 
    print("Please fill out the following information down below.\n")
    while True:
        vdate = input("Please provide a violation date (YYYY-MM-DD). Hit enter if not applicable: ")
        if vdate == '':
            vdate =  datetime.date.today()
            break
        else:
            try:
                year, month, day = vdate.split('-')
                datetime.datetime(int(year),int(month),int(day))
                if len(month) == 1:
                    month = "0" + month   
                vdate = year +'-' + month +'-'+ day                    
                break
            except ValueError:
                print("Invalid Date")
                
    while True:
        violation = input('Please provide the violation description: ')
        if violation != '':
            break
        else:
            print('Invalid input')
    
    while True:
        fine = input('Please provide a fine amount (minimum: $1): ')
        fine = int(fine)
        if fine > 1:
            break
        else:
            print('Invalid input')
            
    # creating a tno
    # find the current highest ticket number and increase it by 1
    c.execute('SELECT tno FROM tickets ORDER BY tno DESC')
    tno = c.fetchone()[0] + 1
    
    c.execute('INSERT INTO tickets(tno,regno,fine,violation,vdate) VALUES (?, ?, ?, ?, ?)', (tno, regno, fine, violation, vdate))
    conn.commit()
    
    
          
def eight():
    pass

if __name__ == "__main__":
    main()