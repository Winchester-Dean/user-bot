from session_config import SessionConfig
from telethon import events
from googlesearch import search

class GoogleSearchModule(SessionConfig):
    """Google search module; command: <code>.google</code>"""
    async def google_search_handler(self, msg):
        query = msg.text.split(" ", 1)[1]
        search_results = search(query, num=5, stop=5, lang="en")
        response = f"<b>Google search results for:</b> <i>{query}</i>\n\n"

        for idx, result in enumerate(search_results, start=1):
            response += f"<b>{idx}.</b> <a href='{result}'>{result}</a>\n"

        await msg.reply(response, parse_mode="html")

    def start(self):
        self.client.add_event_handler(
            self.google_search_handler,
            events.NewMessage(pattern="^[./-_=]*(?i)\.google")
        )
