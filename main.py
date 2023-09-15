import openai
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

# Credentials
MY_EMAIL = "ENTER SENDER'S ADDRESS"
OUT_EMAIL = "ENTER RECEIVER'S ADDRESS"
PASSWORD = "ENTER THE WEBAPP PASSWORD"

motivational_topics = [
    "Goal setting and achievement",
    "Overcoming obstacles",
    "Positive thinking",
    "Self-confidence",
    "Perseverance",
    "Personal growth",
    "Mindfulness",
    "Leadership",
    "Success stories",
    "Time management",
    "Relationship",
    "Couple"
]

couples_images = [
    "Young couple in love",
    "Elderly couple holding hands",
    "Romantic beach sunset couple",
    "Adventurous hiking couple",
    "Happy wedding couple",
    "Cute couple cuddling",
    "Playful couple in the park",
    "Couple cooking together",
    "Interracial couple",
]

# OpenAI---------------------------------------------------------------------------------------------------------------
# Retrieve the API key from the environment variable
api_key = os.environ["OPENAI_API_KEY"]

# Set the API key for OpenAI
openai.api_key = api_key

motivation = f"Generate one nice motivational quote on {random.choice(motivational_topics)}"
poem = "Ask for poem"

question = motivation

response = openai.Completion.create(
    engine="text-davinci-003",  # You can choose a different engine if needed
    prompt=question,
    max_tokens=50,  # Adjust as per your requirements
)

answer = response.choices[0]["text"]

# print("Answer:", answer)

# Ai Generated Image

response_image = openai.Image.create(
    prompt=f"Beautiful Abstract painting of {random.choice(couples_images)}",
    n=1,
    size="512x512",
)
image_url = response_image["data"][0]["url"]

# SENT THE EMAIL--------------------------------------------------------------------------------------------------------


with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Daily Dose of Motivation by Vamz"
    msg['From'] = MY_EMAIL
    msg['To'] = "ssjshivam2777@gmail.com"

    # Create the body of the message (a plain-text and an HTML version).
    # text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    html = f"""\
    <html>
      <head>
          <link rel="preconnect" href="https://fonts.googleapis.com">
          <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
          <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&display=swap" rel="stylesheet">
      </head>
      <body>
        <h1 style="text-align:center; font-family: 'Caveat', cursive;display: block;
        margin-left: auto;
        margin-right: auto;">{answer}</h1>
        <img style="display: block;
        margin-left: auto;
        margin-right: auto;" src={image_url}>
      </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html. (ONLY JUST HTML FOR NOW)
    # part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    # msg.attach(part1)
    msg.attach(part2)

    connection.starttls()
    connection.login(user=MY_EMAIL, password=PASSWORD)
    connection.sendmail(from_addr=MY_EMAIL, to_addrs=OUT_EMAIL,
                        msg=msg.as_string())
