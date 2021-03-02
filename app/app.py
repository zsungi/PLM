from tkinter import *
import dataAccess
import message

class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("PLM")
        
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (StartPage, LogIn, SignUp, Home, Project):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame(StartPage)
        
    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

    def log_in(self, user):
        frame = self.frames[Home]
        frame.update(user)
        frame.tkraise()

class StartPage(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)

		label = Label(self, text="Welcome")
		label.pack(padx=10, pady=10)
		login_page = Button(self, text="Log In", command=lambda:controller.show_frame(LogIn))
		login_page.pack()
		signup_page = Button(self, text="Sign Up", command=lambda:controller.show_frame(SignUp))
		signup_page.pack()

class LogIn(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        
        emailLabel = Label(self, text="Email: ")
        emailLabel.grid(row=0)
        passwordLabel = Label(self, text="Password: ")
        passwordLabel.grid(row=1)

        self.emailTextField = Entry(self)
        self.passwordTextField = Entry(self)

        self.emailTextField.grid(row=0, column=1)
        self.passwordTextField.grid(row=1, column=1)

        self.logInButton = Button(self, text = 'Log In', command = self.log_in)
        self.logInButton.grid(row = 3)

        self.backButton = Button(self, text = 'Back', command=lambda:controller.show_frame(StartPage))
        self.backButton.grid(row = 3, column=1)

    def log_in(self):
        users = dataAccess.load_users()
        correntUser = None

        for u in users:
            if u.email == self.emailTextField.get() and u.password == self.passwordTextField.get():
                currentUser = u

        if currentUser is not None:
            print(currentUser.name)
            self.controller.log_in(currentUser)
        else:
            self.newWindow = Toplevel(self.master)
            message.MessageAlert(self.newWindow, "Wrong email or password")

class SignUp(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        options = {"Client", "Designer", "Customer Service", "Manufacturing"}

        self.role = StringVar(self.master)
        self.role.set("Client")

        self.nameLabel = Label(self, text="Name: ").grid(row=0)
        self.emailLabel = Label(self, text="Email: ").grid(row=1)
        self.passwordLabel = Label(self, text="Password: ").grid(row=2)
        self.roleLabel = Label(self, text="Role: ").grid(row=3)

        self.emailTextField = Entry(self)
        self.passwordTextField = Entry(self)
        self.nameTextField = Entry(self)
        self.roleOptionMenu = OptionMenu(self, self.role, *options)

        self.nameTextField.grid(row = 0, column = 1)
        self.emailTextField.grid(row=1, column=1)
        self.passwordTextField.grid(row=2, column=1)
        self.roleOptionMenu.grid(row=3, column=1)

        self.logInButton = Button(self, text = 'Sign Up', command = self.sign_up)
        self.logInButton.grid(row = 5)

        self.backButton = Button(self, text = 'Back', command=lambda:controller.show_frame(StartPage))
        self.backButton.grid(row = 5, column=1)

    def email_is_available(self, email):
        available = True
        users = dataAccess.load_users()
        for user in users:
            if user.email == email:
                available = False
        return available

    def sign_up(self):
        if self.email_is_available(self.emailTextField.get()):
            currentUser = dataAccess.User(self.nameTextField.get(), self.emailTextField.get(), self.passwordTextField.get(), self.role.get())
            dataAccess.add_user(currentUser)
            self.newWindow = Toplevel(self.master)
            self.app = message.MessageAlert(self.newWindow, "You successfully signed up, Welcome")
            self.controller.log_in(currentUser)
        else:
            self.newWindow = Toplevel(self.master)
            self.app = message.MessageAlert(self.newWindow, "This email is not available, we have a user with this email.")

class Home(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.user = None
        self.controller = controller

        self.nameLabel = Label(self, text="")
        self.nameLabel.grid(row=0)
        Label(self, text = "Available projects:").grid(row=1)

        self.logOutButton = Button(self, text= 'Log Out', command = self.log_out)
        self.logOutButton.grid(row=0, column=1)

        self.projectsList = Listbox(self)
        self.projectsList.grid(row=3)

        self.openProjectButton = Button(self, text = 'Open Project', command = self.open_project)
        self.openProjectButton.grid(row = 4, column = 0)

        self.editProjectButton = Button(self, text = 'Edit Project', command = self.open_project)
        self.editProjectButton.grid(row = 4, column = 1)
        
    def log_out(self):
        self.controller.show_frame(StartPage)

    def update(self, user):
        self.user = user
        project_names = self.get_project_names(user)
        self.nameLabel.config(text=user.name)
        self.projectsList.delete(0,'end')
        self.projectsList.insert("end", *project_names)

    def get_project_names(self, user):
        projects = dataAccess.load_projects_for_user(user)
        names = []
        for project in projects:
            names.append(project.name)
        return names

    def open_project(self):
        selection=self.projectsList.curselection()[0]
        

class Project(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)




app = App()
app.mainloop()