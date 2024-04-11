from cmu_graphics import *
import datetime as datetime
import sqlite3
from datetime import datetime

# UI
#new by Adrien Coquet from Noun Project (CC BY 3.0)
new_post = Image('new_icon.png', 330, 330)
signInButton = Image('sign_in2.png', 5,5)
signInButton.centerX = 20
signInButton.centerY = 20

seperator = Line(0,80, 400,80, fill='black',opacity=35)
ForYou= Label('For you', 125,55, size=15,bold=True)
Following=Label('Following', 265,55, size=15,bold=True)

Logo=Image('x_logo.png', 178,-2)
Logo.width= 45
Logo.height = 45

## pages
app.header = Group(signInButton,seperator,ForYou,Following,Logo)
app.text = ""
app.name = ""
app.user_welcome = Label("", 110,20)
app.tweetPage = Group()
app.tweetBox = Group()
app.signIn = Group()

#Tweet Box
#backarrow
Backarrow=Group(Polygon(12,25,25,15,25,35),Line(25,25,45,25))
drafts= Label('Drafts',260,30,size=15,bold=True)
Post=Group(Oval(330,30,50,20),Label('Post',330,30,size=15, bold=True,fill='white'))
#app.textBox
tweet_circle = Circle(35,95,20)
app.line1 = Label('What is Happening?!',165,95, size=20,fill='darkgray')
app.line2 = Label('',165,120,size=20)
app.line3 = Label('',165,145,size=20)
app.list_of_lines = [app.line1, app.line2, app.line3]
app.tweet_text = Group(app.line1, app.line2, app.line3)
tweet_seperator = Line(0,300,400,300,lineWidth=.25)
app.tweetBox.add(Backarrow,drafts,Post, app.tweet_text, tweet_circle, tweet_seperator)
app.tweetBox.visible = False

# Sign in
welcome = Label("Welcome to X",140,120, size=30)
nameBox = Rect(50,150,300,50, fill=None, border="black")
app.textBox= Label("Enter your name here", 100,170,size=30, font="grenze")
submitButton=Group( Rect(250,325,100,20),Label('Sign In',300,335,fill='white',bold=True))
Picture= Image('Aamir Azad.png',50,225)
SigninCircle=Circle(Picture.centerX-2.5,Picture.centerY,30,fill='darkgray',opacity=45)
SigninCircle.toBack()
Instruction=Label('Insert Picture',Picture.centerX+95,Picture.centerY, bold=True, size=15, font='monospace' )
app.signIn.add(welcome,nameBox, app.textBox,submitButton,Picture,SigninCircle,Instruction)
app.signIn.visible = False
#Vecteezy :denyzdrozd

### INIT DATABASE

connection = sqlite3.connect("database.db")
connection.execute('''
                   CREATE TABLE IF NOT EXISTS Tweets(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT NOT NULL,
                   icon TEXT,
                   content TEXT NOT NULL,
                   date_created INTEGER NOT NULL)''')
connection.commit()
connection.close()

def manage_db(query):
    connection = sqlite3.connect("database.db")
    rows = connection.execute(query).fetchall()
    return rows

# manage tweet group
def printTweets():    
    yVal = 120    
    app.tweetPage.clear()
    db = manage_db("SELECT * FROM Tweets")
    full_tweet = Group()  
    for tweet in db:
        icon = Image(tweet[2], 20,yVal-30)
        icon.width=20
        icon.height=20
        username = Label(tweet[1], 80, yVal-30,font='montserrat',bold=True)
        message = Label(tweet[3],username.right,yVal-10,size=20)
        barline=Line(0,message.bottom+30,400,message.bottom+30,opacity=30)
        yVal += 67.5
        full_tweet.add(icon,username,message, barline)
    app.tweetPage.add(full_tweet)    
printTweets()

# ui manager
def handlePage(page):
    app.tweetPage.visible = False
    app.tweetBox.visible = False
    app.signIn.visible = False
    new_post.visible = True
    
    page.visible = True

def new_tweet():
    handlePage(app.tweetBox)
    app.stepsPerSecond = 30
    app.header.visible=False

def sign_in_page():
    handlePage(app.signIn)
    app.stepsPerSecond = 30
    app.text = ""
    new_post.visible = False

def go_home_page():
    handlePage(app.tweetPage)
    app.header.visible=True

def submitName():
    handlePage(app.tweetPage)
    app.name = app.textBox.value

def submitTweet():
    handlePage(app.tweetBox)
    print(app.text)

def checkClick(objects, mouseX, mouseY):
    run = False
    for object in objects:
        run = object.hits(mouseX,mouseY) and object.visible
    return run

# manage mouse clicks
def onMousePress(mouseX,mouseY):
    if new_post.hits(mouseX,mouseY) and new_post.visible:
        new_tweet()
    elif signInButton.hits(mouseX,mouseY) and signInButton.visible:
        sign_in_page()
    elif (ForYou.hits(mouseX,mouseY) and ForYou.visible) or (Logo.hits(mouseX,mouseY) and Logo.visible):
        go_home_page()
    elif Backarrow.hits(mouseX,mouseY) and Backarrow.visible:
        handlePage(app.header)
        handlePage(app.tweetPage)
    elif submitButton.hits(mouseX,mouseY) and submitButton.visible:
        submitName()
    elif checkClick(Post, mouseX, mouseY):
        submitTweet()
        
# handle keypress
def onKeyPress(key):
    valid_characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYabcdefghijklmnopqrstuvwxyz0123456789'    
    list_of_valid_characters = list(valid_characters)
    if key == "backspace":
        app.text = app.text[:-1]
    elif key == "enter":
        if app.text.count("\n") < 2:
            app.text += "\n"
    elif key in list_of_valid_characters:
        if app.textBox.visible:
            if len(app.text) <= 8:
                app.text += key
        else:
            app.text += key
        #textBox
    if app.signIn.visible:
        line = app.text.splitlines()
        try:
            app.textBox.value = line[0]
            app.text = line[0]
        except:
            app.textBox.value = ""
        app.textBox.left = 60
    if app.tweetBox.visible:
        app.textBox.value = ""
        lines = app.text.splitlines()
        if lines:
            for count, line in enumerate(lines):
                if line:
                    app.list_of_lines[count].fill = "black"
                    app.list_of_lines[count].value = line

            

cmu_graphics.run()