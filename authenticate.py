from SMSReminders.client import SMSRemindersClient

client: SMSRemindersClient = SMSRemindersClient(
    app_credentials_fp="./resources/app_credentials.json",
    user_credentials_fp="./resources/user_credentials.json",
    sms_credentials_fp="./resources/sms_credentials.json",
    timezone="US/Eastern"
)

# Will force authentication
client.get_sms_text()