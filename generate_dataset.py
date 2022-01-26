import praw, cv2, pytesseract, requests, io, json, sys, random, enchant
from PIL import Image
d = enchant.Dict("en_US")
reddit = praw.Reddit(client_id='P1MphPh8rA_QpYHpaRmvQw',
    client_secret='maW8AMKmBReeelY-nBVRGlH31wZVyQ',
    user_agent='Image Fetcher',
    username='RedditBotFinder',
    password='2392339F61FC8E51A9863B4F48602089E47B6E72F5FBBA1B6C49AF4404FFED2B')

# fetch the hot posts from r/greentext
subreddit = reddit.subreddit('greentext')
hot_posts = subreddit.top(limit=10000)
post_count = 0

for post in hot_posts:
    try:
        if post.is_self is False:
            response = requests.get(post.url)
            img = Image.open(io.BytesIO(response.content))
            width, height = img.size
            if width * height < 200000:
                continue
            text = pytesseract.image_to_string(img, lang='eng', config='--psm 6 -c tessedit_char_whitelist="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!>:./=?!\'\\""')
            text = text.split('\n')[1:]
            final_text = []
            for line in text:
                if '>' in line:
                    line = '>' + line.split('>')[1].strip()
                if ' KB' in line or "No." in line or "File" in line:
                    final_text = []
                    continue
                if line != '':
                    if line == '>':
                        continue
                    for word in line.split(' '):
                        if "I" != word and "I" in word and not d.check(word):
                            if d.check(word.replace("I", "l")):
                                line = line.replace(word, word.replace("I", "l"))
                            elif d.check(word.replace("I", "t")):
                                line = line.replace(word, word.replace("I", "t"))
                        if "l" in word and not d.check(word):
                            if d.check(word.replace("l", "t")):
                                line = line.replace(word, word.replace("l", "t"))
                    if not line.startswith(">") and len(final_text) > 0:
                        final_text[-1] += " " + line
                    else:
                        final_text.append(line)
            with open('data.json', 'r') as f:
                previous_data = json.load(f)
                previous_data[post.title] = final_text.join('\n')
                with open('data.json', 'w') as f2:
                    json.dump(previous_data, f2)
        post_count += 1
        print(f"[{format(post_count, '03d')}] Added post: {post.title}")
    except KeyboardInterrupt:
        sys.exit()
