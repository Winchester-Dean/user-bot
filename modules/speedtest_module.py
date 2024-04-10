from speedtest import Speedtest
from session_config import SessionConfig
from telethon import events

class SpeedTestModule(SessionConfig):
    """Speedtest module; command: <code>.speedtest</code>"""
    async def speedtestt(self, msg):
        try:
            st = Speedtest()

            await msg.edit("Running testing...")

            st.download()
            st.upload()
            st.get_best_server()

            download_speed = st.results.download / 1024 / 1024
            upload_speed = st.results.upload / 1024 / 1024
            ping = st.results.ping

            await msg.edit(
                "<b>Results:</b>\n\n"
                f"<b>🔽 Download:</b> {download_speed:.2f} Mbps\n"
                f"<b>🔼 Upload:</b> {upload_speed:.2f} Mbps\n"
                f"<b>Ping:</b> {ping:.2f} ms",
                parse_mode="html"
            )
        except Exception as error:
            await msg.edit(
                f"⚠️ <b>Error:</b> <code>{error}</code>",
                parse_mode="html"
            )
    
    def start(self):
        self.client.add_event_handler(
            self.speedtestt,
            events.NewMessage(pattern="^[./-_=]*(?i)\.speedtest")
        )
