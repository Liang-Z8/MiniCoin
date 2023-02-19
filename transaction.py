import json
from utils import *

class Transaction:
    def __init__(self, inputs, outputs, private_key):
        self.inputs = inputs    
        self.outputs = outputs
        if not inputs:
            self.signature = ''
        else:
            self.signature = self.sign(private_key)
        self.number = self.get_number()

    # def to_dict(self):
    #     return {
    #         "number": self.number,
    #         "input": [input.to_dict() for input in self.inputs],
    #         "output": [output.to_dict() for output in self.outputs],
    #         "sig": self.signature.encode(encoder=nacl.encoding.HexEncoder).decode('utf-8')
    #     }

    def to_json(self):
        return json.dumps(self.to_json_ob)

    def to_json_ob(self):
        data = {
            "number": self.number,
            "input": self.inputs,
            "output": self.outputs,
            "sig": self.signature
        }
        return data

    def get_number(self):
        data = {
            "input": self.inputs,
            "output": self.outputs,
            "sig": self.signature
        }
        data_str = json.dumps(data)
        return hash(data_str)

    def sign(self, private_key):
        message = {
            "input": self.inputs,
            "output": self.outputs
        }
        message = json.dumps(message)
        return sign(message, private_key)
