import smtplib

class AlertSystem:
    def __init__(self, config):
        self.config = config
    
    def send_alert(self, message):
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(
                self.config["sender"],
                self.config["password"]
            )
            server.sendmail(
                self.config["sender"],
                self.config["receiver"],
                f"Subject: Network Alert\n\n{message}"
            )
            server.quit()
            return True
        except Exception as e:
            raise Exception(f"Email alert failed: {e}")