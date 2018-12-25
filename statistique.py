from __future__ import division
from collections import Counter
import os

class Statistique:
       
    def addQuestions(self,questions):  
        self.questions = questions
         
        
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
                
    
        
        for q in questions :
            answersSet,rep = self.frequencyTableForQuestion(q)
            self.printResults(q,answersSet,rep)
            
            
        return questions

    def printResults(self, question, answersSet, rep):
        
        numbers=sum(rep)
        percentages=[(x/numbers)*100 for x in rep]

        print question
        print "----------------------------------------------------"
        
        ii = 0

        for answer in answersSet:
            print answer + "\t" + "%.2f" %percentages[ii] + " %"
            ii = ii + 1
        print ""
        print ""


                   
        
       

    
        
        
        
          
