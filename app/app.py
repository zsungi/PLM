from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import dataAccess
from datetime import datetime
import uuid


class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("PLM")
        
        currentUser = None
        currentProject = None
        currentProduct = None

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, LogIn, SignUp, Home, Project, CreateProject, AddRole, CreateProduct, Product, AddDocument, EditProduct):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

    def open(self, frame):
        frame = self.frames[frame]
        frame.update()
        frame.tkraise()

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
            self.emailTextField.insert(0, '')
            self.passwordTextField.insert(0, '')
            self.controller.open(Home)
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
            app.currentUser = dataAccess.User(str(uuid.uuid1()), self.nameTextField.get(
            ), self.emailTextField.get(), self.passwordTextField.get(), self.role.get())
            dataAccess.add_user(app.currentUser)
            messagebox.showinfo(
                "Welcome", "You successfully signed up, Welcome")
            self.nameTextField.insert(0, '')
            self.emailTextField.insert(0, '')
            self.passwordTextField.insert(0, '')
            self.role.set("Client")
            self.controller.open(Home)
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
        self.requestAccessButton.grid(row=4, column=2)

        self.createProject = Button(
            self, text='Create Project', command=lambda: controller.show_frame(CreateProject))
        self.createProject.grid(row=4, column=1)

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
            app.currentProject = self.projects[selection[0]]
            self.controller.open(Project)
        else:
            messagebox.showerror("Error", "Select one project")

    def create_project(self):
        self.controlle.open(CreateProject)

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
        Label(self, text="Creator: ").grid(row=5,  columnspan = 2)
        Label(self, text="Budget: ").grid(row=6,  columnspan = 2)
        Label(self, text="Messages: ").grid(row=8, columnspan=4)

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
        self.creatorLabel = Label(self, text="")
        self.creatorLabel.grid(row=5, column=2,  columnspan = 2)
        self.budgetlabel = Label(self, text="")
        self.budgetlabel.grid(row=6, column=2,  columnspan = 2)

        self.messageList = Listbox(self)
        self.messageList.grid(row=9, columnspan=4)

        self.messageEntry = Entry(self)
        self.messageEntry.insert(0, 'Message')
        self.messageEntry.grid(row=10, column=0, columnspan = 3)
        # Todo: make placeholder works
        self.messageEntry.bind(
            "<FocusIn>", self.messageEntry.delete("0", "end"))
        self.messageEntry.bind(
            "<FocusOut>", self.messageEntry.insert(0, "Message"))

        self.sendMessageButton = Button(
            self, text='Send', command=self.send_message)
        self.sendMessageButton.grid(row=10, column=3)

        self.openProductButton = Button(
            self, text='Open product', command=self.open_product)
        self.openProductButton.grid(row=13, column=0)

        self.createProductButton = Button(
            self, text='Create new product', command=lambda: controller.show_frame(CreateProduct))
        self.createProductButton.grid(row=13, column=1)

        Label(self, text="Products:").grid(row=11, columnspan=4)

        self.productList = Listbox(self)
        self.productList.grid(row=12, columnspan=4)

        self.editProjectButton = Button(
            self, text='Edit Project', command=self.edit_project)
        self.editProjectButton.grid(row=7, column=0,  columnspan = 2)

        self.addRoleButton = Button(
            self, text='Add Role', command=lambda: controller.show_frame(AddRole))
        self.addRoleButton.grid(row=7, column=2,  columnspan = 2)

        self.backButton = Button(
            self, text='Back', command=lambda: controller.show_frame(Home))
        self.backButton.grid(row=13, column=3)

    def open_product(self):
        selection = self.productList.curselection()
        if len(selection) == 1:
            app.currentProduct = self.project.products[selection[0]]
            self.controller.open(Product)
        else:
            messagebox.showerror("Error", "Select one product")

    def edit_project(self):
        print("")

    def send_message(self):
        message = dataAccess.Message(str(uuid.uuid1()), app.currentUser.name, self.messageEntry.get(), str(datetime.now()))
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

    def update(self):
        self.project = dataAccess.load_project(app.currentProject)
        message_list = self.load_messages()
        self.messageList.delete(0, 'end')
        self.messageList.insert("end", *message_list)

        self.product_list = self.load_products()
        self.productList.delete(0, 'end')
        self.productList.insert("end", *self.product_list)

        self.nameLabel.config(text=app.currentProject.name)
        self.startTimeLabel.config(text=app.currentProject.startTime)
        self.deadlineLabel.config(text=app.currentProject.deadline)
        self.descriptionLabel.config(text=app.currentProject.description)
        self.priorityLabel.config(text=app.currentProject.priority)
        self.creatorLabel.config(text=app.currentProject.creator.name)
        self.budgetlabel.config(text=app.currentProject.budget)

class CreateProject(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller

        Label(self, text="Name of project: ").grid(row=0)
        Label(self, text="Start time: ").grid(row=1)
        Label(self, text="Deadline: ").grid(row=2,)
        Label(self, text="Description: ").grid(row=3)
        Label(self, text="Priority: ").grid(row=4)
        Label(self, text="Budget: ").grid(row=5)

        self.nameEntry = Entry(self, text="")
        self.nameEntry.grid(row=0, column=1)
        self.startTimeEntry = Entry(self, text="")
        self.startTimeEntry.grid(row=1, column=1)
        self.deadlineEntry = Entry(self, text="")
        self.deadlineEntry.grid(row=2, column=1)
        self.descriptionEntry = Entry(self, text="")
        self.descriptionEntry.grid(row=3, column=1)
        self.priorityEntry = Entry(self, text="")
        self.priorityEntry.grid(row=4, column=1)
        self.budgetEntry = Entry(self, text="")
        self.budgetEntry.grid(row=5, column=1)

        self.createProjectButton = Button(
            self, text='Create Project', command=self.create_project)
        self.createProjectButton.grid(row=6, column=0)

        self.backButton = Button(
            self, text='Back', command=self.open_home)
        self.backButton.grid(row=6, column=1)

    def open_home(self):
        self.controller.open(Home)

    def create_project(self):
        project = dataAccess.Project(
            str(uuid.uuid1()),
            self.nameEntry.get(),
            self.startTimeEntry.get(),
            self.deadlineEntry.get(),
            self.descriptionEntry.get(),
            self.priorityEntry.get(),
            self.budgetEntry.get(),
            app.currentUser)
        dataAccess.create_project(project)
        dataAccess.add_role_to_project(dataAccess.Role(app.currentUser.id, app.currentUser.role), project)
        self.nameEntry.insert(0, '')
        self.startTimeEntry.insert(0, '')
        self.deadlineEntry.insert(0, '')
        self.descriptionEntry.insert(0, '')
        self.priorityEntry.insert(0, '')
        self.budgetEntry.insert(0, '')
        self.controller.open(Home)

class AddRole(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller

        options = {"Client", "Designer", "Customer Service", "Manufacturing"}

        self.role = StringVar(self.master)
        self.role.set("Client")

        Label(self, text="Email of the user: ").grid(row=0)
        Label(self, text="Role: ").grid(row=1)

        self.emailEntry = Entry(self, text="")
        self.emailEntry.grid(row=0, column=1)
        self.roleOptionMenu = OptionMenu(self, self.role, *options)
        self.roleOptionMenu.grid(row=1, column=1)

        self.createProductButton = Button(
            self, text='Add Role', command=self.add_role)
        self.createProductButton.grid(row=6, column=0)

        self.backButton = Button(
            self, text='Back', command=lambda: controller.show_frame(Project))
        self.backButton.grid(row=6, column=1)

    def add_role(self):
        users = dataAccess.load_users()
        done = False
        for user in users:
            if user.email == self.emailEntry.get():
                done = True
                role = dataAccess.Role(user.id, self.role.get())
                dataAccess.add_role_to_project(role, app.currentProject)
                self.emailEntry.insert(0, '')
                self.role.set("Client")
                messagebox.showinfo(
                        "Done", "You successfully added " + user.name + " as a " + self.role.get())
                self.controller.open(Project)
        if done is False:
            messagebox.showerror(
                        "Error", "There is no user with this email address: " + self.emailEntry.get())

class CreateProduct(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller

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

        self.backButton = Button(
            self, text='Back', command=lambda: controller.show_frame(Project))
        self.backButton.grid(row=6, column=1)

    def create_product(self):
        product = dataAccess.Product(
            str(uuid.uuid1()), self.nameEntry.get(), self.referenceEntry.get(), self.SupplierEntry.get())
        dataAccess.create_product(product, app.currentProject)
        self.nameEntry.insert(0, '')
        self.referenceEntry.insert(0, '')
        self.SupplierEntry.insert(0, '')
        self.controller.open(Project)

class Product(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.project = None
        self.product = None
        self.document_list = []
        self.controller = controller

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

        self.editProduct = Button(
            self, text='Edit Product', command=self.edit_product)
        self.editProduct.grid(row=3, column=2)

        self.documentList = Listbox(self)
        self.documentList.grid(row=5, columnspan=2)

        self.messageList = Listbox(self)
        self.messageList.grid(row=8, columnspan=2)

        self.addDocumentButton = Button(
            self, text='Add Document', command=lambda: controller.show_frame(AddDocument))
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

    def update(self):
        self.project = dataAccess.load_project(app.currentProject)
        for prod in self.project.products:
            if prod.reference == app.currentProduct.reference:
                self.product = prod

        message_list = self.load_messages()
        self.messageList.delete(0, 'end')
        self.messageList.insert("end", *message_list)
        self.messageEntry.delete(0, 'end')
        self.messageEntry.insert(0, 'Message')

        self.document_list = self.load_documents()
        self.documentList.delete(0, 'end')
        self.documentList.insert("end", *self.document_list)

        self.nameLabel.config(text=app.currentProduct.name)
        self.referenceLabel.config(text=app.currentProduct.reference)
        self.supplierLabel.config(text=app.currentProduct.supplier)
        self.statusLabel.config(text=app.currentProduct.status)

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

    def edit_product(self):
        self.controller.open(EditProduct)

    def open_document(self):
        print()
    
    def send_message(self):
        message = dataAccess.Message(
            str(uuid.uuid1()), app.currentUser.name, self.messageEntry.get(), str(datetime.now()))
        dataAccess.send_message(self.project, message, self.product)
        self.product.messages.append(message)
        message_list = self.load_messages()
        self.messageList.delete(0, 'end')
        self.messageList.insert("end", *message_list)

    def change_status(self):
        print()

class AddDocument(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller
        self.filepath = ""

        Label(self, text="Name of document: ").grid(row=0)
        self.nameEntry = Entry(self, text="")
        self.nameEntry.grid(row=0, column=1, columnspan = 2)

        Label(self, text="Selected file: ").grid(row=1)
        self.pathLabel = Label(self, text="")
        self.pathLabel.grid(row=1, column = 1, columnspan = 2)

        self.addDocumentButton = Button(
            self, text='Add Document', command=self.add_document)
        self.addDocumentButton.grid(row=2, column=1)

        self.browseButton = Button(
            self, text='Browse a file', command=self.browse)
        self.browseButton.grid(row=2, column=0)

        self.backButton = Button(
            self, text='Back', command=lambda: controller.show_frame(Product))
        self.backButton.grid(row=2, column=2)

    def browse(self):
        self.filepath = filedialog.askopenfilename(initialdir = "/", title = "Select a File")
        self.pathLabel.config(text=self.filepath)

    def add_document(self):
        if self.filepath != "" and self.nameEntry.get() != "":
            document = dataAccess.Document(str(uuid.uuid1()), self.nameEntry.get(), self.filepath, str(datetime.now()))
            dataAccess.create_document(document, app.currentProduct, app.currentProject)
            self.controller.open(Product)
        if self.filepath == "" and self.nameEntry.get() != "":
            messagebox.showerror("Error", "Please select a file!")
        if self.filepath != "" and self.nameEntry.get() == "":
            messagebox.showerror("Error", "Please give a name to the Document!")
        if self.filepath == "" and self.nameEntry.get() == "":
            messagebox.showerror("Error", "Please give a name to the Document, and select a file!")
            
class EditProduct(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller
        self.status = StringVar(self.master)
        options = {"Created", "Concept", "Planning", "Development", "Qualification", "Launch"}

        Label(self, text="Name of product: ").grid(row=0)
        Label(self, text="Reference: ").grid(row=1)
        Label(self, text="Supplier: ").grid(row=2)
        Label(self, text="Status: ").grid(row=3)

        self.nameEntry = Entry(self, text="")
        self.nameEntry.grid(row=0, column=1)
        self.referenceEntry = Entry(self, text="")
        self.referenceEntry.grid(row=1, column=1)
        self.SupplierEntry = Entry(self, text="")
        self.SupplierEntry.grid(row=2, column=1)
        self.statusOptionMenu = OptionMenu(self, self.status, *options)
        self.statusOptionMenu.grid(row=3, column=1)

        self.createProductButton = Button(
            self, text='Edit product', command=self.edit_product)
        self.createProductButton.grid(row=6, column=0)

        self.backButton = Button(
            self, text='Back', command=lambda: controller.show_frame(Project))
        self.backButton.grid(row=6, column=1)

    def edit_product(self):
        product = dataAccess.Product(
            app.currentProduct.id, self.nameEntry.get(), self.referenceEntry.get(), self.SupplierEntry.get(), self.status.get())
        dataAccess.edit_product(product, app.currentProject)
        self.controller.open(Project)

    def update(self):
        self.status = app.currentProduct.status
        self.nameEntry.insert(0, app.currentProduct.name)
        self.referenceEntry.insert(0, app.currentProduct.reference)
        self.SupplierEntry.insert(0, app.currentProduct.supplier)



app = App()
app.mainloop()
