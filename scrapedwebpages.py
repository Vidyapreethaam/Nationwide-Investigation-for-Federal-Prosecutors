import urllib.request
from bs4 import BeautifulSoup as BS
import csv
# quote_page = "https://www.justice.gov/news?date%5Bvalue%5D%5Bmonth%5D=&date%5Bvalue%5D%5Byear%5D=&f%5B0%5D=field_pr_component%3A451&f%5B1%5D=type%3Apress_release&f%5B2%5D=field_pr_topic%3A25306"

class Release(object):
    def __init__(self, title, releaseDate, body):
        self.title = title
        self.releaseDate = releaseDate
        self.body = body
        
    def __iter__(self):
        return iter([self.title, self.releaseDate, self.body])

def getReleases(quote_page):
    page = urllib.request.urlopen(quote_page)
    soup = BS(page, 'html.parser')
    links = soup.findAll('div', attrs={'class':'views-field views-field-title'})

    for link in links:
        temp = "https://www.justice.gov" + link.find('a')['href'].strip()
        # print(temp)

        sub_page = urllib.request.urlopen(temp)
        soup1 = BS(sub_page, 'html.parser')


        title = soup1.find('h1', attrs={'class':'node-title'}).get_text(strip=True)
        releaseDate = soup1.find('span', attrs={'class':'date-display-single'})['content'].strip()
        body = soup1.find('div', attrs={'class':'field field--name-field-pr-body field--type-text-long field--label-hidden'}).get_text(strip=True)
        pressReleases.append(Release(title, releaseDate, body))

if __name__ == "__main__":
    quote_page = "https://www.justice.gov/usao/pressreleases?items_per_page=50&f%5B0%5D=field_pr_topic%3A34671&f%5B1%5D=field_pr_topic%3A34596"
    pressReleases = []
    lastPage = 26

    getReleases(quote_page)

    for count in range(1, lastPage + 1):
        try:
            new_quote_page = quote_page + "&page=" + str(count)
            getReleases(new_quote_page)
            print(count)
        except:
            print("Page {} not extracted".format(str(count)))
            continue

    
    headers = ["Title", "Release Date", "Data"]
    with open("pressReleases.csv", 'w', encoding='utf-8') as csv_file:
        wr = csv.writer(csv_file, delimiter=',', lineterminator='\n')
        wr.writerow(headers)
        wr.writerows(pressReleases)
        # for pr in pressReleases:
        #     wr.writerow(list(pr))
# r = pressReleases[67]
# print(r.title, "\n", r.releaseDate, "\n", r.body)
# temp = "https://www.justice.gov" + links[0].find('a')['href'].strip()
# sub_page = urllib.request.urlopen(temp)
# soup1 = BS(sub_page, 'html.parser')
# title = soup1.find('h1', attrs={'class':'node-title'}).get_text(strip=True)
# releaseDate = soup1.find('span', attrs={'class':'date-display-single'})['content'].strip()
# body = soup1.find('div', attrs={'class':'field field--name-field-pr-body field--type-text-long field--label-hidden'}).get_text(strip=True)

# print(title, "\n", releaseDate, "\n", body)
# print(releaseDate)
