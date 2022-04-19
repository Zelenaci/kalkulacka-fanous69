import tkinter as tk
from tkinter import ANCHOR, Frame, messagebox, Listbox, END, ACTIVE
from os.path import basename, splitext
import math



class Application(tk.Tk):

    nazev = basename(splitext(basename(__file__.capitalize()))[0])
    nazev = "kalkulačkys"
    


    def __init__(self):

        super().__init__(className=self.nazev)

        self.title(self.nazev)
        self.bind("<Escape>", self.quit)
        self.protocol("WM_DELETE_WINDOW", self.quit)        
        self.bind("<Return>", self.insert)


        self.var_field = tk.Variable()


        self.entry_field = tk.Entry(self, textvariable = self.var_field, width = 40)
        self.entry_field.grid(row = 1, column=1, columnspan = 4)
        
        self.listbox = Listbox(self, width = 35)
        self.listbox.grid(row = 2, column = 1, pady = 25, columnspan = 4)
        

        self.frame = Frame(self)
        self.frame.grid(row = 2, column = 5)

        self.btn_up = tk.Button(self.frame, text = "NAHORU", command = self.up, width = 10, border = 5, background = "#c3ffb5")
        self.btn_up.pack()

        self.btn_down = tk.Button(self.frame, text = "DOLŮ", command = self.down, width = 10, border = 5, background = "#c3ffb5")
        self.btn_down.pack()
        
        self.btn_quit = tk.Button(self, text = "ZAVŘÍT", command = self.quit, width = 12, border = 5, background = "#adb1ff")
        self.btn_quit.grid(row = 4, column = 2)

        self.btn_del = tk.Button(self, text = "SMAZAT", command = self.del_storage, width = 12, border = 5, background = "#adb1ff")
        self.btn_del.grid(row = 4, column = 4)


        self.storage = []
        self.double_operand = {}
        self.double_operand["+"] = lambda a, b: a + b
        self.double_operand["-"] = lambda a, b: a - b
        self.double_operand["*"] = lambda a, b: a * b
        self.double_operand["/"] = lambda a, b: a / b
        self.double_operand["//"] = lambda a, b: a // b
        self.double_operand["**"] = lambda a, b: a ** b

        self.single_operand = {}
        self.single_operand["sin"] = math.sin
        self.single_operand["cos"] = math.cos
        self.single_operand["tg"] = math.tan
        self.single_operand["tan"] = math.tan



    def insert(self, event = None):
        
        raw = self.var_field.get().split()

        if len(raw) == 0:
            count = 1

        else:
            count = len(raw)

        for i in range(0, count):

            if len(raw) == 0:
                messagebox.showerror("Chyba", "Nevalidní operace nebo číslo!")

            else:
                item = raw[i]

                if item == "":
                    messagebox.showerror("Chyba", "Nevalidní operace nebo číslo!")

                try:
                    self.storage.append(float(item))

                except:
                    pass

                if item.upper() == "Q":
                    self.quit()

                if item.upper() == "PI":
                    self.listbox.insert(END, math.pi)
                    self.storage.append(math.pi)

                if item in self.double_operand.keys():

                    if len(self.storage) >= 2:

                        b = self.storage.pop()
                        a = self.storage.pop()
                        self.storage.append(self.double_operand[item](a, b))
                        self.listbox.insert(END, self.double_operand[item](a, b))

                    else:
                        messagebox.showerror("Chyba", "Nedostatek proměnných")
                
                if item in self.single_operand.keys():

                    if len(self.storage) >= 1:

                        a = self.storage.pop()
                        self.storage.append(self.single_operand[item](a))
                        self.listbox.insert(END, self.single_operand[item](a))

                    else:
                        messagebox.showerror("Chyba", "Nedostatek proměnných")
                self.listbox_reload()

    def down(self, event = None):

        if self.listbox.get(ACTIVE) != "":

            item = self.listbox.curselection()[0]
            self.storage[item], self.storage[item + 1] = self.storage[item + 1], self.storage[item]
            self.listbox_reload()
          
            self.listbox.selection_set(item + 1)
            self.listbox.activate(item + 1) 

        else:
            messagebox.showerror("Výběr", "Nic není vybráno vyber nějaké číslo!")

    def up(self, event = None):

        if self.listbox.get(ACTIVE) != "":

            item = self.listbox.curselection()[0]
            self.storage[item], self.storage[item - 1] = self.storage[item - 1], self.storage[item]
            self.listbox_reload()
          
            self.listbox.selection_set(item - 1)
            self.listbox.activate(item - 1)

        else:
            messagebox.showerror("Výběr", "Nic není vybráno vyber nějaké číslo!")
           

    def del_storage(self):

        if self.listbox.get(ANCHOR) != "":

            item = self.listbox.curselection()[0]
            self.storage.pop(item)
            self.listbox_reload()
        
        else:
            messagebox.showerror("Výběr", "Nic není vybráno vyber nějaké číslo!")


    def listbox_reload(self):

        self.var_field.set("")
        self.listbox.delete(0, END)

        for item in self.storage:
            self.listbox.insert(END, item)

    def quit(self, event = None):
        super().quit()


app = Application()
app.mainloop()