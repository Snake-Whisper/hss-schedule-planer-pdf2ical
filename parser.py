import PyPDF2
import os 
import re
import datetime

class YearlySchedule:
    
    def __init__(self, path):
        with open( path, 'rb' ) as pdf:
            Reader = PyPDF2.PdfFileReader( pdf )
            PageObject = Reader.getPage(0)
            self.ScheduleRaw = PageObject.extractText().split('\n')
        
        self.filterData()
    
    def filterData(self):
        self.ScheduleData = []
        
        for data in self.ScheduleRaw:
            FoundClass = re.findall("\AE\d\BFI", data)
            FoundDate  = re.findall("[0123][0-9][.][ ][][MDFS][oira]", data)

            if FoundDate or FoundClass: 
                     
                self.ScheduleData.append(data)
            
    def TreeObject(self):
        Object = { '1': {}, '2': {}, '3': {}, '4': {}, '5': {}, '6': {}, '7': {}, '8': {}, '9': {}, '10': {}, '11': {}, '12': {} }
        Limit  = { '1': 30, '2': 31, '3': 30, '4': 31, '5': 31, '6': 28, '7': 31, '8': 30, '9': 31, '10': 30, '11': 31, '12': 31 }
        
        day    = ['mo', 'di', 'mi', 'do', 'fr', 'sa', 'so']
        
        zMonth = 0
        
        Done = False
        secoundHalf = False
        
        for data in self.ScheduleData:
            
            if len(data) == 6:
                if data[2] == '.' and data[4:6].lower() in day:
                    
                    name = data.replace(' ', '')
                    zMonth += 1

                    if zMonth > 6 and secoundHalf == False:
                        zMonth = 1
                    elif zMonth > 12 and secoundHalf:
                        zMonth = 7

                    if len(Object[ str(zMonth) ]) + 1 > Limit[ str(zMonth) ]:
                        zMonth += 1
                        for i in range(zMonth, 7):
                            if len(Object[ str(i) ]) + 1 <= Limit[ str(i) ]:
                                zMonth = i
                                Done   = True
                                break 
                        if Done == False:
                            for a in range(1, 7):
                                if len(Object[ str(a) ]) + 1 <= Limit[ str(a) ]:
                                    zMonth = a
                                    Done   = True
                                    break
                            if Done == False:
                                secoundHalf = True
                                for b in range(7, 13):
                                    if len(Object[ str(b) ]) + 1 <= Limit[ str(b) ]:
                                        zMonth = b
                                        break 
                                                     
                    Object[ str(zMonth) ][ str(name) ] = []
                    
                else:
                    if data[1] != '.' and data[2] != '.':
                        Object[ str(zMonth) ][ str(name) ].append( data )
            
            else:
                if len(data) > 2:
                    if data[1] != '.' and data[2] != '.':
                        Object[ str(zMonth) ][ str(name) ].append( data )
                        
            Done = False        
            
        """
        * Structur:
        *           Month       ->  1 = September ... 12 = August
        *           └01.Mo      ->  01.Mo | Key : [ 'E1FI1', 'E2FI1', ... ]
        *            └E1FI1
        *            └E2FI1
        *            └E3FI1
        *            └E1FI2
        *           └02.Di
        *            └E2FI1     ->  E2FI1 String
        *            └...
        """  
        return Object    
    
        
if __name__ == '__main__':
    Stundenplan = YearlySchedule( os.getcwd().replace('\\', '/') + '/Jahreswochenplan21_22_FI_V2.pdf')

    new = Stundenplan.TreeObject()
    print(new['8'])