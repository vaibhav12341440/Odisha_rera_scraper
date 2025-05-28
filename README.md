# Odisha_rera_scraper



**1. Import necessary libraries:**

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
```

* `selenium.webdriver`: This is the core Selenium library for interacting with web browsers.
* `selenium.webdriver.common.by.By`: Used to specify different locator strategies (e.g., by ID, by XPath, by class name).
* `selenium.webdriver.support.ui.WebDriverWait`: Used for explicit waits, allowing the script to wait for certain conditions to be met before proceeding.
* `selenium.webdriver.support.expected_conditions as EC`: Provides a set of predefined conditions that can be used with `WebDriverWait`.
* `webdriver_manager.chrome.ChromeDriverManager`: This library automatically downloads and manages the `chromedriver.exe` executable, which is required for Selenium to control the Chrome browser. This is a very convenient way to avoid `NoSuchDriverException` errors.
* `time`: Used for introducing delays (`time.sleep()`) in the script, which can be helpful for letting pages load completely.
* `pandas as pd`: A powerful library for data manipulation and analysis, used here to create and save a DataFrame to CSV.

**2. Start the browser and navigate:**

```python
# Start browser
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://rera.odisha.gov.in/projects/project-list")
time.sleep(5)
```

* `driver = webdriver.Chrome(ChromeDriverManager().install())`: This line initializes the Chrome WebDriver.
    * `ChromeDriverManager().install()`: This part checks your Chrome browser version, downloads the compatible `chromedriver.exe` if not already present, and returns the path to it.
    * `webdriver.Chrome(...)`: This then uses the path to launch a new Chrome browser instance, which Selenium will control. The `driver` object is your interface to this browser.
* `driver.get("https://rera.odisha.gov.in/projects/project-list")`: This command tells the browser to navigate to the specified URL, which is the project list page on the Odisha RERA website.
* `time.sleep(5)`: This pauses the script for 5 seconds, giving the page ample time to load all its content, especially dynamic elements that might be loaded via JavaScript.

**3. Initialize data storage and loop parameters:**

```python
data = []
NUM_PAGES = 3
```

* `data = []`: An empty list is created to store the extracted project information. Each project will be stored as a dictionary, and these dictionaries will be appended to this list.
* `NUM_PAGES = 3`: This variable defines how many pages of project data the script will attempt to scrape. You can change this value to scrape more or fewer pages.

**4. Loop through pages to scrape data:**

```python
for page in range(NUM_PAGES):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "tbody"))
    )

    rows = driver.find_elements(By.XPATH, "//table/tbody/tr")

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) >= 6:
            project = {
                "Project Name": cols[0].text.strip(),
                "Registration No.": cols[1].text.strip(),
                "Promoter Name": cols[2].text.strip(),
                "District": cols[3].text.strip(),
                "Project Type": cols[4].text.strip(),
                "Status": cols[5].text.strip()
            }
            data.append(project)

    # Next page navigation
    try:
        next_btn = driver.find_element(By.XPATH, "//a[contains(@class,'paginate_button next')]")
        if "disabled" in next_btn.get_attribute("class"):
            break # Exit loop if next button is disabled
        next_btn.click()
        time.sleep(3)
    except:
        break # Exit loop if next button is not found (e.g., last page)
```

This is the core scraping logic:

* **`for page in range(NUM_PAGES):`**: This loop iterates for the specified number of pages (e.g., 3 times).
* **`WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))`**: This is an explicit wait. It tells Selenium to wait for up to 10 seconds until the `<tbody>` (table body) element is present on the page. This is crucial for ensuring the table data has loaded before trying to scrape it.
* **`rows = driver.find_elements(By.XPATH, "//table/tbody/tr")`**: This line finds all table row (`<tr>`) elements within the `<tbody>` of the main table. `find_elements` returns a list of web elements.
* **`for row in rows:`**: This inner loop iterates through each row found on the current page.
* **`cols = row.find_elements(By.TAG_NAME, "td")`**: Inside each row, this finds all table data (`<td>`) cells.
* **`if len(cols) >= 6:`**: This check ensures that the row has at least 6 columns before attempting to extract data. This helps prevent errors if some rows have unexpected structures (e.g., header rows, empty rows).
* **`project = { ... }`**: A dictionary named `project` is created. Each key in the dictionary corresponds to a column name (e.g., "Project Name"), and its value is the text content of the respective table data cell (`cols[index].text.strip()`).
    * `.text`: Extracts the visible text content of the element.
    * `.strip()`: Removes any leading or trailing whitespace from the text.
* **`data.append(project)`**: The `project` dictionary (containing data for one row) is added to the `data` list.
* **Next Page Navigation:**
    * **`try...except` block**: This handles potential errors during navigation.
    * **`next_btn = driver.find_element(By.XPATH, "//a[contains(@class,'paginate_button next')]")`**: This tries to find the "Next" button for pagination. It uses an XPath to locate an `<a>` (anchor) tag that has the class `paginate_button` and `next`.
    * **`if "disabled" in next_btn.get_attribute("class"): break`**: It checks if the "Next" button has a "disabled" class. If it does, it means there are no more pages, so the loop breaks.
    * **`next_btn.click()`**: If the button is found and not disabled, this clicks it to navigate to the next page.
    * **`time.sleep(3)`**: A 3-second pause is added to allow the next page to load completely after clicking the "Next" button.
    * **`except: break`**: If for some reason the `next_btn` is not found (e.g., on the last page, or if the website structure changes), the `except` block catches the error and breaks out of the loop.

**5. Quit the browser:**

```python
driver.quit()
```

* `driver.quit()`: This is a crucial step. It closes the browser window and terminates the `chromedriver` process, freeing up system resources. It's good practice to always call `driver.quit()` when you are done with the browser.

**6. Save data to CSV:**

```python
# Save to CSV
df = pd.DataFrame(data)
df.to_csv("odisha_rera_projects.csv", index=False)
print("CSV file saved as 'odisha_rera_projects.csv'")
```

* `df = pd.DataFrame(data)`: The list of dictionaries (`data`) is converted into a Pandas DataFrame. Pandas DataFrames are tabular data structures that are very convenient for handling datasets.
* `df.to_csv("odisha_rera_projects.csv", index=False)`: This saves the DataFrame `df` to a CSV file named `odisha_rera_projects.csv`.
    * `index=False`: This prevents Pandas from writing the DataFrame's index as a column in the CSV file.
* `print("CSV file saved as 'odisha_rera_projects.csv'")`: A confirmation message is printed to the console.
