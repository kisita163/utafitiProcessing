import json
import csv
import requests
from question import Question
from xlsxwriter.workbook import Workbook
from django.utils.encoding import smart_str


class Parser : 
    
    def __init__(self):
        self.importJsonFile()
        
        
    
    def importJsonFile(self) : 
        params = (('print', 'pretty'),)
        response = requests.get('https://caritas-50fab.firebaseio.com/survey.json', params=params)
        jsonString      = response.text;
        self.result     = json.loads(jsonString);


    def dropRawData(self,csv_output=True):
    
        database     = []

        variables    = ['agent_id', 'survey_id', 'country', 'city', 'latitude', 'longitude', 'start_time', 'end_time', 'date'] #default variables
        ################      0           1         2         3          4          5           6            7           8

        for a in self.getQuestionsSet():
            variables.append(smart_str(a.strip()))
            
        database.append(variables)
        
        if self.result is not None:
            for user in self.result :
                try:
                    for survey in self.result[user]:
                        user_result = []
                        user_result.insert(0,smart_str(user))
                        user_result.insert(1,smart_str(survey))

                        for m in self.result[user][survey]["section_1"]:

                            if m == 'address':

                                user_result.insert(2,smart_str(self.result[user][survey]["section_1"][m]['country']).strip())
                                user_result.insert(3,smart_str(self.result[user][survey]["section_1"][m]['city']).strip())
                                user_result.insert(4,smart_str(self.result[user][survey]["section_1"][m]['latitude']).strip())
                                user_result.insert(5,smart_str(self.result[user][survey]["section_1"][m]['longitude']).strip())

                            if m == 'startTime':
                                user_result.insert(6,smart_str(self.result[user][survey]["section_1"][m]).strip())

                            if m == 'endTime':
                                user_result.insert(7,smart_str(self.result[user][survey]["section_1"][m]).strip())

                            if m == 'date':
                                user_result.insert(8,smart_str(self.result[user][survey]["section_1"][m]).strip())
                        
                        for question in self.result[user][survey]["section_2"]:
                            if question == "name":
                                continue
                            #q = self.result[user][survey]["section_2"][question]["text"]
                            a = self.result[user][survey]["section_2"][question]["choice"]
                            #variables.append(q)
                            user_result.append(smart_str(a.strip()))

                        database.append(user_result)
                               
                except Exception as e:
                    print str(e)

        if csv_output == True:
            self.writeCsv(database)
        return database


    def writeCsv(self,database):

        with open('output/results.csv', 'wb') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(database)

        csvFile.close()
        

    def getQuestionsSet(self):

        questions   = [] 
        
        for user in self.result : 
            try:
                for survey in self.result[user]:
                    for question in self.result[user][survey]["section_2"]:
                        if question == "name":
                            continue
                        q = self.result[user][survey]["section_2"][question]["text"]

                        if q not in questions:
                            questions.append(q)
                            
                            
            except Exception:
                print "Oops! " + user  + " does not participate in the campaign"
       
        return [x.encode('utf-8') for x in questions]
        
       
        
    def getQuestions(self):
    
        questionsAnswers   = [] 
        
        if self.result is not None:
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
