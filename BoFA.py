import time # An included library with Python install.
from selenium import webdriver #you will have to install this
import tkinter # An included library with Python install.
from tkinter import *
import datetime # An included library with Python install.
import ctypes  # An included library with Python install.
import matplotlib.pyplot as plt #you will have to install this
import os # An included library with Python install
import sys # An included library with Python install
import chromedriver_autoinstaller #You will have to install this

chromedriver_autoinstaller.install()

days_of_the_year = []
money_amount_in_bank = []

def popupmsg(msg):
	#COMMENT OUT THE LINE BELOW IF YOU HAVE A MAC
	ctypes.windll.user32.MessageBoxW(0, msg, "Bofa scraper", 1) #this popup will not work on macs.
	#return None <- UNCOMMENT THIS LINE IF YOU HAVE A MAC

############################## DEALS WITH ENTERING THE DATE THAT YOU WANT THE DATA TO BE COLLECTED UNTIL ######################
window = tkinter.Tk()

passwordtext = StringVar()
word = Label(window, text = "Enter the Bank of America password")
word.pack()
password_entry = Entry(window, bd = 15, textvariable = passwordtext)
password_entry.pack()
button = Button(window, text = "CLICK WHEN DONE", command = window.destroy)
button.pack()

window.mainloop()

# date = '01/01/2000' #something obnoxiously early so it samples everything all the time

months = {1:"Jan", 2:"Feb", 3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
# try:
# 	month = int(date[:2])
# 	day = int(date[3:5])
# 	year = int(date[6:])
# except:
# 	print("Wrong format!")
# 	exit()

cutoffdate = datetime.date(2000,1,1) #Converts the values into what Python recognizes as the date format

options = webdriver.ChromeOptions() #you will have to install Google Chrome if you don't have it already
options.add_argument("user-data-dir=C:\\Users\\Bluescreenie_III\\AppData\\Local\\Google\\Chrome\\User Data") #Replace this with the path to your own Chrome user data
driver = webdriver.Chrome(options=options)

########################THE SCRAPING FUNCTION########################

filename = "BoFa" + ".csv"

beginning_date = ""

def scraper(url):
	'''takes data from the Bank of America account, and deposits it into a .csv file that can be picked up by Excel
	It also returns the most recent value of the bank account'''
	bigstring = ""
	driver.get(url);

	# username = driver.find_element_by_name('dummy-onlineId') <-THIS IS NOT NEEDED AFTER YOU TELL CHROME TO REMEMBER YOU ON THE BOFA WEBSITE
	# username.send_keys('iroatuva')

	password = driver.find_element_by_name('dummy-passcode')
	password.send_keys(passwordtext.get()) #remember that password you entered? yeah.


	sign_in_button = driver.find_element_by_name("enter-online-id-submit") 
	sign_in_button.click() #Actually signs the browser into BoFa by pressing the button
	#try:
	time.sleep(10)
	account_button = driver.find_element_by_xpath('//*[@id="Traditional"]/li/div[1]/span[1]/a')
	time.sleep(1)
	account_button.click()
	# except:
	# 	time.sleep(3)
	# 	print('Wrong Password!') #the above will throw an error if you had the wrong password
	# 	exit()

	time.sleep(4)

	first_time = True #checks if this is the first pass through
	amt = 0 #defines the amount variable

	comparator_val = datetime.date(2100,1,1) #Obnoxiously large date just for giggles
	with open(filename, 'w+', encoding = 'utf-8') as g:
		pass #clears the file
	while(comparator_val > cutoffdate):
		try:
			older = driver.find_element_by_name('prev_trans_nav_bottom') #the previous button
		except:
			pass
		dates = driver.find_elements_by_class_name("date-action") #the dates
		balance = driver.find_elements_by_class_name("balance.TL_NPI_Amt") #the balance!

		if first_time:
			first_time = False
			amt = balance[0].text #turns the amount into the first thing looked at by the program
		
		duplicate_checker = []
		try:
			with open('BoFa.csv', 'a+', encoding = 'utf-8') as f:
				for i in range(0, len(dates)):
					date = dates[i].text
					beginning_date = date
					if date == 'Processing': #If the bank is still processing it, ignore it!
						continue
					comparator = date.split('/') #splits the date so Python can get the date format based off the slashes
					comparator_val = datetime.date(int(comparator[2]),int(comparator[0]),int(comparator[1])) #converts to the Python date format
					balance[i] = balance[i].text.replace(',','')
					if date not in duplicate_checker and (comparator_val > cutoffdate): #doesn't do duplicate dates, simply takes the most recent amount from a certain date
						f.write(date + ',' + balance[i] + '\n')
						days_of_the_year.append(date)
						money_amount_in_bank.append(balance[i])
						duplicate_checker.append(date) #adds the date to the duplicate checker so that other dates of the same don't appear
					else:
						continue
		except:
			pass

		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #scrolls down to see the button
		try:
			older.click() #clicks on the previous button
		except:
			print("The account can't go any further back!") #displays this when you can't click the previous button anymore
			break
	
	driver.quit()
	plt.figure(figsize=(20,10))	
	x_ticks = []
	end_date = days_of_the_year[0]
	end_date = end_date.strip().split('/')
	money_amount_in_bank.reverse()
	days_of_the_year.reverse()
	for i in range(len(money_amount_in_bank)):
		money_amount_in_bank[i] = float(money_amount_in_bank[i])
		if (( (i % (len(days_of_the_year)//5) == 0) and (len(days_of_the_year) - i > len(days_of_the_year)//5)) or (i == len(days_of_the_year) - 1)):
			x_ticks.append(days_of_the_year[i])
	plt.plot(days_of_the_year, money_amount_in_bank, '-ro')
	plt.xticks(x_ticks)
	month = int(beginning_date[:2])
	day = int(beginning_date[3:5])
	year = int(beginning_date[6:])
	plt.xlabel("Days (starting " + str(months[month]) + " " + str(day) + ", " + str(year) + " and ending " + str(months[int(end_date[0])]) + " " + str(end_date[1]) + " " + str(end_date[2]) + ")" )
	plt.ylabel("Money in the bank account")
	plt.tight_layout()
	plt.ylim(ymin=0.0)
	today = str(datetime.datetime.now()).split('-')
	yearr = int(today[0])
	monthh = int(today[1])
	dayy = int(today[2][:2])
	plt.savefig("Bank_Account_Data_IRO_" + str(month) + "_" + str(day) + "_" + str(year)+"to" + str(monthh) + "_" + str(dayy) + "_" + str(yearr) + ".png")

	popupmsg("the deed is done.\nThe current balance on the checking account is: " + amt)

	return amt #returns the most recent balance

print("The current balance on the account is " + str(scraper('https://secure.bankofamerica.com/login/sign-in/signOnV2Screen.go')))

