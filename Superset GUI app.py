from cmu_graphics import *
import copy, string, itertools, random

####################################################
# onAppStart: called only once when app is launched
####################################################
"""
Creative Elements:
biggest thing (took over an hour): 
- Ocean theme: uses emojis and image backgrounds for cards

medium effort things (took a little over an hour to do all):
- shows demo of theme on theme selection page
- shows example of set on help page
- displays score (which is just time elapsed) and high score, and shows if you beat it
- hints feature: if you have incorrect cards selected, instead of deselecting all it deselects one at a time
- when a round is lost, it highlights the found set in blue. it still highlights the incorrect user answer in red, 
  but if the user answer and the found set have a card in common, it defaults to highlighting blue

smaller things, not a lot of effort: 
- beach image on help screen, blue background for app, looping background music
- click sound effect for clicking a valid key or clicking a card 
- confirm sound effect when setting a new dimension or new theme
- error sound effect when trying to set an invalid dimension, or if the dimension is too large for chosen theme
- displaying dimension on theme page so user knows when theme is incompatible

"""
def onAppStart(app):
    app.width = 1000
    app.height = 600
    backgroundUrl = "cmu://786010/29203000/mixkit-jamaican-241.mp3"
    errorUrl = "cmu://786010/29202734/mixkit-click-error-1110.wav"
    clickUrl = "cmu://786010/29202768/mixkit-hard-typewriter-click-1119.wav"
    confirmUrl = "cmu://786010/29202790/mixkit-positive-interface-beep-221.wav"
    app.beach = "cmu://786010/29225885/depositphotos_391902574-stock-illustration-tropical-sandy-beach-flat-color.jpg"
    app.blowfish = "cmu://786010/29224102/blowfish.png"
    app.octopus = "cmu://786010/29224073/octopus.png"
    app.whale = "cmu://786010/29224107/whale.png"
    app.backgroundOne = "cmu://786010/29225435/underwater-4286600_640+(1).png" 
    app.backgroundTwo = "cmu://786010/29225425/premium_photo-1681190674383-4bf3d2a9a337+(1).png"
    app.backgroundThree = "cmu://786010/29225350/linus-nylund-UCIZh0-OYPw-unsplash+(1).png"
    app.music = Sound(backgroundUrl)
    app.error = Sound(errorUrl)
    app.click = Sound(clickUrl)
    app.confirm = Sound(confirmUrl)
    app.music.play(loop=True)
    app.currDims = [3, 3, 3]
    app.newDims = [3, 3, 3]
    app.currTheme = "Letters"
    app.newTheme = "Letters"
    app.stepsPerSecond = 30
    app.highScore = 0
    app.highScoreBeat = False
    app.background= "lightBlue"
    app.cardsPerSet = min(app.currDims)
    app.targetBoardSize = 8
    app.rotateAngleDemo= 5
    app.playing = False

####################################################
# Code used by multiple screens
####################################################

def onKeyPressHelper(app, key):
    # Since every screen does the same thing on key presses, we can
    # write the main logic here and just have them call this helper fn
    # You should add/edit some code here...
    if   key == 'd': 
        app.click.play()
        setActiveScreen('setDimsScreen')
    elif key == 't': 
        app.click.play()
        setActiveScreen('setThemeScreen')
    elif key == '?': 
        app.click.play()
        setActiveScreen('helpScreen')
    elif key == 'p':
        app.click.play()
        if not app.playing:
            playScreen_startGame(app)
            app.playing = True
        setActiveScreen('playScreen')
    elif key == "n":
        app.click.play()
        setActiveScreen('playScreen')
        playScreen_startGame(app)

def drawScreenTitle(app, screenTitle):
    drawLabel('SuperSet!', app.width/2, 20, size=20, bold=True)
    drawLabel(screenTitle, app.width/2, 50, size=16, bold=True)
    # You will want to remove the following line:
    #drawLabel('To get you started, press one of d,t,?,p to switch screens', app.width/2, 100, size=16)

####################################################
# helpScreen
####################################################

def helpScreen_redrawAll(app):
    drawScreenTitle(app, 'Help Screen')
    drawLabel('Press p to play', 50, 50, size = 15, align = "left")
    drawLabel('Press n to start a new game', 50, 70,size = 15, align = "left")
    drawLabel('Press d to set dimensions (number of features and options)', 50, 90, size = 15, align = "left")
    drawLabel('Press t to set theme (how cards look)', 50, 110, size = 15, align = "left")
    drawLabel('Press ? to show help screen (this screen)', 50, 130, size = 15, align = "left")
    drawLabel('When playing, press h for hints. Remember there is a 15 sec penalty for each hint used!', 
              50, 150, size = 15, align = "left")
    drawLine(100, 170, app.width-100, 170)
    drawLabel("To play SuperSet, click cards from the board to create a set", 50, 200, size = 15, align = "left")
    drawLabel("The number of cards in a set is the same as the minimum dimension", 50, 220, size = 15, align = "left")
    drawLabel("For each feature in a particular set, all cards will have the exact same feature or all different. Below is an example of a set:", 
              50, 240, size = 15, align = "left")
    drawLabel("(All octopus, all same size, all rotating at same speed, all have different backgrounds)", 
              50, 260, size = 10, align = "left")
    imageWidth, imageHeight = getImageSize(app.beach)
    drawImage(app.beach, app.width/2, app.height//2+150, 
    width = imageWidth*1.7, height = imageHeight*1.7, align="center")
    for i in range(3):
        drawRect(50+(i*170), 350, 140, 200, fill = "white", border = "black", borderWidth = 5)
    drawImage(app.backgroundOne, 55, 355 )
    drawImage(app.backgroundTwo, 225, 355 )
    drawImage(app.backgroundThree, 395, 355 )
    for i in range(3):
        emojiWidth, emojiHeight = getImageSize(app.octopus)
        drawImage(app.octopus, 120+(i*170), 450, 
        width = emojiWidth//2, height = emojiHeight//2, 
        align = "center", rotateAngle = app.rotateAngleDemo)

def helpScreen_onKeyPress(app, key):
    onKeyPressHelper(app, key)

def helpScreen_onStep(app):
    app.rotateAngleDemo += 2

####################################################
# setDimsScreen
####################################################

def setDimsScreen_onScreenActivate(app):
    pass

def setDimsScreen_redrawAll(app):
    drawScreenTitle(app, 'Set Dimensions Screen')
    drawLabel("Set dimension using numbers 3-5 and backspace as needed.",
              app.width/2, 200, size = 20)
    drawLabel("Dimensions must be of length 2 to 5, with the sum being less than 15", app.width/2, 240, size = 20)
    drawLabel("Press enter to set the new dimensions and to p to play", app.width/2, 280, size = 20)
    drawLabel("Changing dimensions during a game will start a new game", app.width/2, 320, size = 20)
    drawLabel(f"Current Dimensions: {app.currDims}", app.width/2, 400, size = 30, fill = "blue")
    drawLabel(f"New Dimensions: {app.newDims}", app.width/2, 450, size = 30, fill = "red")

def sumOfDims(app):
    result = 0
    for dim in app.newDims:
        result += dim
    return result

def setDimsScreen_onKeyPress(app, key):
    check = sumOfDims(app)
    if key.isdigit():
        key = int(key)
        if check + key <= 15:
            if 2 < key < 5:
                if len(app.newDims) < 5:
                    app.click.play()
                    app.newDims.append(key)
            if key == 5:
                if app.newDims.count(5) == 0:
                    app.click.play()
                    app.newDims.append(key)
                else:
                    app.error.play()
        else:
            app.error.play()
    elif key == "backspace":
        if app.newDims != []:
            app.click.play()
            app.newDims = app.newDims[0: -1]
        else:
            app.error.play()
    elif key == "enter":
        if len(app.newDims) > 1 and app.newDims != app.currDims:
            app.confirm.play()
            app.currDims = copy.copy(app.newDims)
            playScreen_startGame(app)
    onKeyPressHelper(app, key)

####################################################
# setThemeScreen
####################################################

def setThemeScreen_redrawAll(app):
    drawScreenTitle(app, 'Set Theme Screen')
    drawLabel('For shapes, special, and ocean, the dimensions must only contain the number 3 and be of length 4 or less. Letters works for any dimension', 
                app.width/2, 100, size = 15)
    drawLabel('Use numbers to select theme. Changing theme during a game will start a new game', 
                app.width/2, 120, size = 15)
    drawLabel("Press enter to set the new theme and p to play", app.width/2, 140, size = 15)
    drawLabel('Theme 0: Letters',50, 170, size = 20, align = "left")
    drawLabel('Theme 1: Shapes', 50, 190, size = 20,  align = "left")
    drawLabel('Theme 2: Special', 50, 210, size = 20,  align = "left")
    drawLabel('Theme 3: Ocean', 50, 230, size = 20,  align = "left")
    drawLabel(f"Current Dimensions: {app.currDims}", app.width/2, app.height/2-80, size = 20)
    drawLabel(f"Current Theme: {app.currTheme}", app.width/2, app.height/2-40, size = 30, fill = "blue")
    drawLabel(f"New Theme: {app.newTheme}", app.width/2, app.height/2, size = 30, fill = "red")
    drawLabel("New Theme Preview:", app.width/2, app.height/2+35, size = 15)
    drawRect(app.width/2, app.height/2+150, 140, 200, fill = "white", 
                 border = "black", borderWidth = 5, align = "center")
    if app.newTheme == "Letters":
        drawLabel("ABC", app.width/2, app.height/2+150, size = 28, bold = True)
        drawLabel("Features: Letters A-E", app.width/2, app.height/2+280, size = 15)
    elif app.newTheme == "Shapes":
        drawRegularPolygon(app.width/2, app.height/2+120, 20, 3, fill = "red")
        drawRegularPolygon(app.width/2,  app.height/2+180, 20, 3, fill = "red")
        drawLabel("Features: Shapes, Colors, Number, Opacity", app.width/2, app.height/2+280, size = 15)
    elif app.newTheme == "Special":
        drawRegularPolygon(app.width/2, app.height/2+150, 40, 3, fill = "pink", border = "black", dashes = True, rotateAngle = app.rotateAngleDemo)
        drawLabel("Features: Shapes, Colors, Rotation Speed (includes direction), Border", app.width/2, app.height/2+280, size = 15)
    else:
        drawImage(app.backgroundOne, app.width/2, app.height/2+150, align = "center")
        emojiWidth, emojiHeight = getImageSize(app.octopus)
        drawImage(app.octopus, app.width/2, app.height/2+150, align = "center", width = emojiWidth//2, height= emojiHeight//2, rotateAngle = app.rotateAngleDemo)
        drawLabel("Features: Animal, Background, Size, Rotation Speed (includes direction)", app.width/2, app.height/2+280, size = 15)
        

def dimsTooLargeForTheme(dims, theme):
    if (4 in dims) or (5 in dims) or (len(dims) > 4):
        return True
    return False

def setThemeScreen_onKeyPress(app, key):
    if key == "0":
        app.click.play()
        app.newTheme = "Letters"
    elif key == "1":
        app.click.play()
        app.newTheme = "Shapes"
    elif key == "2":
        app.click.play()
        app.newTheme = "Special"
    elif key == "3":
        app.click.play()
        app.newTheme = "Ocean"
    elif key == "enter":
        if dimsTooLargeForTheme(app.currDims, app.newTheme) and app.newTheme != "Letters":
            app.error.play()
            app.currTheme = "Letters"
        elif app.newTheme != app.currTheme:
            app.confirm.play()
            app.currTheme = app.newTheme
            playScreen_startGame(app)
    onKeyPressHelper(app, key)

def setThemeScreen_onStep(app):
    if app.newTheme == "Special" or app.newTheme == "Ocean":
        app.rotateAngleDemo += 2

####################################################
# playScreen
####################################################

def playScreen_startGame(app):
    app.timeElapsed = 0
    app.playScreenCounter = 0
    app.rounds = 4
    app.lives = 2
    app.highScoreBeat = False
    playScreen_startRound(app)

def playScreen_startRound(app):
    app.board, app.foundSet = getRandomBoardWithSet(app.currDims, app.targetBoardSize)
    app.guessSet = []
    app.gameWon = False
    app.gameLost = False
    app.roundWon = False
    app.roundLost = False
    app.borderColor = "black"
    app.selectedBorder = "yellow"
    app.showFound = False
    app.foundBorder = "black"
    app.afterWinCounter = 0
    app.afterLossCounter = 0
    app.dRotateAngle = 5

def playScreen_redrawAll(app):
    if not (app.gameWon or app.gameLost):
        for i in range(app.targetBoardSize):
            left, top, width, height = getCardBounds(app, i)
            if app.board[i] in app.guessSet and not app.roundLost: 
                drawRect(left, top, width, height, fill = "white", 
                         border = app.selectedBorder, borderWidth = 5, dashes = True)
            elif app.board[i] in app.guessSet and app.roundLost:
                if app.board[i] not in app.foundSet:
                    drawRect(left, top, width, height, fill = "white", 
                         border = app.selectedBorder, borderWidth = 5, dashes = True)
                else:
                    drawRect(left, top, width, height, fill = "white", 
                         border = app.foundBorder, borderWidth = 5, dashes = False)
            elif app.board[i] in app.foundSet and not app.roundLost:
                drawRect(left, top, width, height, fill = "white", 
                        border = app.borderColor, borderWidth = 5, dashes = False)
            elif app.board[i] in app.foundSet and app.roundLost:
                drawRect(left, top, width, height, fill = "white", 
                        border = app.foundBorder, borderWidth = 5, dashes = False)
            else:
                drawRect(left, top, width, height, fill = "white", 
                        border = app.borderColor, borderWidth = 5, dashes = False)
            card = app.board[i]
            if app.currTheme == "Letters":
                drawCardInLettersTheme(app, card, left, top, width, height)
            elif app.currTheme == "Shapes":
                drawCardinShapesTheme(app, card, left, top, width, height)
            elif app.currTheme == "Special":
                drawCardInSpecialTheme(app, card, left, top, width, height)
            else:
                drawCardInOceanTheme(app, card, left, top, width, height)
        if app.roundWon:
            drawLabel("Correct! Press any key or mouse to continue.", app.width/2, 80, size = 20)
        elif app.roundLost:
            drawLabel("That's not a set! Press any key or mouse to continue", app.width/2, 80, size = 20)
            
    elif app.gameLost:
        drawLabel("Game Over :( Press n to play again",
                  app.width/2, app.height/2, size=30, fill='red')
    else:
        drawLabel(f"Game Won in {app.timeElapsed} seconds! Press n to play again", 
                  app.width/2, app.height/2-10, size=30, fill='green')
        if app.highScoreBeat:
            drawLabel("New High Score!", app.width/2, app.height/2 + 60, size=30, fill = "green")
        else:
            drawLabel(f"Score: {app.timeElapsed}", app.width/2, app.height/2 + 60, size=30, fill = "Blue")
        drawLabel(f'High Score: {app.highScore}', app.width/2, app.height/2 + 100, size=30,)
    drawScreenTitle(app, 'Play Screen')
    drawLabel(f'Rounds: {app.rounds}', 40, 50, size=20, fill='green', align = "left")
    drawLabel(f'Lives: {app.lives}', 40, 70, size=20, fill='green', align = "left")
    drawLabel(f'Time Elapsed = {app.timeElapsed}', 40, 90, size=20, fill='green', align = "left")
    drawLabel(f'High Score: {app.highScore}', 40, 110, size=20, fill = "green", align = "left")

def drawCardInLettersTheme(app, card, left, top, width, height):
    drawLabel(card, left+width/2, top+height/2, size = 28, bold = True)

def getNewCard(card):
    newCard = []
    for feature in card:
        if feature == "A":
            newCard.append(0)
        elif feature == "B":
            newCard.append(1)
        elif feature == "C":
            newCard.append(2)
    return newCard

def drawCardinShapesTheme(app, card, left, top, width, height):
    newCard = getNewCard(card)
    shape = ["oval", "star", "diamond"]
    colors = ["red", "green", "blue"]
    number = [1, 2, 3]
    opaqueness = [10, 50, 100]
    if len(newCard) == 2:
        numberIndex = 1
        opacity = 100
    elif len(newCard) == 3:
        numberIndex =  number[newCard[2]]
        opacity = 100
    elif len(newCard) == 4:
        numberIndex =  number[newCard[2]]
        opacity = opaqueness[newCard[3]]
    spacing = 200 / numberIndex
    for i in range(numberIndex):
        cx = left+width/2
        cy = top+(i+0.5)*spacing
        if shape[newCard[0]] == "oval":
            drawOval(cx,cy, 100, 50, fill = colors[newCard[1]], opacity = opacity)
            drawOval(cx, cy, 100, 50, fill = None, border = "black")
        if shape[newCard[0]] == "star":
            drawStar(cx, cy, 20, 5, fill = colors[newCard[1]], opacity = opacity)
            drawStar(cx, cy, 20, 5, fill = None, border = "black")
        if shape[newCard[0]] == "diamond":
            drawPolygon(cx-40, cy, cx, cy-20, cx+40, cy, cx, cy+20,fill = colors[newCard[1]], opacity = opacity)
            drawPolygon(cx-40, cy, cx, cy-20, cx+40, cy, cx, cy+20,fill = None, border = "black")

def drawCardInSpecialTheme(app, card, left, top, width, height):
    newCard = getNewCard(card)
    points = [3, 4, 5]
    colors = ["orange", "pink", "yellow"]
    rotate = [1, 5, -1]
    border = ["dashed", "normal", "bold"]
    if len(newCard) == 2:
        drawRegularPolygon(left+width/2, top+height/2, 40, points[newCard[0]], 
                           fill = colors[newCard[1]], border = "black", rotateAngle = app.dRotateAngle)
    elif len(newCard) == 3:
        drawRegularPolygon(left+width/2, top+height/2, 40, points[newCard[0]], 
                           fill = colors[newCard[1]], border = "black", rotateAngle = app.dRotateAngle*rotate[newCard[2]])
    elif len(newCard) == 4:
        if border[newCard[3]]== "dashed":
            drawRegularPolygon(left+width/2, top+height/2, 40, points[newCard[0]], fill = colors[newCard[1]], 
                               rotateAngle = app.dRotateAngle*rotate[newCard[2]], border = "black", dashes=True)
        if border[newCard[3]]== "thin":
            drawRegularPolygon(left+width/2, top+height/2, 40, points[newCard[0]], fill = colors[newCard[1]], 
                               rotateAngle = app.dRotateAngle*rotate[newCard[2]], border = "black")
        if border[newCard[3]]== "bold":
            drawRegularPolygon(left+width/2, top+height/2, 40, points[newCard[0]], fill = colors[newCard[1]], 
                               rotateAngle = app.dRotateAngle*rotate[newCard[2]], border = "black", borderWidth=5)

def drawCardInOceanTheme(app, card, left, top, width, height):
    newCard = getNewCard(card)
    emojis = [app.octopus, app.blowfish, app.whale]
    backgrounds = [app.backgroundOne, app.backgroundTwo, app.backgroundThree]
    size = ["small", "normal", "large"]
    rotate = [1, 5, -1]
    emojiWidth, emojiHeight = getImageSize(emojis[newCard[0]])
    if len(newCard) == 2:
        emojiWidth, emojiHeight = emojiWidth // 2, emojiHeight // 2
    if len(newCard) > 2:
        if size[newCard[2]] == "small":
             emojiWidth, emojiHeight = emojiWidth // 4, emojiHeight //4
        elif size[newCard[2]] == "normal":
            emojiWidth, emojiHeight = emojiWidth // 2, emojiHeight // 2
        else:
            emojiWidth, emojiHeight = emojiWidth // 1.3, emojiHeight //1.3
    if len(newCard) < 4:
        rotateSpeed = 1
    if len(newCard) == 4:
        rotateSpeed = rotate[newCard[3]]
    drawImage(backgrounds[newCard[1]], left+width/2, top+height/2, align = "center")
    drawImage(emojis[newCard[0]], left+width/2, top+height/2, 
              width = emojiWidth , height = emojiHeight, 
              align = "center", rotateAngle = rotateSpeed*app.dRotateAngle)
    

def playScreen_onMousePress(app, mouseX, mouseY):
    if app.rounds > 0 and app.lives > 0:
        if not app.roundWon and not app.roundLost:
            if len(app.guessSet) < app.cardsPerSet:
                for i in range(app.targetBoardSize):
                    left, top, width, height = getCardBounds(app, i)
                    if (left <= mouseX <= left+width) and (top <= mouseY <= top+height):
                        if app.board[i] not in app.guessSet:
                            app.click.play()
                            app.guessSet.append(app.board[i])
                        else:
                            app.click.play()
                            app.guessSet.remove(app.board[i])
            if len(app.guessSet) == app.cardsPerSet:
                if isSet(app.guessSet):
                    app.rounds -= 1
                    app.selectedBorder = "green"
                    app.roundWon = True
                else:
                    app.lives -= 1
                    app.selectedBorder = "red"
                    app.roundLost = True
        elif app.roundWon or app.roundLost:
            playScreen_startRound(app)
    if app.afterWinCounter != 0:
        app.gameWon = True
        if app.highScore == 0 or app.timeElapsed < app.highScore:
            app.highScoreBeat = True
            app.highScore = app.timeElapsed
    if app.afterLossCounter != 0:
        app.gameLost = True

def getCardBounds(app, i):
    left = 175 + ((i%4)*170)
    if i < 4:
        top = 120
    else:
        top = 350
    width = 140
    height = 200
    return left, top, width, height

def guessSetWrong(guessSet, foundSet):
    for card in guessSet:
        if card not in foundSet:
            return True
    return False

def findFirstCardNotInOtherSet(foundSet, guessSet):
    for card in foundSet:
        if card not in guessSet:
            return card

def playScreen_onKeyPress(app, key):
    if key == "n":
        playScreen_startGame(app)
    if key == "p" and not (app.roundWon or app.roundLost):
        return
    onKeyPressHelper(app, key)
    if app.rounds > 0 and app.lives > 0:
        if not (app.roundWon or app.roundLost):
            if key == "h":
                app.click.play()
                for card in app.guessSet:
                    if card not in app.foundSet:
                        app.guessSet.remove(card)
                app.guessSet.append(findFirstCardNotInOtherSet(app.foundSet, app.guessSet))
                app.timeElapsed += 15
                if len(app.guessSet) == app.cardsPerSet:
                    if isSet(app.guessSet):
                        app.rounds -= 1
                        app.selectedBorder = "green"
                        app.roundWon = True
                    else:
                        app.lives -= 1
                        app.selectedBorder = "red"
                        app.roundLost = True
        elif app.roundWon or app.roundLost:
            playScreen_startRound(app)
    if app.afterWinCounter != 0:
        app.gameWon = True
        if app.highScore == 0 or app.timeElapsed < app.highScore:
            app.highScoreBeat = True
            app.highScore = app.timeElapsed
    if app.afterLossCounter != 0:
        app.gameLost = True
    elif (app.gameWon or app.gameLost) and key == "n":
        app.click.play()
        playScreen_startGame(app)

def playScreen_onStep(app):
    app.playScreenCounter += 1
    if app.playScreenCounter % 30 == 0 and not (app.gameWon or app.gameLost):
        app.timeElapsed += 1
    if app.currTheme == "Special" or app.currTheme == "Ocean":
        app.dRotateAngle += 1
    if app.rounds == 0:
        app.afterWinCounter += 1
    if app.lives == 0:
        app.afterLossCounter += 1
    if app.roundLost:
        app.showFound = True
        app.foundBorder = "blue"

###############################################
# Functions copied from console-based app
###############################################

# Copy-Paste required code from console-based app here!
# Just copy your helper functions along with stringProduct() and
# combinations().  You do not need to copy the
# "Console-Based playSuperSet (for debugging)" section.
def stringProduct(L):
    # This helper function (which is extremely useful for makeSuperSetDeck)
    # is provided for students, since it uses some concepts we have not
    # yet covered.  This takes a list of strings and returns a list of
    # their product -- that is, a list of strings where the first character
    # is any letter from the first string, the second character is the any
    # letter from the second string, and so on.
    # For example:
    # stringProduct(['AB', 'CDE']) returns ['AC', 'AD', 'AE', 'BC', 'BD', 'BE']
    # Also:
    # stringProduct(['AB', 'CD', 'EFG']) returns ['ACE', 'ACF', 'ACG', 'ADE',
    #                                             'ADF', 'ADG', 'BCE', 'BCF',
    #                                             'BCG', 'BDE', 'BDF', 'BDG']   
    resultTuples = list(itertools.product(*L))
    resultStrings = [''.join(t) for t in resultTuples]
    return resultStrings

def combinations(L, n):
    # This helper function (which is extremely useful for findFirstSet)
    # is provided for students, since it uses some concepts we have not
    # yet covered.  
    # Given a list of values L and a non-negative integer n,
    # this function returns a list of all the possible lists
    # made up of any n values in L.
    # For example:
    # combinations(['A', 'B', 'C', 'D'], 2) returns:
    # [['A', 'B'], ['A', 'C'], ['A', 'D'], ['B', 'C'], ['B', 'D'], ['C', 'D']]
    # See how this is a list of all the possible lists made up of
    # any 2 values in L.
    # Also, order does not matter.  See how ['A', 'B'] is in the result
    # and so ['B', 'A'] is not.
    return [list(v) for v in itertools.combinations(L, n)]

###############################################
# Functions for you to write
###############################################

def allSame(L):
    # Returns True if all the values in the list L are equal and False
    # otherwise.  You may assume L is non-empty.
    for i in range(len(L)-1):
        if L[i] != L[i+1]:
            return False
    return True

def allDiffer(L):
    # Returns True if all the values in the list L are different and False
    # otherwise.  You may assume L is non-empty.
    for i in range(len(L)-1):
        if L[i] in L[i+1:]:
            return False
    return True

def isSet(cards):
    # Given a list of cards, return True if those cards form a set,
    # and False otherwise.
    # Here you may assume the list of cards is non-empty and that each card
    # is a string of valid options from the same list of possible features.
    # Thus, just confirm that for every feature, every card either has the
    # same option or every card has a different option.
    currFeature = []
    lengthCards = len(cards)
    lengthFeatures = len(cards[0])
    for i in range(len(cards[0])):
        for j in range((len(cards))):
            currFeature.append(cards[j][i])
        if not (allSame(currFeature) or allDiffer(currFeature)):
            return False
        currFeature = []
    return True

def makeSuperSetDeck(dims):
    # This generates all possible cards with the given dimensions
    # and returns them in a sorted list.
    # For example, consider makeSuperSetDeck([3,4]):
    # Here, there are two features:
    #     * feature0 has 3 features ('A', 'B', or 'C')
    #     * feature1 has 4 features ('A', 'B', 'C', or 'D')
    # Each card in the deck includes an option from each feature,
    # resulting in this deck:
    # ['AA', 'AB', 'AC', 'AD', 'BA', 'BB', 'BC', 'BD', 'CA', 'CB', 'CC', 'CD']
    # Thus, makeSuperSetDeck([3,4]) returns that list.
    # Hint: use stringProduct() here!
    letters = ["A", "B", "C", "D", "E"]
    temp = ""
    features = []
    for i in range(len(dims)):
        for j in range(dims[i]):
            temp += letters[j]
        features.append(temp)
        temp = ""
    resultStrings = stringProduct(features)
    return resultStrings

def boardContainsSelection(board, selection):
    # helper function for checkSelectionIsSet()
    # Return True if every card in the selection (a list of cards) is
    # also on the board (another list of cards), and False otherwise.
    for card in selection:
        if card not in board:
            return False
    return True

def checkSelectionIsSet(board, selection, cardsPerSet):
    # Given a board (a list of cards from the deck), a selection
    # (a non-empty list of cards on the board), and the cardsPerSet
    # (a positive number of cards required to make a set), return True
    # if the selection is legal and in fact forms a set.
    # Instead of returning False, return a string with a
    # description of why the selection is not a set, as such:
    # 1. If the board is empty, return 'Empty board!'
    # 2. If the number of cards in the selection does not match the
    #    required number of cards in a set, return 'Wrong number of cards!'
    # 3. If any of the cards in the selection are not actually on the board,
    #    return 'Some of those cards are not on the board!'
    # 4. If any of the cards in the selection are duplicates,
    #    return 'Some of those cards are duplicates!'
    # 5. If the cards in the selection do not form a legal set,
    #    return 'Those cards do not form a set!'
    if board == []:
        return "Empty board!"
    elif len(selection) != cardsPerSet:
        return "Wrong number of cards!"
    elif not boardContainsSelection(board, selection):
        return "Some of those cards are not on the board!"
    for i in range(len(selection)):
        if selection[i] in selection[i+1:]:
            return "Some of those cards are duplicates!"
    if not isSet(selection):
        return "Those cards do not form a set!"
    return True

def findFirstSet(board, cardsPerSet):
    # helper function for dealUntilSetExists()
    # Given a possibly-empty board, and a positive number of cards per set,
    # loop over combinations(board, cardsPerSet) and return the
    # first list of cards that are on the board and form a set.  Return None
    # if there are no sets on the board.
    # Note that this function will be tested when we test dealUntilSetExists.
    # Hint: you will want to use the combinations() helper function
    # that we provided above.
    if board == []:
        return None
    combos = combinations(board, cardsPerSet)
    for combo in combos:
        if checkSelectionIsSet(board, combo, cardsPerSet) == True:
            return combo
    return None

def dealUntilSetExists(deck, cardsPerSet):
    # Start with an empty board.
    # Keep adding cards from the top of the deck (that is, "dealing")
    # (without modifying the deck) to the board until
    # there is a set among the cards in the board.
    # Return a sorted list of just the cards that form that set.
    # Notes:
    #  1. This function does not deal a fixed number of cards.  It keeps
    #     dealing until it finds a set, no matter how many cards that requires.
    #  2. You can ignore the error case where the deck runs out
    #     of cards before a set is found -- that is, you should never return None.
    # Hint: findFirstSet will be useful here.
    board = []
    i = 0
    while findFirstSet(board, cardsPerSet) == None:
        board.append(deck[i])
        i += 1
    result = findFirstSet(board, cardsPerSet)
    return sorted(result)

def getRandomBoardWithSet(dims, targetBoardSize):
    # Make a new SuperSet deck with the given dimensions,
    # then shuffle the deck, deal cards until a set is dealt.
    # Call that the foundSet.
    # Then, form a board starting with that set, and adding
    # more cards from the deck (that are not already in the set)
    # until the board is the given size.  Then sort and return it
    # in a tuple along with the foundSet.
    # Hint: to randomly shuffle a list L, do this:  random.shuffle(L),
    # which mutatingly shuffles (randomizes the order) of the list L.
    cardsPerSet = min(dims)
    deck = makeSuperSetDeck(dims)
    random.shuffle(deck)
    foundSet = dealUntilSetExists(deck, cardsPerSet)
    for card in foundSet:
       deck.remove(card) 
    board = copy.copy(foundSet)
    i = 0
    while len(board) < targetBoardSize:
       board.append(deck[i])
       i += 1
    board.sort()
    return(board, foundSet)

####################################################
# main function
####################################################

def main():
    runAppWithScreens(initialScreen='helpScreen')

main()
