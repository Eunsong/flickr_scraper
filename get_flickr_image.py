import urllib.request
import re

searchTerm = 'dog'
search_url = 'https://api.flickr.com/services/feeds/photos_public.gne?format=json&tags=' + searchTerm
request = urllib.request.Request(search_url)
response = urllib.request.urlopen(request).read().decode()
image_srcs = re.findall(r'media\"\: \{\"m\"\:\"(.+?)\"', response)
print(image_srcs) 

#print(response)
#with open('test.txt', 'w') as f:
#    f.write(response.decode())


"""
imageUrl = f['responseData']['results'][0]['unescapedUrl']
file = cStringIO.StringIO(urllib.urlopen(imageUrl).read())
img = Image.open(file)
"""
