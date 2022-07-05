# authentication
# login
# view for listing all todos
# view creating a new todo
# view for fetching specific todo
# list all todos created by authenticated user
# view for updating a specific todo
# view for deleting a specific todo
# logout

from todosapp.model import users,todos

def authenticate(**kwargs):
    username=kwargs.get("username")
    password=kwargs.get("password")
    user=[user for user in users if user["username"]==username and user["password"]==password][0]
    return user

def get_todo(id): #to retrieve todo of given todId
    todo=[todo for todo in todos if todo["todoId"]==id][0]
    return todo

def signin_required(fn):
    def wrapper(*args,**kwargs):
        if "user" in session:
            return fn(*args,**kwargs)
        else:
            print("you must login")
    return wrapper

session={}
class SignInView:
    def get(self,*args,**kwargs):
        username = kwargs.get("username")
        password = kwargs.get("password")
        user=authenticate(username=username,password=password)
        if user:
            session["user"]=user
            print("login successful")
            print(f"welcome {user['username']}")
        else:
            print("invalid credentials")

class TodosView:
    @signin_required
    def get(self,*args,**kwargs):  # view for listing all todos
        print(f"all todos: {todos}")

    @signin_required
    def post(self,*args,**kwargs):  # view creating a new todo
        userId=session["user"]["id"]
        kwargs["userId"]=userId
        todos.append(kwargs)
        print(todos)

class SpecificTodo:
    @signin_required
    def get(self,*args,**kwargs):  # view for fetching specific todo
        todoId=kwargs.get("todoId")
        todo=get_todo(todoId)
        print(f"todo with todoId {todoId} : {todo}")

class MyTodo:
    @signin_required
    def get(self,*args,**kwargs):  # list all todos created by authenticated user
        userId=session["user"]["id"]
        todo=[todo for todo in todos if todo["userId"]==userId]
        print(f"my todos : {todo}")

    @signin_required
    def put(self,*args,**kwargs):  # view for updating a specific todo
        todoId=kwargs.get("todoId")
        data=kwargs.get("data")
        todo=get_todo(todoId)
        if data:
            todo.update(data)
            print(f"updated todo : {todo}")

    @signin_required
    def delete(self,*args,**kwargs): # view for deleting a specific todo
        todoId=kwargs.get("todoId")
        todo=get_todo(todoId)
        todos.remove(todo)
        print(todos)

@signin_required
def signout():
    user=session.pop("user")
    print(f"{user['username']} logged out successfully")

login=SignInView()
login.get(username="akhil",password="Password@123")

tv=TodosView()
tv.get()
tv.post(todoId=9,task_name="new task",completed=False)

sp=SpecificTodo()
sp.get(todoId=7)

mt=MyTodo()
mt.get()
data={
"task_name": "updated task", "completed":True
}
mt.put(todoId=2,data=data)
mt.delete(todoId=8)

signout()
