import json
from question import Question
import requests

class Parser : 
    
    def __init__(self):
        self.importJsonFile()
        
        
    
    def importJsonFile(self) : 
        params = (('print', 'pretty'),)
        response = requests.get('https://caritas-50fab.firebaseio.com/survey.json', params=params)
        jsonString      = response.text;
        self.result     = json.loads(jsonString);
        
       
        
    def getQuestions(self):
    
        questionsAnswers   = []

        if self.result is None:
            return questionsAnswers
        
        for user in self.result : 
            try:
                for survey in self.result[user]:
                    for question in self.result[user][survey]["section_2"]:
                        if question == "name":
                            continue
                        q = self.result[user][survey]["section_2"][question]["text"]
                        a = self.result[user][survey]["section_2"][question]["choice"]
                        
                        #print q,a
                        questionsAnswers.append(Question(q,a))
                            
                            
            except Exception:
                print "Oops! " + user  + " does not participate in the campaign"
                
        return questionsAnswers   
        

    
    
