import hashlib
from io import BytesIO
import os
import PIL
from PIL import Image
import random
import requests
import string
import threading
import time
from fake_headers import Headers

doesnotexisthash = "8b61c3a7e12f9c5f6c623981131d568b"
header = Headers(headers=True)

def isexist(img):
    img_hash = None
    with open(img, 'rb') as f:
        img_hash = hashlib.md5(f.read()).hexdigest()
    os.remove(img)
    print(f'{img} removed')
    return img_hash != doesnotexisthash

def scrape_pics(count_per_thread):
    i = 0
    while i < count_per_thread:
        length = random.choice((5, 7))
        ext = random.choice(('.png', '.jpg', '.jpeg'))
        url = 'http://i.imgur.com/'

        url += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
        url += ext

        filename = url.split('/')[-1]
        print(url)
        response = requests.get(url, headers=header.generate())
        if response.ok:
            try:
                img = Image.open(BytesIO(response.content))
                img.save(f'./.cache/.tmp_{filename}')
                print(f'Saved tmp_{filename}')
                if isexist(f'./.cache/.tmp_{filename}'):
                    img.save(f"./.cache/{filename}")
                    print(f"{url} => {filename}")
                    i += 1
                else:
                    os.remove(f'./.cache/.tmp_{filename}')
            except (PIL.UnidentifiedImageError, OSError):
                pass
        else:
            return print(response.status_code)


start = time.time()
print(f"Your IP: {requests.get('https://ipv4.icanhazip.com').content.decode('utf-8').strip()}")
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
input("Press Enter to exit...")
