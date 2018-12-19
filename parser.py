import json
from question import Question

class Parser : 
    
    def __init__(self,jsonPath):
        self.jsonPath = jsonPath;
        self.importJsonFile()
        
        
    
    def importJsonFile(self) : 
        self.jsonFile   = open(self.jsonPath, "r");
        jsonString      = self.jsonFile.read();
        self.result     = json.loads(jsonString);
        
       
        
    def getQuestions(self):
    
        questionsAnswers   = [] 
        
        for user in self.result['survey'] : 
            try:
                for survey in self.result['survey'][user]:
                    for question in self.result['survey'][user][survey]["section_2"]:
                        if question == "name":
                            continue
                        q = self.result['survey'][user][survey]["section_2"][question]["text"]
                        a = self.result['survey'][user][survey]["section_2"][question]["choice"]
                        
                        #print q,a
                        questionsAnswers.append(Question(q,a))
                            
                            
            except Exception:
                print "Oops! " + user  + " does not participate in the campaign"
                
        return questionsAnswers   
        

    
    