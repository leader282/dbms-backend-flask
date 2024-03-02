from flask_mail import Mail
import re
import os

def isValidEmail(email):
    email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    return re.match(email_regex, email)

def forgot_pass_body(new_pass, name):
    return f"Dear {name},\n\nWe hope this email finds you well. We would like to inform you that your password has been successfully reset. Your new password is: {new_pass}. For security reasons, we recommend changing it after logging in.\n\nThank you for choosing our services.\n\nBest regards,\nThe Support Team"

def first_prize_body(event_name, username):
    return f"Dear {username},\n\nWe are thrilled to inform you that you have been selected as the first prize winner in the {event_name}. Congratulations! Your outstanding achievement deserves recognition, and we are delighted to award you this honor. Your prize will be delivered to you shortly.\n\nThank you for your participation and dedication.\n\nWarm regards,\nThe Organizing Committee"

def second_prize_body(event_name, username):
    return f"Dear {username},\n\nWe are pleased to announce that you have secured the second prize in the {event_name}. Congratulations on this remarkable accomplishment! Your hard work and talent have not gone unnoticed. Your prize will be dispatched to you soon.\n\nThank you for being a part of this event.\n\nSincerely,\nThe Organizing Committee"

def third_prize_body(event_name, username):
    return f"Dear {username},\n\nWe are writing to inform you that you have won the third prize in the {event_name}. Congratulations on this well-deserved recognition! Your dedication and efforts have paid off, and we are honored to award you this prize. Your prize will be sent to you in the coming days.\n\nThank you for your participation and enthusiasm.\n\nKind regards,\nThe Organizing Committee"

def sponsor_approval_body(event_name, sponsor_name):
    return f"Dear {sponsor_name},\n\nWe are pleased to inform you that your sponsorship request for {event_name} has been approved. We greatly appreciate your support and commitment to our cause. Your contribution will play a significant role in the success of the event.\n\nThank you for your generosity and partnership.\n\nWarm regards,\nThe Event Management Team"


def send_mail(to, subject, body):
    from app import mail  
    sender_email = os.environ.get("MAIL_USERNAME")
    print(sender_email)
    print(os.environ.get("MAIL_PASSWORD"))

    if not isValidEmail(to):
        return False
    try:
        mail.send_message(
            subject=subject,
            sender=sender_email,
            recipients=[to],
            body=body
        )
        return True
    except Exception as e:
        print(e)
        return False
