# Player class, fields: life, score.
class Player:
    # constructor.
    def __init__(self, numberOfLife, startingScore, livingSituation):
        self.life = numberOfLife
        self.score = startingScore
        self.isDead = livingSituation
        self.lastHit = False

    # function to correct answer
    def correct(self):
        # score is up by 100
        self.score = self.score + 100
        # boolean value set to to true
        self.lastHit = True

    # function to incorrect answer
    def lost(self):
        # if last life remaining to player , game lost
        if self.life == 1:
            # boolean value to true indicate player is dead
            self.isDead = True
            self.life = 0
        # if player has life remaining , decrease it by one
        else:
            self.life = self.life - 1
        # boolean value set to to false
        self.lastHit = False

    # getters functions
    def lifeUpdate(self):
        return self.isDead

    def getScore(self):
        return self.score

    def getLife(self):
        return self.life

    def checkDead(self):
        return self.isDead

    def isLastHit(self):
        return self.lastHit

    # heart icons to show on screen.
    def getHeartLife(self):
        if self.life == 2:
            return "♥♥"
        if self.life == 1:
            return "♥"
        else:
            return "☠"

