import multi_page_scrap as mps

# "https://www.flipkart.com/search?q=tv&page=1"

def tagQuery(search_term):
    url = "https://top-hashtags.com/search/?"
    page = 1
    scraped_tags = []
    while True:
        starturl = f"{url}q={search_term}&opt=top&sp={page}"
        print('getting data from',starturl,'...')
        soup = mps.get(starturl)
        if page>100:
            break
        if len(scraped_tags)>100:
            break
        if not soup:
            print('scraper closed')
            break
        else:
            output = mps.extract(soup)
            if len(output) == 0:
                print('scraper closed')
                break
            counter = len(scraped_tags)
            if len(scraped_tags) >0 :
                for item in output:
                    if item in scraped_tags:
                        counter-=1
                if counter == 0:
                    print('scraper closed')
                    break
                print(counter,)
            scraped_tags.extend(output)
            print('total size of collected data', len(scraped_tags))
            page += 1

    # save the stuff
    return scraped_tags



if __name__ == "__main__":
    data =tagQuery('red')
    print(data)


