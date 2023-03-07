from PIL import Image, ImageDraw, ImageFont

def gen_image_jpg(text,caption):

    # Create a black image with a size of 500x500 pixels
    image = Image.new('RGB', (1024, 1024), color='black')

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Set the maximum width and height of the text
    max_width = 960
    max_height = 960

    # Add main text in the center of the image with automatic line breaks
    # text = ''' Life is what happens to you while you're busy making other plans '''
    font = ImageFont.truetype('verdana.ttf', 32)

    # Calculate the bounding box of the text with line breaks
    text_bbox = draw.multiline_textbbox((0, 0), text, font=font)

    # Check if the text exceeds the available width of the frame
    if text_bbox[2] - text_bbox[0] > max_width:
        words = text.split()
        lines = []
        current_line = words[0]
        for word in words[1:]:
            if draw.textbbox((0, 0), current_line + ' ' + word, font=font)[2] - text_bbox[0] <= max_width:
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        text = '\n'.join(lines)

    # Calculate the new bounding box of the text with line breaks
    text_bbox = draw.multiline_textbbox((0, 0), text, font=font)

    # Calculate the x and y coordinates of the text
    text_x = (image.width - text_bbox[2] + text_bbox[0]) // 2
    text_y = (image.height - text_bbox[3] + text_bbox[1]) // 2

    # Add the main text to the image with automatic line breaks
    draw.multiline_text((text_x, text_y), text, font=font, fill='white', align='center')

    # Add caption below the main text with centered alignment
    # caption = 'John Lennon'
    caption_font = ImageFont.truetype('verdana.ttf', 24)

    # Calculate the x and y coordinates of the caption
    caption_width, caption_height = draw.textsize(caption, caption_font)
    caption_x = (image.width - caption_width) // 2
    # caption_y = text_bbox[3] + text_y + 20
    caption_y = max_height - (text_y//3)

    # Add the caption to the image with centered alignment
    draw.text((caption_x, caption_y), caption, font=caption_font, fill='white', align='center')

    # Add hashtag in the lower right corner
    hashtag = '@_theosophie_'
    hashtag_font = ImageFont.truetype('verdana.ttf', 18)
    hashtag_width, hashtag_height = draw.textsize(hashtag, hashtag_font)
    hashtag_x = image.width - hashtag_width - 10
    hashtag_y = image.height - hashtag_height - 10
    draw.text((hashtag_x, hashtag_y), hashtag, font=hashtag_font, fill='white')

    # Save the image
    image.save('quote.jpg')