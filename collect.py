"""Collect taste-relevant data from Spotify."""

import json
from pathlib import Path

from spotify_client import get_client

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def collect_top_items(sp):
    """Fetch top tracks and artists across all time ranges."""
    results = {}
    for time_range in ("short_term", "medium_term", "long_term"):
        results[f"top_tracks_{time_range}"] = sp.current_user_top_tracks(
            limit=50, time_range=time_range
        )["items"]
        results[f"top_artists_{time_range}"] = sp.current_user_top_artists(
            limit=50, time_range=time_range
        )["items"]
    return results


def collect_saved_tracks(sp):
    """Fetch all saved/liked tracks."""
    tracks = []
    offset = 0
    while True:
        batch = sp.current_user_saved_tracks(limit=50, offset=offset)["items"]
        if not batch:
            break
        tracks.extend(batch)
        offset += 50
    return tracks


def collect_audio_features(sp, track_ids):
    """Fetch audio features for a list of track IDs (batches of 100)."""
    features = []
    for i in range(0, len(track_ids), 100):
        batch = sp.audio_features(track_ids[i : i + 100])
        features.extend(f for f in batch if f is not None)
    return features


def collect_recently_played(sp):
    """Fetch recently played tracks (max 50)."""
    return sp.current_user_recently_played(limit=50)["items"]


def save(name, data):
    path = DATA_DIR / f"{name}.json"
    path.write_text(json.dumps(data, indent=2))
    print(f"  Saved {path} ({len(data) if isinstance(data, list) else 'object'})")


def main():
    sp = get_client()

    print("Collecting top items...")
    top = collect_top_items(sp)
    for key, items in top.items():
        save(key, items)

    print("Collecting saved tracks...")
    saved = collect_saved_tracks(sp)
    save("saved_tracks", saved)

    print("Collecting recently played...")
    recent = collect_recently_played(sp)
    save("recently_played", recent)

    # Gather all unique track IDs for audio features
    all_track_ids = set()
    for key, items in top.items():
        if "tracks" in key:
            all_track_ids.update(t["id"] for t in items)
    all_track_ids.update(t["track"]["id"] for t in saved)
    all_track_ids.update(t["track"]["id"] for t in recent)

    print(f"Collecting audio features for {len(all_track_ids)} tracks...")
    features = collect_audio_features(sp, list(all_track_ids))
    save("audio_features", features)

    print("Done.")


if __name__ == "__main__":
    main()
