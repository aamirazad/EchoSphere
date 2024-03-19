import os
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
#textbox
tweet_text=Group(
    Circle(35,95,20),
    Label('What is Happening?!',165,95, size=20,fill='darkgray'),
    Line(0,300,400,300,lineWidth=.25))
app.tweetBox.add(Backarrow,drafts,Post,tweet_text)
app.tweetBox.visible = False

# Sign in
welcome = Label("Welcome to X",140,120, size=30)
nameBox = Rect(50,150,300,50, fill=None, border="black")
textBox= Label("Enter your name here", 100,170,size=30, font="grenze")
submitButton=Group( Rect(250,225,100,20),Label('Sign In',300,235,fill='white',bold=True))
app.signIn.add(welcome,nameBox, textBox,submitButton)
app.signIn.visible = False

tweets = [{
    "username": "MrBeast",
    "icon": "Mrbeastlogo.png",
    "text": "hello world"
},
{
    "username": "Yvan",
    "icon": "Mrbeastlogo.png",
    "text": "x/twitter"
},
{
    "username": "Aamir",
    "icon": "Mrbeastlogo.png",
    "text": "is bad"
},
]

# manage tweet group
def printTweets():
    yVal = 100
    app.tweetPage.clear()
    for tweet in tweets:
        icon = Image(tweet["icon"], 50,yVal-10)
        username = Label(tweet["username"], 100, yVal-5)
        message = Label(tweet["text"],180,yVal)
        yVal += 30
        full_tweet = Group(icon,username,message)
        app.tweetPage.add(full_tweet)
    if app.name:
        app.user_welcome.value = "Welcome, " + app.name

# ui manager
def handlePage(page):
    printTweets()
    app.tweetPage.visible = False
    app.tweetBox.visible = False
    app.signIn.visible = False
    
    if page == app.signIn:
        app.text = ""
    if page == app.tweetBox:
        app.header.visible=False
    
    page.visible = True

def user_login():
    handlePage(app.tweetPage)
    app.name = textBox.value

def go_home():
    handlePage(app.header)
    app.header.visible=True

# manage mouse clicks
def onMousePress(mouseX,mouseY):
    if new_post.hits(mouseX,mouseY) and new_post.visible:
        handlePage(app.tweetBox)
    elif signInButton.hits(mouseX,mouseY) and signInButton.visible:
        handlePage(app.signIn)
    elif (ForYou.hits(mouseX,mouseY) and ForYou.visible) or (Logo.hits(mouseX,mouseY) and Logo.visible):
        handlePage(app.tweetPage)
    elif Backarrow.hits(mouseX,mouseY) and Backarrow.visible:
        handlePage(app.header)
        handlePage(app.tweetPage)
    elif submitButton.hits(mouseX,mouseY) and submitButton.visible:
        user_login()

# handle changes
def onStep():
    #textbox
    if textBox.visible:
        textBox.value = app.text
        textBox.left = 60

        
# handle keypress
def onKeyPress(key):
    valid_characters = r'!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~'

    list_of_valid_characters = list(valid_characters)
    if key == "backspace":
        app.text = app.text[:-1]
    elif key == "enter":
        app.text += "\n"
    elif key in list_of_valid_characters and len(app.text) <= 8:
        app.text += key
   
printTweets()
cmu_graphics.run()