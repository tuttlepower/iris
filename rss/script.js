async function loadRSSFeed(url) {
    try {
        const response = await fetch(`https://api.allorigins.win/get?url=${encodeURIComponent(url)}`);
        const data = await response.json();
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(data.contents, "text/xml");
        return xmlDoc;
    } catch (error) {
        console.error('Error fetching RSS feed:', error);
        return null;
    }
}

async function displayRSSFeed(url) {
    const rssFeed = await loadRSSFeed(url);
    if (!rssFeed) return;

    const items = rssFeed.querySelectorAll('item');
    let htmlContent = '';

    items.forEach(item => {
        const title = item.querySelector('title').textContent;
        const link = item.querySelector('link').textContent;
        const description = item.querySelector('description').textContent;
        let image = '';
        if (item.querySelector('enclosure')) {
            image = item.querySelector('enclosure').getAttribute('url');
        }

        htmlContent += `
            <div class="col-md-4">
                <div class="card">
                    ${image ? `<img src="${image}" class="card-img-top" alt="${title}">` : ''}
                    <div class="card-body">
                        <h5 class="card-title">${title}</h5>
                        <p class="card-text">${description}</p>
                        <a href="${link}" class="btn btn-primary">Read More</a>
                    </div>
                </div>
            </div>`;
    });

    document.getElementById('rss-feeds').innerHTML += htmlContent;
}

// Replace these URLs with the actual RSS feed URLs
displayRSSFeed('https://feeds.npr.org/1001/rss.xml');
displayRSSFeed('https://feeds.npr.org/1001/rss.xml');
displayRSSFeed('https://back.nber.org/rss/new.xml');
displayRSSFeed('https://apps.bea.gov/rss/rss.xml');
displayRSSFeed('http://export.arxiv.org/rss/econ');
displayRSSFeed('https://jmlr.org/jmlr.xml');

