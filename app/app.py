from tkinter import *
from tkinter import messagebox
import dataAccess
from datetime import datetime


class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("PLM")

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.user = None

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
        self.user = user
        frame = self.frames[Home]
        frame.update(user)
        frame.tkraise()

    def open_project(self, project):
        frame = self.frames[Project]
        frame.update(project, self.user)
        frame.tkraise()

#    def request_access(self, project):


class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label = Label(self, text="Welcome")
        label.pack(padx=10, pady=10)
        login_page = Button(self, text="Log In",
                            command=lambda: controller.show_frame(LogIn))
        login_page.pack()
        signup_page = Button(self, text="Sign Up",
                             command=lambda: controller.show_frame(SignUp))
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
        self.passwordTextField = Entry(self, show="*")

        self.emailTextField.grid(row=0, column=1)
        self.passwordTextField.grid(row=1, column=1)

        self.logInButton = Button(self, text='Log In', command=self.log_in)
        self.logInButton.grid(row=3)

        self.backButton = Button(
            self, text='Back', command=lambda: controller.show_frame(StartPage))
        self.backButton.grid(row=3, column=1)

    def log_in(self):
        users = dataAccess.load_users()
        currentUser = None

        for u in users:
            if u.email == self.emailTextField.get() and u.password == self.passwordTextField.get():
                currentUser = u

        if currentUser is not None:
            self.controller.log_in(currentUser)
        else:
            messagebox.showerror(
                "Wrong email or password", "We dont have account with this email or your password is wrong, please try again or sign up if You do not have an account yet!")


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
        self.passwordTextField = Entry(self, show="*")
        self.nameTextField = Entry(self)
        self.roleOptionMenu = OptionMenu(self, self.role, *options)

        self.nameTextField.grid(row=0, column=1)
        self.emailTextField.grid(row=1, column=1)
        self.passwordTextField.grid(row=2, column=1)
        self.roleOptionMenu.grid(row=3, column=1)

        self.logInButton = Button(self, text='Sign Up', command=self.sign_up)
        self.logInButton.grid(row=5)

        self.backButton = Button(
            self, text='Back', command=lambda: controller.show_frame(StartPage))
        self.backButton.grid(row=5, column=1)

    def email_is_available(self, email):
        available = True
        users = dataAccess.load_users()
        for user in users:
            if user.email == email:
                available = False
        return available

    def sign_up(self):
        if self.email_is_available(self.emailTextField.get()):
            currentUser = dataAccess.User(self.nameTextField.get(
            ), self.emailTextField.get(), self.passwordTextField.get(), self.role.get())
            dataAccess.add_user(currentUser)
            messagebox.showinfo(
                "Welcome", "You successfully signed up, Welcome")
            self.controller.log_in(currentUser)
        else:
            messagebox.showerror(
                "Error", "This email is not available, we have a user with this email.")


class Home(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.user = None
        self.controller = controller
        self.projects = []

        self.nameLabel = Label(self, text="")
        self.nameLabel.grid(row=0)
        Label(self, text="Available projects:").grid(row=1)

        self.logOutButton = Button(self, text='Log Out', command=self.log_out)
        self.logOutButton.grid(row=0, column=1)

        self.projectsList = Listbox(self)
        self.projectsList.grid(row=3)

        self.openProjectButton = Button(
            self, text='Open Project', command=self.open_project)
        self.openProjectButton.grid(row=4, column=0)
        self.requestAccessButton = Button(
            self, text='Request Access', command=self.request_access)

    def log_out(self):
        self.controller.show_frame(StartPage)

    def update(self, user):
        self.user = user
        self.projects = dataAccess.load_projects_for_user(user)
        project_names = self.get_project_names(user)
#        self.otherprojects = dataAccess.load_projects_for_user(user)
        self.nameLabel.config(text=user.name)
        self.projectsList.delete(0, 'end')
        self.projectsList.insert("end", *project_names)

    def get_project_names(self, user):
        names = []
        for project in self.projects:
            names.append(project.name)
        return names

    def open_project(self):
        selection = self.projectsList.curselection()
        if len(selection) == 1:
            self.controller.open_project(self.projects[selection[0]])
        else:
            messagebox.showerror("Error", "Select one project")

    def request_access(self):
        selection = self.projectsList.curselection()
        if len(selection) == 1:
            self.controller.request_access(self.projects[selection[0]])
        else:
            messagebox.showerror("Error", "Select one project")


class Project(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.project = None
        self.user = None
        self.controller = controller

        Label(self, text="Name of project: ").grid(row=0)
        Label(self, text="Start time: ").grid(row=1)
        Label(self, text="Deadline: ").grid(row=2)
        Label(self, text="Description: ").grid(row=3)
        Label(self, text="Priority: ").grid(row=4)
        Label(self, text="Budget: ").grid(row=5)
        Label(self, text="Messages: ").grid(row=6, columnspan=2)

        self.nameLabel = Label(self, text="")
        self.nameLabel.grid(row=0, column=1)
        self.startTimeLabel = Label(self, text="")
        self.startTimeLabel.grid(row=1, column=1)
        self.deadlineLabel = Label(self, text="")
        self.deadlineLabel.grid(row=2, column=1)
        self.descriptionLabel = Label(self, text="")
        self.descriptionLabel.grid(row=3, column=1)
        self.priorityLabel = Label(self, text="")
        self.priorityLabel.grid(row=4, column=1)
        self.budgetlabel = Label(self, text="")
        self.budgetlabel.grid(row=5, column=1)

        self.messageList = Listbox(self)
        self.messageList.grid(row=7, columnspan=2)

        self.messageEntry = Entry(self)
        self.messageEntry.insert(0, 'Message')
        self.messageEntry.grid(row=8, column=0)
        # Todo: make placeholder works
        self.messageEntry.bind(
            "<FocusIn>", self.messageEntry.delete("0", "end"))
        self.messageEntry.bind(
            "<FocusOut>", self.messageEntry.insert(0, "Message"))

        self.sendMessageButton = Button(
            self, text='Send', command=self.send_message)
        self.sendMessageButton.grid(row=8, column=1)

        self.editProjectButton = Button(
            self, text='Edit Project', command=self.edit_project)
        self.editProjectButton.grid(row=9, column=0)

        self.backButton = Button(
            self, text='Back', command=lambda: controller.show_frame(Home))
        self.backButton.grid(row=9, column=1)

    def edit_project(self):
        print("")

    def send_message(self):
        message = dataAccess.Message(
            self.user.name, self.messageEntry.get(), str(datetime.now()))
        dataAccess.send_message(self.project, message)
        self.project.messages.append(message)
        message_list = self.load_messages(self.project)
        self.messageList.delete(0, 'end')
        self.messageList.insert("end", *message_list)

    def load_messages(self, project):
        messages = []
        for message in project.messages:
            messages.append(message.sender + ": " + message.message)
        return messages

    def update(self, project, user):
        self.user = user
        self.project = project
        message_list = self.load_messages(project)
        self.messageList.delete(0, 'end')
        self.messageList.insert("end", *message_list)

        self.nameLabel.config(text=project.name)
        self.startTimeLabel.config(text=project.startTime)
        self.deadlineLabel.config(text=project.deadline)
        self.descriptionLabel.config(text=project.description)
        self.priorityLabel.config(text=project.priority)
        self.budgetlabel.config(text=project.budget)


app = App()
app.mainloop()
