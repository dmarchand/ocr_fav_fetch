from lxml import html
import requests
import urllib
import urllib2

def download_mp3(url):
        file_name = url.split('/')[-1]
        u = urllib2.urlopen(url)
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)

        file_size_dl = 0
        block_sz = 8192
        while True:
                buffer = u.read(block_sz)
                if not buffer:
                        break

                file_size_dl += len(buffer)
                f.write(buffer)
                status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                status = status + chr(8)*(len(status)+1)
                print status,

        f.close()

page = requests.get('https://dl.dropboxusercontent.com/u/52921017/All%20Faves.html')
tree = html.fromstring(page.content)

names = tree.xpath('//td[4]/text()')

for name in names:
	encoded = urllib.quote_plus(name)
	search_page = requests.get('http://ocremix.org/quicksearch/remix/?qs_query=' + encoded)
	search_tree = html.fromstring(search_page.content)
	
	links = search_tree.xpath("//a[@class='main']/@href")

	if len(links) == 0:
		continue

	link = links[0] 
        full_link = "http://www.ocremix.org" + link
	
	main_page = requests.get(full_link)
	main_page_tree = html.fromstring(main_page.content)

	download_links = main_page_tree.xpath("//a[text()='Download from ocrmirror.org']/@href")
	
	if len(download_links) == 0:
		continue

	download_mp3(download_links[0])
