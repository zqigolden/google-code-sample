"""A video player class."""

from typing import Dict, Optional
from .video_library import VideoLibrary
from .video import Video
from enum import Enum
from random import randint
from .video_playlist import Playlist


class PlayStatus(str, Enum):
    STOPPED = 'STOPPED'
    PLAYING = 'PLAYING'
    PAUSED = 'PAUSED'


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._playing_video: Optional[Video] = None
        self._status: PlayStatus = PlayStatus.STOPPED
        # Using lowercase playlist name as key, original name stored at Playlist.name
        self._play_lists: Dict[str, Playlist] = {}
        # self._flags: {video_id: reason}
        self._flags: Dict[str, str] = {}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        for video in sorted(self._video_library.get_all_videos(), key=lambda x: x.title.lower()):
            if video.video_id in self._flags:
                print(
                    f'{video} - FLAGGED (reason: {self._flags[video.video_id]})')
            else:
                print(video)

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id=video_id)
        if video is None:  # video_id not exist
            print('Cannot play video: Video does not exist')
            return
        if video_id in self._flags:
            print(f'Cannot play video: '
                  f'Video is currently flagged (reason: {self._flags[video_id]})')
            return
        if self._status in [PlayStatus.PLAYING, PlayStatus.PAUSED]:
            self.stop_video()
        self._playing_video = video
        self._status = PlayStatus.PLAYING
        print(f'Playing video: {self._playing_video.title}')

    def stop_video(self):
        """Stops the current video."""
        if self._status in [PlayStatus.PLAYING, PlayStatus.PAUSED]:
            print(f'Stopping video: {self._playing_video.title}')
            self._status = PlayStatus.STOPPED
            self._playing_video = None
        else:
            print('Cannot stop video: No video is currently playing')

    def play_random_video(self):
        """Plays a random video from the video library."""
        videos = [video for video in self._video_library.get_all_videos(
        ) if video.video_id not in self._flags]
        if len(videos) > 0:
            self.play_video(videos[randint(0, len(videos) - 1)].video_id)
        else:
            print("No videos available")

    def pause_video(self):
        """Pauses the current video."""
        if self._status is PlayStatus.STOPPED:
            print('Cannot pause video: No video is currently playing')
        elif self._status is PlayStatus.PAUSED:
            print(f'Video already paused: {self._playing_video.title}')
        else:
            self._status = PlayStatus.PAUSED
            print(f'Pausing video: {self._playing_video.title}')

    def continue_video(self):
        """Resumes playing the current video."""
        if self._status is PlayStatus.STOPPED:
            print('Cannot continue video: No video is currently playing')
        elif self._status is PlayStatus.PLAYING:
            print('Cannot continue video: Video is not paused')
        else:
            self._status = PlayStatus.PLAYING
            print(f"Continuing video: {self._playing_video.title}")

    def show_playing(self):
        """Displays video currently playing."""
        if PlayStatus.STOPPED == self._status:
            print('No video is currently playing')
        else:
            print(f'Currently playing: {self._playing_video} - {self._status}')

    def create_playlist(self, playlist_name: str):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() in self._play_lists:
            print('Cannot create playlist: '
                  'A playlist with the same name already exists')
        else:
            self._play_lists[playlist_name.lower()] = Playlist(
                name=playlist_name)
            print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        video = self._video_library.get_video(video_id=video_id)
        if playlist_name.lower() not in self._play_lists:
            print(
                f'Cannot add video to {playlist_name}: Playlist does not exist')
        elif video is None:
            print(f'Cannot add video to {playlist_name}: Video does not exist')
        elif video_id in self._play_lists[playlist_name.lower()].list:
            print(f'Cannot add video to {playlist_name}: Video already added')
        elif video_id in self._flags:
            print(f'Cannot add video to {playlist_name}: '
                  f'Video is currently flagged (reason: {self._flags[video_id]})')
        else:
            self._play_lists[playlist_name.lower()].list[video_id] = video
            print(f"Added video to {playlist_name}: {video.title}")

    def show_all_playlists(self):
        """Display all playlists."""
        if len(self._play_lists) == 0:
            print('No playlists exist yet')
        else:
            playlist_names = sorted(i.name for i in self._play_lists.values())
            print('\n'.join(['Showing all playlists:'] + playlist_names))

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() not in self._play_lists:
            print(
                f'Cannot show playlist {playlist_name}: Playlist does not exist')
        else:
            print(f'Showing playlist: {playlist_name}')
            videos = [
                i for i in self._play_lists[playlist_name.lower()].list.values()]
            for video in videos:
                if video.video_id in self._flags:
                    print(
                        f'{video} - FLAGGED (reason: {self._flags[video.video_id]})')
                else:
                    print(video)
            if len(videos) == 0:
                print('No videos here yet')

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        video = self._video_library.get_video(video_id=video_id)
        if playlist_name.lower() not in self._play_lists:
            print(
                f'Cannot remove video from {playlist_name}: Playlist does not exist')
        elif video is None:
            print(
                f'Cannot remove video from {playlist_name}: Video does not exist')
        elif video_id not in self._play_lists[playlist_name.lower()].list:
            print(
                f'Cannot remove video from {playlist_name}: Video is not in playlist')
        else:
            title = self._play_lists[playlist_name.lower()
                                     ].list[video_id].title
            del self._play_lists[playlist_name.lower()].list[video_id]
            print(f"Removed video from {playlist_name}: {title}")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() not in self._play_lists:
            print(
                f'Cannot clear playlist {playlist_name}: Playlist does not exist')
        else:
            self._play_lists[playlist_name.lower()].list.clear()
            print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() not in self._play_lists:
            print(
                f'Cannot delete playlist {playlist_name}: Playlist does not exist')
        else:
            del self._play_lists[playlist_name.lower()]
            print(f"Deleted playlist: {playlist_name}")

    #search_mode in ['all', 'tag']
    def _search_video(self, search_term=None, search_mode='all'):
        results = []
        videos = self._video_library.get_all_videos()
        for video in sorted(videos, key=lambda x: x.title.lower()):
            if 'all' == search_mode and search_term.lower() in str(video).lower() and video.video_id not in self._flags:
                results.append(video)
            elif 'tag' == search_mode and search_term.lower() in {i.lower() for i in video.tags} and video.video_id not in self._flags:
                results.append(video)
        if len(results) == 0:
            print(f'No search results for {search_term}')
            return
        print(f'Here are the results for {search_term}:')
        for i, video in enumerate(results, start=1):
            print(f'{i}) {video}')
        print("Would you like to play any of the above? "
              "If yes, specify the number of the video.")
        print("If your answer is not a valid number, "
              "we will assume it's a no.")
        choose = input()
        if choose.isdigit() and 0 < int(choose) <= len(results):
            self.play_video(results[int(choose) - 1].video_id)

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        self._search_video(search_term=search_term, search_mode='all')

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        self._search_video(search_term=video_tag, search_mode='tag')

    def flag_video(self, video_id, flag_reason="Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video = self._video_library.get_video(video_id=video_id)
        if video is None:
            print('Cannot flag video: Video does not exist')
        elif video_id in self._flags:
            print('Cannot flag video: Video is already flagged')
        else:
            self._flags[video_id] = flag_reason
            if self._playing_video and self._playing_video.video_id == video_id:
                self.stop_video()
            print(f'Successfully flagged video:'
                  f' {video.title} (reason: {flag_reason})')

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id=video_id)
        if video is None:
            print('Cannot remove flag from video: Video does not exist')
        elif video_id not in self._flags:
            print('Cannot remove flag from video: Video is not flagged')
        else:
            del self._flags[video_id]
            print(f'Successfully removed flag from video: {video.title}')
