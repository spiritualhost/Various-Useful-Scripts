# Various Useful Scripts

A lot of scripts that are pretty raw and malleable, ready to be used for various purposes. Improvements can be made before pushing into any repeated use. 

## Included
- gzip_all - zips and compresses an entire directory of files (.tar.gz)
- qbkiller - kill some background processes that can cause network issues with QuickBooks Desktop
- openai_invoices - downloading copies of invoices from the brower page can take forever, especially the way OpenAI has it set up. With a little JS and a little python, this can be automated. I used pyinstaller to make the clone to usage process a little quicker, so use the .exe if that's better for you. 

    1) Login to the OpenAI API portal. Go to the invoices page located at https://platform.openai.com/settings/organization/billing/history. 
    2) (This needs to be done because of OpenAI's robots.txt) Paste the JS code into the console after Inspecting the OpenAI API invoices portal page. There should be a series of buttons that say "View" on the righthand side, with columns labeled Invoice, Status, Amount, and Created. It will spit out an array (right click on the array and "Copy Object"). Paste the array into "test.txt", over the previous data if any is still there (create test.txt in the same folder as the Python script if it isn't there already). 
    3) Run the openai.py script (You can double click the file itself, but it's recommended to run in the terminal). Give a date range. Every invoice captured in the scrape will be downloaded automatically so long as it lies within the range. Leave the terminal alone -- you can minimize it, but just ensure that nothing else is touching the downloads folder during operation. 

    ** This script works, but is messy and could really do with some refactoring. 