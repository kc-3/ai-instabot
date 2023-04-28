# ai-instabot

This is an application that uses gpt-3 models as a custom API. It is instructed to give 4 responses a quote, author name, caption and hashtag to maximize the reach in instagram.

It uses openAI LLM `text-davinci-003` to give responses, however similar results can be achieved with `gpt-3.5-turbo` which is much faster and cost efficient, but it's capabilities are limited due to chat like responses.

The application is promptly engineered to give responses in a certain format. The prompt can be read in the code app.py

The response is then extracted using regex and given to image_gen.py which converts the text into an image.

This image is given as input to `instabot` which is an open source instagram library. It uses our credentials and uploads the image with the caption and hastags that we provide.
