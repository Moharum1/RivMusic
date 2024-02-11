"""
    A Command Line Interface to play music
"""
import cmd
from RivMusic.Sound.Player import WindowsPlayer


class Musically(cmd.Cmd):
    intro = "Welcome to Musically"
    prompt = "Musically> "

    def do_EOF(self, line):
        return True

    def __init__(self):
        super().__init__()
        self._player = None

    def do_play(self, file_path):
        """
            Play an audio file
            :param
                file_path (String): The path to the audio file
            :return:
                None
        """
        print(f"Playing {file_path}")
        self._player = WindowsPlayer(file_path)
        self._player.play()

    def do_volume(self, volume: int):
        """
            Set the volume of the audio file
            :param
                volume (int): The volume to set a number from 0 to 100
            :return:
                None
        """
        if self._player is None:
            print("No audio file is playing")
            return
        self._player.set_volume(int(volume))

    def do_pause(self):
        """
            Stop the audio file
        :return:
            None
        """
        if self._player is None:
            print("No audio file is playing")
            return
        self._player.pause()

    def do_resume(self):
        """
            Resume the audio file
        :return:
            None
        """
        if self._player is None:
            print("No audio file is playing")
            return
        self._player.resume()


if __name__ == "__main__":
    Musically().cmdloop()
