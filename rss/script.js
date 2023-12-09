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

    let items = Array.from(rssFeed.querySelectorAll('item'));
    // Sort items by date
    items.sort((a, b) => {
        let dateA = new Date(a.querySelector('pubDate').textContent);
        let dateB = new Date(b.querySelector('pubDate').textContent);
        return dateB - dateA; // Sort in descending order
    });

    let htmlContent = '';

    items.forEach((item, index) => {
        const title = item.querySelector('title').textContent;
        const link = item.querySelector('link').textContent;
        const pubDate = item.querySelector('pubDate') ? new Date(item.querySelector('pubDate').textContent).toLocaleString() : 'No date';
        const description = item.querySelector('description').textContent;

        htmlContent += `
            <tr>
                <td>${title}</td>
                <td>${pubDate}</td>
                <td><a href="${link}" target="_blank">Read More</a></td>
                <td>
                    <button class="btn btn-secondary btn-sm" onclick="toggleDescription('desc-${index}')">Toggle Description</button>
                    <p id="desc-${index}" style="display: none;">${description}</p>
                </td>
            </tr>`;
    });

    document.getElementById('rss-feeds').innerHTML += htmlContent;
}

function toggleDescription(id) {
    const element = document.getElementById(id);
    if (element.style.display === "none") {
        element.style.display = "block";
    } else {
        element.style.display = "none";
    }
}

// Replace these URLs with the actual RSS feed URLs
displayRSSFeed('https://feeds.npr.org/1001/rss.xml');
displayRSSFeed('https://back.nber.org/rss/new.xml');
displayRSSFeed('https://apps.bea.gov/rss/rss.xml');
displayRSSFeed('http://export.arxiv.org/rss/econ');
displayRSSFeed('https://jmlr.org/jmlr.xml');
