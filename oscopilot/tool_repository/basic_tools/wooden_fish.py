import os

class VideoPlayer:
    def __init__(self, vlc_path='/Applications/VLC.app/Contents/MacOS/VLC'):
        self.vlc_path = vlc_path

    def play_video(self, video_path, times):
        """
        Play a video a specified number of times using VLC.

        Args:
        video_path (str): The path to the video file.
        times (int): The number of times to play the video.

        Returns:
        None
        """
        for _ in range(times):
            os.system(f'"{self.vlc_path}" --fullscreen --play-and-exit "{video_path}"')

class WoodFishTapper:
    def __init__(self, video_player, video_path):
        self.video_player = video_player
        self.video_path = video_path

    def tap_wood_fish(self):
        """
        Calculate the number of times the video should be played based on user input.
        """
        try:
            taps = int(input("How many times do you want to tap the wood fish? "))
            if taps <= 0:
                print("The number of taps must be a positive integer.")
            else:
                video_play_times = taps // 10
                if video_play_times > 0:
                    print(f"The video will play {video_play_times} times.")
                    self.video_player.play_video(self.video_path, video_play_times)
                else:
                    print("The number of taps is too low to play the video.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    video_player = VideoPlayer()
    wood_fish_tapper = WoodFishTapper(video_player, "/Users/suya/IMG_3571.MP4")
    wood_fish_tapper.tap_wood_fish()