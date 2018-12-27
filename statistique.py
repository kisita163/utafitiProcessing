from __future__ import division
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter
import json
import os

class Statistique:

    def __init__(self):
        if not os.path.exists("output"):
            os.makedirs("output")
       
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
        results   = []
        f= open("output/results.json","w+")
        ii = 1
        
        for q in self.questions :
            if q.getQuestion() not in questions : 
                questions.append(q.getQuestion())
                #print q.getQuestion()
        
        for q in questions :
            
            answersSet,rep = self.frequencyTableForQuestion(q)
            self.printResults(q,answersSet,rep)
            percentages  = self.getPercentages(rep)
            survey={}
            
            percentages  = ["%.2f"%p for p in percentages]
            
            a = [{"choice" : t, "score": s} for t, s in zip(answersSet,percentages)]
            o = {"question": q , "answers": a} 
            
    
            results.append(o)

            patches, texts = plt.pie(rep, shadow=False, startangle=90)
            plt.legend(patches,answersSet, loc="best")
            plt.axis('equal')
            plt.title(q)
            plt.tight_layout()
            plt.savefig('output/'+str(ii)+'.png')
            ii = ii + 1 
            
        
        survey['name']='Survey'
        survey['length']=len(questions)
        survey['results']=results


        json.dump(survey,f,indent=2)
        f.close()       


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


    def getPercentages(self,rep):

        numbers=sum(rep)
        percentages=[(x/numbers)*100 for x in rep]

        return percentages



                   
        
       

    
        
        
        
          
