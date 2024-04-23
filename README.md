# Project Name : PopularityPoll

## About
PopularityPoll is a website developed as the final project in April 2024 for Harvard's CS50x: Introduction to Computer Science Course where users can see the popularity of items in each topic and vote based on their interests!

### Technologies Used
+ Python
+ Flask
+ SQLite3
+ HTML
+ CSS

## Demonstration

Video Demo can be found [here](https://youtu.be/UnOWoh99_6w?si=bAgf2rBl6C_Afm16)

## Description:

### Features
+ Registering as a new user
+ Logging in to your account
+ Choosing from existing polls
+ Table for each poll with ranks, name and total number of votes
+ Voting
+ Adding more options in existing polls
+ Creating new polls
+ Changing username & passwords by accesing the profile

### Database
There are a total of three tables in the **SQL** database **project.db**:
+ users
  - Stores information about the user such as the user_id, username and password in the form of a hash.
+ votes
  - Stores information about the number of votes in each poll. Has 3 columns: genre, name and votes.
+ genres
  - Stores information about the number of genres available.

### Session
Session is used to remember the user_id of the user that has logged in, whether the user has selected any polls or whether the user has faced any errors and if so, to display error messages.

### Routes

### Routes through method "GET"
All routes accessed through the method "GET" which is by clicking on links from the navigation bar, will show the templates for each respective route.

### Routes thorough method "POST"

#### /register
Register asks the user for their username, password and to confirm their password. If password and confirmation does not match, it returns an error message. If successful, the information is inserted into **users** inside ***project.db*** and the user is redirected to login page.

#### /login
Login asks the user for thier username and password and matches it with the data inside **users**. If a match was found, the user is redirected to choose a genre for the poll.

#### /genres
Data inside **genres** is taken and displayed inside a select form from which the user can choose the topic of the poll. After the user has submitted their choice, they are then redirected to each poll's respective page with all the rankings, number of votes and the name of the items.

From there, the user is able to add new options by clicking the Add button seen underneath the table, or vote for each item by clicking the vote button both of which the update their own respective tables inside ***project.db***

#### /create
Create asks the user to input the name of the poll after which the information is inserted into the table **genres**. Then, the user is redirected to the page for the newly created poll where they can add their own options.

## Installations

Make sure you have Flask, SQL and Python installed in your code editor.
For instructions on how to install them, you can access them through the links given underneath.
+ [Flask](https://flask.palletsprojects.com/en/2.3.x/installation/)
+ [SQL](https://www.geeksforgeeks.org/how-to-install-sql-workbench-for-mysql-on-windows/)
+ [Python](https://www.geeksforgeeks.org/how-to-install-python-on-windows/)

To download the package from github, follow the instructions given [here](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
