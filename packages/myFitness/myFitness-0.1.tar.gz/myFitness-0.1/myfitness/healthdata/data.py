class Person: 
    def __init__(self, name, age, gender):
        """Create a object of class Person()
        Parameters: name, age, gender
        
        Return: An object of class Person"""
        
        # assign the name, age, and gender to the class object in initialization
        self.name = name
        try: 
            self.age = int(age)
        except: 
            print("Age is an integer")
            self.age = None
        
        self.gender = gender
    
    def display(self):
        """Display the name, age and gender of a Person() object
        Parameters: Person() object

        Return: name, age, and gender"""
        
        # display the name, age, and gender of initialized object
        return "Name: {}, Age: {}, Gender: {}". format(self.name, self.age, self.gender)

class healthdata(Person): 
    def __init__(self, name, age, gender, file =''):
        """Create a object of class healthdata() this inherits from the superclass Person()
        Parameters: name, age, gender, file
        
        Return: An object of class healthdata"""
        
        # inherit Person class name, age, gender and assign to heathdata object      
        Person.__init__(self, name, age, gender)
        # assign the file to the object in initialization
        
        self.file = file
    
    def data(self):
        """Import the file assigned to the healthdata() object into a dataframe and assign it to the healthdata() object
        Parameters: healthdata() object initialized above
        
        Return: Display of healthdata object attributes name, age, gender and dataframe containing healthdata() object file"""
        
        import pandas as pd # ensure pandas is imported
        
        try: 
            self.data = pd.read_csv(self.file) # import the self.file into a dataframe using pandas
        except FileNotFoundError:
            print("File does not exist")
            return False
            
        Person.display(self) #display object attributes using inherited display() finction 
        return self.data
