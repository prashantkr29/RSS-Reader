from flask import Flask, render_template
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/')
def index():
    # Fetch XML data from wired.com
    url = 'https://www.wired.com/feed/rss'
    response = requests.get(url)
    xml_data = response.text

    # Parse XML data
    root = ET.fromstring(xml_data)

    # Initialize variables
    news_items = []

    # Iterate over each item in the XML feed
    for item in root.findall('.//item'):
        # Extract data from each item
        title = item.find('title').text
        description = item.findtext('description')
        link = item.find('link').text
        category = item.find('category').text
        image_url = item.find('media')
        pubdate = item.find('pubDate').text
        pubdate = pubdate[:26]

        print(image_url)
        # Append data to news_items list
        news_items.append({
            'title': title,
            'link': link,
            'description':description,
            'category':category,
            'pubdate':pubdate,
            'image':image_url
        })

    # Render the template with fetched data
    return render_template('index.html', news_items=news_items)

if __name__ == '__main__':
    app.run()
