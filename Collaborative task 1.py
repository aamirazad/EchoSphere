import sqlite3
from datetime import datetime
from random import randint
from identicons import generate, save
from cmu_graphics import *

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
app.text = ["", "", ""]
app.name = ""
app.icon=''
app.user_welcome = Label("", 110,20)
app.tweetPage = Group()
app.tweetBox = Group()
app.signIn = Group()

#Tweet Box
#backarrow
Backarrow=Group(Polygon(12,25,25,15,25,35),Line(25,25,45,25))
drafts= Label('Drafts',260,30,size=15,bold=True)
Post=Group(Oval(330,30,50,20),Label('Post',330,30,size=15, bold=True,fill='white'))
#app.signInBox
tweet_circle = Circle(35,95,20)
app.line1 = Label('What is Happening?!',165,95, size=20,fill='darkgray')
app.line2 = Label('',165,120,size=20)
app.line3 = Label('',165,145,size=20)
app.list_of_lines = [app.line1, app.line2, app.line3]
app.tweet_text = Group(app.line1, app.line2, app.line3)
tweet_seperator = Line(0,300,400,300,lineWidth=.25)
app.tweetBox.add(Backarrow,drafts,Post, app.tweet_text, tweet_circle, tweet_seperator)
app.tweetBox.visible = False
app.arrows=Group(Polygon(360,90,370,110,350,110),Polygon(350,270,370,270,360,290))
# Sign in
welcome = Label("Welcome to X",140,120, size=30)
nameBox = Rect(50,150,300,50, fill=None, border="black")
app.signInBox= Label("Enter username", 200,170,size=30, font="grenze", fill="darkGray")
submitButton=Group( Rect(250,325,100,20),Label('Sign In',300,335,fill='white',bold=True))
Picture= Image('Aamir Azad.png',50,225)
SigninCircle=Circle(Picture.centerX-2.5,Picture.centerY,30,fill='darkgray',opacity=45)
SigninCircle.toBack()
urlLabel=Label("Insert URL",85,310,size=15,font='monospace')
SubmitUrl=Group(Rect(35,300,200,25,fill=None,border='Black'),urlLabel)
SubmitUrl.visible=False
Instruction=Label('Insert Picture',Picture.centerX+95,Picture.centerY, bold=True, size=15, font='monospace' )
app.signIn.add(welcome,nameBox, app.signInBox,submitButton,Picture,SigninCircle,Instruction,SubmitUrl)
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

def query_db(query):
    connection = sqlite3.connect("database.db")
    rows = connection.execute(query).fetchall()
    connection.close()
    return rows

r = lambda: randint(0,255)
print('#%02X%02X%02X' % (r(),r(),r()))

# manage tweet group
def printTweets(line = 1):    
    yVal = 80    
    app.tweetPage.clear()
    db = query_db("SELECT * FROM Tweets")
    full_tweet = Group()
    for tweet in db:
        identicon = generate(tweet[1], primary=0xFFD700, secondary=0x8B0000)
        save(identicon, tweet[1] + "_icon.png", 500, 500)
        icon = Image(tweet[1] + "_icon.png", 20,yVal+10)
        icon.width=20
        icon.height=20
        username = Label(tweet[1], 80, yVal+10,font='montserrat',bold=True)
        message = Group()
        for count, line in enumerate(tweet[3].splitlines()):
            lineYVal = (count * 30) + (yVal+35)
            message.add(Label(line,username.right,lineYVal,size=20))
            message.left = 70
        barline=Line(0,message.bottom+30,400,message.bottom+30,opacity=30)
        #yVal += 67.5
        yVal = barline.bottom
        full_tweet.add(icon,username,message, barline)
    if line == 1:
        for tweet in full_tweet:
            print(tweet.bottom)
    app.tweetPage.add(full_tweet, app.arrows)
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
    app.text = ""
    for line in app.list_of_lines:
        line.value = ""
    app.list_of_lines[0].value = "What is Happening?!"
    app.stepsPerSecond = 30
    app.header.visible=False

def sign_in_page():
    handlePage(app.signIn)
    app.stepsPerSecond = 30
    app.text = ""
    new_post.visible = False
    SubmitUrl.visible=False

def go_home_page():
    handlePage(app.tweetPage)
    printTweets()
    app.header.visible=True

def submitName():
    go_home_page()
    app.icon=urlLabel.value
    app.name = app.signInBox.value

def submitTweet():
    if app.name and app.text:
        connection = sqlite3.connect("database.db")
        connection.execute("INSERT INTO Tweets (username, icon, content, date_created) VALUES (?, ?, ?)", (app.name, app.icon, app.text, datetime.now()))
        connection.commit()
        connection.close()
    go_home_page()

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
    elif SigninCircle.hits(mouseX,mouseY) and SigninCircle.visible:
        SubmitUrl.visible= not SubmitUrl.visible

# handle keypress
def onKeyPress(key):
    #elif key == "enter":
    #    if app.text.count("\n") < 2:
    #        app.text += "\n"
    if app.signIn.visible:
        if SubmitUrl.visible:
            if urlLabel.value == "Insert URL":
                urlLabel.value = ""
            if key == "backspace":
                urlLabel.value = urlLabel.value[:-1]
            else:
                urlLabel.value += key
            urlLabel.left = 40
        else:
            if key == "backspace":
                app.text = app.text[:-1]
            valid_characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYabcdefghijklmnopqrstuvwxyz0123456789'
            list_of_valid_characters = list(valid_characters)
            if key in list_of_valid_characters and len(app.text) <= 8:
                app.text += key
            lines = app.text.splitlines()
            if lines:
                app.signInBox.fill = "black"
                app.signInBox.value = lines[0]
                app.signInBox.left = 60
            else:
                app.signInBox.value = ""
            # for line in lines:
            #     if line.count("\n") < 2 and len(line) < 20:
            #         app.text += key
            # app.text += key
    elif app.tweetBox.visible:
        if key == "space":
            app.text += " "
        lines = app.text.splitlines()
        for line in lines:
            if len(line) >= 20:
                if app.text.count("\n") < 2:
                    app.text += "\n"
        lines = app.text.splitlines()
        for count, line in enumerate(lines):
                app.list_of_lines[count].fill = "black"
                app.list_of_lines[count].value += key
                app.list_of_lines[count].left = 65
cmu_graphics.run()
