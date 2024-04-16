import os
import platform
import psutil
import contextlib

from session_config import SessionConfig
from telethon import events

def bytes_to_gb(b: int) -> int:
    return round(b / 1024 ** 3, 1)

def bytes_to_megabytes(b: int) -> int:
    return round(b / 1024 / 1024, 1)

class ServerInfoModule(SessionConfig):
    """Module for getting information about server; command: <code>.serverinfo</code>"""
    
    strings = {
        "name": "ServerInfo",
        "loading": (
            "<b>Loading server info...</b>"
        ),
        "serverinfo": (
            "<b>💻 Server Info: \n\n"
            "🐧 OS: {os}\n"
            "⚙️ Karnel: {karnel}\n"
            "💻 Arch: {arch}\n"
            "💾 Disk: {disk_used}G / {disk_total}G / ({disk_load}%)\n"
            "🔄 CPU: {cpu} cores {cpu_load}%\n"
            "🧠 RAM: {ram}MB / {ram_load_mb}MB ({ram_load}%)</b>"
        ),
    }

    async def serverinfo(self, msg):
        try:
            await msg.edit(self.strings["loading"], parse_mode="html")

            info = {
                "os": "n/a",
                "karnel": "n/a",
                "arch": "n/a",
                "disk_total": "n/a",
                "disk_used": "n/a",
                "disk_load": "n/a",
                "cpu": "n/a",
                "cpu_load": "n/a",
                "ram": "n/a",
                "ram_load_mb": "n/a",
                "ram_load": "n/a"
            }

            with contextlib.suppress(Exception):
                system = os.popen("cat /etc/*release").read()
                b = system.find('DISTRIB_DESCRIPTION=') + 21
                system = system[b : system.find('"', b)]
                info["os"] = system
            
            with contextlib.suppress(Exception):
                o = platform.system()
                g = platform.release()

                info["karnel"] = (o + ' ' + g)
            
            with contextlib.suppress(Exception):
                info["arch"] = platform.architecture()[0]
            
            with contextlib.suppress(Exception):
                disk_partitions = psutil.disk_partitions(all=False)
                
                for partition in disk_partitions:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                    info["disk_total"] = bytes_to_gb(partition_usage.total)
            
            with contextlib.suppress(Exception):
                disk_partitions = psutil.disk_partitions(all=False)
                
                for partition in disk_partitions:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                    info["disk_used"] = bytes_to_gb(partition_usage.used)

            with contextlib.suppress(Exception):
                disk_partitions = psutil.disk_partitions(all=False)
                
                for partition in disk_partitions:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                    info["disk_load"] = partition_usage.percent
            
            with contextlib.suppress(Exception):
                info["cpu"] = psutil.cpu_count(logical=True)
            
            with contextlib.suppress(Exception):
                info["cpu_load"] = psutil.cpu_percent()
            
            with contextlib.suppress(Exception):
                info["ram"] = bytes_to_megabytes(
                    psutil.virtual_memory().total - psutil.virtual_memory().available
                )
            
            with contextlib.suppress(Exception):
                info["ram_load_mb"] = bytes_to_megabytes(
                    psutil.virtual_memory().total
                )
            
            with contextlib.suppress(Exception):
                info["ram_load"] = psutil.virtual_memory().percent
            
            await msg.edit(
                self.strings["serverinfo"].format(**info),
                parse_mode="html"
            )
        except Exception as error:
            await msg.edit(
                f"⚠️ <b>Error:</b> <code>{error}</code>",
                parse_mode="html"
            )
    
    def start(self):
        self.client.add_event_handler(
            self.serverinfo,
            events.NewMessage(pattern="^[./-_=]*(?i)\.serverinfo")
        )
