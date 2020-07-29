import email, smtplib, ssl, csv

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def mailConn():
	context = ssl.create_default_context()
	port = 465  # SSL port
	sender = "enter your email here" # sender email address
	print()
	print(f"Attempting login to: {sender} \n")
	password = input("Enter Password: ")
	smtp_server = "smtp.gmail.com"
	
	return context, port, sender, password, smtp_server


def impContacts(row):
	name = row[0]
	email = row[1]
	orderID = row[2]
	
	return name, email, orderID
	
	
def manualContact():
	name = input("Enter contact name: ")
	email = input("Enter contact email: ")
	orderID = input("Enter order ID: ")

	return name, email, orderID
	

def addText(name, recipient, orderID, sender):
	message = MIMEMultipart("alternative")
	message["Subject"] = f"Opportunities at {orderID}"
	message["From"] = sender
	message["To"] = recipient
	
	text = (
		f"Dear {name}, \n"
		f"\n"
		f"Your order #{orderID} has been recieved. \n"
		f"\n"
		f"We have attached your receipt. \n"
		f"Thank You! \n"
		f"\n"
		f"Company X"
	)
	
	html = (
		f"<html>"
			f"<body>"
				f"<p>Dear {name}, <br>"
					f"<br>"
					f"Your order #{orderID} has been recieved. <br>"
					f"<br>"
					f"We have attached your receipt. <br>"
					f"<br>"
					f"Thank You! <br>"
					f"<br>"
					f"<strong>Company X</strong> <br>"
				f"</p>"
			f"</body>"
		f"</html>"
	)

	
	# creates plain/html MIMEText objects
	part1 = MIMEText(text, "plain")
	part2 = MIMEText(html, "html")
	
	# Add HTML/plain-text parts to MIMEMultipart message
	message.attach(part1)
	message.attach(part2)
	
	return recipient, message
	

def addReceipt(message):
	filename = "enter file name here"  # Add your file in the same directory as the script

	# Open PDF file in binary mode
	with open(filename, "rb") as attachment:
		# Add file as application/octet-stream
		receipt = MIMEBase("application", "octet-stream")
		receipt.set_payload(attachment.read())
	
	# Encode files in ASCII characters to send by email    
	encoders.encode_base64(receipt)
	
	# Add headers as key/value pair to attachment part
	receipt.add_header(
		"Content-Disposition",
		f"attachment; filename= {filename}",
	)
	
	message.attach(receipt)
	payload = message.as_string()
	
	return payload
	
	
def main():
	context, port, sender, password, smtp_server = mailConn()
	
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		server.login(sender, password)
		
		print()
		menu_choice = input("Import contacts from CSV(1) or Enter contact manually(2)?: ")
		
		if menu_choice == "1":
			msg_count = 0
			with open("importContacts.csv") as file:
				reader = csv.reader(file)
				next(reader)  # Skip header row
					
				for row in reader:
					name, email, orderID = impContacts(row)
					recipient, message = addText(name, email, orderID, sender)
					payload = addreceipt(message)
					server.sendmail(sender, recipient, payload)
					msg_count += 1	
				
				print()				
				print(f"{msg_count} messages sent successfully")
				exit()
					
		if menu_choice == "2":
			while True:
				try:
					name, email, orderID = manualContact()
					recipient, message = addText(name, email, orderID, sender)
					payload = addreceipt(message)
					server.sendmail(sender, recipient, payload)
				
				except:
					print()
					print("Email address does not exist. Try Again.")
					continue
				
				else:
					print()
					print("Message sent successfully")
					exit()
			
main()