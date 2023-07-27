from io import BytesIO
import PIL
from PIL import Image
import random
import requests
import string
import threading
import time

def scrape_pics(count_per_thread):
    i = 0
    while i <= count_per_thread:
        url = 'http://i.imgur.com/'
        length = random.choice((5, 6))
        if length == 5:
            url += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
        else:
            url += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))
            url += ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))

        url += '.jpg'

        filename = url.split('/')[-1]
        try:
            Image.open(BytesIO(requests.get(url).content)).save(f"./.cache/{filename}")
            print(url)
            i += 1
        except (PIL.UnidentifiedImageError, OSError):
            pass



start = time.time()
count = int(input('Count of images: '))

thread_amount = count // 2 if count % 2 == 0 else (count // 2) + 1
threads = []
count_per_thread = count // thread_amount
for i in range(0, thread_amount):
    thread = threading.Thread(target=scrape_pics, args=(count_per_thread,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

end = time.time()
total = "{:.2f} s".format(end - start)
print("Total time:", total)