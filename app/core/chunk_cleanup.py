import asyncio
from datetime import datetime


async def cleanup_old_chunks_once() -> int:
    from app.main import CHUNKS_DIR, CHUNK_TTL

    if not CHUNKS_DIR.exists():
        return 0

    cutoff = datetime.now().timestamp() - CHUNK_TTL.total_seconds()
    removed = 0

    for path in CHUNKS_DIR.iterdir():
        if not path.is_file():
            continue
        if path.stat().st_mtime < cutoff:
            try:
                path.unlink()
                removed += 1
            except OSError:
                pass

    return removed


async def chunk_cleanup_loop() -> None:
    from app.main import CLEANUP_INTERVAL

    while True:
        try:
            await cleanup_old_chunks_once()
        except Exception:
            pass

        await asyncio.sleep(CLEANUP_INTERVAL)
