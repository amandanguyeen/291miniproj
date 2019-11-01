import sqlite3
import time

conn = None
c = None

def connect(path):
    global conn, c

    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(' PRAGMA foreign_keys=ON;')
    conn.commit()
    return


def drop_tables():
   
    c.executescript('''
        drop table if exists demeritNotices;
        drop table if exists tickets;
        drop table if exists registrations;
        drop table if exists vehicles;
        drop table if exists marriages;
        drop table if exists births;
        drop table if exists persons;
        drop table if exists payments;
        drop table if exists users;
    ''')
    conn.commit()


def define_tables():
    
    c.executescript('''
        create table persons (
          fname		char(12),
          lname		char(12),
          bdate		date,
          bplace	char(20), 
          address	char(30),
          phone		char(12),
          primary key (fname, lname)
        );
        create table births (
          regno		int,
          fname		char(12),
          lname		char(12),
          regdate	date,
          regplace	char(20),
          gender	char(1),
          f_fname	char(12),
          f_lname	char(12),
          m_fname	char(12),
          m_lname	char(12),
          primary key (regno),
          foreign key (fname,lname) references persons,
          foreign key (f_fname,f_lname) references persons,
          foreign key (m_fname,m_lname) references persons
        );
        create table marriages (
          regno		int,
          regdate	date,
          regplace	char(20),
          p1_fname	char(12),
          p1_lname	char(12),
          p2_fname	char(12),
          p2_lname	char(12),
          primary key (regno),
          foreign key (p1_fname,p1_lname) references persons,
          foreign key (p2_fname,p2_lname) references persons
        );
        create table vehicles (
          vin		char(5),
          make		char(10),
          model		char(10),
          year		int,
          color		char(10),
          primary key (vin)
        );
        create table registrations (
          regno		int,
          regdate	date,
          expiry	date,
          plate		char(7),
          vin		char(5), 
          fname		char(12),
          lname		char(12),
          primary key (regno),
          foreign key (vin) references vehicles,
          foreign key (fname,lname) references persons
        );
        create table tickets (
          tno		int,
          regno		int,
          fine		int,
          violation	text,
          vdate		date,
          primary key (tno),
          foreign key (regno) references registrations
        );
        create table demeritNotices (
          ddate		date, 
          fname		char(12), 
          lname		char(12), 
          points	int, 
          desc		text,
          primary key (ddate,fname,lname),
          foreign key (fname,lname) references persons
        );
        create table payments (
          tno		int,
          pdate		date,
          amount	int,
          primary key (tno, pdate),
          foreign key (tno) references tickets
        );
        create table users (
          uid		char(8),
          pwd		char(8),
          utype		char(1),	
          fname		char(12),
          lname		char(12), 
          city		char(15),
          primary key(uid),
          foreign key (fname,lname) references persons
        );
        ''')

    conn.commit()

    return


def insert_data():
    global conn, c
    persons_sql = "INSERT INTO persons(fname, lname, bdate, bplace, address, phone) VALUES (?,?,?,?,?,?)"
    persons_values = [('Amanda', 'Nguyen', '28-01-1999', 'Edmonton', '16115 - 140 Street', '780 902 9107')]
    users_sql = "INSERT INTO users(uid, pwd, utype, fname, lname, city) VALUES (?, ?, ?, ?, ?, ?)"
    users_values = [('amanda6', 'password', '1', 'Amanda', 'Nguyen', 'Edmonton')]

    c.executemany(persons_sql,persons_values)
    c.executemany(users_sql,users_values)
    conn.commit()
    return


def main():
    global conn, c

    path = "./database_test.db"
    connect(path)
    drop_tables()
    define_tables()
    insert_data()


    conn.commit()
    conn.close()
    return


if __name__ == "__main__":
    main()