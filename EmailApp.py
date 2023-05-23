import pickle
import tkinter as tk
import tkinter.font as tkFont
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from Network import Network
from Enc_Dec import encrypt_file,decrypt_file
from EmailsWithMasterKeys import Emails
import re
class LoginWindow:
    def __init__(self, root):
        self.root = root
        root.title("Login")
        width = 600
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        ft = tkFont.Font(family="Times", size=12)
        label_Email = tk.Label(root)
        label_Email["font"] = ft
        label_Email["fg"] = "#333333"
        label_Email["text"] = "Email:"
        label_Email.place(x=70, y=50, width=70, height=25)
        label_Password = tk.Label(root)
        label_Password["font"] = ft
        label_Password["fg"] = "#333333"
        label_Password["text"] = "Password:"
        label_Password.place(x=70, y=120, width=70, height=25)
        self.entry_Email = tk.Entry(root)
        self.entry_Email["borderwidth"] = "1px"
        self.entry_Email["font"] = ft
        self.entry_Email["fg"] = "#333333"
        self.entry_Email.place(x=200, y=50, width=250, height=25)
        self.entry_Password = tk.Entry(root, show="*")
        self.entry_Password["borderwidth"] = "1px"
        self.entry_Password["font"] = ft
        self.entry_Password["fg"] = "#333333"
        self.entry_Password.place(x=200, y=120, width=250, height=25)
        button_Login = tk.Button(root)
        button_Login["bg"] = "#f0f0f0"
        button_Login["font"] = ft
        button_Login["fg"] = "#000000"
        button_Login["text"] = "Login"
        button_Login.place(x=280, y=210, width=80, height=25)
        button_Login["command"] = self.button_Login_command

    def button_Login_command(self):
        global sender
        sender = self.entry_Email.get()
        password = self.entry_Password.get()
        if self.verify_credentials(sender, password):
            self.root.destroy()
            compose_window = tk.Tk()
            app = App(compose_window, sender, password)
            compose_window.mainloop()
        else:
            print("Invalid credentials")

    def verify_credentials(self, sender, password):
        try:
            smtp_server = smtplib.SMTP("smtp-mail.outlook.com", port=587)
            smtp_server.starttls()
            smtp_server.login(sender, password)
            smtp_server.quit()
            return True
        except smtplib.SMTPAuthenticationError:
            return False


class App:
    def __init__(self, root, sender, password):
        self.sender = sender
        self.password = password
        self.tovar = ""

        root.title("Secure Mail Composer")
        width = 600
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        ft = tkFont.Font(family="Times", size=12)
        label_To = tk.Label(root)
        label_To["font"] = ft
        label_To["fg"] = "#333333"
        label_To["justify"] = "right"
        label_To["text"] = "To:"
        label_To.place(x=40, y=40, width=70, height=25)
        label_Subject = tk.Label(root)
        label_Subject["font"] = ft
        label_Subject["fg"] = "#333333"
        label_Subject["justify"] = "right"
        label_Subject["text"] = "Subject:"
        label_Subject.place(x=40, y=90, width=70, height=25)
        self.email_To = tk.Entry(root, textvariable=self.tovar)
        self.email_To["borderwidth"] = "1px"
        self.email_To["font"] = ft
        self.email_To["fg"] = "#333333"
        self.email_To["justify"] = "left"
        self.email_To["text"] = "To"
        self.email_To.place(x=120, y=40, width=420, height=30)
        self.email_Subject = tk.Entry(root)
        self.email_Subject["borderwidth"] = "1px"
        self.email_Subject["font"] = ft
        self.email_Subject["fg"] = "#333333"
        self.email_Subject["justify"] = "left"
        self.email_Subject["text"] = "Subject"
        self.email_Subject.place(x=120, y=90, width=417, height=30)
        self.email_Body = tk.Text(root)
        self.email_Body["borderwidth"] = "1px"
        self.email_Body["font"] = ft
        self.email_Body["fg"] = "#333333"
        self.email_Body.place(x=50, y=140, width=500, height=302)
        button_Send = tk.Button(root)
        button_Send["bg"] = "#f0f0f0"
        button_Send["font"] = ft
        button_Send["fg"] = "#000000"
        button_Send["justify"] = "center"
        button_Send["text"] = "Send"
        button_Send.place(x=470, y=460, width=70, height=25)
        button_Send["command"] = self.button_Send_command

    def send_email(self, subject, body, attach, recipients):
        global reply,sender
        print("replyyyy",reply[0])
        print(Emails[sender]['masterKey']," hahahah")
        with open('encryptedSKB.txt', 'wb') as outfile:
            outfile.write(reply[0])
        with open('encryptedSKA.txt', 'wb') as outfile:
            outfile.write(reply[1])
        decrypt_file(Emails[sender]['masterKey'],'encryptedSKA.txt','SessionKeyDecrypted.txt')
        print("line1")
        with open('SessionKeyDecrypted.txt', 'rb') as infile:
            SessionKey = infile.read()
            print(SessionKey,"lalalalala")
        with open('body.txt', 'wb') as outfile:
            outfile.write(body.encode())
            print("line4")
        encrypt_file(SessionKey,'body.txt','EncryptedMessageBody.txt')



        print("3amal send")
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = self.sender
        msg["To"] = recipients
        msg.attach(MIMEText("This is dummy email"))
        part = MIMEApplication(body, Name="EncryptedMessageBody.txt")
        part["Content-Disposition"] = 'attachment; filename=EncryptedMessageBody.txt'
        msg.attach(part)
        part = MIMEApplication(reply[0], Name="encryptedSKB.txt")
        part["Content-Disposition"] = 'attachment; filename=encryptedSKB.txt'
        msg.attach(part)
        smtp_server = smtplib.SMTP("smtp-mail.outlook.com", port=587)
        smtp_server.starttls()
        smtp_server.login(self.sender, self.password)
        smtp_server.sendmail(self.sender, recipients, msg.as_string())
        smtp_server.quit()

    def button_Send_command(self):
        global sender,reply
        n = Network()
        tovar = self.email_To.get()
        subject = self.email_Subject.get()
        body = self.email_Body.get("1.0", "end")
        print("tamaam")
        reply=n.send("("+sender+"("+tovar+"("+body)
        print("reply=",reply)
        # with open("in.txt", "w") as file:
        #     file.write(body)
        att = "Placeholder for the key"
        self.send_email(subject, body, att, tovar)


if __name__ == "__main__":

    root = tk.Tk()
    login_window = LoginWindow(root)
    root.mainloop()
