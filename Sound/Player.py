# Python Package to run Audio files
from ctypes import windll, c_buffer
from time import sleep



class AudioPlayerException(Exception):
    """
        An exception to raise when an error occurs in the audio player
    """
    pass


class _MCI:
    """
        A class to Interact with the Windows MCI API

        This class is Based on Microsoft's MCI (Media Control Interface) API
        The approach was Inspired but not copied from the following sources:
            https://github.com/TaylorSMarks/playsound
    """

    def __init__(self):
        """
            Calling the MCI API from the Windows DLL
                The function need to be in the following format
                self._mci(command, buffer, buffer_size, Callback_handler) -> int
                self._mciError(error_code, buffer, buffer_size)
        """
        self._mci = windll.winmm.mciSendStringA
        self._mciError = windll.winmm.mciGetErrorStringA

    def send_command(self, command):
        """
            Send a command to the MCI API
            :param
                command (String): The command to send
                        The command should be in the following format:
                            "command \"file_path\" type file_type alias alias_name"
            :return:
                None
        """
        buffer = c_buffer(255)
        error_code = self._mci(command.encode(), buffer, 254, 0)

        if error_code:
            raise AudioPlayerException(self.get_error(error_code))
        return buffer.value

    def get_error(self, error_code) -> str:
        """
            Get the error message from the MCI API
            :param
                error_code (int): The error code
            :return:
                String: The error message
        """
        buffer = c_buffer(255)
        self._mciError(error_code, buffer, 254)
        return buffer.value.decode()


class WindowsPlayer:
    """
        A class to perform basic audio function on audio files on Windows
    """

    def __init__(self, file_path: str = None):
        self._mci = _MCI()
        self._file_path = file_path

    # TODO : allow play to specify the start and end position of the audio
    def play(self):
        """
            Play an audio file
            :param
                file_path (String): The path to the audio file
            :return:
                None
        """
        self._mci.send_command(f"open \"{self._file_path}\" alias mp3")
        self._mci.send_command("play mp3")

    def stop(self):
        """
            Stop the audio file
        :return:
            None
        """
        self._mci.send_command("stop mp3")

    def pause(self):
        """
            Pause the audio file
        :return:
            None
        """
        self._mci.send_command("pause mp3")

    def resume(self):
        """
            Resume the audio file
        :return:
            None
        """
        self._mci.send_command("resume mp3")

    def set_volume(self, volume: int):
        """
            Set the volume of the audio file
            :param
                volume (int): The volume to set a number from 0 to 100
            :return:
                None
        """
        if volume < 0 or volume > 100:
            raise ValueError("Volume should be between 0 and 100")
        self._mci.send_command(f"setaudio mp3 volume to {volume * 10}")

    def __del__(self):
        self._mci.send_command("close mp3")


# if __name__ == '__main__':
#     player = WindowsPlayer("E:\Vidio Editing\Music\Lil Nas X - INDUSTRY BABY (Lyrics) _ I told you long ago on the road.mp3")
#     player.play()
#     player.set_volume(10)
#     input("Press Enter to stop the audio")
#     player.stop()
