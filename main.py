from media_downloader import start, logger
import asyncio
from utils.meta import print_meta
import logging

async def main():
    while True:
        try:
            await start()  # DO NOT await
            print("Section ended:)")
        except Exception as e:
            print("Error:", e)

        await asyncio.sleep(30 * 60)

if __name__ == "__main__":
    print_meta(logger)
    asyncio.run(main())
    start_web_ui(port=8080)
