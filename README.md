# harvem

Harvesting email addresses from website(s). Another email scraper.

The scrapy_splash package must be installed even if you are not going to use Splash.

Example command lines. First with a normal Scrapy request, second with a Scrapy-Splash.

To collect email addresses from a specific website:

```
.../harvem$ scrapy crawl site -a url=http://www.autoszovgyongyos.hu/  -o o.csv
.../harvem$ scrapy crawl sitesplash -a url=http://www.autoszovgyongyos.hu/  -o o.csv
```

To collect email from multiple sites listed in a .csv file:
```
.../harvem$ scrapy crawl csv -a file=teszt/tesztin.csv -o o2.csv
.../harvem$ scrapy crawl csvsplash -a file=teszt/tesztin.csv -o o2.csv

```

From list file:
```
.../harvem$ scrapy crawl list -a file=teszt/tesztin.lll -o o3.csv
.../harvem$ scrapy crawl listsplash -a file=teszt/tesztin.lll -o o3.csv

```

With proxy: 
```
.../harvem$ scrapy crawl site -s PROXY=http://localhost:8118 -a url=http://www.autoszovgyongyos.hu/  -o o.csv
.../harvem$ scrapy crawl sitesplash -s PROXY=http://localhost:8118 -a url=http://www.autoszovgyongyos.hu/  -o o.csv
```

Set the LEA variable so that you can determine which pages to crawl. The following example will crawl all the pages:
```
.../harvem$ scrapy crawl site -s LEA= -s DOWNLOAD_DELAY=2 -a url=https://golyankerekpar.hu -o golyan.csv
```

You can specify the identifier field of the input csv like this:
```
scrapy crawl csv -s INID=placeid -a file=../mailwalk/teszt/pizza.tatabanya2.csv -o tatab.csv
```

If you are using dockered Splash and the proxy is running on localhost, check the end of the settings.py file. More info: https://stackoverflow.com/questions/48546124/what-is-linux-equivalent-of-host-docker-internal/61001152

Tested with Scrapy 2.0.1

