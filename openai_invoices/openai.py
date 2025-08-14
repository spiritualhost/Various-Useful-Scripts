import pandas as pd
from datetime import datetime
import ast

#Convert date given by user to an integer
def datestringToDatetime(position: str):
    datestring = input(f"Give me the {position} date in the range as 'mm/dd/yyyy': ").strip().lower()
    datetimeFormatted = pd.to_datetime(datestring, format="%m/%d/%Y").date()
    return datetimeFormatted


#Get the date range
try:
    #Set goodrange to 1 when the last date is after the first date
    goodrange = 0

    firstDate = datestringToDatetime("first")
    lastDate = datestringToDatetime("last")
    difference = (lastDate-firstDate).days

    #Check that the range works
    while goodrange == 0:
        #Less than 0, not less than or equal to, so as to allow all invoices from one day
        if difference < 0:
            print(f"That second date won't work here. Try a date after {firstDate}")
            firstDate = datestringToDatetime("first")
            lastDate = datestringToDatetime("last")
            difference = (lastDate-firstDate).days

        else:
            print(f"Ok! Let's get all the invoices between {firstDate} and {lastDate}!")
            goodrange += 1


except Exception as e:
    print(f"Date error: {e}")
    quit()



#Invoice number is at the first spot, price is at the third, date the fourth

#Paste the following code into the console in the browser after inspecting the page:
#const tds = Array.from(document.querySelectorAll("td"));

#const tdTexts = tds.map(td => {
#    const link = td.querySelector("a.lkCln");
#    return link ? link.href : td.textContent.trim();
#});
#
#console.log(tdTexts);

#The javascript will output an array. Copy and paste the object into "test.txt" above. 



with open("test.txt", "r") as f:
    rawString = f.read()

#Raw list of all items
rawList = ast.literal_eval(rawString)



#Parse the data into a dictionary
rawData = {"invoice": [], 
           "price": [], 
           "date": [],
           "link": []}

for i in range(len(rawList)):
    #Invoice numbers
    if i == 0 or i % 5 == 0:
        rawData["invoice"].append(rawList[i])
    
    #Prices
    elif "$" in rawList[i] and "stripe.com" not in rawList[i]:
        rawData["price"].append(rawList[i])


    #Dates
    elif " AM" in rawList[i] or " PM" in rawList[i]:

        #do the date conversion here
        rawData["date"].append(rawList[i])

    #Links
    elif "stripe.com" in rawList[i]:
        rawData["link"].append(rawList[i])

#Testing
#print(rawData["invoice"])
#print(rawData["price"])
#print(rawData["date"])
#print(rawData["link"])



slice_a = 0
slice_b = len(rawData["date"])-1
print(slice_b)


#Get slice range that matches [firstDate: lastDate]
for i in range(len(rawData["date"])):

    #Convert string date from dictionary to datetime object
    dateConverted = datetime.strptime(rawData["date"][i], "%b %d, %Y, %I:%M %p").date()

    #Difference between final range value and current list date value
    lastDifference = (lastDate - dateConverted).days
    print(difference)

    #Difference between first range value and current list date value
    firstDifference = (firstDate - dateConverted).days
    print(firstDifference)

    #If the current date is larger than the entire range
    if lastDifference <= 0:
        slice_a = i
    elif firstDifference <= 0:
        slice_b = i


print(slice_a, " ", slice_b)


    


