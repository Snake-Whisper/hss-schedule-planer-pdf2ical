import PyPDF2

#URL = "https://www.hss-wiesloch.de/wp-content/uploads/2021/04/Jahreswochenplan21_22_FI_V2.pdf"
FILE = "Jahreswochenplan21_22_FI_V2.pdf"


pdfFileObj = open(FILE, 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
pageObj = pdfReader.getPage(0)
 
# extracting text from page
for line in pageObj.extractText().split():
    print (line)
 
# closing the pdf file object
pdfFileObj.close()
