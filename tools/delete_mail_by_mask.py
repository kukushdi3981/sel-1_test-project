import imaplib

def delete_mail_mask(userlogin, userpassword, mask):
	host = "imap.mail.ru"
	port = "993"
	login = userlogin
	password = userpassword

	mail = imaplib.IMAP4_SSL(host, port)
	mail.login(login, password)
	mail.select('INBOX')
#	data = mail.search(None, 'FROM', '"attestorgooo@mail.ru"')[1][0]
#	seach_criteria = "'(FROM \"" + mask + "\")'"
#	print(seach_criteria)
	data = mail.search(None, 'ALL')[1][0]
	for num in data.split() :
		mail.store(num, '+FLAGS', '\\Deleted')
	mail.expunge()
	mail.close()
	mail.logout()


delete_mail_mask("attesting@mail.ru", "Bp1cTesting777", "")
