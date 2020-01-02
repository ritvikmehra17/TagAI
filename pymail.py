import smtplib 
from models import User,Session

def doValidation(email):
    ses = Session()
    resultset = ses.query(User).filter(User.email==email).all()
    if len(resultset)> 0:
        user = resultset[0]
        return user.password
    


def send(email):
    try:
        # creates SMTP session 
        s = smtplib.SMTP('smtp.gmail.com', 587)         
        # start TLS for security 
        s.starttls() 
        # Authentication 
        s.login("189303115ritvik@gmail.com","189303115")    
        out = doValidation(email)
        if out:
            # message to be sent
            message = f"You have requested to view your password.\nYour password is: {out}"
            s.sendmail("189303115ritvik@gmail.com", email, message) 
            s.quit()
        else:
            return False
    except Exception as e:
        print(e)
        return False
    return True
            
##testing
if __name__ == "__main__":
    if (send('xaidmeta@gmail.com')):
        print('done')