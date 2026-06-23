#!/usr/bin/env python3
import sys
import os
import time
import libtorrent as lt

def download(magnet: str, save_path: str = "."):
    ses = lt.session()
    ses.listen_on(6881, 6891)

    params = lt.parse_magnet_uri(magnet)
    params.save_path = save_path

    print(f"\n⏳ Fetching metadata...")
    handle = ses.add_torrent(params)

    while not handle.has_metadata():
        time.sleep(1)

    info = handle.get_torrent_info()
    print(f"📦 Name:  {info.name()}")
    print(f"📁 Size:  {info.total_size() / 1_000_000:.1f} MB")
    print(f"💾 Saving to: {save_path}\n")

    while not handle.is_seed():
        s = handle.status()
        bar_len = 30
        filled = int(bar_len * s.progress)
        bar = "█" * filled + "░" * (bar_len - filled)
        dl = s.download_rate / 1000
        ul = s.upload_rate / 1000
        peers = s.num_peers
        print(
            f"\r[{bar}] {s.progress * 100:.1f}%  "
            f"↓ {dl:.0f} kB/s  ↑ {ul:.0f} kB/s  peers: {peers}  ",
            end="", flush=True
        )
        time.sleep(1)

    print(f"\n\n✅ Done! Saved to: {save_path}/{info.name()}")


def main():
    magnet = input("Magnet link: ").strip()
    if not magnet.startswith("magnet:"):
        print("❌ Not a valid magnet link")
        sys.exit(1)

    save_path = input("Save path [~/Downloads]: ").strip() or "~/Downloads"
    save_path = os.path.expanduser(save_path)

    try:
        download(magnet, save_path)
    except KeyboardInterrupt:
        print("\n\n⛔ Cancelled")
        sys.exit(0)


if __name__ == "__main__":
    main()