'''
======= CREATED BY PAUL MENDOZA =======
======= PYTHON 3.12.7 =======
'''


from tkinter import *
from tkinter import filedialog, simpledialog
from tkinter import messagebox
from PyPDF2 import PdfReader, PdfWriter
import os
import traceback




root = Tk()
root.title("PDF Protector by Falcon")
root.geometry("1000x650")
root.resizable(False, False)

def browse():
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title="Select a File",
                                          filetypes=(("PDF files", "*.pdf"),
                                                     ("all files", "*.*")))
    label1_entry.insert("end", filename)

def protect():
    mainfile = label1_entry.get()
    protectfile = target_entry.get()
    code = password_entry.get()
    
    if not mainfile or not protectfile or not code:
        messagebox.showerror("Error", "All fields are required")
        return
    if not mainfile.endswith(".pdf"):
        messagebox.showerror("Error", "Source file must be a .pdf file")
        return
    if not protectfile.endswith(".pdf"):
        messagebox.showerror("Error", "Target file must be a .pdf file")
        return
    
    
    else:
        try:
            pdf = PdfReader(filename)
            pdf_writer = PdfWriter()
            for page in pdf.pages:
                pdf_writer.add_page(page)
            
            #Password
            pdf_writer.encrypt(code)
            output_pdf = open(protectfile, "wb")
            pdf_writer.write(output_pdf)
            
            messagebox.showinfo("Success", "PDF file has been protected successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error in protecting PDF file{e};\n{traceback.format_exc()}")
            return  



def remove_password():
    window = Toplevel(root)
    window.title("Remove Password")
    window.geometry("810x300")
    window.resizable(False, False)
    window.configure(bg="#C9E7C1")
    
    def browse_w():
        global filename_w
        filename_w = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                title="Select a File",
                                                filetypes=(("PDF files", "*.pdf"),
                                                            ("all files", "*.*")))
        remove_label_entry.insert("end", filename_w)
    
    def forgot_pass():
        # Open a new window with instructions
        forgot_window = Toplevel(window)
        forgot_window.title("Forgot Password")
        forgot_window.geometry("800x200")
        forgot_window.resizable(False, False)
        forgot_window.configure(bg="#F9D5C9")
        
        message = """
        If you've forgotten the password for the PDF, you have a few options:
        1. Try to remember the password or check for backups.
        2. Use online PDF password recovery tools to unlock the PDF.
        3. Contact the document creator for the password.
        
        Please note: Some of these methods might not work depending on the encryption level.
        """
        
        try:
            image_icon1 = PhotoImage(file="images/icon.png")
            forgot_window.iconphoto(False, image_icon1)
        except Exception as e:
            messagebox.showerror("Error", f"Icon not found{e};\n{traceback.format_exc()}")
            forgot_window.destroy()
        
        label = Label(forgot_window, text=message, font=("Arial", 12), fg="black", bg="#F9D5C9", justify=LEFT)
        label.pack(padx=20, pady=20)
        
        close_btn = Button(forgot_window, text="Close", font=("Arial", 12), command=forgot_window.destroy)
        close_btn.pack(pady=10)
    
    def remove():
        mainfile = remove_label_entry.get()
        protectfile = remove_target_entry.get()

        if not mainfile or not protectfile:
            messagebox.showerror("Error", "All fields are required")
            return
        if not mainfile.endswith(".pdf"):
            messagebox.showerror("Error", "Source file must be a .pdf file")
            return
        if not protectfile.endswith(".pdf"):
            messagebox.showerror("Error", "Target file must be a .pdf file")
            return

        try:
            pdf1 = PdfReader(mainfile)

            # Check if the PDF is encrypted
            if pdf1.is_encrypted:
                # Ask the user for the password
                password = simpledialog.askstring("Password", "Enter the password for the protected PDF:", show='*')
                if password is None:  # User pressed cancel
                    return

                # Attempt to decrypt with the provided password
                decryption_status = pdf1.decrypt(password)
                if decryption_status == 0:  # Failed to decrypt
                    messagebox.showerror("Error", "Failed to decrypt the PDF. The password might be incorrect.")
                    return

            # Now write the pages to a new PDF
            pdf_writer1 = PdfWriter()
            for page in pdf1.pages:
                pdf_writer1.add_page(page)

            # Remove Password and save as new file
            with open(protectfile, "wb") as output_pdf:
                pdf_writer1.write(output_pdf)
            
            messagebox.showinfo("Success", "Password has been removed successfully")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error in removing password: {e};\n{traceback.format_exc()}")
            print(traceback.format_exc())
    
    
    try:
        image_icon1 = PhotoImage(file="images/icon.png")
        window.iconphoto(False, image_icon1)
    except Exception as e:
        messagebox.showerror("Error", f"Icon not found{e};\n{traceback.format_exc()}")
        window.destroy()
    remove_frame = Frame(window, width=980, height=300, bd=2, relief=GROOVE, bg="#F9D5C9", pady=20)
    remove_frame.pack()

    label2 = Label(remove_frame, text="Protected PDF File:", font=("Arial", 15), fg="black", bg="#F9D5C9")
    label2.place(x=10, y=10)
    remove_label_entry = Entry(remove_frame, font=("Arial", 15), width=50, bd=1)    
    remove_label_entry.place(x=200, y=10)
    
    select_btn_icon_w = PhotoImage(file="images/select_icon.png")
    select_btn_w = Button(remove_frame, image=select_btn_icon_w, width=30, height=23, command=browse_w)
    select_btn_w.place(x=760, y=10)

    remove_target = Label(remove_frame, text="Target PDF File:", font=("Arial", 15), fg="black", bg="#F9D5C9")
    remove_target.place(x=10, y=80)
    remove_target_entry = Entry(remove_frame, font=("Arial", 15), width=50, bd=1)
    remove_target_entry.place(x=200, y=80)

    btn_remove_icon = PhotoImage(file="images/remove_pass.png")
    remove_btn = Button(remove_frame, image=btn_remove_icon, width=300, height=50, bd=2,command=remove)
    remove_btn.place(x=300, y=150)
    
    forgot_password_btn = Button(remove_frame, text="Forgot Password?", font=("Arial", 12), command=forgot_pass)
    forgot_password_btn.place(x=350, y=220)
    
    
    window.mainloop()

try:
    image_icon = PhotoImage(file="images/icon.png")
    root.iconphoto(False, image_icon)
except Exception as e:
    messagebox.showerror("Error", f"Icon not found{e};\n{traceback.format_exc()}")
    root.destroy()
try:
    top_image = PhotoImage(file="images/images1.png")
    lbl = Label(root, image=top_image)
    lbl.pack()
except Exception as e:
    messagebox.showerror("Error", f"Image not found{e};\n{traceback.format_exc()}")
    root.destroy()

frame = Frame(root,width=980,height=440,bd=2,relief=GROOVE,bg="#C9E7C1",pady=20)
frame.pack()

label1 = Label(frame, text="Source PDF File:", font=("Arial", 15),fg="black",bg="#C9E7C1").place(x=10, y=10)
label1_entry = Entry(frame, font=("Arial", 15), width=50,bd=1)
label1_entry.place(x=200, y=10)

select_btn_icon = PhotoImage(file="images/select_icon.png")
select_btn = Button(frame, image=select_btn_icon, width=30, height=23,command=browse).place(x=760, y=10)

target = Label(frame, text="Target PDF File:", font=("Arial", 15),fg="black",bg="#C9E7C1").place(x=10, y=80)
target_entry = Entry(frame, font=("Arial", 15), width=50,bd=1)
target_entry.place(x=200, y=80)

password = Label(frame, text="Password:", font=("Arial", 15),fg="black",bg="#C9E7C1").place(x=10, y=150)
password_entry = Entry(frame, font=("Arial", 15), width=50,bd=1)
password_entry.place(x=200, y=150)

button_icon = PhotoImage(file="images/btn_image.png")
protect_btn = Button(frame,image=button_icon, width=300, height=50,bd=2,command=protect)
protect_btn.place(x=300, y=220)

remove_password_icon = PhotoImage(file="images/remove_password_image.png")
remove_password_btn = Button(frame,image=remove_password_icon, width=300, height=50, bd=2, command=remove_password)  
remove_password_btn.place(x=300, y=290)  





root.mainloop()
