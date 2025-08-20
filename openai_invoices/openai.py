import pandas as pd
from datetime import datetime
import ast, os, time, glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



#Convert date given by user to an integer
def datestringToDatetime(position: str):
    datestring = input(f"Give me the {position} date in the range as 'mm/dd/yyyy': ").strip().lower()
    datetimeFormatted = pd.to_datetime(datestring, format="%m/%d/%Y").date()
    return datetimeFormatted


#Download invoice by following provided link
def invoiceGrabbed(link: str):


    options = Options()
    options.add_argument("--headless")

    # Configure Firefox profile to download PDFs automatically
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)  # use custom folder
    profile.set_preference("browser.download.dir", os.path.join(os.path.expanduser("~"), "Downloads"))
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    profile.set_preference("pdfjs.disabled", True)  # disable built-in PDF viewer

    # Attach profile to options
    options.profile = profile

    # Launch browser
    driver = webdriver.Firefox(options=options)
    driver.get(link)

    # Click the download button
    download_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[contains(text(),'Download invoice')]]")
        )
    )
    download_button.click()

    # Wait a few seconds to allow the download to start
    time.sleep(10)

    driver.quit()


#Rename the most recently downloaded file with proper formatting
#Give the function the previously sliced lists and traverse them backwards (the most recently downloaded PDF will be the last one in the list, the most recent)
def renameRecent(prices: list, dates: list, invoices: list):
    
    #Get downloads folder (cross-platform), then get list of all applicable PDFs in the download folder
    downloads_path = os.path.expanduser("~/Downloads")

    #get list of all applicable PDFs in the download folder
    pdfs = [pdf for pdf in glob.glob(os.path.join(downloads_path, "*.pdf")) if "Invoice-" in pdf]
    pdfs.sort(key=os.path.getmtime, reverse=True)
    print(pdfs)

    for i in range(len(invoices)):
        for j in range(len(pdfs)):
            if invoices[i] in pdfs[j]:
                os.rename(pdfs[j], os.path.join(downloads_path, f"{dates[i]} OpenAI Invoice {invoices[i]} {prices[i]}.pdf"))
                break

    return 0
    

#Main body of script

if __name__ == "__main__":


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


    #Paste the JS output into test.txt before this (preferably before the script runs)

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



    #Filter the dictionary for the date range we want

    #Range above given is [firstDate: lastDate]


    try:
        #Going over the index of the date list (organized from latest date to earliest date) in rawData, check if the datetime version of that date is before (i.e, the diff is neg or zero for same day) 
        #or after (i.e., the diff is positive) the last date in the user-provided range

        slice_a_list = [i for i in range(len(rawData["date"])-1) if (datetime.strptime(rawData["date"][i], "%b %d, %Y, %I:%M %p").date() - lastDate).days <= 0]
        slice_a = slice_a_list[0]

        #Doing the opposite for the earliest date (slice_b), which will be the value furthest along in the list that isn't earlier than the firstDate value

        slice_b_list = [i for i in range(len(rawData["date"])-1) if (datetime.strptime(rawData["date"][i], "%b %d, %Y, %I:%M %p").date() - firstDate).days >= 0]
        slice_b = slice_b_list[-1]

    except Exception as e:
        print(f"Slice issue: {e}")
        quit()




    #Get filtered dictionary links
    invoices = rawData["invoice"][slice_a:slice_b]
    prices = rawData["price"][slice_a:slice_b]
    dates = rawData["date"][slice_a:slice_b]
    links = rawData["link"][slice_a:slice_b]


    #The invoice.stripe.com links are accessible to anybody, signed in or not, because of the cryptography that goes into their generation
    #Selenium will headlessly open each of the invoice links, download to a folder, prenamed

    #Testing
    #print(links)


    #Get start time, helps tell how long the script runs for
    starttime = datetime.now()


    #Create progress bar
    done = "#"
    todo = "~"
    fullbar = str(todo*len(links))
    
    
    print("Progress: ", fullbar)

    for i in range(len(links)):
        invoiceGrabbed(links[i])
        
        progress = str(done*(i+1)) + str(todo*(len(links)-(i+1)))        
        print("Progress: ", progress, f"{round(((i+1)*100)/len(links), 2)}% complete")



    #Convert dates list to remove illegal characters
    dates = [
        datetime.strptime(d, "%b %d, %Y, %I:%M %p").strftime("%m-%d-%Y")
        for d in rawData["date"][slice_a:slice_b]
    ]

    renameRecent(prices, dates, invoices)


    #How long did the script run for
    endtime = datetime.now()
    print("This operation took ", endtime-starttime)