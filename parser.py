import PyPDF2
import datetime
import re
import calendar
import icalendar

#URL = "https://www.hss-wiesloch.de/wp-content/uploads/2021/04/Jahreswochenplan21_22_FI_V2.pdf"
FILE = "Jahreswochenplan21_22_FI_V2.pdf"
CURRENTYEAR = 2021

month_mapper = [[9,10,11,12,1,2], [3,4,5,6,7,8]]
month_on_limit = set()
current_month = 0
data_mapping = {}

pdfFileObj = open(FILE, 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
pageObj = pdfReader.getPage(0)

content = pageObj.extractText()
pdfFileObj.close()

#TODO Clean up file
half_year = content.split(f"{CURRENTYEAR+1}\n"*6)

def translate_day (text):
    days = {"Mo": "Mon", "Di": "Tue", "Mi": "Wed", "Do": "Thu", "Fr": "Fri", "Sa": "Sat", "So": "Sun"}
    for part in text.split():
        if part in days:
            return (text.replace(part, days[part]), days[part])

mydate = None
for line in half_year[0].split("\n"):
    if re.match("\d\d. (Mo|Di|Mi|Do|Fr|Sa|So)", line):
        trans = translate_day (line)
        mydate = datetime.datetime.strptime(trans[0], "%d. %a")
        mydate = mydate.replace (month = month_mapper[0][current_month])
        if mydate.month >= 9 and mydate.month <= 12:
            mydate = mydate.replace (year = CURRENTYEAR)
        else:
            mydate = mydate.replace (year = CURRENTYEAR + 1)
        if mydate.day >= calendar.monthrange(mydate.year, mydate.month)[1]:
            month_on_limit.add( mydate.month )
        assert mydate.strftime("%a") == trans[1], f"got: '{mydate.strftime('%a')}', but exspected '{trans[1]}'"
        while len(month_on_limit) < 6:
            current_month = (current_month + 1) % 6
            if month_mapper[0][current_month] not in month_on_limit:
                break
        data_mapping[mydate] = []
    elif mydate:
        data_mapping[mydate].append(line)
print(data_mapping)

def transform2ICal(classname):
    for date in [datevalue for datevalue in data_mapping if classname in data_mapping[classname]]:
        event = icalendar.Event()
