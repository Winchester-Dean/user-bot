import requests

from session_config import SessionConfig
from telethon import events
from bs4 import BeautifulSoup
from faker import Faker

class GoogleModule(SessionConfig):
    """Google search module; command: <code>.google {text}</code>"""

    fake = Faker("ru_RU")

    async def google(self, msg):
        try:
            query = msg.text.split(maxsplit=1)[1]

            search_results = self.google_search(query)

            if search_results:
                result_text = "<b>Google Search Results:</b>\n\n"

                for idx, result in enumerate(search_results, start=1):
                    result_text += f"<b>{idx}. {result['title']}</b>\n"
                    result_text += f"<a href='{result['link']}'>{result['link']}</a>\n"
                    result_text += f"{result['snippet']}\n\n"
                
                await msg.edit(result_text, parse_mode="html")
            else:
                await msg.edit(
                    "<b>No search results found.</b>",
                    parse_mode="html"
                )
        except Exception as error:
            await msg.edit(
                f"⚠ <b>Error:</b> <code>{error}</code>",
                parse_mode="html"
            )
    
    def google_search(self, query):
        url = 'https://www.google.com/search?q=' + '+'.join(query.split())
        headers = {'User-Agent': self.fake.user_agent()}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            search_results = soup.find_all('div', class_='tF2Cxc')
            results = []

            for result in search_results:
                title = result.find('h3').text
                link = result.find('a')['href']
                snippet = result.find('span', class_='aCOpRe').text
                results.append({'title': title, 'link': link, 'snippet': snippet})
            
            return results
        else:
            return None
    
    def start(self):
        self.client.add_event_handler(
            self.google,
            events.NewMessage(pattern="^[./-_=]*(?i)\.google")
        )
