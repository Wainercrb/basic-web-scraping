# This program scrapes naukri.com's page and gives our result as a
# list of all the job_profiles which are currently present there.
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent


DRIVER_PATH = '/home/wainer/Downloads/chromedriver'
SITE_URL = 'https://www.melon.com/mymusic/playlist/mymusicplaylistview_inform.htm?plylstSeq=473505374&memberKey=&ref=etc&snsGate=Y'


# headless config
useragent = UserAgent()
options = ChromeOptions()
options.headless = True
options.add_argument('user-agent={0}'.format(useragent.random))


# create web driver service
service = Service(DRIVER_PATH)


# initiating the webdriver. Parameter includes the path of the webdriver.
driver = Chrome(options=options, service=service)
driver.get(SITE_URL)

# Now, we could simply apply bs4 to html variable
soup = BeautifulSoup(driver.page_source, 'lxml')
links = soup.find_all('a', {'class': 'fc_gray'})


# printing top ten job profiles
for job_profile in links:
	print(job_profile.text)


driver.close()
