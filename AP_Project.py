from tkinter import *
from PIL import Image, ImageTk
import mysql.connector as mysql
import tkinter.font as tkFont
import tkinter.messagebox as MB

root = Tk()
root.title('BusTicket Booking')
root.iconbitmap("bus_icon.ico")
root.withdraw()


def to_home():
    top.withdraw()
    root.deiconify()


def on_closing():
    if MB.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


def insert_db():
    if e1.get() == '' or e2.get() == '' or e3.get() == '' or e4.get() == '' or e5.get() == '' or e6.get() == '' or e7.get() == '' or e8.get() == '' or e9.get() == '' or e10.get() == '' or e11.get() == '' or e12.get() == '':
        MB.showerror('Insert Status', 'All Fields are mandatory.')
    elif e6.get() == e7.get():
        MB.showerror('Insert Status', 'Source and Destination should be different.')
    else:
        if ((e8.get()[0:4].isdigit()) == False or (e8.get()[5:7].isdigit() == False) or (
                e8.get()[8:].isdigit() == False) or (e8.get()[4] != '-') or (e8.get()[7] != '-') or (
                len(e8.get()) != 10)):
            MB.showerror('Insert Status', 'Wrong Date Format.')
        else:
            con = mysql.connect(host='localhost', user='root', password='Jai12345*', database='BusService')
            cur = con.cursor()
            cur.execute(
                "insert into bus_info values('" + e1.get() + "', '" + e2.get() + "', '" + e3.get() + "', '" + e4.get() + "', '" + e5.get() + "', '" + e6.get() + "', '" + e7.get() + "', '" + e8.get() + "', '" + e9.get() + "', '" + e10.get() + "', " + e11.get() + ", '" + e12.get() + "')")
            cur.execute("commit")
            MB.showinfo('Insert Status', 'Bus inserted successfully')
            con.close()



def book_tickets(contact_no):
    cnt =0
    con = mysql.connect(host='localhost', user='root', password='Jai12345*', database='BusService')
    cur = con.cursor()
    for i in range(total_no_of_seats):
        if seats[i].get() == 1:
            cnt += 1
    if MB.askyesno('Booking Status', 'Are you sure you want to book ' + str(cnt) +  ' tickets') :
        cur.execute("Update bus_info set Seats = Seats-" + str(cnt) + " where ContactNo = '" + str(contact_no) + "'")
        cur.execute('commit')
        for i in range(total_no_of_seats):
            if seats[i].get() == 1:
                cur.execute("Insert into booked_seats values('" + str(contact_no) + "', " + str(i+1) +")")
                cur.execute('commit')

        MB.showinfo('Booking Status', 'Your tickets have been booked successfully')

        con.close()



def see_all_seats():
    global tickets_frame, seats, total_no_of_seats
    contact_no = rows[x.get()][1]
    no_of_seats = rows[x.get()][11]
    seats = []
    tickets_frame.destroy()
    tickets_frame = LabelFrame(my_frame, text='Tickets')
    tickets_frame.grid(row=record_number, column=2, columnspan=7)
    con = mysql.connect(host='localhost', user='root', password='Jai12345*', database='BusService')
    cur = con.cursor()
    cur.execute("Select NoOfSeats from bus_seats where ContactNo=" + contact_no)
    total_no_of_seats = cur.fetchall()[0][0]
    #cur.execute('commit')
    for i in range(total_no_of_seats):
        seat_no = IntVar()
        seats.append(seat_no)
        cur.execute("select * from booked_seats where ContactNo = '"+contact_no + "' and SeatNo = " + str(i+1))
        is_booked = cur.fetchall()
        if len(is_booked):
            Checkbutton(tickets_frame, text=i + 1, variable=seats[i], onvalue=1, offvalue=0, state = DISABLED).grid(row=int(i / 10),
                                                                                              column=i % 10, padx=5)
        else:
            Checkbutton(tickets_frame, text=i + 1, variable=seats[i], onvalue=1, offvalue=0).grid(row=int(i / 10),
                                                                                                      column=i % 10,
                                                                                                      padx=5)
    Button(my_frame, text='BOOK', font=('Arial Black', 10), padx=5, command=lambda:book_tickets(contact_no)).grid(row=record_number,
                                                                                               column=10, columnspan=2)
    con.close()


def search_db():
    global top_s, var, e1, e2, e3, my_frame, row, rows, i, my_list, my_label, x, record_number, tickets_frame
    if var.get() == '' or e1.get() == '' or e2.get() == '' or e3.get() == '':
        MB.showerror('Search Status', 'All Fields are mandatory.')
    elif e1.get() == e2.get():
        MB.showerror('Search Status', 'Source and Destination should be different.')
    else:
        top_s = Toplevel()
        top_s.iconbitmap("bus_icon.ico")
        Label(top_s, image=my_image).grid(row=0, column=0, pady=20, padx=30)
        if ((e3.get()[0:4].isdigit()) == False or (e3.get()[5:7].isdigit() == False) or (
                e3.get()[8:].isdigit() == False) or (e3.get()[4] != '-') or (e3.get()[7] != '-') or (
                len(e3.get()) != 10)):
            MB.showerror('Insert Status', 'Wrong Date Format.')
        else:
            con = mysql.connect(host='localhost', user='root', password='Jai12345*', database='BusService')
            cur = con.cursor()
            if var.get() == 'Any':
                cur.execute(
                    "select * from Bus_info where PointofDeparture = '" + e1.get() + "' and PointofArrival = '" + e2.get() + "'and Dateofbus = '" + e3.get() + "'")
            else:
                cur.execute(
                    "select * from Bus_info where BusType = '" + var.get() + "' and PointofDeparture = '" + e1.get() + "' and PointofArrival = '" + e2.get() + "'and Dateofbus = '" + e3.get() + "'")
            rows = cur.fetchall()
            my_frame = LabelFrame(top_s, text='Available Buses', bd=5)
            my_frame.grid(row=9, column=0, padx=10, pady=10, columnspan=5)
            Label(my_frame, text='FullName', font=('Arial Black', 10)).grid(row=0, column=0)
            Label(my_frame, text='ContactNo.', font=('Arial Black', 10)).grid(row=0, column=1)
            Label(my_frame, text='Address', font=('Arial Black', 10)).grid(row=0, column=2)
            Label(my_frame, text='Operator', font=('Arial Black', 10)).grid(row=0, column=3)
            Label(my_frame, text='BusType', font=('Arial Black', 10)).grid(row=0, column=4)
            Label(my_frame, text='PointofDeparture', font=('Arial Black', 10)).grid(row=0, column=5)
            Label(my_frame, text='PointofArrival', font=('Arial Black', 10)).grid(row=0, column=6)
            Label(my_frame, text='Dateofbus', font=('Arial Black', 10)).grid(row=0, column=7)
            Label(my_frame, text='DepartureTime', font=('Arial Black', 10)).grid(row=0, column=8)
            Label(my_frame, text='ArrivalTime ', font=('Arial Black', 10)).grid(row=0, column=9)
            Label(my_frame, text='Fare', font=('Arial Black', 10)).grid(row=0, column=10)
            Label(my_frame, text='Seats', font=('Arial Black', 10)).grid(row=0, column=11)
            no_of_records = len(rows)
            tickets_frame = LabelFrame(my_frame, text='Tickets')
            x = IntVar()
            x.set(None)
            record_number = 1
            for row in rows:
                my_list = []
                for i in row:
                    my_list.append(i)
                for i in range(len(my_list)):
                    Label(my_frame, text=my_list[i]).grid(row=record_number, column=i, padx=20)
                Radiobutton(my_frame, variable=x, value=record_number - 1, command= see_all_seats).grid(
                    row=record_number, column=13)
                record_number += 1
            MB.showinfo('Records', str(no_of_records) + ' record(s) fetched.')
            cur.execute("commit")
            con.close()



def motion_fnc(event):
    top.destroy()
    root.deiconify()


def front_page():
    global top
    top = Toplevel()
    top.iconbitmap("bus_icon.ico")
    Label(top, text='PROJECT TITLE- ', font=heading_font, fg='red').grid(row=0, column=0, pady=10, padx=5)
    Label(top, text='Bus Booking System', font=heading_font).grid(row=0, column=1, pady=10, padx=10)
    Label(top, text='Developed as part of the course Advanced Programming Lab & DBMS LAB', font=('Caladea', 16)).grid(
        row=1, column=0, columnspan=2, pady=5)
    Label(top, text='DEVELOPED BY- ', font=('David Libre', 22, 'bold', 'italic'), fg='red').grid(row=2, column=0,
                                                                                                 pady=5)
    Label(top, text='MRITYUANJAYA GUPTA', font=('David Libre', 22, 'bold', 'italic')).grid(row=2, column=1, pady=10,
                                                                                           padx=5)
    Label(top, text='PROJECT SUPERVISORS- ', font=('David Libre', 22, 'bold', 'italic'), fg='red').grid(row=3, column=0,
                                                                                                        pady=5)
    Label(top, text='Dr. MAHESH KUMAR & Dr. NILESH KUMAR PATEL', font=('David Libre', 22, 'bold', 'italic')).grid(row=3,
                                                                                                                  column=1,
                                                                                                                  pady=10,
                                                                                                                  columnspan=2,
                                                                                                                  padx=5)
    Label(top, text='Make mouse movement over this screen to close ', font=('David Libre', 14, 'bold', 'italic'),
          fg='blue').grid(row=4, column=0,
                          pady=15, columnspan=2)

    top.bind('<Motion>', motion_fnc)
    top.protocol("WM_DELETE_WINDOW", on_closing)


def add_button():
    global e4, e5, e6, e7, e8, e9, e10, e11, e12
    Label(top, text='Operator: ', font=text_font).grid(row=7, column=0)
    e4 = Entry(top, width=30)
    e4.grid(row=7, column=1)
    Label(top, text='Bus Type: ', font=text_font).grid(row=8, column=0)
    e5 = StringVar()
    e5.set('AC-Sleeper')
    OptionMenu(top, e5, 'AC', 'Non-AC', 'AC-Sleeper', 'Non-AC-Sleeper').grid(row=8, column=1)
    Label(top, text='From: ', font=text_font).grid(row=9, column=0)
    e6 = Entry(top, width=30)
    e6.grid(row=9, column=1)
    l1 = Label(top, text='To: ', font=text_font).grid(row=10, column=0)
    e7 = Entry(top, width=30)
    e7.grid(row=10, column=1)
    Label(top, text='Date (yyyy-mm-dd): ', font=text_font).grid(row=11, column=0)
    e8 = Entry(top, width=30)
    e8.grid(row=11, column=1)
    Label(top, text='Departure Time: (hh:mm:ss)', font=text_font).grid(row=12, column=0)
    e9 = Entry(top, width=30)
    e9.grid(row=12, column=1)
    Label(top, text='Arrival Time: (hh:mm:ss)', font=text_font).grid(row=13, column=0)
    e10 = Entry(top, width=30)
    e10.grid(row=13, column=1)
    Label(top, text='Fare: ', font=text_font).grid(row=14, column=0)
    e11 = Entry(top, width=30)
    e11.grid(row=14, column=1)
    Label(top, text='Seats: ', font=text_font).grid(row=15, column=0)
    e12 = Entry(top, width=30)
    e12.grid(row=15, column=1)
    Button(top, text='Save', font=text_font, padx=10, bd=3, command=insert_db).grid(row=16, column=1, pady=10)


def add_fnc():
    global my_image
    global top
    global e1, e2, e3
    root.withdraw()
    top = Toplevel()
    top.iconbitmap("bus_icon.ico")
    top.title('Add_Bus_Window')
    Label(top, text='BUS BOOKING SERVICE', font=heading_font, fg='black', bg='lightblue', padx=15).grid(row=0, column=1,
                                                                                                        columnspan=3)
    Label(top, image=my_image).grid(row=1, column=1, columnspan=2, pady=20, padx=30)
    Label(top, text='Bus Operator Details Filling', font=text_font2, bd=4).grid(row=2, column=1)
    Label(top, text='Full Name: ', font=text_font).grid(row=3, column=0)
    e1 = Entry(top, width=30)
    e1.grid(row=3, column=1)
    Label(top, text='Contact No.: ', font=text_font).grid(row=4, column=0)
    e2 = Entry(top, width=30)
    e2.grid(row=4, column=1)
    Label(top, text='Address: ', font=text_font).grid(row=5, column=0)
    e3 = Entry(top, width=30)
    e3.grid(row=5, column=1)
    Button(top, text='Add Details', font=text_font, command=add_button, bd=3).grid(row=6, column=1)
    Button(top, text='HOME', font=text_font, command=to_home, bd=3).grid(row=2, column=2, pady=10)
    top.protocol("WM_DELETE_WINDOW", on_closing)


def search_fnc():
    global my_image
    global top
    root.withdraw()
    top = Toplevel()
    top.iconbitmap("bus_icon.ico")
    top.title('Search_Bus_Window')
    Label(top, text='BUS BOOKING SERVICE', font=heading_font, fg='black', bg='lightblue', padx=15).grid(row=0, column=1,
                                                                                                        columnspan=2)
    Label(top, image=my_image).grid(row=1, column=1, columnspan=2, pady=20, padx=30)
    Label(top, text='Listing Buses', font=text_font2, bd=4).grid(row=2, column=1)
    Label(top, text='Bus Type: ', font=text_font).grid(row=3, column=0)
    global var, e1, e2, e3
    var = StringVar()
    var.set('AC-Sleeper')
    OptionMenu(top, var, 'AC', 'Non-AC', 'AC-Sleeper', 'Non-AC-Sleeper', 'Any').grid(row=3, column=1)
    Label(top, text='From: ', font=text_font).grid(row=4, column=0)
    e1 = Entry(top, width=30)
    e1.grid(row=4, column=1)
    Label(top, text='To: ', font=text_font).grid(row=5, column=0)
    e2 = Entry(top, width=30)
    e2.grid(row=5, column=1)
    Label(top, text='Date (yyyy-mm-dd): ', font=text_font).grid(row=6, column=0)
    e3 = Entry(top, width=30)
    e3.grid(row=6, column=1)
    Button(top, text='Search', font=text_font, command=search_db).grid(row=7, column=1, pady=5)
    Button(top, text='HOME', font=text_font, command=to_home, bd=3).grid(row=8, column=0, pady=5)
    top.protocol("WM_DELETE_WINDOW", on_closing)


heading_font = tkFont.Font(family='David Libre', size=32, weight='bold', slant='italic')
text_font = tkFont.Font(family='Caladea', size=12, slant='italic')
text_font2 = tkFont.Font(family='Caladea', size=14, slant='italic', weight='bold')

front_page()
Label(root, text='BUS BOOKING SERVICE', font=heading_font, fg='black', bg='lightblue', padx=15).grid(row=0, column=0,
                                                                                                     columnspan=2)
my_image = ImageTk.PhotoImage((Image.open('Bus_Booking.jpg')).resize((470, 250), Image.ANTIALIAS))
Label(root, image=my_image).grid(row=1, column=0, columnspan=2, pady=20, padx=10)
Add_button = Button(root, text='Add Bus', bd=3, font=text_font, padx=5, command=add_fnc).grid(row=2, column=0, pady=5)
Search_button = Button(root, text='Search Bus', bd=3, font=text_font, padx=5, command=search_fnc).grid(row=2, column=1,
                                                                                                       pady=5)


root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()