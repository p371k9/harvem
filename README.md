# harvem

### staus: PRE ALPHA!!!

Harvest email addresses with Scrapy-Splash from a specific website:

```
.../harvem$ scrapy crawl site -a url=http://www.autoszovgyongyos.hu/  -o o.csv
```

or from multiple websites listed in a .csv file: 
```
.../harvem$scrapy crawl csv -a file=teszt/tesztin.csv -o o2.csv

```

Tested with Scrapy 2.5.1

