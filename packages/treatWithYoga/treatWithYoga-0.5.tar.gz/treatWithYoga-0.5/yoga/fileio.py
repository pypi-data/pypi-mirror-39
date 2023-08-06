
import csv
class ExportUsers:
    def __init__(self):
        pass
    def pcsv(pobject,filename):
        try:
            with open(filename, 'w', newline='') as csvfile:
                uwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for i in pobject:
                    uwriter.writerow([i.id, i.password, i.salution, i.getfName(),i.getmName(), i.getlName(), i.getRev()])
            return True
        except:
            print("Error while exporting patiient file")
            return False
    def ecsv(pobject,filename):
        try:
            with open(filename, 'w', newline='') as csvfile:
                uwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for i in pobject:
                    uwriter.writerow([i.name, i.time])
            return True
        except:
            print("Error while exporting exercise file")
            return False
