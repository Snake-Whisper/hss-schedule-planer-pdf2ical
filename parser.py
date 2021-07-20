import PyPDF2

class YearlySchedule:
    
    def __init__(self, path):
        with open( path, 'rb' ) as pdf:
            Reader = PyPDF2.PdfFileReader( pdf )
            PageObject = Reader.getPage(0)
            self.ScheduleRaw = PageObject.extractText().split('\n')
    
    def TreeObject(self):
        Object = { '1': {}, '2': {}, '3': {}, '4': {}, '5': {}, '6': {}, '7': {}, '8': {}, '9': {}, '10': {}, '11': {}, '12': {} }
        Limit  = { '1': 30, '2': 31, '3': 30, '4': 31, '5': 31, '6': 28, '7': 31, '8': 30, '9': 31, '10': 30, '11': 31, '12': 31 }
        
        day    = ['mo', 'di', 'mi', 'do', 'fr', 'sa', 'so']
        
        zMonth = 0
        
        Done = False
        secoundHalf = False
        
        """
        TODO    self.ScheduleRaw 
        !       REMOVE      first 7 lines
        !       REMOVE      2021 2022 strings (like first 7)
        !       REMOVE      last 19 lines (JUNK)
        !   OR 
        §       FILTER FOR MASK 
        §           DATE: (2[01-31] + '. ' + [MO-SO])
        §           CLASS:  ('E' + [1-4]) + ('Fl' + [1-4])
        §                                 + ('Fl' + [A-Z] + [1-4])
        §       PROBLEM:
        §                 HOW TO DEAL WITH PUBLIC HOLIDAYS LIKE 'XMAS'
        §   OR
        """
        
        for data in self.ScheduleRaw[6:-19]:
            
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
    Stundenplan = YearlySchedule('Jahreswochenplan21_22_FI_V2.pdf')
    
    new = Stundenplan.TreeObject()
    for key, value in new.items():
        print(value)