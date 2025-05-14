from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import time, os, csv

# Load credentials
load_dotenv()
EMAIL = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")

# Job parameters
JOB_TITLE = "DevOps Engineer"
LOCATION = "Bangalore"
COVER_LETTER_TEXT = "Dear Hiring Manager, I am a passionate DevOps engineer with 3 years of experience..."

# Chrome Options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-gpu")
options.add_argument("--log-level=3")

# Set up ChromeDriver
chromedriver_path = r"C:\Users\akhil\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

# ✅ Define wait after initializing the driver
wait = WebDriverWait(driver, 10)

def login():
    driver.get("https://www.linkedin.com/login")
    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(EMAIL)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(3)

def search_jobs():
    search_url = f"https://www.linkedin.com/jobs/search/?keywords={JOB_TITLE}&location={LOCATION}&f_AL=true"
    driver.get(search_url)
    time.sleep(3)

def apply_to_jobs():
    job_cards = driver.find_elements(By.CLASS_NAME, "job-card-container__link")

    print(f"Found {len(job_cards)} jobs")
    applied_jobs = []

    for card in job_cards:
        try:
            card.click()
            time.sleep(2)

            easy_apply_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "jobs-apply-button")))
            easy_apply_btn.click()
            time.sleep(2)

            # Check if it's a simple application
            try:
                submit_btn = driver.find_element(By.XPATH, "//button[@aria-label='Submit application']")
                if COVER_LETTER_TEXT:
                    try:
                        textarea = driver.find_element(By.TAG_NAME, "textarea")
                        textarea.clear()
                        textarea.send_keys(COVER_LETTER_TEXT)
                    except:
                        pass
                submit_btn.click()
                print("✅ Applied successfully.")
                applied_jobs.append(driver.current_url)
            except:
                print("⚠️ Multi-step application. Skipping...")
                driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']").click()
        except Exception as e:
            print(f"❌ Error applying: {e}")
            continue

    with open("applied_jobs_log.csv", "a", newline="") as file:
        writer = csv.writer(file)
        for job in applied_jobs:
            writer.writerow([job, time.strftime("%Y-%m-%d %H:%M:%S")])

def close():
    driver.quit()

# Main flow
login()
search_jobs()
apply_to_jobs()
close()
