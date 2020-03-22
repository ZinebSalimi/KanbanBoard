# KanbanBoard

# App functionalities 
- Sign up to create a profile
- Log in and out of their personalized board
- Add tasks as "to do", "doing" or "done". Tasks can be moved from one category to another in that order. They can then be deleted when "done"
- The user can see each task's title, description, date created and deadline

![Image of Kanban Board](kanban_picture.png)


# Running the application on your computer

**Install dependencies**

1. Install python3 and pip3

```
$ brew install python3
```

2. Install virutalenv
```
$ pip3 install virtualenv
```
OR 
```
$ python3 -m venv venv
```

4. Activate virtualenv
```
$ source venv/bin/activate
```

5. Install dependencies inside virtual environment
```
(venv) $ pip3 install -r requirements.txt
```

6. Deactivate virtual environment
```
$ deactivate
```

**Run the app**
1. Start the server by running
```
$ export FLASK_ENV=development
$ export FLASK_APP=web
$ python3 -m flask run
```

Go to "localhost:5000", you should see the login page to your kanban board. Hooray!


# Contributions

Thanks to Jason Liang, Juan Carlos CF, Ahmed Kamel and Danyal Naeem for their help on this assignment. The README.md from the CS162 habit team github also inspired the above README.md. 

