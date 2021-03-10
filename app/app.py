from tkinter import *
from tkinter import messagebox
import dataAccess
from datetime import datetime


class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("PLM")
        
        currentUser = None

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, LogIn, SignUp, Home, Project, CreateProduct, Product):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

    def log_in(self):
        frame = self.frames[Home]
        frame.update()
        frame.tkraise()

    def open_project(self, project):
        frame = self.frames[Project]
        frame.update(project)
        frame.tkraise()

    def open_product(self, product, project):
        frame = self.frames[Product]
        frame.update(product, project)
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
        app.currentUser = None

        for u in users:
            if u.email == self.emailTextField.get() and u.password == self.passwordTextField.get():
                app.currentUser = u

        if app.currentUser is not None:
            self.controller.log_in()
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
            self.controller.log_in()
        else:
            messagebox.showerror(
                "Error", "This email is not available, we have a user with this email.")

class Home(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

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
        self.requestAccessButton.grid(row=4, column=1)

    def log_out(self):
        self.controller.show_frame(StartPage)

    def update(self):
        self.projects = dataAccess.load_projects_for_user(app.currentUser)
        project_names = self.get_project_names(app.currentUser)
        self.nameLabel.config(text=app.currentUser.name)
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
        print()
        #Todo:
        #-add new key to project jsons: request
        #-if you request add your request to this list
        #-add new key to project json: creator
        #if the creator log in show message dialog with the request to accept or deny            

class Project(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.project = None
        self.controller = controller
        self.product_list = []

        Label(self, text="Name of project: ").grid(row=0,  columnspan = 2)
        Label(self, text="Start time: ").grid(row=1,  columnspan = 2)
        Label(self, text="Deadline: ").grid(row=2,  columnspan = 2)
        Label(self, text="Description: ").grid(row=3,  columnspan = 2)
        Label(self, text="Priority: ").grid(row=4,  columnspan = 2)
        Label(self, text="Budget: ").grid(row=5,  columnspan = 2)
        Label(self, text="Messages: ").grid(row=7, columnspan=4)

        self.nameLabel = Label(self, text="")
        self.nameLabel.grid(row=0, column=2,  columnspan = 2)
        self.startTimeLabel = Label(self, text="")
        self.startTimeLabel.grid(row=1, column=2,  columnspan = 2)
        self.deadlineLabel = Label(self, text="")
        self.deadlineLabel.grid(row=2, column=2,  columnspan = 2)
        self.descriptionLabel = Label(self, text="")
        self.descriptionLabel.grid(row=3, column=2,  columnspan = 2)
        self.priorityLabel = Label(self, text="")
        self.priorityLabel.grid(row=4, column=2,  columnspan = 2)
        self.budgetlabel = Label(self, text="")
        self.budgetlabel.grid(row=5, column=2,  columnspan = 2)

        self.messageList = Listbox(self)
        self.messageList.grid(row=8, columnspan=4)

        self.messageEntry = Entry(self)
        self.messageEntry.insert(0, 'Message')
        self.messageEntry.grid(row=9, column=0, columnspan = 3)
        # Todo: make placeholder works
        self.messageEntry.bind(
            "<FocusIn>", self.messageEntry.delete("0", "end"))
        self.messageEntry.bind(
            "<FocusOut>", self.messageEntry.insert(0, "Message"))

        self.sendMessageButton = Button(
            self, text='Send', command=self.send_message)
        self.sendMessageButton.grid(row=9, column=3)

        self.editProjectButton = Button(
            self, text='Open product', command=self.open_product)
        self.editProjectButton.grid(row=12, column=0)

        Label(self, text="Products:").grid(row=10, columnspan=4)

        self.productList = Listbox(self)
        self.productList.grid(row=11, columnspan=4)

        self.editProjectButton = Button(
            self, text='Edit Project', command=self.edit_project)
        self.editProjectButton.grid(row=6, column=0,  columnspan = 4)

        self.backButton = Button(
            self, text='Back', command=lambda: controller.show_frame(Home))
        self.backButton.grid(row=12, column=3)

    def open_product(self):
        selection = self.productList.curselection()
        if len(selection) == 1:
            self.controller.open_product(self.project.products[selection[0]], self.project)
        else:
            messagebox.showerror("Error", "Select one product")

    def edit_project(self):
        print("")

    def send_message(self):
        message = dataAccess.Message(
            app.currentUser.name, self.messageEntry.get(), str(datetime.now()))
        dataAccess.send_message(self.project, message)
        self.project.messages.append(message)
        message_list = self.load_messages()
        self.messageList.delete(0, 'end')
        self.messageList.insert("end", *message_list)

    def load_messages(self):
        messages = []
        for message in self.project.messages:
            messages.append(message.sender + ": " + message.message)
        return messages

    def load_products(self):
        products = []
        for product in self.project.products:
            products.append(product.name + " - " + product.reference)
        return products

    def update(self, project):
        self.project = dataAccess.load_project(project.name)
        message_list = self.load_messages()
        self.messageList.delete(0, 'end')
        self.messageList.insert("end", *message_list)

        self.product_list = self.load_products()
        self.productList.delete(0, 'end')
        self.productList.insert("end", *self.product_list)

        self.nameLabel.config(text=project.name)
        self.startTimeLabel.config(text=project.startTime)
        self.deadlineLabel.config(text=project.deadline)
        self.descriptionLabel.config(text=project.description)
        self.priorityLabel.config(text=project.priority)
        self.budgetlabel.config(text=project.budget)

class CreateProduct(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        Label(self, text="Name of product: ").grid(row=0)
        Label(self, text="Reference: ").grid(row=1)
        Label(self, text="Supplier: ").grid(row=2)

        self.nameEntry = Entry(self, text="")
        self.nameEntry.grid(row=0, column=1)
        self.referenceEntry = Entry(self, text="")
        self.referenceEntry.grid(row=1, column=1)
        self.SupplierEntry = Entry(self, text="")
        self.SupplierEntry.grid(row=2, column=1)

        self.createProductButton = Button(
            self, text='Create product', command=self.create_product)
        self.createProductButton.grid(row=6, column=0)

    def create_product(self):
        product = dataAccess.Product(
            self.nameEntry.get(), self.referenceEntry.get(), self.SupplierEntry.get(), )
        dataAccess.send_message(self.project, message)
        self.project.messages.append(message)
        message_list = self.load_messages(self.project)
        self.messageList.delete(0, 'end')
        self.messageList.insert("end", *message_list)

class Product(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.project = None
        self.product = None
        self.document_list = []

        Label(self, text="Name of product: ").grid(row=0)
        Label(self, text="Reference: ").grid(row=1)
        Label(self, text="Supplier: ").grid(row=2)
        Label(self, text="Status: ").grid(row=3)
        Label(self, text="Documents: ").grid(row=4, columnspan=2)
        Label(self, text="Messages: ").grid(row=7, columnspan=2)


        self.nameLabel = Label(self, text="")
        self.nameLabel.grid(row=0, column=1)
        self.referenceLabel = Label(self, text="")
        self.referenceLabel.grid(row=1, column=1)
        self.supplierLabel = Label(self, text="")
        self.supplierLabel.grid(row=2, column=1)
        self.statusLabel = Label(self, text="")
        self.statusLabel.grid(row=3, column=1)

        self.documentList = Listbox(self)
        self.documentList.grid(row=5, columnspan=2)

        self.messageList = Listbox(self)
        self.messageList.grid(row=8, columnspan=2)

        self.addDocumentButton = Button(
            self, text='Add Document', command=self.add_document)
        self.addDocumentButton.grid(row=6, column=0)

        self.openDocumentButton = Button(
            self, text='Open Document', command=self.open_document)
        self.openDocumentButton.grid(row=6, column=1)

        self.messageEntry = Entry(self)
        self.messageEntry.insert(0, 'Message')
        self.messageEntry.grid(row=9, column=0)

        self.sendMessageButton = Button(
            self, text='Send', command=self.send_message)
        self.sendMessageButton.grid(row=9, column=1)

        self.backButton = Button(
            self, text='Back', command=lambda: controller.show_frame(Project))
        self.backButton.grid(row=12, column=3)

    def update(self, product, project):

        self.project = dataAccess.load_project(project.name)
        for prod in self.project.products:
            if prod.reference == product.reference:
                self.product = prod

        message_list = self.load_messages()
        self.messageList.delete(0, 'end')
        self.messageList.insert("end", *message_list)

        self.document_list = self.load_documents()
        self.documentList.delete(0, 'end')
        self.documentList.insert("end", *self.document_list)

        self.nameLabel.config(text=product.name)
        self.referenceLabel.config(text=product.reference)
        self.supplierLabel.config(text=product.supplier)
        self.statusLabel.config(text=product.status)

    def load_messages(self):
        messages = []
        for message in self.product.messages:
            messages.append(message.sender + ": " + message.message)
        return messages

    def load_documents(self):
        documents = []
        for document in self.product.documents:
            documents.append(document.name)
        return documents

    def open_document(self):
        print()

    def add_document(self):
        print()
    
    def send_message(self):
        message = dataAccess.Message(
            app.currentUser.name, self.messageEntry.get(), str(datetime.now()))
        dataAccess.send_message(self.project, message, self.product)
        self.product.messages.append(message)
        message_list = self.load_messages()
        self.messageList.delete(0, 'end')
        self.messageList.insert("end", *message_list)

    def change_status(self):
        print()



app = App()
app.mainloop()
