import tkinter.filedialog
from tkinter import *
from tkinter import ttk,messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image,ImageTk
import backend
import threading


def addnew_record():
    add_screen = Toplevel()
    add_screen.geometry("1000x500")
    add_screen.title("Add New Record")
    add_screen.maxsize(1000,500)

    header_add_screen = Frame(add_screen,bg="blue")
    header_add_screen.place(x=0,y=0,width=1000,height=60)
    add_image = ImageTk.PhotoImage(Image.open('database.png'))


    l_title = Label(header_add_screen,text="Add New Record",font=("",25,'bold'),bg='blue',fg='white')
    l_title.place(x= 20,y=10)

    image_label = Label(header_add_screen, image=add_image,bg="blue")
    image_label.image = add_image
    image_label.place(x=290,y=5)

    increment = 0
    for l_text in backend.column:
        labels = Label(add_screen,text=l_text,font=("",13))
        labels.place(x = 20,y = 100+increment)
        increment = increment+50

    e_AccountID = ttk.Combobox(add_screen, values=backend.AccountIDs, font=("", 13))
    e_AccountID.place(x=200, y=104)
    e_AccountID.set(backend.AccountIDs[0])

    e_month = ttk.Combobox(add_screen,values=backend.months,font=("",13))
    e_month.place(x=200,y=154)


    e_year = ttk.Combobox(add_screen, values=backend.years, font=("", 13))
    e_year.place(x=200, y=204)

    e_units = Entry(add_screen,width=20,font=("",13))
    e_units.place(x=200,y=254)

    e_KECharges = Entry(add_screen, width=20,font=("",13))
    e_KECharges.place(x=200, y=304)

    e_GovtCharges = Entry(add_screen,width=20,font=("",13))
    e_GovtCharges.place(x=200,y=354)

    e_Bill = Entry(add_screen, width=20,font=("",13))
    e_Bill.place(x=200, y=404)



    add_sumbit = Button(add_screen,text="Sumbit",command=lambda : sumbit([e_AccountID.get(),e_month.get(),e_year.get()
            ,e_units.get(),e_KECharges.get(),e_GovtCharges.get(),e_Bill.get()]),font=("",13))
    add_sumbit.place(x=750,y=304,width=100,height=40)


    def sumbit(data_list):
        e_year.delete(0,END)
        e_units.delete(0,END)
        e_month.delete(0,END)
        e_Bill.delete(0,END)
        e_KECharges.delete(0,END)
        e_GovtCharges.delete(0,END)
        e_AccountID.delete(0,END)

        e_AccountID.set(backend.AccountIDs[0])

        if(data_list[0]=='' or data_list[1]=='' or data_list[2]=='' ):
            messagebox.showerror(title="Invalid Info",message="Invalid Input")
        else:
            # Check if Year is present in database or not
            # if not present then append in the Year list
            if (int(data_list[2]) not in backend.years):
                    backend.years.append(int(data_list[2]))
                    # reassign the value
                    e_year['values'] = backend.years
                    ed_year['values'] = backend.years

            if(data_list[0] not in backend.AccountIDs):
                backend.AccountIDs.append(data_list[0])
                e_AccountID['values'] = backend.AccountIDs
                ed_AccountID['values'] = backend.AccountIDs
            backend.add_data(data_list)

            successfull = Label(add_screen,text="Added Successfully",font=("",10))
            successfull.place(x=750,y=350)

            # delete after some time (3sec)
            add_screen.after(3000, lambda :successfull.destroy())
        # print(data_list)





def exportexcel():
    foldername = tkinter.filedialog.asksaveasfile(filetypes=[("Excel File","*.xlsx")],defaultextension=".xlsx")
    backend.export_data(foldername.name)

def importexcel():
    root.filename = tkinter.filedialog.askopenfilename(initialdir="C:\\Users",title="Select a file",filetypes=(("Excel", "*.xlsx"), ("All files", "*.*")))
    backend.import_data(root.filename)
    ed_AccountID['values'] = backend.AccountIDs
    ed_year['values'] = backend.years
    ed_year.set(backend.years[0])
    plot_graph_price(backend.years[0],backend.AccountIDs[0])
    plot_graph_units(backend.years[0],backend.AccountIDs[0])





def plot_graph_price(year,AccountNo = '0400009513165'):
    figure2 = backend.plt.figure(figsize=(5, 5), dpi=100)
    figure2.set_size_inches(6.4, 4)
    backend.plot_graph_price(int(year),AccountNo)
    canvas2 = FigureCanvasTkAgg(figure2, frame2)
    canvas2.draw()
    canvas2.get_tk_widget().place(x=0, y=0)
    plot_graph_units(year,AccountNo)


def plot_graph_units(year,AccountNo = '0400009513165'):
    figure1 = backend.plt.figure(figsize=(5, 5), dpi=100)
    figure1.set_size_inches(5.5, 4)
    backend.plot_graph_units(int(year),AccountNo)
    canvas1 = FigureCanvasTkAgg(figure1, frame1)
    canvas1.draw()
    canvas1.get_tk_widget().place(x=0, y=0)

root = Tk()

root.title("Energy Monitoring System")
root.geometry("1280x760")
root.config(background='#eff5f6')

# ----------------------------------------------------------------------------------------------------------
# ------------------------------------------HEADER-------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------
header = Frame(root,bg = 'blue')
header.place(x = 0,y=0,width = 1920,height = 60)
title = Label(header,text="Energy Monitoring System",bg="blue",fg='white',font=("",20,'bold'))
title.place(x = 10, y = 10)


# ------------------------------------------------------------------------------------------------------------
# --------------------------------------------SIDEBAR-----------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------

sideframe = Frame(root,bg = 'white')
sideframe.place(x=0,y=60,width=250,height=1080)

add = Button(sideframe,text="Add new",command=addnew_record,bg='white',font=("",13))
add.place(x = 70,y=300,width=100,height=20 )

export = Button(sideframe,text="Export",command=exportexcel,bg='white',font=("",13))
export.place(x = 70,y=350,width=100,height=20)

import_csv = Button(sideframe,text="Import Excel",command=importexcel,bg = 'white',font=("",13))
import_csv.place(x=70,y=400,width=100,height=20)

quit = Button(sideframe,text="Quit",command=lambda : root.quit(),bg = 'white',font=("",13))
quit.place(x=70,y=450,width=100,height=20)

# -------------------------------------------------------------------------------------------------------------------
# ----------------------------------BODY--------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------


frame1= Frame(root,bg = 'white')
frame1.place(x = 260,y=70,width=510,height=400)  #----- x = 260 y = 70
figure1 = backend.plt.figure(figsize=(5,5),dpi=100)
figure1.set_size_inches(5.5,4)
backend.plot_graph_units(backend.years[0],backend.AccountIDs[0])
canvas1 = FigureCanvasTkAgg(figure1,frame1)
canvas1.draw()
canvas1.get_tk_widget().place(x=0,y=0)

frame2= Frame(root,bg = 'green')
frame2.place(x = 780,y=70,width=580,height=400)
figure2 = backend.plt.figure(figsize=(5,5),dpi= 100)
figure2.set_size_inches(6.4,4)
backend.plot_graph_price(backend.years[0],backend.AccountIDs[0])
canvas2 = FigureCanvasTkAgg(figure2,frame2)
canvas2.draw()
canvas2.get_tk_widget().place(x=0,y=0)

frame3 = Frame(root,bg = "yellow")
frame3.place(x =260,y=470,width=1100,height=250)







ed_year = ttk.Combobox(frame3,values=backend.years)

ed_year.place(x=430, y=20, width=150, height=30)
ed_year.set(backend.years[0])



ed_AccountID = ttk.Combobox(frame3,values=backend.AccountIDs)
ed_AccountID.place(x=430, y=50, width=150, height=30)
ed_AccountID.set((backend.AccountIDs[0]))

sumbit = Button(frame3,text="Show",command=lambda : plot_graph_price(ed_year.get(),ed_AccountID.get()),font=("",13))
sumbit.place(x = 582,y=20,height=30,width=50)

ed_Cyear = ttk.Combobox(frame3,values=backend.years)
ed_Cyear.place(x=682,y=20)

root.mainloop()