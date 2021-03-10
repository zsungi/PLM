import json


class Project:
    def __init__(self, name, startTime, deadline, description, priority, budget):
        self.name = name
        self.startTime = startTime
        self.deadline = deadline
        self.description = description
        self.priority = priority
        self.budget = budget
        self.messages = []
        self.products = []
        self.roles = []

class Product:
    def __init__(self, name, reference, supplier, status = "Created"):
        self.name = name
        self.reference = reference
        self.supplier = supplier
        self.status = status
        self.documents = []
        self.messages = []

class Document:
    def __init__(self, name, filepath, lastModified):
        self.name = name
        self.file = filepath
        self.lastModified = lastModified

class User:
    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = password
        self.role = role


class Message:
    def __init__(self, sender, message, time):
        self.sender = sender
        self.message = message
        self.time = time


class Role:
    def __init__(self, user, role):
        self.user = user
        self.role = role


def add_user(user):
    data_set = {
        "name": user.name,
        "email": user.email,
        "password": user.password,
        "role": user.role
    }

    with open("app/Data/users.json", "r") as file:
        data = json.load(file)
        data["users"].append(data_set)

    with open("app/Data/users.json", "w") as file:
        json.dump(data, file)


def load_users():
    users = []
    with open("app/Data/users.json", "r") as file:
        data = json.load(file)
        for element in data["users"]:
            users.append(User(
                element["name"],
                element["email"],
                element["password"],
                element["role"]))
    return users

def create_product(product, project):
    data_set = {
        "name": product.name,
        "reference": product.reference,
        "supplier": product.supplier,
        "status": product.status,
        "documents": [],
        "messages": []
    }

    with open("app/Data/projects.json", "r") as file:
        data = json.load(file)
        for idx, p in enumerate(data["projects"]):
            if p["name"] == project.name:
                data["projects"][idx]["products"].append(data_set)

    with open("app/Data/projects.json", "w") as file:
        json.dump(data, file)

def create_document(document, product, project):
    data_set = {
        "name": document.name,
        "file": document.file,
        "last modified": document.lastModified
    }

    with open("app/Data/projects.json", "r") as file:
        data = json.load(file)
        for projidx, proj in enumerate(data["projects"]):
            if proj["name"] == project.name:
                for prodidx, prod in enumerate(data["projects"][projidx]["products"]):
                        if prod["reference"] == product.reference:
                            data["projects"][projidx]["products"][prodidx]["documents"].append(data_set)


    with open("app/Data/projects.json", "w") as file:
        json.dump(data, file)

def load_projects():
    projects = []
    with open("app/Data/projects.json", "r") as file:
        data = json.load(file)
        for element in data["projects"]:
            project = project.Project(
                element["name"],
                element["start time"],
                element["deadline"],
                element["description"],
                element["priority"],
                element["budget"],
            )
            for message in element["messages"]:
                project.messages.append(
                    Message(message["sender"], message["message"], message["time"]))
            for role in element["roles"]:
                project.roles.append(Role(role["user"], role["role"]))
            for product in element["products"]:
                temp = Product(product["name"], product["reference"], product["supplier"], product["status"])
                for document in product["documents"]:
                    temp.documents.append(Document(document["name"], document["file"], document["last modified"]))
                for message in product["messages"]:
                    temp.messages.append(Message(message["sender"], message["message"], message["time"]))
                project.products.append(temp)

            for role in element["roles"]:
                project.roles.append(Role(user["user"], role["role"]))
            projects.append(project)
    return projects

def load_project(projectname):
    with open("app/Data/projects.json", "r") as file:
        data = json.load(file)
        for element in data["projects"]:
            if element["name"] == projectname:
                project = Project(
                element["name"],
                element["start time"],
                element["deadline"],
                element["description"],
                element["priority"],
                element["budget"],
                )
                for message in element["messages"]:
                    project.messages.append(
                        Message(message["sender"], message["message"], message["time"]))
                for role in element["roles"]:
                    project.roles.append(Role(role["user"], role["role"]))
                for product in element["products"]:
                    temp = Product(product["name"], product["reference"], product["supplier"], product["status"])
                    for document in product["documents"]:
                        temp.documents.append(Document(document["name"], document["file"], document["last modified"]))
                    for message in product["messages"]:
                        temp.messages.append(Message(message["sender"], message["message"], message["time"]))
                    project.products.append(temp)
    return project

def load_projects_for_user(user):
    projects = []
    with open("app/Data/projects.json", "r") as file:
        data = json.load(file)
        for element in data["projects"]:
            access = False
            project = Project(
                element["name"],
                element["start time"],
                element["deadline"],
                element["description"],
                element["priority"],
                element["budget"],
            )
            for message in element["messages"]:
                project.messages.append(
                    Message(message["sender"], message["message"], message["time"]))
            for role in element["roles"]:
                project.roles.append(Role(role["user"], role["role"]))
                if role["user"] == user.name:
                    access = True
            for product in element["products"]:
                temp = Product(product["name"], product["reference"], product["supplier"], product["status"])
                for document in product["documents"]:
                    temp.documents.append(Document(document["name"], document["file"], document["last modified"]))
                for message in product["messages"]:
                    temp.messages.append(Message(message["sender"], message["message"], message["time"]))
                project.products.append(temp)
            if access:
                projects.append(project)
    return projects

def send_message(project, message, product = None):
    if product is None:
        data_set = {
            "sender": message.sender,
            "message": message.message,
            "time": message.time,
        }

        with open("app/Data/projects.json", "r") as file:
            data = json.load(file)
            for idx, p in enumerate(data["projects"]):
                if p["name"] == project.name:
                    data["projects"][idx]["messages"].append(data_set)

        with open("app/Data/projects.json", "w") as file:
            json.dump(data, file)
    if product is not None:
        data_set = {
            "sender": message.sender,
            "message": message.message,
            "time": message.time,
        }

        with open("app/Data/projects.json", "r") as file:
            data = json.load(file)
            for projidx, proj in enumerate(data["projects"]):
                if proj["name"] == project.name:
                    for prodidx, prod in enumerate(data["projects"][projidx]["products"]):
                        if prod["reference"] == product.reference:
                            data["projects"][projidx]["products"][prodidx]["messages"].append(data_set)

        with open("app/Data/projects.json", "w") as file:
            json.dump(data, file)

