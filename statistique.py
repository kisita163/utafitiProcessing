import matplotlib.pyplot as plt
from collections import Counter

class Statistique:
    def __init__ (self,questions):
        self.questions = questions;
        
    
        
    def frequencyTableForQuestion(self,question):
        
        answers    = []
        answersSet = []
        rep        = []
        
        for q in self.questions :
            if q.getQuestion() == question :
                answers.append(q.getAnswer())
        freq = Counter(answers)
        
        for answer in answers:
            if answer not in answersSet : 
                answersSet.append(answer)
                rep.append(freq[answer])
                #print '%s : %d' % (answer, freq[answer])
        return answersSet,rep
 
      

    
        
    def frequencyTableForQuestions(self):
        
        questions = []
        
        for q in self.questions :
            if q.getQuestion() not in questions : 
                questions.append(q.getQuestion())
                #print q.getQuestion()
                
    
        ii = 1;
        
        for q in questions :
            answersSet,rep = self.frequencyTableForQuestion(q)
            plt.figure(ii)        
            #plt.subplot(x*100 + 10 + ii)
            patches, texts = plt.pie(rep, shadow=False, startangle=90)
            plt.legend(patches,answersSet, loc="best")
            plt.axis('equal')
            plt.title(q)
            #plt.tight_layout()
            ii = ii + 1 
        plt.show()    
            
        