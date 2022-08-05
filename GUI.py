import tkinter as tk
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import TwitterBot

window = tk.Tk()
window.geometry("1280x800")
window.config(bg='#C0C0C0')
window.resizable(0,0)


#weigth of first and second column
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.columnconfigure(3, weight=1)
window.columnconfigure(4, weight=1)



l1 = tk.Label(window,text="T-stats")
l1.config(font=("Impact",45),bg='#C0C0C0',fg='#51087E')
l1.grid(column=1, row=0,columnspan=3, sticky=tk.NS)

l2 = tk.Label(window,text='Twitter Hashtag : ',font=('Helvetica',15,'bold'),fg='#DA00C0')
l2.grid(column=1, row=1, sticky=tk.E,padx= 30,pady=30)
l2.config(bg='#C0C0C0')
entry = tk.Entry(window,font=('Helvetica',15,'normal'))
entry.grid(column=3, row=1, sticky=tk.W,padx = 30,pady=30)



def getStats():
    global canvas
    global text
    hashTag = entry.get()
    listStats = TwitterBot.fetch(hashTag)
    p = listStats[0]
    q = listStats[1]
    n = listStats[2]
    x = ['Positive', 'Negative', 'Neutral']

    y = [p,q,n]

    fig = plt.figure(figsize=(4, 5))
    plt.bar(x=x, height=y)

    # You can make your x axis labels vertical using the rotation
    plt.xticks(x)
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=3, column=0,columnspan = 2,sticky=tk.E,padx = 50,pady=30)
    m1 = "Positive tweet highlight : \n"
    m2 = "\nNegative tweet highlight : \n"



    message = "\n"+listStats[3]
    message2 = "\n"+listStats[4]

    text = tk.Text(window)
    text.tag_configure("bold",font=('Impact',18,'bold'),foreground='#8b0000')
    text.tag_configure("twee", font=('Helvetica',14,'bold'),foreground="#D1B000")
    text.insert(INSERT,m1,"bold")
    

    text.insert(INSERT,message,"twee")
    text.insert(END,m2,"bold")
    text.insert(END,message2,"twee")
    text.grid(row=3,column=3,columnspan = 2,sticky=tk.W,pady=30,padx=50)

def clearStats():

    for item in canvas.get_tk_widget().find_all():
       canvas.get_tk_widget().delete(item)
    text.delete("1.0","end")
    



button1 = tk.Button(window, text=' Get Stats ',bg='purple',command=getStats,font=('Helvetica',12,'bold'),fg='#D1B000')
button1.grid(row=2,column=1,sticky=tk.E,padx=20,pady=10)
button2 = tk.Button(window, text=' Clear ',command=clearStats,bg='lightsteelblue2',font=('Helvetica',12,'bold'),fg='#D1B000')
button2.grid(row=2,column=2,sticky=tk.W)
button3 = tk.Button(window, text=' Exit ',command=window.destroy,bg='red',font=('Helvetica',12,'bold'),fg='#D1B000')
button3.grid(row=2,column=3,sticky=tk.E)



window.mainloop()