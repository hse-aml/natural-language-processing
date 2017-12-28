import requests
import json
import numpy as np
from collections import OrderedDict

class Grader(object):
    def __init__(self):
        self.submission_page = 'https://www.coursera.org/api/onDemandProgrammingScriptSubmissions.v1'
        self.assignment_key = '7DdYfMQFEeevjw7-W7Fr0A'
        self.parts = OrderedDict([('98mDT', 'Question2Vec'), 
                                  ('nc7RP', 'HitsCount'), 
                                  ('bNp90', 'DCGScore'), 
                                  ('3gRlQ', 'W2VTokenizedRanks'), 
                                  ('mX6wS', 'StarSpaceRanks')])
        self.answers = {key: None for key in self.parts}

    @staticmethod
    def ravel_output(output):
        '''
           If student accidentally submitted np.array with one
           element instead of number, this function will submit
           this number instead
        '''
        if isinstance(output, np.ndarray) and output.size == 1:
            output = output.item(0)
        return output

    def submit(self, email, token):
        submission = {
                    "assignmentKey": self.assignment_key, 
                    "submitterEmail": email, 
                    "secret": token, 
                    "parts": {}
                  }
        for part, output in self.answers.items():
            if output is not None:
                submission["parts"][part] = {"output": output}
            else:
                submission["parts"][part] = dict()
        request = requests.post(self.submission_page, data=json.dumps(submission))
        response = request.json()
        if request.status_code == 201:
            print('Submitted to Coursera platform. See results on assignment page!')
        elif u'details' in response and u'learnerMessage' in response[u'details']:
            print(response[u'details'][u'learnerMessage'])
        else:
            print("Unknown response from Coursera: {}".format(request.status_code))
            print(response)

    def status(self):
        print("You want to submit these parts:")
        for part_id, part_name in self.parts.items():
            answer = self.answers[part_id]
            if answer is None:
                answer = '-'*10
            print("Task {}: {}".format(part_name, answer[:100] + '...'))
               
    def submit_part(self, part, output):
        self.answers[part] = output
        print("Current answer for task {} is: {}".format(self.parts[part], output[:100] + '...'))

    def submit_tag(self, tag, output):
        part_id = [k for k, v in self.parts.items() if v == tag]
        if len(part_id) != 1:
            raise RuntimeError('cannot match tag with part_id: found {} matches'.format(len(part_id)))
        part_id = part_id[0]
        self.submit_part(part_id, str(self.ravel_output(output)))
