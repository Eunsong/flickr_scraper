"""
    flickr image scraper works under python3
"""

import urllib.request
import re
import argparse
import os

def scrape_images(search_term, numImages=1, file_path=''):
    """ will download images matching search_term(e.g. 'dog').
        file names will be search_term + file_index + '.jpg'.
    """
    downloaded = 0
    page = 1
    while ( downloaded < numImages ):
        image_urls = get_image_links(search_term, page)
        size = len(image_urls)
        if (downloaded + size > numImages):
            size = numImages - downloaded 
            image_urls = image_urls[:size] # only use part of the urls
        download_images(image_urls, search_term, file_path, downloaded + 1)
        downloaded += size
        page += 1

def get_image_links(search_term, page=1, per_page=60):
    """ returns list of urls to the images corresponding to the search_term """
    # per_page : number of images to be requested per page(doesn't seem to work..
    # always finds 60. use different page number instead to download more images
    search_url = 'https://www.flickr.com/search/?q=' + search_term +\
                 '&per_page=' + str(per_page) + '&page=' + str(page)
    request = urllib.request.Request(search_url)
    response = urllib.request.urlopen(request).read().decode()
    image_srcs = re.findall(r'data\-defer\-src\=\"(.+?)\"', response)
    image_srcs = list(filter(lambda x: 'https' in x, image_srcs)) # remove something like {{src}} 
    return image_srcs

def download_images(image_urls, file_name, file_path='',  file_name_start_index=1):
    index = file_name_start_index
    for url in image_urls:
        download_image(url, file_name + str(index), file_path )
        index += 1 

def download_image(url, file_name, file_path=''):
    request_url = urllib.request.Request(url)
    data = urllib.request.urlopen(request_url).read()
    # check if path already exists and if not create a new folder
    if not ( file_path == '' ):
        if not os.path.isdir(file_path):
            os.mkdir(file_path)
    # if specified file name does not contain jpg file extension, append '.jpg' to it
    if not ( file_name[-4:] == '.jpg'):
        file_name += '.jpg'
    try:
        if (file_path[:2] == './'):
            file_path = file_path[2:]
        elif ( file_path[:1] == '/'):
            file_path = file_path[1:]
        if (file_path[-1:] == '/'): 
            file_path = file_path[:-1]
        if file_path:
            file_path += '/'
    except IndexError:
        file_name = ''
        pass
    with open(file_path + file_name, 'wb') as f:
        f.write(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('keyword', help = 'search keyword for images')
    parser.add_argument('--number', '-n', default=1,\
                        help = 'number of images to be downloaded. default is 1')
    parser.add_argument('--path', '-p', default='',\
                        help = 'path to where images will be downloaded')
    arg = parser.parse_args()
    scrape_images(arg.keyword, int(arg.number), arg.path) 
