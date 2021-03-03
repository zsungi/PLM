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
        self.roles = []

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

    with open("Data/users.json", "r") as file:
        data = json.load(file)
        data["users"].append(data_set)

    with open("Data/users.json", "w") as file:
        json.dump(data, file)

def load_users():
    users = []
    with open("Data/users.json", "r") as file:
        data = json.load(file)
        for element in data["users"]:
            users.append(User(
                element["name"],
                element["email"],
                element["password"],
                element["role"]))
    return users

def load_projects():
    projects = []
    with open("Data/projects.json", "r") as file:
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
                project.messages.append(Message(message["sender"], message["message"], message["time"]))
            for role in element["roles"]:
                project.roles.append(Role(user["user"], role["role"]))
            projects.append(project)
    return projects

def load_projects_for_user(user):
    projects = []
    with open("Data/projects.json", "r") as file:
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
                project.messages.append(Message(message["sender"], message["message"], message["time"]))
            for role in element["roles"]:
                project.roles.append(Role(role["user"], role["role"]))
                if role["user"] == user.name:
                    access = True
            if access:
                projects.append(project)
    return projects

def send_message(project, message):
    data_set = {
            "sender": message.sender,
            "message": message.message,
            "time": message.time,
        }

    with open("Data/projects.json", "r") as file:
        data = json.load(file)
        for idx, p in enumerate(data["projects"]):
            if p["name"] == project.name:
                data["projects"][idx]["messages"].append(data_set)

    with open("Data/projects.json", "w") as file:
        json.dump(data, file)
