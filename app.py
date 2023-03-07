from instabot import Bot
import os
import openai
import re
from image_gen import gen_image_jpg
import json


password = os.environ.get("insta_pass")
openai.api_key = os.environ.get("OPEN_AI_KEY")

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5,
        presence_penalty = 1.0,
        # context = context,
        # id='fb3e8900-7180-4c91-bb09-a2910b45a7c9'
    )
    return response.choices[0].text.strip()

prompt = '''You are an AI bot that has knowledge of various philosophical concepts of longest known history.
            You will generate a random philosophical quote whenever i ask you for a quote with a prompt as "give me a quote".
            You will generate a random quote with deep meanings and do not repeat quotes that you've already given me.
            The quotes that you generate will be connecting with many people psychologically and will generate a good
            amount of reach with the quotes. You will also generate a suitable caption and atleast 15 good
            list of hastags that can maximize the reach of the post to various individuals.
            You will answer only in the following format.

            Quote : [The_Quote] ,
            Author : [The_Person_who_wrote_the_quote] ,
            Caption : [Caption_for_the_quote] ,
            Hashtags : [Hashtags_for_the_quote]
            
            '''

# Set up the initial context with the starting prompt
if not os.path.isfile("context.json"):
    context = {
        "prompt": prompt,
    }
else:
    # with open("context.json","r") as f:
    #     context  = f.read()
    #     f.close()
    context = json.load(open("context.json"))

new_prompt = "give me a quote"
new_prompt = f'{context} {new_prompt}'.strip()
resp = generate_response(new_prompt)
context["prompt"] += f"\n{resp}"

with open("context.json","w") as f:
    f.write(json.dumps(context))
    f.close()
# print(resp)

# Extract the Quote
quote = re.search(r'Quote : "(.*?)"', resp).group(1)

# Extract the Author
author = re.search(r'Author : (.*?),', resp).group(1)

# Extract the Caption
caption = re.search(r'Caption : (.*?),', resp).group(1)

# Extract the Hashtags
hashtags = re.findall(r'#\w+', resp)

print("Quote: ", quote)
print("Author: ", author)
print("Caption: ", caption)
print("Hashtags: ", hashtags)

gen_image_jpg(text=quote,caption=author)


bot = Bot()
# Set the user-agent string to include a delay of 5 seconds between requests
user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
)
bot.api.user_agent = user_agent + " Instabot (delay=5)"

# Login to your Instagram account
bot.login(username='_theosophie_', password=password)

insta_caption = caption +"\n\n\n\n" +' '.join(hashtags)

# Upload a photo with a caption
bot.upload_photo('quote.jpg', caption=insta_caption)


# Logout from your account
bot.logout()