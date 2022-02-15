from tkinter import *
import datetime
import random
from random import sample
from tkinter import messagebox
from PIL import Image, ImageGrab, ImageTk
from os import path
import mysql.connector
from datetime import date
from tkinter import colorchooser

class Quiz:
    
    def __init__(self, question, answers, CorrectOption):
        self.question = question
        self.answers = answers
        self.CorrectOption = CorrectOption

    def checkOption(self, Option, view):
        global right, wrong, skipped
        response1 = True
        if(Option == self.CorrectOption):
            self.label.config(text = "Right!", bg = "light blue", fg = "blue")
            right += 1
        elif(Option == "S"):
            self.label.config(text = "Skipped!", bg = "light blue")
            skipped += 1
        elif(Option == "T"):
            response1 = messagebox.askyesno("End the Quiz?", "Do you really want to End the Test?")
            if response1 == True:
                self.label.config(text = "You terminated the Test!!", bg = "light blue", fg = "red")
        else:
            self.label.config(text = "Wrong!\nCorrect answer is : " + self.answers[ord(self.CorrectOption) - 65], bg = "light blue", fg = "red")
            wrong += 1
        if response1 == True:
            self.button0.pack_forget()
            self.button1.pack_forget()
            self.button2.pack_forget()
            self.button3.pack_forget()
            self.skip.pack_forget()
            self.termin.pack_forget()
            view.after(1500, lambda *args: self.unpackView(Option, view))

    def getView(self, root):
        global index
        self.view1 = Frame(root, bg = "light blue")

        self.view1.pack(fill = X)
        PyQuiz = Label(self.view1, bg = "light blue", text = "Python Quiz", font = ("Algerian", 20, "bold underline")).pack()

        view = Frame(root, bg = "yellow")
        
        Label(view, text = str(index + 1) + ". " + self.question, bg = "pink", fg = "brown",
              font = ("Cambria", 16, "bold italic")).pack(fill = X)
        
        self.button0 = Button(view, bg = "orange", fg = "blue", activebackground = "light blue", font = ("Calibri", 14, "italic"),
               text = self.answers[0], command = lambda *args: self.checkOption("A", view))
        self.button0.pack(fill = X)
        self.button1 = Button(view, bg = "orange", fg = "blue", activebackground = "light blue", font = ("Calibri", 14, "italic"),
               text = self.answers[1], command = lambda *args: self.checkOption("B", view))
        self.button1.pack(fill = X)
        self.button2 = Button(view, bg = "orange", fg = "blue", activebackground = "light blue", font = ("Calibri", 14, "italic"),
               text = self.answers[2], command = lambda *args: self.checkOption("C", view))
        self.button2.pack(fill = X)
        self.button3 = Button(view, bg = "orange", fg = "blue", activebackground = "light blue", font = ("Calibri", 14, "italic"),
               text = self.answers[3], command = lambda *args: self.checkOption("D", view))
        self.button3.pack(fill = X)
        Label(view, bg = "yellow").pack()
        
        self.skip = Button(view, width = 20, bg = "red", fg = "yellow", activebackground = "pink", activeforeground = "blue",
               font = ("Cambria", 14, "bold italic"), text = "Skip", command = lambda *args: self.checkOption("S", view))
        self.skip.pack()
        self.termin = Button(view, width = 20, bg = "green", fg = "pink", activebackground = "pink", activeforeground = "blue",
               font = ("Cambria", 14, "bold italic"), text = "End the Test!", command = lambda *args: self.checkOption("T", view))
        self.termin.pack()

        self.label = Label(view, bg = "yellow", font = ("Cambria", 18, "bold italic"))
        self.label.pack()
        Label(view, bg = "yellow").pack()

        textFrame = PanedWindow(view, bg = "yellow")
        textFrame.pack(fill = BOTH)

        t = Text(textFrame, font = ("Verdana", 14, "bold"), bg = "#85FEFA", fg = "blue", wrap = WORD)
        t.insert(END, "Space for Rough Work\n")
        t.pack(fill = BOTH)
        t.tag_add("here", "1.0", "1.20")
        t.tag_config("here", background = "black", foreground = "red")
        t.focus_set()

        self.scroll = Scrollbar(root, orient = VERTICAL, command = t.yview)
        t.configure(yscrollcommand = self.scroll.set)
        self.scroll.pack(side = RIGHT, fill = Y)

        def butn_enter(butn):
            butn.config(bg = "#FF00FF", fg = "white")

        def butn_leave(butn):
            butn.config(bg = "orange", fg = "blue")

        self.button0.bind("<Enter>", lambda *args : butn_enter(self.button0))
        self.button0.bind("<Leave>", lambda *args : butn_leave(self.button0))

        self.button1.bind("<Enter>", lambda *args : butn_enter(self.button1))
        self.button1.bind("<Leave>", lambda *args : butn_leave(self.button1))

        self.button2.bind("<Enter>", lambda *args : butn_enter(self.button2))
        self.button2.bind("<Leave>", lambda *args : butn_leave(self.button2))

        self.button3.bind("<Enter>", lambda *args : butn_enter(self.button3))
        self.button3.bind("<Leave>", lambda *args : butn_leave(self.button3))

        def skip_enter():
            self.skip.config(bg = "#0000B2")

        def skip_leave():
            self.skip.config(bg = "red")

        self.skip.bind("<Enter>", lambda *args : skip_enter())
        self.skip.bind("<Leave>", lambda *args : skip_leave())

        def termin_enter():
            self.termin.config(bg = "#0000B2")

        def termin_leave():
            self.termin.config(bg = "green")

        self.termin.bind("<Enter>", lambda *args : termin_enter())
        self.termin.bind("<Leave>", lambda *args : termin_leave())
        
        return view

    def unpackView(self, Option, view):
        self.view1.pack_forget()
        view.pack_forget()
        self.scroll.pack_forget()
        askQuestion(Option)


def getMathView():
    global index

    view1 = Frame(root, bg = "light blue")
    view1.pack(fill = X)
    MatQuiz = Label(view1, bg = "light blue", text = "\nMaths Quiz\n", font = ("Algerian", 20, "bold underline")).pack(fill = X)
    
    view = Frame(root, bg = "yellow")
    N = random.randint(0, 10)
    N1 = random.randint(1, 10)
    symbol = random.randint(1, 5)
    if symbol == 1:
        sym = "+"
        n1 = N + N1
    elif symbol == 2:
        sym = "-"
        n1 = N - N1
    elif symbol == 3:
        sym = "*"
        n1 = N * N1
    elif symbol == 4:
        sym = "//"
        n1 = N // N1
    else:
        sym = "%"
        n1 = N % N1
    
    Label(view, text = str(index + 1) + ". What is " + str(N) + " " + sym + " " + str(N1) + "?", bg = "pink", fg = "brown",
          font = ("Cambria", 20, "bold italic")).pack(fill = X)
    Label(view, text = "(Enter your answer in the entry box below and then press 'Enter' or click 'Submit' button)", bg = "pink", fg = "red",
          font = ("Cambria", 20, "italic")).pack(fill = X)
    Label(view, bg = "yellow").pack()
    e5 = Entry(view, width = 40, fg = "red", bg = "light blue", font = ("Arial", 18, "italic"))
    e5.pack()
    e5.bind("<Return>", lambda *args : checkMath("E"))
    e5.focus_set()

    def e5_enter():
        e5.config(bg = "#85FEFA")

    def e5_leave():
        e5.config(bg = "light blue")

    e5.bind("<Enter>", lambda *args : e5_enter())
    e5.bind("<Leave>", lambda *args : e5_leave())

    def checkMath(Option):
        global right, wrong, skipped
        response1 = True
        n = ""
        n = e5.get()
        
        if n == str(n1):
            label.config(text = "Right!", bg = "light blue", fg = "blue")
            right += 1
        elif Option == "S":
            label.config(text = "Skipped!", bg = "light blue")
            skipped += 1
        elif Option == "T":
            response1 = messagebox.askyesno("End the Quiz?", "Do you really want to End the Test?")
            if response1 == True:
                label.config(text = "You terminated the Test!!", bg = "light blue", fg = "red")
        else:
            label.config(text = "Wrong!\n" + str(N) + " " + sym + " " + str(N1) + " is " + str(n1) + ".", bg = "light blue", fg = "red")
            wrong += 1

        def unpackMathView(Option):
            view1.pack_forget()
            view.pack_forget()
            scroll.pack_forget()
            askQuestion(Option)
            
        if response1 == True:            
            label.pack()
            e5.pack_forget()
            submit.pack_forget()
            skip.pack_forget()
            termin.pack_forget()
            view.after(1000, lambda *args: unpackMathView(Option))
        
    Label(view, bg = "yellow").pack()
    
    submit = Button(view, width = 20, fg = "orange", bg = "green", activebackground = "pink", activeforeground = "blue",
                text = "Submit", font = ("Algerian", 15, "bold italic"), command = lambda *args : checkMath("E"))
    submit.pack()

    Label(view, bg = "yellow").pack()
    
    skip = Button(view, width = 20, bg = "red", fg = "yellow", activebackground = "pink", activeforeground = "blue",
            font = ("Cambria", 14, "bold italic"), text = "Skip", command = lambda *args: checkMath("S"))
    skip.pack()
    termin = Button(view, width = 20, bg = "green", fg = "pink", activebackground = "pink", activeforeground = "blue",
               font = ("Cambria", 14, "bold italic"), text = "End the Test!", command = lambda *args: checkMath("T"))
    termin.pack()

    label = Label(view, bg = "yellow", font = ("Cambria", 18, "bold italic"))
    label.pack()
    Label(view, bg = "yellow").pack()

    textFrame = PanedWindow(view, orient = VERTICAL, bg = "yellow")
    textFrame.pack(fill = BOTH)

    t = Text(textFrame, font = ("Verdana", 14, "bold"), bg = "#85FEFA", fg = "blue", wrap = WORD)
    t.insert(END, "Space for Rough Work\n")
    t.pack(fill = X)
    t.tag_add("here", "1.0", "1.20")
    t.tag_config("here", background = "black", foreground = "red")

    scroll = Scrollbar(root, orient = VERTICAL, command = t.yview)
    t.configure(yscrollcommand = scroll.set)
    scroll.pack(side = RIGHT, fill = Y)

    def submit_enter():
        submit.config(bg = "#0000B2")

    def submit_leave():
        submit.config(bg = "green")

    submit.bind("<Enter>", lambda *args : submit_enter())
    submit.bind("<Leave>", lambda *args : submit_leave())

    def skip_enter():
        skip.config(bg = "#0000B2")

    def skip_leave():
        skip.config(bg = "red")

    skip.bind("<Enter>", lambda *args : skip_enter())
    skip.bind("<Leave>", lambda *args : skip_leave())

    def termin_enter():
        termin.config(bg = "#0000B2")

    def termin_leave():
        termin.config(bg = "green")

    termin.bind("<Enter>", lambda *args : termin_enter())
    termin.bind("<Leave>", lambda *args : termin_leave())

    return view


def askQuestion(terminate = None):
    global questions, root, index, right, wrong, skipped, start

    Subject = ""
    if var.get() == 2:
        Subject = "Maths"
    else:
        Subject = "Python"
    
    s5 = var1.get()
    if s5 == 5:
        No_of_Questions = 5
    elif s5 == 10:
        No_of_Questions = 10
    elif s5 == 20:
        No_of_Questions = 20
    elif s5 == 30:
        No_of_Questions = 30
    else:
        No_of_Questions = default

    name = e1.get()
    age = e2.get()
    
    if No_of_Questions == index + 1 or terminate == "T":
        end = datetime.datetime.now()
        elapsed = end - start

        root.overrideredirect(False)

        root.title("Quiz Application")
        
        f = Frame(root, height = 500, width = 750, bg = "light blue")
        f.propagate(0)
        f.pack(anchor = CENTER, padx = 40, pady = 50)
        
        Label(f, bg = "light blue", text = "\n\n").pack()

        Label(f, text = "Name: " + name.upper() + "\nAge: " + age + "\nSubject: " + Subject, fg = "blue", font = ("Cambria", 15, "bold italic")).pack()
        
        Label(f, bg = "light blue").pack()
        Label(f, text = "Thank you " + name.upper() + " for answering the question(s). \n" + str(right) + " of " + str(No_of_Questions) + " question(s) answered right.",
              fg = "red", font = ("Cambria", 15, "bold italic")).pack()
        if terminate == "T":
            Label(f, text = "Unattempted Question(s): " + str(No_of_Questions - (right + skipped + wrong)), fg = "blue", font = ("Cambria", 15, "italic")).pack()
        if skipped > 0:
            Label(f, text = "Skipped Question(s): " + str(skipped), fg = "blue", font = ("Cambria", 15, "italic")).pack()
        if wrong > 0:
            Label(f, text = "Wrong Answer(s): " + str(wrong), fg = "blue", font = ("Cambria", 15, "italic")).pack()
        Label(f, bg = "light blue").pack()
        
        percent = round(((right / No_of_Questions) * 100), 2)
        if percent >= 80:
            Label(f, text = "Congratulations! Your performance is very good.", fg = "blue", font = ("Cambria", 18, "bold italic")).pack()
        elif percent < 40:
            Label(f, text = "You haven't performed good. Improvement required!!", fg = "red", font = ("Cambria", 17, "bold italic")).pack()
        else:
            Label(f, text = "Your performance is good. But there is scope for improvement.\nKeep working hard!", fg = "red", font = ("Cambria", 17, "bold italic")).pack()
        
        Label(f, bg = "light blue").pack()
        Label(f, text = "Total time taken is " + str(elapsed.seconds) + " seconds.", fg = "red", font = ("Cambria", 15, "italic")).pack()
        Label(f, bg = "light blue").pack()
        
        def GetResult():
            root.destroy()
            result = Tk()
            result.configure(bg = 'chartreuse1')
            result.title("Results")
            result.geometry("960x540")
            result.state("zoomed")
            result.resizable(0, 0)
            Label(result, text = "\n", bg = 'chartreuse1', font = ("Algerian", 20, "bold underline")).pack()
            resFrame = Frame(result, height = 350)
            resFrame.pack(fill = BOTH)
            if percent >= 60:
                label1 = Label(resFrame, fg = "orange", text = "\nCertificate of Merit", font = ("Algerian", 20, "bold underline"))
                label1.pack()
                label2 = Label(resFrame, text = "\nThis is to certify that", font = ("Cambria", 17, "bold italic"))
                label2.pack()
                label3 = Label(resFrame, text = name, fg = "blue", font = ("Algerian", 17, "bold italic underline"))
                label3.pack()
                label4 = Label(resFrame, text = "has been awarded this\nCertificate of Merit for\nscoring " + str(percent) + "%\nin " + Subject + " Quiz.\n",
                      font = ("Cambria", 17, "bold italic"))
                label4.pack()
                
                today = date.today()
                label5 = Label(resFrame, text = "\nDate: " + today.strftime("%B %d, %Y") + "\n", font = ("Cambria", 17, "bold italic"))
                label5.pack()
                if Subject == "Maths":
                    canvas2 = Canvas(resFrame, width = 243, height = 208, bg = "light blue")
                    canvas2.place(x = 80, y = 110)
                    img2 = ImageTk.PhotoImage(Image.open("maths.jpg"))
                    canvas2.create_image(0, 0, anchor = NW, image = img2)
                else:
                    canvas3 = Canvas(resFrame, width = 265, height = 190, bg = "light blue")
                    canvas3.place(x = 80, y = 110)
                    img3 = ImageTk.PhotoImage(Image.open("python.jpg"))
                    canvas3.create_image(0, 0, anchor = NW, image = img3)

                canvas1 = Canvas(resFrame, width = 289, height = 175, bg = "light green")
                canvas1.place(x = 1000, y = 110)
                img1 = ImageTk.PhotoImage(Image.open("quiz time.jpg"))
                canvas1.create_image(0, 0, anchor = NW, image = img1)
                
            else:
                resFrame.config(bg = "light blue")
                Label(resFrame, bg = "light blue", fg = "red", text = "\n\nYou are not eligible for a Certificate of Merit as you have got less than 60%!!!\n\n",
                      font = ("Cambria", 17, "bold italic")).pack()

            def screen():
                save = Toplevel()
                save.configure(bg = 'orange')
                save.grab_set()
                save.resizable(0, 0)
                save.title("Name of Image")
                save.geometry("840x300")
                Label(save, text = "\n\nPlease enter the name of the image in the entrybox below and then press 'Enter' to save. \n(*)",
                       bg = 'orange', font = ("Cambria", 15, "bold")).pack()
                saveentry = Entry(save, bg = "#85FEFA", width = 15, font = ("Cambria", 14))
                saveentry.pack()
                Label(save, text = "", bg = 'orange', font = ("Cambria", 15, "bold")).pack()
                saveentry.focus_set()

                def saveentry_enter():
                    saveentry.config(bg = "magenta")

                def saveentry_leave():
                    saveentry.config(bg = "#85FEFA")

                saveentry.bind("<Enter>", lambda *args : saveentry_enter())
                saveentry.bind("<Leave>", lambda *args : saveentry_leave())

                def saveimage():
                    s = ""
                    s = saveentry.get()
                    if s == "":
                        messagebox.showerror("No Image Name", "No Image name provided by you. Please Enter a name to save the image.")
                        z = False
                    else:
                        if path.exists(s + ".jpg"):
                            messagebox.showerror("Save error", "An image(.jpg) already exists with the same name. Please Enter a different name.")
                            z = False
                        else:
                            save.destroy()
                            z = True

                    def screengrab():
                        img = ImageGrab.grab(bbox = None)
                        image = img.crop((0, 85, result.winfo_screenwidth(), resFrame.winfo_reqheight() + 130))
                        image.save(s + ".jpg")
                        root = Tk()
                        root.configure(bg = 'yellow')
                        root.title("Image Saved")
                        root.geometry("600x240")
                        root.resizable(0, 0)
                        Label(root, bg = 'yellow', font = ("Cambria", 15, "bold")).pack()
                        l = Label(root, text = "Your Certificate image is saved as '" + s + ".jpg'.", font = ("Cambria", 15, "bold"))
                        l.pack()
                        root.after(3000, root.destroy)

                    if z == True:
                        root.after(1000, lambda *args : screengrab())
                
                saveentry.bind("<Return>", lambda *args : saveimage())
                savebutton = Button(save, width = 20, bg = "yellow", activebackground = "pink", text = "Save Image", font = ("Cambria", 15), command = lambda *args : saveimage())
                savebutton.pack()
                Label(save, bg = "orange").pack()
                exit_btn = Button(save, width = 20, bg = "chartreuse1", activebackground = "pink", text = "Exit", font = ("Cambria", 15), command = save.destroy)
                exit_btn.pack()

                def savebutton_enter():
                    savebutton.config(bg = "blue", fg = "white")

                def savebutton_leave():
                    savebutton.config(bg = "yellow", fg = "black")
        
                savebutton.bind("<Enter>", lambda *args : savebutton_enter())
                savebutton.bind("<Leave>", lambda *args : savebutton_leave())

                def exit_btn_enter():
                    exit_btn.config(bg = "blue", fg = "white")

                def exit_btn_leave():
                    exit_btn.config(bg = "chartreuse1", fg = "black")
        
                exit_btn.bind("<Enter>", lambda *args : exit_btn_enter())
                exit_btn.bind("<Leave>", lambda *args : exit_btn_leave())
                
                save.mainloop()
                
            if percent >= 60:
                def choose_color():
                     _, color = colorchooser.askcolor(title ="Choose color")
                     if color != None:
                         resFrame.config(bg = color)
                         rescolor = True
                         for r in _:
                             if r < 100:
                                 rescolor = False
                                 break

                         if rescolor == True:
                             label1.config(bg = color, fg = "orange")
                             label2.config(bg = color, fg = "black")
                             label3.config(bg = color, fg = "black")
                             label4.config(bg = color, fg = "black")
                             label5.config(bg = color, fg = "black")
                         
                         else:
                             label1.config(bg = color, fg = "white")
                             label2.config(bg = color, fg = "white")
                             label3.config(bg = color, fg = "white")
                             label4.config(bg = color, fg = "white")
                             label5.config(bg = color, fg = "white")           

                Label(result, bg = 'chartreuse1', font = ("Algerian", 20, "bold underline")).pack()
                color_btn = Button(result, width = 20, bg = "#85FEFA", activebackground = "pink", text = "Choose Color for Certificate", font = ("Cambria", 15, "bold"),
                       command = lambda *args : choose_color())
                color_btn.pack()

                def color_enter():
                    color_btn.config(bg = "blue", fg = "white")

                def color_leave():
                    color_btn.config(bg = "#85FEFA", fg = "black")

                color_btn.bind("<Enter>", lambda *args : color_enter())
                color_btn.bind("<Leave>", lambda *args : color_leave())
                
                Label(result, bg = 'chartreuse1', font = ("Algerian", 20, "bold underline")).pack()
                saveCert = Button(result, width = 20, bg = "yellow", activebackground = "pink", text = "Save Certificate", font = ("Cambria", 15, "bold"),
                       command = lambda *args : screen())
                saveCert.pack()

                def saveCert_enter():
                    saveCert.config(bg = "blue", fg = "white")

                def saveCert_leave():
                    saveCert.config(bg = "yellow", fg = "black")
        
                saveCert.bind("<Enter>", lambda *args : saveCert_enter())
                saveCert.bind("<Leave>", lambda *args : saveCert_leave())

            Label(result, bg = 'chartreuse1', font = ("Algerian", 20, "bold underline")).pack()
            exit_butn = Button(result, width = 10, bg = "orange", activebackground = "pink", text = "Exit", font = ("Cambria", 15, "bold"), command = result.destroy)
            exit_butn.pack()

            def exit_butn_enter():
                exit_butn.config(bg = "blue", fg = "white")

            def exit_butn_leave():
                exit_butn.config(bg = "orange", fg = "black")
        
            exit_butn.bind("<Enter>", lambda *args : exit_butn_enter())
            exit_butn.bind("<Leave>", lambda *args : exit_butn_leave())

            menu = Menu(result) 
            result.config(menu = menu)
            filemenu = Menu(menu)
            menu.add_cascade(label = 'File', menu = filemenu)
            filemenu.add_command(label = 'Exit', command = result.destroy)

            result.mainloop()

        next_btn = Button(f, width = 10, bg = "orange", activebackground = "pink", text = "Next", font = ("Cambria", 15, "bold"), command = GetResult)
        next_btn.pack()
        Label(f, bg = "light blue").pack()
        Label(f, bg = "pink", fg = "red", text = "Click the button 'Next' to see your Certificate!", font = ("Cambria", 15, "bold italic")).pack()

        def btn_enter(btn):
            btn.config(bg = "blue", fg = "white")

        def btn_leave(btn):
            btn.config(bg = "orange", fg = "black")
        
        next_btn.bind("<Enter>", lambda *args : btn_enter(next_btn))
        next_btn.bind("<Leave>", lambda *args : btn_leave(next_btn))

        def savedata():
            datasave = Toplevel()
            datasave.configure(bg = 'magenta')
            datasave.resizable(0, 0)
            datasave.grab_set()
            datasave.title("Save data to Database")
            datasave.geometry("840x500")
            Label(datasave, text = "\n\n", bg = 'magenta', font = ("Cambria", 15, "bold")).pack()
            Label(datasave, text = "Enter your root password (*): ", font = ("Cambria", 15, "bold italic")).pack()
            passentry = Entry(datasave, width = 15, bg = "#85FEFA", fg = "red", font = ("Cambria", 14), show = "*")
            passentry.pack()
            passentry.focus_set()
            Label(datasave, bg = 'magenta', font = ("Cambria", 15, "bold")).pack()
            Label(datasave, text = "Feedback: ", font = ("Cambria", 15, "bold italic")).pack()

            def passentry_enter():
                passentry.config(bg = "yellow")

            def passentry_leave():
                passentry.config(bg = "#85FEFA")

            passentry.bind("<Enter>", lambda *args : passentry_enter())
            passentry.bind("<Leave>", lambda *args : passentry_leave())

            var2 = IntVar()

            datarb1 = Radiobutton(datasave, fg = "blue", bg = "#85FEFA", activebackground = "light blue", font = ("Arial", 14, "bold"), variable = var2,
                  cursor = "dotbox", text = "1", value = 1)
            datarb2 = Radiobutton(datasave, fg = "blue", bg = "#85FEFA", activebackground = "light blue", font = ("Arial", 14, "bold"), variable = var2,
                  cursor = "dotbox", text = "2", value = 2)
            datarb3 = Radiobutton(datasave, fg = "blue", bg = "#85FEFA", activebackground = "light blue", font = ("Arial", 14, "bold"), variable = var2,
                  cursor = "dotbox", text = "3", value = 3)
            datarb4 = Radiobutton(datasave, fg = "blue", bg = "#85FEFA", activebackground = "light blue", font = ("Arial", 14, "bold"), variable = var2,
                  cursor = "dotbox", text = "4", value = 4)
            datarb5 = Radiobutton(datasave, fg = "blue", bg = "#85FEFA", activebackground = "light blue", font = ("Arial", 14, "bold"), variable = var2,
                  cursor = "dotbox", text = "5(Default)", value = 5)

            def datarb1_enter():
                datarb1.config(bg = "yellow")

            def datarb1_leave():
                datarb1.config(bg = "#85FEFA")

            datarb1.bind("<Enter>", lambda *args : datarb1_enter())
            datarb1.bind("<Leave>", lambda *args : datarb1_leave())

            def datarb2_enter():
                datarb1.config(bg = "yellow")
                datarb2.config(bg = "yellow")

            def datarb2_leave():
                datarb1.config(bg = "#85FEFA")
                datarb2.config(bg = "#85FEFA")

            datarb2.bind("<Enter>", lambda *args : datarb2_enter())
            datarb2.bind("<Leave>", lambda *args : datarb2_leave())

            def datarb3_enter():
                datarb1.config(bg = "yellow")
                datarb2.config(bg = "yellow")
                datarb3.config(bg = "yellow")

            def datarb3_leave():
                datarb1.config(bg = "#85FEFA")
                datarb2.config(bg = "#85FEFA")
                datarb3.config(bg = "#85FEFA")

            datarb3.bind("<Enter>", lambda *args : datarb3_enter())
            datarb3.bind("<Leave>", lambda *args : datarb3_leave())

            def datarb4_enter():
                datarb1.config(bg = "yellow")
                datarb2.config(bg = "yellow")
                datarb3.config(bg = "yellow")
                datarb4.config(bg = "yellow")

            def datarb4_leave():
                datarb1.config(bg = "#85FEFA")
                datarb2.config(bg = "#85FEFA")
                datarb3.config(bg = "#85FEFA")
                datarb4.config(bg = "#85FEFA")

            datarb4.bind("<Enter>", lambda *args : datarb4_enter())
            datarb4.bind("<Leave>", lambda *args : datarb4_leave())

            def datarb5_enter():
                datarb1.config(bg = "yellow")
                datarb2.config(bg = "yellow")
                datarb3.config(bg = "yellow")
                datarb4.config(bg = "yellow")
                datarb5.config(bg = "yellow")

            def datarb5_leave():
                datarb1.config(bg = "#85FEFA")
                datarb2.config(bg = "#85FEFA")
                datarb3.config(bg = "#85FEFA")
                datarb4.config(bg = "#85FEFA")
                datarb5.config(bg = "#85FEFA")

            datarb5.bind("<Enter>", lambda *args : datarb5_enter())
            datarb5.bind("<Leave>", lambda *args : datarb5_leave())

            datarb1.place(x = 280, y = 210)
            datarb2.place(x = 325, y = 210)
            datarb3.place(x = 370, y = 210)
            datarb4.place(x = 415, y = 210)
            datarb5.place(x = 460, y = 210)

            def database():
                word = ""
                feed = ""
                word = passentry.get()
                if word == "":
                    messagebox.showerror("Password Error", "Please Enter your root Password.")
                    z = False
                else:
                    z = True
                if z == True:
                    if feed == "":
                        feed = 5
                    else:    
                        feed = var2.get()

                    mydb = mysql.connector.connect(host = "localhost", user = "root", password = word)
                    mycursor = mydb.cursor()

                    mycursor.execute("SHOW DATABASES")
                    if ('quiz_certification', ) not in mycursor:
                        mycursor.execute("CREATE DATABASE Quiz_Certification")

                    mydb = mysql.connector.connect(host = "localhost", user = "root", password = "iamritik", database = "Quiz_Certification")
                    mycursor = mydb.cursor()
                    
                    mycursor.execute("SHOW TABLES")
                    if ('quiz_certificate', ) not in mycursor:
                        mycursor.execute("CREATE TABLE Quiz_Certificate (Id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Age INT(3), Subject VARCHAR(255), Total_Questions INT(10), Correct INT(10), Unattempted INT(10), Skipped INT(10), Wrong INT(10), Percent INT(10), Time_Taken INT(10), Feedback_Rating INT(1))")

                    sql = "INSERT INTO Quiz_Certificate (Name, Age, Subject, Total_Questions, Correct, Unattempted, Skipped, Wrong, Percent, Time_Taken, Feedback_Rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                    val = [name.upper(), age, Subject, No_of_Questions, right, (No_of_Questions - (right + skipped + wrong)), skipped, wrong, percent, elapsed.seconds, feed]

                    mycursor.execute(sql, val)
                    mydb.commit()
                    Label(datasave, text = "Data inserted in database.", bg = 'orange', font = ("Cambria", 15, "bold")).place(x = 300, y = 400)
                    datasave.after(3000, datasave.destroy)

            passentry.bind("<Return>", lambda *args : database)
            datasub = Button(datasave, width = 10, bg = "yellow", activebackground = "pink", text = "Submit", font = ("Cambria", 15, "bold"), command = lambda *args : database)
            datasub.place(x = 355, y = 270)

            def datasub_enter():
                datasub.config(bg = "blue", fg = "white")

            def datasub_leave():
                datasub.config(bg = "yellow", fg = "black")
        
            datasub.bind("<Enter>", lambda *args : datasub_enter())
            datasub.bind("<Leave>", lambda *args : datasub_leave())
            
            dataexit = Button(datasave, width = 10, bg = "chartreuse1", activebackground = "pink", text = "Exit", font = ("Cambria", 15, "bold"), command = datasave.destroy)
            dataexit.place(x = 355, y = 320)

            def dataexit_enter():
                dataexit.config(bg = "blue", fg = "white")

            def dataexit_leave():
                dataexit.config(bg = "chartreuse1", fg = "black")
        
            dataexit.bind("<Enter>", lambda *args : dataexit_enter())
            dataexit.bind("<Leave>", lambda *args : dataexit_leave())
            
        sd_btn = Button(root, width = 20, bg = "orange", activebackground = "pink", text = "Save Data", font = ("Cambria", 15, "bold"), command = savedata)
        sd_btn.pack()
        sd_btn.bind("<Enter>", lambda *args : btn_enter(sd_btn))
        sd_btn.bind("<Leave>", lambda *args : btn_leave(sd_btn))

        Label(root, bg = "light green", fg = "red", text = "Click the button 'Save Data' to save your data!", font = ("Cambria", 15, "bold italic")).pack()
        
        menu = Menu(root) 
        root.config(menu = menu)
        filemenu = Menu(menu)
        menu.add_cascade(label = 'File', menu = filemenu)
        filemenu.add_command(label = 'Exit', command = root.destroy)
        
        return
    
    index += 1
    if index == 0:
        root.overrideredirect(True)
        start = datetime.datetime.now()
    if Subject == "Maths":
        root.title("Maths Quiz")
        getMathView().pack(fill = X)
    elif Subject == "Python":
        root.title("Python Quiz")
        questions[index].getView(root).pack(fill = X)

questions = []
file = open("Python.txt", "r")
line = file.readline()
while(line != ""):
    QuestionString = line
    answers = []
    for i in range(4):
        answers.append(file.readline())
        
    CorrectOption = file.readline()
    CorrectOption = CorrectOption[:-1]
    questions.append(Quiz(QuestionString, answers, CorrectOption))
    line = file.readline()
    questions = sample(questions, len(questions))
    
file.close()

index = -1
right = 0
wrong = 0
skipped = 0
default = 10

root = Tk()
root.configure(bg = 'light green')
root.title("Quiz Application")
root.geometry("1050x700")
root.state("zoomed")
root.resizable(0, 0)

now = datetime.datetime.now()
time_string = now.strftime("%H")

tim = Label(root, bg = "red", fg = "yellow", font = ("Cambria", 15, "bold italic"))
tim.pack()

if int(time_string) >= 0 and int(time_string) < 12:
    tim.config(text = "Good Morning!!!")
elif int(time_string) >= 12 and int(time_string) < 16:
    tim.config(text = "Good afternoon!!!")
else:
    tim.config(text = "Good evening!!!")

root.after(3000, tim.destroy)

today = date.today()
Label(root, text = today.strftime("%B %d, %Y"), bg = "light green", fg = "blue", font = ("Cambria", 15, "bold")).place(x = 1000, y = 0)

frame = Frame(root, height = 500, width = 1000, bg = 'chartreuse1')
frame.propagate(0)
frame.pack(anchor = CENTER, pady = 100)

Label(frame, bg = "pink", fg = "blue", text = "Enter the following details", font = ("Cambria", 15, "bold italic underline")).place(x = 140, y = 50)

l1 = Label(frame, bg = "pink", text = "Enter your Name (*): ", font = ("Cambria", 15, "italic"))
e1 = Entry(frame, width = 30, fg = "blue", bg = "yellow", highlightthickness = 1, highlightcolor = "red", font = ("Algerian", 15, "italic"))

l2 = Label(frame, bg = "pink", text = "Enter your Age (*): ", font = ("Cambria", 15, "italic"))
e2 = Spinbox(frame, from_ = 10, to = 100, width = 10, fg = "blue", bg = "yellow", font = ("Arial", 15, "italic"))

canvas = Canvas(frame, width = 318, height = 159, bg = "light blue")
canvas.place(x = 660, y = 80)
img = ImageTk.PhotoImage(Image.open("quiz.png"))
canvas.create_image(0, 0, anchor = NW, image = img)

def ins_close(f_ins):
    f_ins.destroy()
    cross.config(text = "+ Instruction", bg = "yellow", fg = "black", command = lambda *args : ins())

    def cross_enter():
        cross.config(bg = "light blue", fg = "black")

    def cross_leave():
        cross.config(bg = "yellow", fg = "black")

    cross.bind("<Enter>", lambda *args : cross_enter())
    cross.bind("<Leave>", lambda *args : cross_leave())

def ins():
    f_ins = Frame(root, height = 660, width = 640, bg = 'orange')
    f_ins.place(x = 60, y = 70)
    Label(f_ins, text = "\n1. The default number of questions is set to 10.\n\n2. The default subject is set to Python.\n\n3. The time taken to complete the Quiz will be recorded.\n\n4. You cannot go back to the previous question once they are submitted.\n\n5. You will get a Certificate of Merit only if you score 60% or above.\n",
          bg = "orange", font = ("Cambria", 15, "bold italic")).pack()
    cross.config(text = "X Instruction", bg = "blue", fg = "white", command = lambda *args : ins_close(f_ins))

    def cross_enter():
        cross.config(bg = "red", fg = "white")

    def cross_leave():
        cross.config(bg = "blue", fg = "white")

    cross.bind("<Enter>", lambda *args : cross_enter())
    cross.bind("<Leave>", lambda *args : cross_leave())

cross = Button(root, bg = "yellow", text = "+ Instruction", font = ("Cambria", 12, "bold"), command = lambda *args : ins())
cross.place(x = 250, y = 40)

def cross_enter():
    cross.config(bg = "light blue", fg = "black")

def cross_leave():
    cross.config(bg = "yellow", fg = "black")

cross.bind("<Enter>", lambda *args : cross_enter())
cross.bind("<Leave>", lambda *args : cross_leave())

def py_close(py_ins):
    py_ins.destroy()
    py.config(text = "+ Python", bg = "yellow", fg = "black", command = lambda *args : pyins())

    def py_enter():
        py.config(bg = "light blue", fg = "black")

    def py_leave():
        py.config(bg = "yellow", fg = "black")

    py.bind("<Enter>", lambda *args : py_enter())
    py.bind("<Leave>", lambda *args : py_leave())

def pyins():
    py_ins = Frame(root, height = 660, width = 640, bg = 'yellow')
    py_ins.place(x = 230, y = 70)
    Label(py_ins, text = "\n1. The total number of questions will be according to the selected choice.\n\n2. All the questions will consist of 4 options.\n\n3. Once the option is clicked, it will get selected.\n\n4. A 'Skip' button is provided to move to the next question without answering the current question.\n\n5. A 'End the Test' button is provided to end the test without answering the remaining questions.\n",
          bg = "white", font = ("Cambria", 15, "bold italic")).pack()
    py.config(text = "X Python", bg = "blue", fg = "white", command = lambda *args : py_close(py_ins))

    def py_enter():
        py.config(bg = "red", fg = "white")

    def py_leave():
        py.config(bg = "blue", fg = "white")

    py.bind("<Enter>", lambda *args : py_enter())
    py.bind("<Leave>", lambda *args : py_leave())

py = Button(root, bg = "yellow", text = "+ Python", font = ("Cambria", 12, "bold"), command = lambda *args : pyins())
py.place(x = 640, y = 40)

def py_enter():
    py.config(bg = "light blue", fg = "black")

def py_leave():
    py.config(bg = "yellow", fg = "black")

py.bind("<Enter>", lambda *args : py_enter())
py.bind("<Leave>", lambda *args : py_leave())

def mat_close(mat_ins):
    mat_ins.destroy()
    mat.config(text = "+ Maths", bg = "yellow", fg = "black", command = lambda *args : matins())

    def mat_enter():
        mat.config(bg = "light blue", fg = "black")

    def mat_leave():
        mat.config(bg = "yellow", fg = "black")

    mat.bind("<Enter>", lambda *args : mat_enter())
    mat.bind("<Leave>", lambda *args : mat_leave())

def matins():
    mat_ins = Frame(root, height = 660, width = 640, bg = 'green')
    mat_ins.place(x = 420, y = 70)
    Label(mat_ins, text = "\n1. The total number of questions will be according to the selected choice.\n\n2. All the questions will consist of an entry box where the answer is need to be written.\n\n3. After writing the answer in the answer in the entry box, 'Submit' button needs to be clicked or \n'Enter' button on the keyboard needs to be pressed to submit the answer and move to the next question.\n\n4. A 'Skip' button is provided to move to the next question without answering the current question.\n\n5. A 'End the Test' button is provided to end the test without answering the remaining questions.\n",
          bg = "green", fg = "white", font = ("Cambria", 15, "bold italic")).pack()
    mat.config(text = "X Maths", bg = "blue", fg = "white", command = lambda *args : mat_close(mat_ins))

    def mat_enter():
        mat.config(bg = "red", fg = "white")

    def mat_leave():
        mat.config(bg = "blue", fg = "white")

    mat.bind("<Enter>", lambda *args : mat_enter())
    mat.bind("<Leave>", lambda *args : mat_leave())

mat = Button(root, bg = "yellow", text = "+ Maths", font = ("Cambria", 12, "bold"), command = lambda *args : matins())
mat.place(x = 1000, y = 40)

def mat_enter():
    mat.config(bg = "light blue", fg = "black")

def mat_leave():
    mat.config(bg = "yellow", fg = "black")

mat.bind("<Enter>", lambda *args : mat_enter())
mat.bind("<Leave>", lambda *args : mat_leave())

var1 = IntVar()

l3 = Label(frame, bg = "pink", text = "How many questions do\nyou want to attempt?",
           font = ("Cambria", 15, "italic"))
rb3 = Radiobutton(frame, fg = "blue", bg = "yellow", activebackground = "light blue", font = ("Arial", 12), variable = var1,
                  cursor = "dotbox", text = "5", value = 5)
rb4 = Radiobutton(frame, fg = "blue", bg = "yellow", activebackground = "light blue", font = ("Arial", 12), variable = var1,
                  cursor = "dotbox", text = "10 (Default)", value = 10)
rb5 = Radiobutton(frame, fg = "blue", bg = "yellow", activebackground = "light blue", font = ("Arial", 12), variable = var1,
                  cursor = "dotbox", text = "20", value = 20)
rb6 = Radiobutton(frame, fg = "blue", bg = "yellow", activebackground = "light blue", font = ("Arial", 12), variable = var1,
                  cursor = "dotbox", text = "30", value = 30)

var = IntVar()

l4 = Label(frame, bg = "pink", text = "Please select the subject for the Quiz.", font = ("Cambria", 15, "italic"))
rb1 = Radiobutton(frame, fg = "blue", bg = "yellow", activebackground = "light blue", font = ("Arial", 12, "italic underline"), variable = var,
                  cursor = "dotbox", indicatoron = True, text = "Python (Default)", value = 1)
rb2 = Radiobutton(frame, fg = "blue", bg = "yellow", activebackground = "light blue", font = ("Arial", 12, "italic underline"), variable = var,
                  cursor = "dotbox", text = "Maths", value = 2)

def rb_enter(rb):
    rb.config(bg = "#85FEFA")

def rb_leave(rb):
    rb.config(bg = "yellow")

e1.bind("<Enter>", lambda *args : rb_enter(e1))
e1.bind("<Leave>", lambda *args : rb_leave(e1))
e2.bind("<Enter>", lambda *args : rb_enter(e2))
e2.bind("<Leave>", lambda *args : rb_leave(e2))

rb1.bind("<Enter>", lambda *args : rb_enter(rb1))
rb1.bind("<Leave>", lambda *args : rb_leave(rb1))
rb2.bind("<Enter>", lambda *args : rb_enter(rb2))
rb2.bind("<Leave>", lambda *args : rb_leave(rb2))
rb3.bind("<Enter>", lambda *args : rb_enter(rb3))
rb3.bind("<Leave>", lambda *args : rb_leave(rb3))
rb4.bind("<Enter>", lambda *args : rb_enter(rb4))
rb4.bind("<Leave>", lambda *args : rb_leave(rb4))
rb5.bind("<Enter>", lambda *args : rb_enter(rb5))
rb5.bind("<Leave>", lambda *args : rb_leave(rb5))
rb6.bind("<Enter>", lambda *args : rb_enter(rb6))
rb6.bind("<Leave>", lambda *args : rb_leave(rb6))

l1.place(x = 80, y = 100)
e1.place(x = 270, y = 100)
e1.focus_set()

l2.place(x = 80, y = 150)
e2.place(x = 260, y = 150)

def AgeFocus():
    e2.focus_set()

e1.bind("<Return>", lambda *args : AgeFocus())

l3.place(x = 80, y = 200)
rb3.place(x = 290, y = 210)
rb4.place(x = 340, y = 210)
rb5.place(x = 460, y = 210)
rb6.place(x = 520, y = 210)

l4.place(x = 80, y = 270)
rb1.place(x = 400, y = 270)
rb2.place(x = 560, y = 270)

e2.bind("<Return>", lambda *args : changeFrame())

Label(frame, bg = "pink", fg = "red", text = "Click the following button 'Start Quiz' to Start the Quiz!",
      font = ("Cambria", 15, "bold italic")).place(x = 80, y = 320)

button = Button(frame, width = 25, height = 2, fg = "orange", bg = "blue", activebackground = "yellow", activeforeground = "blue",
                text = "Start Quiz", font = ("Algerian", 20, "bold italic"), command = lambda *args : changeFrame())
button.place(x = 175, y = 370)

def button_enter():
    button.config(bg = "#0000B2", fg = "magenta")

def button_leave():
    button.config(bg = "blue", fg = "orange")

button.bind("<Enter>", lambda *args : button_enter())
button.bind("<Leave>", lambda *args : button_leave())

def changeFrame():
    sub = ""
    if var.get() == 2:
        sub = "Maths"
    else:
        sub = "Python"
    x = ""
    y = ""
    name = ""
    age = ""
    ques = ""
    name = e1.get()
    age = e2.get()
    if name != "":
        for i in name:
            if i.isalpha() or i.isspace():
                x = True
            else:
                x = False
                break
        if x == False:
            messagebox.showerror("Name Error", "The name provided by you is not appropriate. Enter Name with alphabets only.")
    else:
        messagebox.showerror("No Name", "No name provided by you. Please Enter your Name.")
        x = False
        
    if x != False:
        if age != "":
            for i in age:
                if i.isdigit():
                    y = True
                else:
                    y = False
                    break
            if y == False:
                messagebox.showerror("Age Error", "The age provided by you is not appropriate. Enter Age in digits only.")
        else:
            messagebox.showerror("No Age", "No age provided by you. Please Enter your Age.")
            y = False
    if x != False and y != False:
        if int(age) < 10 or int(age) > 100:
            messagebox.showerror("Age error", "Age cannot be less than 10 or greater than 100. Please Enter your Age.")
            y = False
        else:
            y = True

    if sub == "Python" and var1.get() > len(questions):
        messagebox.showerror("Question error", "The total number of questions available for Python are " + str(len(questions)) + ". So, choose number of questions less than this.")
        x = False
            
    if x != False and y != False:
        if var1.get() == 5:
            ques = 5
        elif var1.get() == 10:
            ques = 10
        elif var1.get() == 20:
            ques = 20
        elif var1.get() == 30:
            ques = 30
        else:
            ques = default
    
        messagebox.showinfo("Test", "Hello " + name.upper() + "! There are a total of " + str(ques) + " question(s). Your " + sub + " exam is going to start!!")
        
        response = messagebox.askyesno("Continue?", "Do you want to Start the Quiz?")
        
        if response == True:
            button.pack_forget()
            frame.after(1000, lambda *args: unpackFrame())

def unpackFrame():
    cross.destroy()
    py.destroy()
    mat.destroy()
    frame.pack_forget()
    askQuestion()

root.mainloop()

