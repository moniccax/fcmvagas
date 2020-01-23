from flask import request, jsonify, render_template, flash, url_for as flask_url_for, Response


def verifyCpf(cpf):
	if len(cpf)!=14:
		return 0;
	else:
		if cpf[0].isdigit() and cpf[1].isdigit() and cpf[2].isdigit() and cpf[3]=="." and cpf[4].isdigit() and cpf[5].isdigit() and cpf[6].isdigit() and cpf[7]=="." and cpf[8].isdigit() and cpf[9].isdigit() and cpf[10].isdigit() and cpf[11]=="-" and cpf[12].isdigit() and cpf[13].isdigit():
		 	return 1;
	return 0;

def random_password():
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8));

def random_token():
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase +string.ascii_lowercase + string.digits) for _ in range(64));

def set_user_token(user):
	token=random_token();
	user.token=token
	user.last_token=datetime.datetime.now();
	db.session.commit()
	return token;

def is_logged(user,token):
	if user.token==token and datetime.datetime.now()-user.last_token<datetime.timedelta(days=2):
		return True;
	return False;

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients.split())
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
