#file Exercise.py

class Exercise():
    _registery = []
    def __init__(self, name, time):
        self._registery.append(self) 
       
        try:
            if len(name) <= 1:
                raise ValueError('Invalid name')
            else:
                self.name = name
        except ValueError:
            print("Invalid name")
            self.name = None
        try:
            self.time = int(time)
        except: 
            self.time = None

    def display(self):
        print("Name of exercise: ", self.name)
        print("Time of exercise in minutes: ", self.time)
        return(0)