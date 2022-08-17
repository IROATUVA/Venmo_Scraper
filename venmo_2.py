#This is a program wholly devoted to looking at the IRO Venmo and collecting information about who has and has not paid dues
#Developed by Mohit Srivastav - IRO Treasurer 2020

import datetime # An included library with Python install.
import re # An included library with Python install.
import csv #An included library with Python install.
import ezgmail #You will have to install this.
# import chromedriver_autoinstaller #You will have to install this

####################### DUES CUTOFFS AND FILES NAMES AND OTHER PREPROCESSING#################################

ten_dues_date = 0
fifteen_dues_date = 0

today = str(datetime.datetime.now()).split('-')
year = int(today[0])
month = int(today[1])
day = int(today[2][:2])
semester = ''
if month <= 12 and month >= 8: #fall semester lies between August and December
	semester = 'fall'
	ten_dues_date = datetime.date(year, 8, 20)
	fifteen_dues_date = datetime.date(year, 1, 1) #start of the previous spring semester
else:
	semester = 'spring'
	ten_dues_date = datetime.date(year, 1, 1)
	fifteen_dues_date = datetime.date(year-1, 8, 10) #start of the previous fall semester



duesFinder = re.compile(r'([A-z]+( [A-z]*)* [A-z]+) paid you (\$10.00|\$15.00)') #A regular expression that matches to suspected dues payments
#group 1 of the regex is the name, group 3 is the value

descrFinder = re.compile(r'paid[<//b>]+ You (.+)Transfer') #matches descriptions of payments inside of the gmailMessage object

filename = "duesPayingMembers.csv" 


###################################### SCRAPING THE EMAIL ACCOUNT ###########################

def scrape():
	paymentList = {}
	venmo_data_threads = ezgmail.search('from:venmo (completed OR paid) newer:' + str(fifteen_dues_date), maxResults = 1000)
	#looks through every venmo payment that was either completed or paid that is newer than the dues date
	semesterPayments = 0
	yearPayments = 0
	for i in venmo_data_threads:
		possible_dues_payment = str(i.messages[0].subject) #all the basic subjects containing people's payments
		date = i.messages[0].timestamp.date()
		try:
			descr = str(i.messages[0])
		except:
			descr = str(i.messages[0]).encode('utf-8') #fucking stupid emojis breaking my code GODDAMNIT

		descr = descr.lower() #make it lowercase to get rid of all capitalizations

		# if 'dues' not in descr:
		# 	continue
		# this is a restrictive version of the current code
		
		if 'diplo' in descr or '+1' in descr or 'plus 1' in descr or 'delegation' in descr or 'merch' in descr or 'delegate' in descr or 'vamun' in descr or 'register' in descr or 'registration' in descr or 'donation' in descr or 'vics' in descr or 'AAPI' in descr: 
		#Do not count diplo ball or VAMUN payments or other stuff as dues payments!
			continue

		for match in duesFinder.finditer(possible_dues_payment):
			amt = int(float(match.group(3).replace('$','')))
			try:
				if (amt == 15 and date > fifteen_dues_date) or (amt == 10 and date > ten_dues_date): #Checks for dues payment
					paymentList[match.group(1)] += amt #throws an error if that dictionary entry doesn't exist
					if date > ten_dues_date:
						semesterPayments += amt #payment was made during this semester
					yearPayments += amt #payment was made sometime in the last year
			
			except: #except statement exists to make sure that I don't have to check when things have to be added to a dictionary
				if (amt == 15 and date > fifteen_dues_date) or (amt == 10 and date > ten_dues_date): #Checks for dues payment
					paymentList[match.group(1)] = amt #adding to a dictionary does so with replacement (so no double counting)
					if date > ten_dues_date:
						semesterPayments += amt
					yearPayments += amt

	return paymentList, semesterPayments, yearPayments

############################################### LEGACY SELENIUM CODE ############################

# options = webdriver.ChromeOptions() #you will have to install Google Chrome if you don't have it already
# options.add_argument("user-data-dir=C:\\Users\\Bluescreenie_III\\AppData\\Local\\Google\\Chrome\\User Data") #Replace this with the path to your own Chrome user data
# driver = webdriver.Chrome(options=options)

# driver.get("https://venmo.com/account/sign-in")

# def login():
# 	try:
# 		username = driver.find_element_by_name('phoneEmailUsername')
# 		username.send_keys('treasurer@iroatuva.org')
# 	except:
# 		print("Username entry failed!")
# 		raise 

# 	try:
# 		password = driver.find_element_by_name('password')
# 		password.send_keys(passwordtext.get())
# 	except:
# 		print("Password entry failed!")
# 		raise
# 	time.sleep(1)
# 	login_button = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div/form/div/button')
# 	login_button.click()

# 	time.sleep(5)

# 	try:
# 		feed_button = driver.find_element_by_xpath("/html/body/div[2]/div[8]/div[1]/div[4]/div[1]/div/div[1]/button[3]")

# 		feed_button.click()
# 	except:
# 		print("Wrong password!")
# 		driver.quit()

# def scrape(cutoff):
# 	dpm_list = {} #A list of dues paying members in IRO
# 	all_data = {} #Literally everything.
# 	sem_dpm_list = {} #People who have paid this semester
# 	time.sleep(4) #Allows for the website to load
# 	amtDues = 0 #The amount paid in dues so far this semester
# 	Lisner_Count = 0 #The number of times Sam Lisner likes a post

# 	while True:  #Just keeps the while loop going forever
# 		payments = driver.find_elements_by_class_name("feed-story-payment") #the physical payments
# 		next_button = driver.find_element_by_css_selector(".feed-more > button:nth-child(1)") #The "load more" button
# 		for i in payments:

# 			if i.text in all_data:
# 				continue #Do not recalculate shit if it's already in there (saves you a buttload of time)

# 			if 'Sam Lisner' in i.text:
# 				Lisner_Count+=1 #JFC Sam Lisner I hope you read this and have a very nice day you are a very nice person

# 			data = i.text.replace("International Relations Organization","").replace("paid","").replace("charged","").strip().split('\n') #format is name, date, mesage, amount, and whether Sam Fucking Lisner liked your godforsaken message
# 			name = data[0].strip()


# 			try:
# 				amount = float(data[3].replace('$','').replace(',',''))
# 			except:
# 				amount = float(data[2].replace('$','')) #handler for emojis as the message (they don't work well!)

# 			date = data[1].replace(',','').split()
# 			date = date[0] + ' ' + date[1] + ' ' + date[2]
# 			date = datetime.datetime.strptime(date, "%B %d %Y").date() #Code block convers date that is recieved to something Python recognizes

# 			if date < cutoff: #if you've gone past the cutoff date stop the collection
# 				driver.quit() #closes the browser
# 				return (dpm_list, len(all_data), Lisner_Count, amtDues, sem_dpm_list) #ends the program
			
# 			if (amount == 15 and date > fifteen_dues_date) or (amount == 10 and date > ten_dues_date): #Checks for dues payment
# 				dpm_list[name] = amount #adds name to the running directory of dues paying members

# 				if date > ten_dues_date:
# 					amtDues += amount #only adds if it has been paid this semester
# 					sem_dpm_list[name] = amount

# 			all_data[i.text] = [amount, str(data[2])]

# 		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #scrolls down to click the button
# 		next_button.click()



########################### POST SCRAPING ACTIVITIES ###########################

def make_dpm_csv(total_dict): #makes the file that records dues paying members
	if not isinstance(total_dict, dict):
		raise TypeError("Function needs a dictionary")
	total_amount = 0
	with open(filename, 'w+') as f:
		csvwriter = csv.writer(f, lineterminator = '\n') #for some reason the csvwriter's default lineterminator is \n\n, so this changes it
		for i in total_dict.keys():
			total_amount += total_dict[i] #adds the amount paid to the running total
			written_list = [i.title(), total_dict[i]] #writes the name in title form, and the amount they paid
			csvwriter.writerow(written_list)
	return total_amount #returns the total amount that was paid

def AnnoySecretary(money, semesterTotal, numP):
	text_to_send = ""
	text_to_send += "$" + str(money) + " were collected from dues so far this year +/- " + str(round(int(money**0.5),-1)) + "\n\n" #standard stat error for large N is sqrt(N), and I can't be arsed to change that
	text_to_send += "$" + str(semesterTotal) + " were collected from dues so far this semester +/- " + str(round(int(semesterTotal**0.5),-1)) + "\n\n"
	text_to_send += "The following " + str(numP) + " people are currently dues paying members:\n"
	with open(filename) as f:
		text_to_send += f.read() #reads all of the people in the list and sends that list
	ezgmail.send('secretary@iroatuva.org', 'DPM List as of ' + str(datetime.datetime.now()), text_to_send)
	ezgmail.send('iro.secretary@gmail.com', 'DPM List as of ' + str(datetime.datetime.now()), text_to_send)
	print("email sent to secretary@iroatuva.org and iro.secretary@gmail.com succesfully!")


if __name__ == '__main__':
	print("Scraping the email account...")
	dpm, semesterTotal, yearTotal = scrape() #scrapes the gmail for the overall dictionary
	print("-"*100)
	print("The following people have requested exemptions from paying dues:")
	with open("duesExceptions.csv") as f:
		for line in f:
			line = line.strip()
			dpm[line] = 0
			print(line)
	print("-"*100)
	amtDues = make_dpm_csv(dpm) #gets the total amount of dues
	AnnoySecretary(amtDues, semesterTotal, len(dpm)) #sends the email
	print(len(dpm), "people are currently dues paying members")
	print("Dues made $" + str(amtDues), "the past 2 semesters")
	print("Dues made $" + str(semesterTotal), "this semester")
