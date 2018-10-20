import os, requests, bs4, webbrowser, random

# ask user for the photo category
#imgType = input('Category:')

# url to the pexels site
# url = 'http://pexels.com/search/'
url_request = 'https://www.pexels.com/search/nature/'
imgType = os.path.basename(url_request)


# get the response form the site
#res = requests.get(url + imgType)
res = requests.get(url_request)
try:
    res.raise_for_status()
except Exception as exc:
    print('Sorry an error occured:', exc)

# print(res.text)
# creating a soup object and targetting the elemnt
soup = bs4.BeautifulSoup(res.text, 'html.parser')
element = soup.select('.js-photo-link img')

for i in range(len(element)):
    #url = element[i].get('src')
    url_request = element[i].get('src')
    name = random.randrange(1, 1000)
    file = open(str(name) + imgType + '.jpg', 'wb')
    #res = requests.get(url)
    res = requests.get(url_request)
    for chunk in res.iter_content(10000):
        file.write(chunk)
    file.close()

print('done')