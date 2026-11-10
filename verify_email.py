"""Send a labeled delivery test using the existing workflow email settings."""
import os
import smtplib
import ssl
from email.message import EmailMessage


def main():
    sender = os.environ["SENDER"]
    receiver = os.environ["RECEIVER"]
    message = EmailMessage()
    message["Subject"] = "Zotero Daily - delivery test"
    message["From"] = sender
    message["To"] = receiver
    message.set_content(
        "This is a delivery test for your Zotero Daily recommendations.\n"
        "It is not today's paper recommendation email.\n"
        "Your daily workflow is scheduled for 06:17 China time (UTC+8).\n"
        "GitHub may delay the scheduled start.\n"
    )
    host = os.environ["SMTP_SERVER"]
    port = int(os.environ["SMTP_PORT"])
    context = ssl.create_default_context()
    if port == 465:
        server = smtplib.SMTP_SSL(host, port, timeout=30, context=context)
    else:
        server = smtplib.SMTP(host, port, timeout=30)
        server.starttls(context=context)
    with server:
        server.login(sender, os.environ["SENDER_PASSWORD"])
        refused = server.send_message(message, from_addr=sender, to_addrs=[receiver])
        if refused:
            raise RuntimeError("The mail server refused the test recipient.")
    print("Delivery test accepted by SMTP server. Inbox delivery still needs confirmation.")
    if path := os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(path, "a") as summary:
            summary.write("Delivery test accepted by SMTP server. Check the inbox and spam folder for 'Zotero Daily - delivery test'.\n")


if __name__ == "__main__":
    main()
