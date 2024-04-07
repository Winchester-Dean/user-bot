import speedtest

from session_config import SessionConfig
from telethon import events

class SpeedTestModule(SessionConfig):
    """Speedtest module; command: <code>.speedtest</code>"""
    async def speedtest(self, msg):
        try:
            st = speedtest.Speedtest()

            await msg.edit("Running testing...")

            st.download()
            st.upload()
            st.get_best_server()

            download_speed = st.results.download / 1024 / 1024
            upload_speed = st.results.upload / 1024 / 1024
            ping = st.results.ping

            await msg.edit(
                "<b>Results:\n\n</b>",
                f"<b>🔽 Download:</b> {download_speed:.2f} Mbps\n"
                f"<b>🔼 Upload:</b> {upload_speed:.2f} Mbps\n"
                f"<b>Ping:</b> {ping:.2f} ms",
                parse_mode="html"
            )
        except Exception as error:
            await msg.edit(
                f"⚠️ <b>Error:</b> <code>{error}</code>"
            )
    
    def start(self):
        self.client.add_event_handler(
            self.speedtest,
            events.NewMessage(pattern=r"^[./-_=]*(?i)\.speedtest$")
        )
