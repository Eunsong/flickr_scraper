import urllib.request
import re

searchTerm = 'dog'
numItems = 50 # number of images to be requested 
page = 10 # page number
search_url = 'https://www.flickr.com/search/?q=' + searchTerm +\
             '&per_page=' + str(numItems) + '&page=' + str(page)
request = urllib.request.Request(search_url)
response = urllib.request.urlopen(request).read().decode()
image_srcs = re.findall(r'data\-defer\-src\=\"(.+?)\"', response)
image_srcs = list( filter( lambda x: 'https' in x, image_srcs)) # remove something like {{src}} 
print(image_srcs) 
print(len(image_srcs))

#print(response)
#with open('test.txt', 'w') as f:
#    f.write(response.decode())


"""
imageUrl = f['responseData']['results'][0]['unescapedUrl']
file = cStringIO.StringIO(urllib.urlopen(imageUrl).read())
img = Image.open(file)
"""
