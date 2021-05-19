import sys
import time
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import datetime
import smtplib, ssl
from firebase import Firebase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
sender_email = None #change
password = None 
receiver_email=None
duration = 1  # seconds
freq = 440  # Hz


if len( sys.argv)<4:
	print("enter argument displayed on app as phone 2 no as 2 and pin as 3")
	exit()
	
def send_mail(mess):

    port = 465 
    smtp_server = "smtp.gmail.com"
    message = MIMEMultipart("alternative")
    message["Subject"] = "covid vacine slots- chrome program"
    message["From"] = sender_email
    message["To"] = receiver_email
    part1 = MIMEText(mess, "plain")
    message.attach(part1)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
db=None
def firebase():
	global db
	config={
	    "apiKey": "AIzaSyCSt9KRzomwUvi_vmuR3_M3VSQPuiwZbE8",
	    "authDomain": "cowin-e58d4.firebaseapp.com",
	    "databaseURL": "https://cowin-e58d4-default-rtdb.firebaseio.com",
	    "projectId": "cowin-e58d4",
	    "storageBucket": "cowin-e58d4.appspot.com",
	    "messagingSenderId": "668386027081",
	    "appId": "1:668386027081:web:30a32e9fd327a57db6c198"
	  }
	firebase=Firebase(config)
	db=firebase.database()
	   
        
driver = webdriver.Chrome('./chromedriver')
#driver.get("https://selfregistration.cowin.gov.in/")

def reset():
	global driver
	print("resetting ")
	driver.close()
	driver = webdriver.Chrome('./chromedriver')
	main()
def find_center_by_distict():
	districtbut=driver.find_element_by_class_name("status-switch")
	districtbut.click()
	sele=driver.find_element_by_class_name("mat-select-empty")
	sele.click() 
	time.sleep(100)
def find_center(pi):
	#time.sleep(100)
	pin=driver.find_element_by_id("mat-input-2")
	pin.clear()
	pin.send_keys(pi)
	time.sleep(11)
	but=driver.find_element_by_class_name("pin-search-btn")
	but.click()
	time.sleep(2)
	try:
		ch18=driver.find_element_by_id("c1")
		driver.execute_script("arguments[0].click()",ch18)
		time.sleep(2)
	except Exception:
		print("age buttn not found")
		#logout()
		reset()
	try:
		ls=driver.find_elements_by_class_name("slot-available-main")
		#print(ls.text)
		#print(l.text)
		for l in ls:
			#print(l.text)
			#continue;
			if (str(l.text)).strip()=="":
				continue
			print("center ")
			x=str(l.text)
			lines=x.split("\n")
			i=0
			for l in lines:
				#print(str(i)+"    "+l)
				i+=1
				if l.strip() != "Booked" and l.strip() != "NA" and l.strip() != "COVAXIN" and l.strip() != "Age 18+" :
					print("checking "+l)
					if int(l.strip())>4: 
						print("found "+ l)
						i=180
						while i>0:
							n = os.fork()
							if n>0:
								os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
								i=i-1
								time.sleep(1)
							else:
								#send_mail(l)
								exit()
								
	except NoSuchElementException:
		print("no slots")
	
def login():
	global current
	current=time.time()
	try:
		driver.get("https://selfregistration.cowin.gov.in/")
		time.sleep(1)
	except Exception:
		print("net error")
		reset()
		return
	curr=datetime.datetime.today()
	cu=curr.strftime('%d-%m-%y %H:%M')
	curr=datetime.datetime.strptime(cu,'%d-%m-%y %H:%M')
	#print(driver.title)
	#print(driver)
	#print(driver.page_source)
	try:
		ph=driver.find_element_by_id("mat-input-0")
		ph.send_keys(sys.argv[2])
	except Exception:
		print("phone no input not found")
		reset()
		return
	try:
		su=driver.find_element_by_class_name("login-btn")
		#su=driver.find_element_by_class_name(".next-btn.vac-btn.login-btn.ion-color ion-color-primary md button button-solid ion-activatable ion-focusable hydrated")
		#print(su)
		su.click()
		time.sleep(3)
	except Exception:
		print("logn button not found")
		reset()
		return 
	#driver.switch_to_window(driver.window_handles[1])


	#print(driver.page_source)
	otp=driver.find_element_by_class_name("otp-field")
	res=db.child(sys.argv[1]).get()
	print(res.val())
	ot=res.val()
	tim,otpmsg=ot.split("#")
	dobj = datetime.datetime.strptime(tim, '%d-%m-%Y %H:%M:%S')
	dob=dobj.strftime('%d-%m-%y %H:%M')
	dobj=datetime.datetime.strptime(dob,'%d-%m-%y %H:%M')
	#fu=datetime.datetime.today()
	#fu=fu.strftime('%d-%m-%y %H:%M:%S')
	#print(fu>curr)
	#print(curr<fu)
	print(dobj)
	print(curr)
	print(dobj<curr)
	#if dobj<curr:
	#print(cu)
	st=time.time()
	while dobj<curr :
		time.sleep(1)
		res=db.child(sys.argv[1]).get()
		if time.time()-st<10:
			print(res.val())
		ot=res.val()
		tim,otpmsg=ot.split("#")
		dobj = datetime.datetime.strptime(tim, '%d-%m-%Y %H:%M:%S')
		if time.time()-st>190:
			try:
				print("resending")
				resend=driver.find_element_by_class_name("resend")
				resend.click()
				st=time.time()
			except Exception:
				print("not found going to main")
				reset()
				return
	print(ot)
	otpfrommsg=otpmsg.split()[6]
	otpf=otpfrommsg[:-1]
	print(otpf)
	otp.send_keys(otpf)
	sub=driver.find_element_by_class_name("button-solid")
	sub.click()

	time.sleep(3)
	
	#print(driver.page_source)
	try:
		sche=driver.find_element_by_class_name("m-lablename")
	#for x in sche:
		#print(sche)
		sche.click()
		time.sleep(0.5)
	except Exception:
		print("schedule now button not found")
		reset()
		return
	"""x=driver.find_elements_by_class_name('chk-box')
	#print(x)
	driver.execute_script("arguments[0].scrollIntoView();", x[0])
	#time.sleep(3)
	x[1].click()
	#time.sleep(2)
	#actions = ActionChains(driver)
	#actions.move_to_element(x[2]).perform()
	driver.execute_script("arguments[0].scrollIntoView();", x[1])


	#time.sleep(2)
	x[2].click()
	driver.execute_script("arguments[0].scrollIntoView();", x[2])


	#time.sleep(2)
	x[3].click()
	time.sleep(0.5)
	sched=driver.find_element_by_class_name("schedule-appointment")
	sched.click()
	time.sleep(3)
	"""
	#return driver
	#logout()
	
	
def logout():
	print("logout")
	logou=driver.find_element_by_class_name("logout-text")
	logou.click()
	time.sleep(3)
	
current=time.time()
#time.sleep(3)
#print(time.time()-current)
def main():
	#driver.get("https://selfregistration.cowin.gov.in/")
	#reset()	
	login()
	while(1):
		print(str(datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')))
		if time.time()-current>13*60:
			logout()
			login()
		#find_center_by_distict()
		find_center(sys.argv[3])
firebase()
main()
#find_center("180001")
#time.sleep(3)
#find_center("180002")
#par=driver.find_element_by_id("mat-checkbox-6-input")
#par.click()
#mus=driver.find_element_by_id("mat-checkbox-8-input")
#mus.click()

#y=driver.find_elements_by_class_name('col-f')
#y[2].click()
#time.sleep(3)
#y[3].click()

