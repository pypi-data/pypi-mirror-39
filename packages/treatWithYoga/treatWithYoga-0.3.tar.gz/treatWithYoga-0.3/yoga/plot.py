import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
class Plot:
    def __init__(self):
        pass
    def revenue(pobject):   
        x=[]
        y=[]
        try:
            for i in pobject:
                x.append(i.id)
                y.append(i.getRev())     
            plt.bar(x,y) 
            plt.title('Revenue by Customer') 
            plt.xlabel('User ID') 
            plt.ylabel('Revenue') 
            plt.show()
            return True
        except:
            print("Invalid Patient Object passed for Plot")
            return False
    def exercise(pobject):   
        x=[]
        y=[]
        try:
            for i in pobject:
                x.append(i.name)
                y.append(i.time)     
            plt.bar(x,y) 
            plt.title('Time by Exercise') 
            plt.xlabel('User ID') 
            plt.ylabel('Time') 
            plt.show()
            return True
        except:
            print("Invalid Exercise Object passed for Plot")
            return False
