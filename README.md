# Various Useful Scripts

A lot of scripts that are pretty raw and malleable, ready to be used for various purposes. Improvements can be made before pushing into any repeated use. 

## Included
- gzip_all - zips and compresses an entire directory of files (.tar.gz)
- openai_invoices - downloading copies of invoices from the brower page can take forever, especially the way OpenAI has it set up. With a little JS and a little python, this can be automated.
    1) Paste the JS code into the console after Inspecting the OpenAI API invoices portal page. There should be a series of buttons that say "View" on the righthand side. It will spit out an array. Paste the array into "test.txt". 
    2) Run the openai.py script. Give a date range. Every invoice captured in the scrape will be downloaded automatically so long as it lies within the range. 