
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Start browser
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://rera.odisha.gov.in/projects/project-list")
time.sleep(5)

data = []
NUM_PAGES = 3

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

    # Next page
    try:
        next_btn = driver.find_element(By.XPATH, "//a[contains(@class,'paginate_button next')]")
        if "disabled" in next_btn.get_attribute("class"):
            break
        next_btn.click()
        time.sleep(3)
    except:
        break

driver.quit()

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("odisha_rera_projects.csv", index=False)
print("CSV file saved as 'odisha_rera_projects.csv'")
