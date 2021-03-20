import json
import os


class Project:
    def __init__(self, ident, name, startTime, deadline, description, priority, budget, creator):
        self.id = ident
        self.name = name
        self.startTime = startTime
        self.deadline = deadline
        self.description = description
        self.priority = priority
        self.budget = budget
        self.creator = creator
        self.messages = []
        self.products = []
        self.roles = []


class Product:
    def __init__(self, ident, name, reference, supplier, status="Created"):
        self.id = ident
        self.name = name
        self.reference = reference
        self.supplier = supplier
        self.status = status
        self.documents = []
        self.messages = []


class Document:
    def __init__(self, ident, name, filepath, filetype, lastModified):
        self.type = filetype
        self.id = ident
        self.name = name
        self.file = filepath
        self.lastModified = lastModified


class User:
    def __init__(self, ident, name, email, password, role):
        self.id = ident
        self.name = name
        self.email = email
        self.password = password
        self.role = role


class Message:
    def __init__(self, ident, sender, message, time):
        self.id = ident
        self.sender = sender
        self.message = message
        self.time = time


class Role:
    def __init__(self, userid, name, role):
        self.userid = userid
        self.name = name
        self.role = role


def add_user(user):
    data_set = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "password": user.password,
        "role": user.role
    }

    with open(os.getcwd() + "/Data/users.json", "r") as file:
        data = json.load(file)
        data["users"].append(data_set)

    with open(os.getcwd() + "/Data/users.json", "w") as file:
        json.dump(data, file)


def load_users():
    users = []
    with open(os.getcwd() + "/Data/users.json", "r") as file:
        data = json.load(file)
        for element in data["users"]:
            users.append(User(
                element["id"],
                element["name"],
                element["email"],
                element["password"],
                element["role"]))
    return users


def create_project(project):
    data_set = {
        "id": project.id,
        "name": project.name,
        "start time": project.startTime,
        "deadline": project.deadline,
        "description": project.description,
        "priority": project.priority,
        "creator": {
            "id": project.creator.id,
            "name": project.creator.name,
            "email": project.creator.email,
            "password": project.creator.password,
            "role": project.creator.role
        },
        "budget": project.budget,
        "messages": [],
        "products": [],
        "roles": []
    }

    with open(os.getcwd() + "/Data/projects.json", "r") as file:
        data = json.load(file)
        data["projects"].append(data_set)

    with open(os.getcwd() + "/Data/projects.json", "w") as file:
        json.dump(data, file)


def add_role_to_project(role, project):
    data_set = {
        "userid": role.userid,
        "name": role.name,
        "role": role.role
    }
    with open(os.getcwd() + "/Data/projects.json", "r") as file:
        data = json.load(file)
        for idx, p in enumerate(data["projects"]):
            if p["id"] == project.id:
                data["projects"][idx]["roles"].append(data_set)

    with open(os.getcwd() + "/Data/projects.json", "w") as file:
        json.dump(data, file)


def create_product(product, project):
    data_set = {
        "id": product.id,
        "name": product.name,
        "reference": product.reference,
        "supplier": product.supplier,
        "status": product.status,
        "documents": [],
        "messages": []
    }

    with open(os.getcwd() + "/Data/projects.json", "r") as file:
        data = json.load(file)
        for idx, p in enumerate(data["projects"]):
            if p["id"] == project.id:
                data["projects"][idx]["products"].append(data_set)

    with open(os.getcwd() + "/Data/projects.json", "w") as file:
        json.dump(data, file)


def edit_product(product, project):
    with open(os.getcwd() + "/Data/projects.json", "r") as file:
        data = json.load(file)
        for projidx, proj in enumerate(data["projects"]):
            if proj["id"] == project.id:
                for prodidx, prod in enumerate(data["projects"][projidx]["products"]):
                    if prod["id"] == product.id:
                        data["projects"][projidx]["products"][prodidx]["name"] = product.name
                        data["projects"][projidx]["products"][prodidx]["reference"] = product.reference
                        data["projects"][projidx]["products"][prodidx]["supplier"] = product.supplier
                        data["projects"][projidx]["products"][prodidx]["status"] = product.status

    with open(os.getcwd() + "/Data/projects.json", "w") as file:
        json.dump(data, file)


def edit_project(project):
    with open(os.getcwd() + "/Data/projects.json", "r") as file:
        data = json.load(file)
        for projidx, proj in enumerate(data["projects"]):
            if proj["id"] == project.id:
                data["projects"][projidx]["name"] = project.name
                data["projects"][projidx]["start time"] = project.startTime
                data["projects"][projidx]["description"] = project.description
                data["projects"][projidx]["priority"] = project.priority
                data["projects"][projidx]["deadline"] = project.deadline
                data["projects"][projidx]["budget"] = project.budget

    with open(os.getcwd() + "/Data/projects.json", "w") as file:
        json.dump(data, file)


def create_document(document, product, project):
    data_set = {
        "id": document.id,
        "name": document.name,
        "file": document.file,
        "type": document.type,
        "last modified": document.lastModified
    }

    with open(os.getcwd() + "/Data/projects.json", "r") as file:
        data = json.load(file)
        for projidx, proj in enumerate(data["projects"]):
            if proj["id"] == project.id:
                for prodidx, prod in enumerate(data["projects"][projidx]["products"]):
                    if prod["id"] == product.id:
                        data["projects"][projidx]["products"][prodidx]["documents"].append(
                            data_set)

    with open(os.getcwd() + "/Data/projects.json", "w") as file:
        json.dump(data, file)


def load_projects():
    projects = []
    with open(os.getcwd() + "/Data/projects.json", "r") as file:
        data = json.load(file)
        for element in data["projects"]:
            creator = User(
                element["creator"]["id"],
                element["creator"]["name"],
                element["creator"]["email"],
                element["creator"]["password"],
                element["creator"]["role"])
            project = Project(
                element["id"],
                element["name"],
                element["start time"],
                element["deadline"],
                element["description"],
                element["priority"],
                element["budget"],
                creator
            )
            for message in element["messages"]:
                project.messages.append(
                    Message(message["id"], message["sender"], message["message"], message["time"]))
            for role in element["roles"]:
                project.roles.append(
                    Role(role["userid"], role["name"], role["role"]))
            for product in element["products"]:
                temp = Product(product["id"], product["name"],
                               product["reference"], product["supplier"], product["status"])
                for document in product["documents"]:
                    temp.documents.append(Document(
                        document["id"], document["name"], document["file"], document["type"], document["last modified"]))
                for message in product["messages"]:
                    temp.messages.append(
                        Message(message["id"], message["sender"], message["message"], message["time"]))
                project.products.append(temp)
            projects.append(project)
    return projects


def load_project(project):
    with open(os.getcwd() + "/Data/projects.json", "r") as file:
        data = json.load(file)
        for element in data["projects"]:
            if element["id"] == project.id:
                creator = User(
                    element["creator"]["id"],
                    element["creator"]["name"],
                    element["creator"]["email"],
                    element["creator"]["password"],
                    element["creator"]["role"])
                project = Project(
                    element["id"],
                    element["name"],
                    element["start time"],
                    element["deadline"],
                    element["description"],
                    element["priority"],
                    element["budget"],
                    creator
                )
                for message in element["messages"]:
                    project.messages.append(
                        Message(message["id"], message["sender"], message["message"], message["time"]))
                for role in element["roles"]:
                    project.roles.append(
                        Role(role["userid"], role["name"], role["role"]))
                for product in element["products"]:
                    temp = Product(
                        product["id"], product["name"], product["reference"], product["supplier"], product["status"])
                    for document in product["documents"]:
                        temp.documents.append(Document(
                            document["id"], document["name"], document["file"], document["type"], document["last modified"]))
                    for message in product["messages"]:
                        temp.messages.append(
                            Message(message["id"], message["sender"], message["message"], message["time"]))
                    project.products.append(temp)
    return project


def load_projects_for_user(user):
    projects = []
    with open(os.getcwd() + "/Data/projects.json", "r") as file:
        data = json.load(file)
        for element in data["projects"]:
            access = False
            creator = User(
                element["creator"]["id"],
                element["creator"]["name"],
                element["creator"]["email"],
                element["creator"]["password"],
                element["creator"]["role"])
            project = Project(
                element["id"],
                element["name"],
                element["start time"],
                element["deadline"],
                element["description"],
                element["priority"],
                element["budget"],
                creator
            )
            for message in element["messages"]:
                project.messages.append(
                    Message(message["id"], message["sender"], message["message"], message["time"]))
            for role in element["roles"]:
                project.roles.append(
                    Role(role["userid"], role["name"], role["role"]))
                if role["userid"] == user.id:
                    access = True
            for product in element["products"]:
                temp = Product(product["id"], product["name"],
                               product["reference"], product["supplier"], product["status"])
                for document in product["documents"]:
                    temp.documents.append(Document(
                        document["id"], document["name"], document["file"], document["type"], document["last modified"]))
                for message in product["messages"]:
                    temp.messages.append(
                        Message(message["id"], message["sender"], message["message"], message["time"]))
                project.products.append(temp)
            if access:
                projects.append(project)
    return projects


def send_message(project, message, product=None):
    if product is None:
        data_set = {
            "id": message.id,
            "sender": message.sender,
            "message": message.message,
            "time": message.time,
        }

        with open(os.getcwd() + "/Data/projects.json", "r") as file:
            data = json.load(file)
            for idx, p in enumerate(data["projects"]):
                if p["id"] == project.id:
                    data["projects"][idx]["messages"].append(data_set)

        with open(os.getcwd() + "/Data/projects.json", "w") as file:
            json.dump(data, file)
    if product is not None:
        data_set = {
            "id": message.id,
            "sender": message.sender,
            "message": message.message,
            "time": message.time,
        }

        with open(os.getcwd() + "/Data/projects.json", "r") as file:
            data = json.load(file)
            for projidx, proj in enumerate(data["projects"]):
                if proj["id"] == project.id:
                    for prodidx, prod in enumerate(data["projects"][projidx]["products"]):
                        if prod["id"] == product.id:
                            data["projects"][projidx]["products"][prodidx]["messages"].append(
                                data_set)

        with open(os.getcwd() + "/Data/projects.json", "w") as file:
            json.dump(data, file)
