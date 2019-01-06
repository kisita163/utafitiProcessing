# -*- coding: latin-1 -*-
from __future__ import division
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter
import dominate
from dominate.tags import *
from django.utils.encoding import smart_str
import os
import json as js

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




    def createAndSaveSurveyImages(self, index, question, availableAnswers, frequences):
        patches, texts = plt.pie(frequences, shadow=False, startangle=90)
        plt.legend(patches, availableAnswers, loc="best")
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig('output/' + str(index) + '.png')

    def frequencyTableForQuestions(self,images=True,html=True,json=False):
        
        survey={}
        questions = []
        results   = []
        
        ii = 1
        
        for q in self.questions :
            if q.getQuestion() not in questions : 
                questions.append(q.getQuestion())
                #print q.getQuestion()
        
        for q in questions :
            
            answersSet,rep = self.frequencyTableForQuestion(q)
            percentages  = self.getPercentages(rep)
            
            #self.printResults(q,answersSet,percentages)
            
            percentages  = ["%.2f"%p for p in percentages]
            
            a = [{"choice" : t, "score": s} for t, s in zip(answersSet,percentages)]
            o = {"question": q , "answers": a} 
            
    
            results.append(o)
            
            if images == True :
                self.createAndSaveSurveyImages(ii, q, answersSet, rep)
            ii = ii + 1 
            
        
        survey['name']='Survey'
        survey['length']=len(questions)
        survey['results']=results
        
        if json == True : 
            f_json= open("output/results.json","w+")
            js.dump(survey,f_json,indent=2)
            f_json.close()    
            
        
        if html == True:
            f_html= open("output/results.html","w+")
            f_html.write(smart_str(self.getHtmlFromDictionary(survey)))
            
            smart_str(self.getHtmlFromDictionary(survey))
            f_html.close()   


    def printResults(self, question, answersSet, percentages):

        print question
        print "-------------------------------------------------------"
        
        ii = 0

        for answer in answersSet:
            print answer + "\t" + "%.2f" %percentages[ii] + " %"
            ii = ii + 1
        print ""
        print ""
        
        
    def getHtmlFromDictionary(self,survey):
        
        doc = dominate.document(title='Summary: {}'.format("utafiti"))
        
        with doc.head:
            style(  
            """table {
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
            }
            
            td, th {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }
            
            h1 {
                background-color: powderblue;
                font-family:courier;
                text-align: center;
                height: 100px;
            }
            
            h2 {
                background-color: #677cec;
                font-family:courier;
                text-align: left;
                padding: 50px;
                color: #FFFFFF;
                font-family: Arial, Helvetica, sans-serif;
            }
            
            tr:nth-child(even) {
                background-color: #dddddd;
            }""")
            meta(charset="UTF-8")
            
        with doc:
            div(id='header')#.add(h1("Utafiti"))
            br()
            br()
            with div():
                attr(cls='body')
                ii = 1
                for question in survey['results']:
                    div().add(h2(question['question']))
                    img(src= str(ii) + '.png', id='logo')
                    ii = ii + 1
                    #print question['question']
                    with table().add(tbody()):               
                        
                        for answer in question['answers']:
                            l = tr()
                            choice = answer['choice']
                            score  = answer['score'] + "%"
                        
                            l.add(td(choice))
                            l.add(td(score))
                            #print answer['choice'] + " " + answer['score']
                    br()
                    br()
                    br()
        
        return doc.render()


    def getPercentages(self,rep):

        numbers=sum(rep)
        percentages=[(x/numbers)*100 for x in rep]

        return percentages



                   
        
       

    
        
        
        
          
