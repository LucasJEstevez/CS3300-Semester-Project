#This test was acquired from ChatGPT, playwright was decided on for its simplicity and lack of requirements compared to selenium and web drivers.
#This test searches the buypage on the website and finds a certain dropdown menu and criteria, and returns with an error mismatch if the filtering failed

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    print("--- Year Test Initiated ---")
    browser = p.chromium.launch(headless=True)  # Launch headless browser
    page = browser.new_page()

    # Navigate to the page
    page.goto("https://cs3300-semester-project-d9a9.onrender.com/buy")

    # Find and click the Year dropdown
    page.click("div.dropbtn:has-text('Year')")  # Click on the 'Year' dropdown by its text
    print("Found Year dropdown menu.")

    # Wait for 5 seconds to ensure the dropdown and year options are loaded
    page.wait_for_timeout(5000)

    # Click the chosen year option directly (without filling the input)
    page.click("div#yearDrop a:has-text('2023')")
    print("Found 2023")

    # Wait for the table rows to be filtered (wait for at least one row to appear)
    page.wait_for_selector("table tr")

    # Get all the rows in the table
    rows = page.query_selector_all("table tr")

    # Wait until the number of rows is updated after filtering
    while len(rows) == 0:
        rows = page.query_selector_all("table tr")
        page.wait_for_timeout(1000)  # Wait 1 second before checking again

    # Check if the rows are filtered correctly
    for row in rows:
        cells = row.query_selector_all("td")
        if len(cells) > 0:  # Make sure there are cells in the row
            # Compare the first cell to ensure the year is filtered correctly
            assert cells[0].text_content().strip() == "2023", f"Year mismatch: {cells[0].text_content()}"

    print("--- Test Passed! ---")

    browser.close()