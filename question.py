

class Question :
    
    def __init__(self,question,choice):
        self.question = question
        self.choice   = choice
        
    def printQuestion(self):
        print self.question + ' -> ' + self.choice
        
    def getQuestion(self):
        return self.question
    
    def getAnswer(self):
        return self.choice