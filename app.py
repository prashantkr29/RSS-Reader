from flask import Flask, render_template
import requests
import xml.etree.ElementTree as ET
import feedparser

app = Flask(__name__)

@app.route('/')
def index():
    # Fetch XML data from wired.com
    url = 'https://www.wired.com/feed/rss'
    response = requests.get(url)
    xml_data = response.text

    # Parse XML data
    root = ET.fromstring(xml_data)

    feed = feedparser.parse(url)


    # Initialize variables
    news_items = []
    # Iterate over each item in the XML feed
    for item in root.findall('.//item'):
        # Extract data from each item
        title = item.find('title').text
        description = item.findtext('description')
        link = item.find('link').text
        category = item.find('category').text
       


        pubdate = item.find('pubDate').text
        pubdate = pubdate[:26]


        # Append data to news_items list
        news_items.append({
            'title': title,
            'link': link,
            'description':description,
            'category':category,
            'pubdate':pubdate
        })
     
        

    i=0
    for entry in feed.entries:
        image_url = entry.media_thumbnail[0]['url'] if 'media_thumbnail' in entry else None
        #print(image_url)
        news_items[i]['image_url'] = image_url
        # print(news_items[i])
        i+=1

    # Render the template with fetched data
    return render_template('index.html', news_items=news_items)

if __name__ == '__main__':
    app.run()
