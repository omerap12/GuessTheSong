import os
from threading import *
from tkinter import *
import wikipedia
from Classes.AnchorClass import Anchor
from Classes.PlayerClass import Player
from Classes.SongClass import Song
import random
import time
from tkinter import DISABLED
from pygame import mixer


# Game class, fields: musicData, player, Anchor
class Game:
    # constructor.
    def __init__(self, music, onePlayer, oneAnchor):
        self.musicData = music
        self.player = onePlayer
        self.size = len(music)
        self.isWon = False
        self.Anchor = oneAnchor
        self.check = False
        self.currentSong = None
        self.saveMeActivated = False
        self.saveMeTimes = 1
        self.stop = False

    # play function, play songs and get user input.
    def play(self):
        # initialize music player
        mixer.init()
        # game loop
        while True:
            # if no more songs left in database and player still alive
            if (self.size == 0) and (self.player.checkDead() == False):
                # wining message
                self.Anchor.winMessage()
                break
            # if no more songs left in database but player id dead
            if self.player.checkDead():
                # losing message
                self.Anchor.loseMessage()
                break
            # shuffle songs
            random.shuffle(self.musicData)
            # getting current song as field
            self.currentSong = self.musicData.pop()
            # loading song
            mixer.music.load(self.currentSong.getPath())
            # play song
            mixer.music.play()
            # size of database decreases by one
            self.size = self.size - 1
            # waiting 7 seconds for song to finish
            if self.stop:
                break
            # waiting for user input
            while not self.check:
                time.sleep(1)
            if self.check:
                # is user pressed on save me button
                if self.saveMeActivated:
                    # calling correct function
                    self.player.correct()
                    # update status bar function.
                    updateStatusBar()
                    # wait
                    time.sleep(1.5)
                    # set check to false (for waiting other user input)
                    self.check = False
                    # stop music
                    mixer.music.stop()
                    # set save me button to false
                    self.saveMeActivated = False
                    # decrease save me button times remaining by one
                    self.saveMeTimes = self.saveMeTimes - 1
                    self.check = False
                    continue
                # get the user input, deleting spaces before and after.
                guessPlayer = userSongGuess.strip()
                # stop music
                mixer.music.stop()
                # comparing user input to answer
                if guessPlayer.lower() == self.currentSong.getName().lower():
                    # correct function
                    self.player.correct()
                # if user was wrong
                else:
                    # incorrect function
                    self.player.lost()
                # update status bar
                updateStatusBar()
                # wait
                time.sleep(1.5)
                # set check to false
                self.check = False

    # setters
    def setCheck(self):
        self.check = True

    # save-button function (game mechanic)
    def save(self):
        # set activation status to True
        self.saveMeActivated = True
        # save me times decreased by one
        self.saveMeTimes = self.saveMeTimes - 1
        # set check to True
        self.check = True
        # if no more saves left disable button
        if (self.saveMeTimes == 0):
            saveMeButton["state"] = DISABLED

    # wining function, if is player still alive and no more songs left - he won
    def setWon(self):
        if (self.player.isDead == False) and (self.size == 0):
            # set won to True
            self.isWon = True
            # calling anchor
            self.Anchor.winMessage(self)

    # getters
    def getSongInfo(self):
        return self.currentSong.getInfo()

    def getIsActivate(self):
        return self.saveMeActivated

    def howManySavesLeft(self):
        return self.saveMeTimes

# global variable, indicate whether user pressed start or not.
isStarted = False

# function start threading
def threading():
    global isStarted
    if isStarted:
        return
    isStarted = True
    t1 = Thread(target=game.play)
    t1.start()


# function for songs initiating
def initSongs(songsData):
    f = open('songs.txt', 'r')
    all_lines = f.readlines()
    # read text file
    for i in range(0, len(all_lines) - 1, 2):
        # get index name of each song
        indexName = all_lines[i].strip()
        # getting it's true name
        songName = all_lines[i + 1].strip()
        # getting it's path
        path = os.getcwd() + '\\songs\\' + indexName
        # call wikiSearch function to get it's information
        info = wikiSearch(songName)
        # create song variable
        song = Song(songName, info, indexName, path)
        # add it to list
        songsData.append(song)
        songsNames.append(songName)


# function wikipedia - get info of song
def wikiSearch(songName):
    # calling function from package
    text = wikipedia.summary(songName)
    # return text
    return text


# save me button function.
def saveMeClick():
    # if game hasn't started yet, do nothing
    if not isStarted:
        return
    # if user has save me left
    if game.howManySavesLeft() > 0:
        # calling save function
        game.save()
        # update text
        songInfoLable['text'] = "Saved!\n" + game.getSongInfo()
        # changing button color to black
        saveMeButton.configure(bg="Black")


# enter button function.
def enterClick():
    # if game hasn't started yet, do nothing
    if not isStarted:
        return
    # calling global variable
    global userSongGuess
    try:
        # get user text
        userSongGuess = userGuess.get()
        # clear grid
        userGuess.delete(0, 'end')
        # sending input for evaluation
        game.setCheck()
        # get song info
        text = game.getSongInfo()
        while not game.check:
            time.sleep(0.2)
        time.sleep(0.3)
        # if user was right
        if player.isLastHit():
            songInfoLable['text'] = "Correct!\n" + text
        else:
            songInfoLable['text'] = "Wrong!\n" + text
    except AttributeError:
        return


# function that updating status bar: score and life remaining
def updateStatusBar():
    statsLable['text'] = "Live: " + (player.getHeartLife()) + "      Score: " + str(player.getScore())


# ending message to screen
def goodBye():
    print("Thanks for playing, songs names are:")
    for i in range(len(songsNames)):
        print(str(i + 1) + ": " + songsNames[i])


# initialize list for songs
songsData = []
# list just for song names
songsNames = []
# calling auxiliary function
initSongs(songsData)
# create player object with 2 life and 0 score
player = Player(2, 0, False)
# create anchor object
anchor = Anchor(player)
# create game object
game = Game(music=songsData, onePlayer=player, oneAnchor=anchor)
# create global variable
global userSongGuess

# tkinter implementation
root = Tk()
# title for the app
root.title("Guess The Song")
# entry for user input
userGuess = Entry(root, width=45, borderwidth=5)
# position
userGuess.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
# enter button
enterButton = Button(root, text="Enter", bg='green', font=('Arial', 13), padx=40, pady=20, command=enterClick)
# position
enterButton.grid(row=2, column=2)
# save me button
saveMeButton = Button(root, text="save me!", bg='pink', font=('Arial', 13), padx=22, pady=20, command=saveMeClick)
# position
saveMeButton.grid(row=2, column=1, columnspan=1)
# start button
startButton = Button(root, text="Start", bg='white', font=('Arial', 13), padx=40, pady=20, command=threading)
# position
startButton.grid(row=3, column=1, columnspan=2)
# song information lable
songInfoLable = Label(root, text="song info will be here", font=('Helvetica', 13), wraplength=300, justify="center")
# position
songInfoLable.grid(row=4, column=1, columnspan=2)
# status lable (life and score)
statsLable = Label(root, text="Live: " + player.getHeartLife() + "      Score: " + str(player.getScore()),
                   font=('Helvetica', 13), wraplength=300, justify="center")
# position
statsLable.grid(row=1, column=1, columnspan=3)
root.mainloop()
# goodbye function
goodBye()
