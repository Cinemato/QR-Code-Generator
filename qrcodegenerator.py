import pyqrcode
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import ImageTk, Image
import os
       
class HomePage(tk.Frame):
    def __init__(self, parent, show_page, next_page):
        super().__init__(parent)
        self.show_page = show_page
        self.next_page = next_page
        self.load_list(parent)
        
    def load_list(self, parent):
        for widgets in self.winfo_children():
            widgets.destroy()
        frame_header = tk.Frame(self, bg="WHITE")
        frame_header.place(x=0, y=0, width=500, height=35)
        
        label = tk.Label(frame_header, text="QR Code Generator", font=('Arial', 18), bg="WHITE")
        label.pack(pady=5)
        
        frame_body = tk.Frame(self, bg="WHITE")
        frame_body.place(x=0, y=30, width=500, height=500)
        
        self.directory = "qr_list"
        if not os.path.exists(self.directory):
                os.mkdir(self.directory)
        
        if len(os.listdir(self.directory)) <= 0:
            label_empty = tk.Label(frame_body, text="List is Empty", font=('Arial', 13), bg="WHITE", fg="RED")
            label_empty.pack(pady=20)
        else:
            canvas = tk.Canvas(frame_body, bg="WHITE")
            scrollbar = tk.Scrollbar(frame_body, orient="vertical", command=canvas.yview)
            
            frame_list = tk.Frame(canvas, bg="WHITE")
            frame_list.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            
            canvas.create_window((0, 0), window=frame_list, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            for filename in os.listdir(self.directory):
                frame_item = tk.Frame(frame_list, width=500, height=50)
                frame_item.pack(pady=5)
        
                label_name = tk.Label(frame_item, text=filename, font=('Arial', 15))
                label_name.place(x=5, y=6, width=200, height=35)
        
                btn_view = tk.Button(frame_item, text="View QR Code", width=20, command=lambda f=filename: self.view_qr(f))
                btn_view.place(x=250, y=12)
                
                btn_delete = tk.Button(frame_item, text="X", width=5, bg="RED", fg="WHITE", command=lambda f=filename: self.del_qr(f,parent))
                btn_delete.place(x=415, y=12)
            
        frame_footer = tk.Frame(self, bg="WHITE")
        frame_footer.place(x=0, y=520, width=500, height=100)
        
        btn_1 = ttk.Button(frame_footer, text="Create", width=20, command=lambda: self.show_page("Create"))
        btn_1.pack()
        
    def view_qr(self, file):
        self.next_page.set_image(self.directory + "/" + file)
        self.show_page("View")
        
    def del_qr(self, file, parent):
        msg_box = tk.messagebox.askquestion('Delete QR', 'Are you sure you want to delete ' + file + "?",icon='warning')
        if msg_box == 'yes':
            os.remove(self.directory + "/" + file)
            self.load_list(parent)
        else:
            pass
            

class CreatePage(tk.Frame):
    def __init__(self, parent, show_page, next_page):
        super().__init__(parent)
        self.show_page = show_page
        self.next_page = next_page
        
        frame_header = tk.Frame(self, bg="WHITE")
        frame_header.place(x=0, y=0, width=500, height=35)
        
        label = tk.Label(frame_header, text="QR Code Generator", font=('Arial', 18), bg="WHITE")
        label.pack(pady=5)
        
        label_qr = tk.Label(self, text="Input QR Code Content:", font=('Arial', 18))
        label_qr.pack(pady=(100,5))
        
        self.entry_qr = ttk.Entry(self,width=26,font=("Sitka Small",11),justify=tk.CENTER)
        self.entry_qr.pack(pady=(10,20))
        
        label_name = tk.Label(self, text="Input File Name:", font=('Arial', 18))
        label_name.pack(pady=(25,5))
        
        self.entry_name = ttk.Entry(self,width=26,font=("Sitka Small",11),justify=tk.CENTER)
        self.entry_name.pack(pady=(10,20))
        
        btn_1 = ttk.Button(self,text="Confirm",width=10, command=lambda: self.create_qr(parent))
        btn_1.pack(pady=0)
        
        btn_2 = ttk.Button(self,text="Go Back",width=10, command=lambda: self.show_page("Home"))
        btn_2.pack(pady=10)
        
    def create_qr(self,parent):
        content = self.entry_qr.get()
        name = self.entry_name.get()
        if content and name:
            qrcode = pyqrcode.create(content)
            if not os.path.exists("qr_list"):
                os.mkdir("qr_list")
            qrcode.png("qr_list/" + name + '.png', scale=10)
            self.clear_entry()
            messagebox.showinfo("Success",'QR Code Created!')
            self.next_page.load_list(parent)
            self.show_page("Home")
        else:
            messagebox.showwarning("Warning",'Entry Fields are Empty.')
            
    def clear_entry(self):
        self.entry_qr.delete(0, 'end')
        self.entry_name.delete(0, 'end')
            
class ViewPage(tk.Frame):
    def __init__(self, parent, show_page):
        super().__init__(parent)
        self.show_page = show_page
        
        frame_header = tk.Frame(self, bg="WHITE")
        frame_header.place(x=0, y=0, width=500, height=35)
        
        label = tk.Label(frame_header, text="QR Code Generator", font=('Arial', 18), bg="WHITE")
        label.pack(pady=5)
        
        self.label_name = tk.Label(self, font=('Arial', 18))
        self.label_name.pack(pady=(45,0))
    
        self.label_image = tk.Label(self)
        self.label_image.pack(pady=(10,20))
        
        btn_1 = ttk.Button(self,text="Save As",width=10, command=lambda: self.save_image())
        btn_1.pack()
        
        btn_2 = ttk.Button(self,text="Go Back",width=10, command=lambda: self.show_page("Home"))
        btn_2.pack(pady=10)
        
        self.img = None
    
    def set_image(self, path):
        img = ImageTk.PhotoImage(Image.open(path))
        self.label_image.config(image=img)
        self.label_image.image = img
        self.img = img
        self.label_name.config(text=os.path.basename(path))
        
    def save_image(self):
        img = Image.open("qr_list/" + self.label_name.cget("text"))
        path = filedialog.asksaveasfilename(defaultextension=".png",)
        if path:
            img.save(path)
            messagebox.showinfo("Sucess","QR Code is Saved ")
     
class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("QR Code Generator")
        self.geometry("500x600")
        self.resizable(0, 0)
        self.configure(bg="WHITE")
        
        self.container = tk.Frame(self, bg="WHITE", width=500, height=600)
        self.container.place(x=0, y=0)
        
        self.pages = {}
        self.current_page = None
        
        self.pages["View"] = ViewPage(self.container, self.show_page)
        self.pages["Home"] = HomePage(self.container, self.show_page, self.pages["View"])
        self.pages["Create"] = CreatePage(self.container, self.show_page, self.pages["Home"])
      
        self.show_page("Home")
        
    def show_page(self, name):
        if self.current_page is not None:
            self.current_page.place_forget()
        page = self.pages[name]
        page.place(width=500, height=600)
        self.current_page = page
        
app = GUI()
app.mainloop()
