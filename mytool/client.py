import subprocess
import threading
import time
import win32gui
import win32con


class client(threading.Thread):
    def __init__(self):
        super.__init__()
        pass

    @classmethod
    def get_handle(cls, window_name):
        return win32gui.FindWindow(None, window_name)

    @classmethod
    def _start_client(cls):
        try:
            import subprocess

            cls.process = subprocess.Popen(
                [
                    "H:\MuMuPlayer-12.0-1\shell\MuMuPlayer.exe",
                    "-p",
                    "com.netease.onmyoji.wyzymnqsd_cps",
                    "-v",
                    "0",
                ],
            )
            print("client started")
            time.sleep(1)
            handle = cls.get_handle("MuMu模拟器12")
            if handle:
                print(f"handle found: {handle}")
                # win32gui.ShowWindow(handle, win32con.SW_MINIMIZE)
                # cls.move_to_second_desktop(handle)
                # win32gui.ShowWindow(handle, win32con.SW_RESTORE)
        except Exception as e:
            print(f"Error executing command: {e}")

    @classmethod
    def start(cls):
        threading.Thread(target=cls._start_client).start()

    @classmethod
    def stop(cls):
        if hasattr(cls, "process"):
            cls.process.kill()
            # cls.app=False
            print("client stopped")
        pass


if __name__ == "__main__":
    client.start()
    time.sleep(10)
    print(client.app)
    if client.app:
        client.stop()
