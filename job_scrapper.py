# Libraries
import time
import pandas as pd
# ------------- #
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from urllib3.util.timeout import Timeout
from urllib.parse import urlparse
import requests
import chromedriver_autoinstaller

timeout = Timeout(connect=5)

chromedriver_autoinstaller.install()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

# Driver path
driver = webdriver.Chrome(options=chrome_options)

# Maximize Window
driver.maximize_window()
driver.minimize_window()
driver.maximize_window()
driver.switch_to.window(driver.current_window_handle)
driver.implicitly_wait(10)

# Enter to the site
driver.get('https://www.linkedin.com/login');
time.sleep(2)

# Accept cookies
#driver.find_element_by_xpath("/html/body/div/main/div[1]/div/section/div/div[2]/button[2]").click()

# User Credentials
user_name = 'maria.real.estate.dxb@gmail.com'
password = 'masha123'
driver.find_element_by_xpath('//*[@id="username"]').send_keys(user_name)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
time.sleep(1)

# Login button
driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button').click()
driver.implicitly_wait(30)

# Jobs page
#driver.find_element_by_xpath('//*[@href="https://www.linkedin.com/jobs/?"]').click()
#time.sleep(3)

def collectLinks():
    # Go to search results directly
    driver.get("https://www.linkedin.com/jobs/search/?geoLocation=riyadh&location=riyadh&f_TPR=r86400")
    time.sleep(1)

    # Get all links for these offers
    links = []
    jobs_dict = {}
    # Navigate 13 pages
    print('Links are being collected now.')
    try:
        for page in range(2,14):
            time.sleep(2)
            #jobs_block = driver.find_element_by_class_name('jobs-search-results__list')
            jobs_list= driver.find_elements(By.CSS_SELECTOR, '.jobs-search-results__list-item')

            for job in jobs_list:
                all_links = job.find_elements_by_tag_name('a')
                print(all_links)
                for a in all_links:
                    if str(a.get_attribute('href')).startswith("https://www.linkedin.com/jobs/view") and a.get_attribute('href') not in links:
                        links.append(a.get_attribute('href'))
                        urlElements = a.get_attribute('href').split('/')
                        jobs_dict[urlElements[5]] = a.get_attribute('href')
                    else:
                        pass
                # scroll down for each job element
                driver.execute_script("arguments[0].scrollIntoView();", job)

            print(f'Collecting the links in the page: {page-1}')
            # go to next page:
            driver.find_element_by_xpath(f"//button[@aria-label='Page {page}']").click()
            time.sleep(3)
    except:
        pass
    print('Found ' + str(len(links)) + ' links for job offers')
    return jobs_dict


def send_message(name, chat_id, jobs):
  apiToken = '6320637983:AAHU0J1QDDgGrVvUkdNJda_CNlKNr5j47Ok'
  chatID = '432672487'
  apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
  for job in jobs:
    print(job)
    response = requests.post(apiURL, json={'chat_id': chatID, 'text': job})

jobs = collectLinks()
chat_id = "432672487"
name = "Saudi Arabia Jobs"
while True:
    new_jobs = collectLinks()
    diff = []
    for key in new_jobs:
        if key not in jobs:
            diff.append(new_jobs[key])
    print(len(diff))
    if len(diff):
        send_message(name, chat_id, diff)
        jobs = new_jobs
    time.sleep(1800)
# Create empty lists to store information
# job_titles = []
# company_names = []
# company_locations = []
# work_methods = []
# post_dates = []
# work_times = []
# job_desc = []

# i = 0
# j = 1
# # Visit each link one by one to scrape the information
# print('Visiting the links and collecting information just started.')
# for i in range(len(links)):
#     try:
#         driver.get(links[i])
#         i=i+1
#         time.sleep(2)
#         # Click See more.
#         driver.find_element_by_class_name("artdeco-card__actions").click()
#         time.sleep(2)
#     except:
#         pass

#     # Find the general information of the job offers
#     contents = driver.find_elements_by_class_name('p5')
#     for content in contents:
#         try:
#             job_titles.append(content.find_element_by_tag_name("h1").text)
#             company_names.append(content.find_element_by_class_name("jobs-unified-top-card__company-name").text)
#             company_locations.append(content.find_element_by_class_name("jobs-unified-top-card__bullet").text)
#             work_methods.append(content.find_element_by_class_name("jobs-unified-top-card__workplace-type").text)
#             post_dates.append(content.find_element_by_class_name("jobs-unified-top-card__posted-date").text)
#             work_times.append(content.find_element_by_class_name("jobs-unified-top-card__job-insight").text)
#             print(f'Scraping the Job Offer {j} DONE.')
#             j+= 1

#         except:
#             pass
#         time.sleep(2)

#         # Scraping the job description
#     job_description = driver.find_elements_by_class_name('jobs-description__content')
#     for description in job_description:
#         job_text = description.find_element_by_class_name("jobs-box__html-content").text
#         job_desc.append(job_text)
#         print(f'Scraping the Job Offer {j}')
#         time.sleep(2)

# # Creating the dataframe
# df = pd.DataFrame(list(zip(job_titles,company_names,
#                     company_locations,work_methods,
#                     post_dates,work_times)),
#                     columns =['job_title', 'company_name',
#                            'company_location','work_method',
#                            'post_date','work_time'])

# # Storing the data to csv file
# df.to_csv('job_offers.csv', index=False)

# # Output job descriptions to txt file
# with open('job_descriptions.txt', 'w',encoding="utf-8") as f:
#     for line in job_desc:
#         f.write(line)
#         f.write('\n')