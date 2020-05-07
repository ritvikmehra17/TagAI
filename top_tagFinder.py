import multi_page_scrap as mps


def tag_query():
    url = "https://top-hashtags.com/instagram/"

    search_term = "Top HashTags on Instagram"
    page = 1
    filename = search_term+'_tag.csv'

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
            
            scraped_tags.extend(output)
            print('total size of collected data', len(scraped_tags))
            page += 1
        

    # save the stuff
    mps.save(scraped_tags,filename)
            

