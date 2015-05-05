#! /usr/bin/python3
# downloadWebtoons.py - Downloads every single Webtoons comic.

import requests
import bs4
import os


n = 186  # initial episode number

# To crossover rel="nofollow"
req_header = {'Referer': 'http://www.webtoons.com/'}

while True:
    url = u'http://www.webtoons.com/zh-hans/action/girls-of-the-wilds\
        /%E7%AC%AC' + str(n) + u'%E8%AF%9D\
        /viewer?title_no=237&episode_no=' + str(n+1)

    res = requests.get(url)
    if res.status_code != requests.codes.ok:
        break

    targetDir = '/home/sjk/Pictures/comic/girls-of-the-wilds/%s' % n

    os.makedirs(targetDir, exist_ok=True)  # store comics in targetDir

    soup = bs4.BeautifulSoup(res.text)
    comicElem = soup.select('#_imageList img')
    if comicElem == []:
        print('Could not find comic image.')
    else:
        # Dowmload current episode.
        print('\nReady to download Episode No.%s...' % n)
        print('<%s images found>\n' % len(comicElem))
        for i in range(0, len(comicElem)):
            comicUrl = comicElem[i].get('data-url')

            # Dowmload the image.
            print('Downloading image %s of Episode No.%s...' % (i+1, n))
            res = requests.get(comicUrl, headers=req_header)
            res.raise_for_status()

            # Save the image to tartgetDir.
            imageFile = open(os.path.join(targetDir, '%s.jpg' % i), 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
    n += 1  # update episode

print('\nUpdate to %s' % (n - 1))  # find update
