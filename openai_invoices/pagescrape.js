    // Invoice number is at the first spot, price is at the third, date the fourth

    // Paste the following code into the console in the browser after inspecting the page:
    
    const tds = Array.from(document.querySelectorAll("td"));

    const tdTexts = tds.map(td => {
        const link = td.querySelector("a.lkCln");
        return link ? link.href : td.textContent.trim();
    });
    
    console.log(tdTexts);

    // The javascript will output an array. Copy and paste the object into "test.txt". 