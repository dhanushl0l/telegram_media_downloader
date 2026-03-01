from media_downloader import start, logger
import asyncio
from utils.meta import print_meta
import os
import time
from pathlib import Path


async def main():
    cleanup_task = asyncio.create_task(daily_cleanup())
    try:
        while True:
            try:
                await start()
                print("Section ended :)")
            except Exception as e:
                print("Error:", e)
            await asyncio.sleep(30 * 60)
    finally:
        cleanup_task.cancel()
        try:
            await cleanup_task
        except asyncio.CancelledError:
            print("Cleanup task cancelled cleanly.")


async def daily_cleanup():
    while True:
        try:
            await asyncio.to_thread(cleanup_old_videos, "video", 7)
            print("Cleanup done")
        except Exception as e:
            print("Cleanup error:", e)
        await asyncio.sleep(24 * 60 * 60)


def cleanup_old_videos(videos_dir: str, days: int):
    cutoff_time = time.time() - (days * 86400)
    videos_path = Path(videos_dir)

    if not videos_path.exists():
        raise FileNotFoundError(f"{videos_dir} does not exist")

    for entry in os.scandir(videos_path):
        try:
            if entry.is_file(follow_symlinks=False):
                if entry.stat().st_mtime < cutoff_time:
                    os.remove(entry.path)

            elif entry.is_dir(follow_symlinks=False):
                with os.scandir(entry.path) as sub_it:
                    for sub in sub_it:
                        if sub.is_file(follow_symlinks=False):
                            if sub.stat().st_mtime < cutoff_time:
                                os.remove(sub.path)

                # Check if folder is now empty and remove it
                with os.scandir(entry.path) as check_it:
                    if not any(check_it):
                        os.rmdir(entry.path)

        except Exception as e:
            print(f"Failed on {entry.path}: {e}")


if __name__ == "__main__":
    print_meta(logger)
    asyncio.run(main())