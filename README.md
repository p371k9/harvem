# harvem

Harvesting email addresses from website(s).

### status: PRE ALPHA!!!

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

Tested with Scrapy 2.0.1

