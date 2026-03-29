
import time
liked_songs = {
    "Shake It Off": {
        "artist": "Taylor Swift",
        "duration": (3, 23),
        "genre": "Pop"
    },
    "Shemesh": {
        "artist": "Mergi",
        "duration": (2, 33),
        "genre": "Israeli"
    },
    "Chop Suey!": {
        "artist": "System of a Down",
        "duration": (3, 30),
        "genre": "Metal"
    },
    "Mimaamakim": {
        "artist": "Idan Raichel",
        "duration": (4, 33),
        "genre": "Israeli"
    },
    "Do I Wanna Know?": {
        "artist": "Arctic Monkeys",
        "duration": (4, 26),
        "genre": "Rock"
    },
    "Love Story": {
        "artist": "Taylor Swift",
        "duration": (3, 55),
        "genre": "Pop"
    },
    "Bo’ee": {
        "artist": "Idan Raichel",
        "duration": (4, 45),
        "genre": "Israeli"
    }
}
def duration_to_seconds(duration):
    minutes, seconds = duration
    return minutes * 60 + seconds


def seconds_to_duration_tuple(total_seconds):
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return (minutes, seconds)


# Step 1: add songs
def add_songs(playlist, new_songs):
    for title, meta in new_songs.items():
        playlist[title] = meta


# Step 2: check if song exists and optionally remove it
def song_exists_and_optionally_remove(playlist, title, remove=False):
    if title in playlist:
        if remove:
            del playlist[title]
            return True, f"Removed: {title}"
        return True, f"Found: {title}"
    return False, f"Not found: {title}"


# Step 3: remove all songs by an artist
def remove_songs_by_artist(playlist, artist_name):
    to_remove = [title for title, meta in playlist.items() if meta.get("artist") == artist_name]
    for title in to_remove:
        del playlist[title]
    return to_remove


# Step 4: build Israeli playlist under max length (minutes)
def israeli_playlist_under_duration(playlist, max_minutes=3.5):
    max_seconds = int(max_minutes * 60)
    result = {}
    for title, meta in playlist.items():
        if meta.get("genre") == "Israeli":
            if duration_to_seconds(meta.get("duration", (0, 0))) <= max_seconds:
                result[title] = meta
    return result


# Step 5: sleep timer playback (simulated). The `speed` parameter scales sleep per real second.
def sleep_timer_playback(playlist, timer_minutes, speed=0.02):
    """Simulate playback with a timer.
    speed: seconds of real time that represent 1 playback second (smaller => faster simulation).
    """
    remaining_seconds = int(timer_minutes * 60)
    if remaining_seconds <= 0:
        print("Timer is zero or negative; nothing to play.")
        return

    for title, meta in playlist.items():
        song_seconds = duration_to_seconds(meta.get("duration", (0, 0)))
        print(f"Now playing: {title} by {meta.get('artist')} (duration {meta.get('duration')})")
        # If the song is longer than remaining time, play partially then stop
        if song_seconds > remaining_seconds:
            # simulate only remaining_seconds
            for sec in range(1, remaining_seconds + 1):
                time.sleep(speed)
            print(f"Timer ended. {title} was played partially ({seconds_to_duration_tuple(remaining_seconds)}). Stopping.")
            return
        else:
            # simulate full song
            for sec in range(1, song_seconds + 1):
                time.sleep(speed)
            remaining_seconds -= song_seconds
            if remaining_seconds > 0:
                print(f"Finished {title}. Time left: {seconds_to_duration_tuple(remaining_seconds)}")
            else:
                print(f"Finished {title}. Timer ended exactly now.")
                return

    # playlist ended before timer
    print("Playlist ended before timer. No more songs.")


def print_playlist(playlist, title="Playlist"):
    print(f"--- {title} ({len(playlist)} songs) ---")
    for t, m in playlist.items():
        print(f"{t} — {m.get('artist')} — {m.get('duration')} — {m.get('genre')}")
    print("------------------------------\n")


def main():
    # Work on a copy to avoid mutating global test data inadvertently
    playlist = dict(liked_songs)

    # Step 1: add at least 3 songs (structure must match)
    my_songs = {
        "New Dawn": {"artist": "Local Artist", "duration": (3, 10), "genre": "Indie"},
        "Short Israeli": {"artist": "Artist X", "duration": (2, 50), "genre": "Israeli"},
        "Calm Night": {"artist": "Sleepy Band", "duration": (4, 0), "genre": "Ambient"},
    }
    print("before adding songs:")
    print_playlist(playlist, "Before adding songs")
    add_songs(playlist, my_songs)
    print_playlist(playlist, "After adding 3 songs")

    # Step 2: check and optionally remove a song by title
    title_to_check = "Shake It Off"
    existed, msg = song_exists_and_optionally_remove(playlist, title_to_check, remove=True)
    print(msg)
    print_playlist(playlist, f"After checking/removing '{title_to_check}'")

    # Step 3: remove all songs by an artist
    artist_to_remove = "Idan Raichel"
    removed = remove_songs_by_artist(playlist, artist_to_remove)
    print(f"Removed songs by {artist_to_remove}: {removed}")
    print_playlist(playlist, f"After removing artist '{artist_to_remove}'")

    # Step 4: create Israeli playlist under 3.5 minutes
    israel_short = israeli_playlist_under_duration(playlist, max_minutes=3.5)
    print_playlist(israel_short, "Israeli songs under 3.5 minutes")

    # Step 5 (challenge): simulate sleep timer playback
    # Example: a 5-minute timer (simulation speed set to 0.01 for fast demo)
    print("Starting sleep timer playback simulation (5 minutes, fast mode)...")
    sleep_timer_playback(playlist, timer_minutes=50, speed=0.01)


if __name__ == "__main__":
    main()