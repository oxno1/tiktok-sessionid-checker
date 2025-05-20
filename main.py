import httpx
import time
import secrets
import threading
from colorama import Fore, Style

class TikTok:
    def __init__(self, file_path: str, threads: int):
        self.valid, self.bad, self.mightbebanned, self.errors, self.checked = 0, 0, 0, 0, 0
        self.threads = threads
        self.file_path = file_path
        self.__load_sessionids()
        self.lock = threading.Lock()
        self.total = len(self.sessions_list)
        
    def __load_sessionids(self):
        lines = open(self.file_path, "r").read().splitlines()
        self.sessions_list = [line for line in lines if line.strip()]

    def __chunkify(self, lst: list, n: int):
        return [lst[i::n] for i in range(n)]

    def checkApi(self, sessionid: str, client: httpx.Client):
        try:
            did = int(bin(int(time.time()) + secrets.randbelow(1000000))[2:] + '00101101010100010100011000000110', 2)
            return client.get(
                url=f"https://api31-normal-alisg.tiktokv.com/passport/account/info/v2/?aid=1233&sdk_version=1012000&refresh_num=11&version_code=30.0.0&language=en-SA&display_density=1284*2778&&device_id={did}&channel=AppStore&click_banner=32&mcc_mnc=42001&show_limit=0&resolution=1284*2778&aid=1233&version_name=9.1.1&os=ios&update_version_code=91115&access=WIFI&carrier=stc&ac=WIFI&os_version=17.3&is_cold_start=0&reason=0&device_platform=iphone&device_brand=AppleInc.&device_type=iPhone13,4",
                headers={
                    "accept-encoding": "gzip",
                    "cookie": f"sessionid={sessionid}",
                    "host": "api31-normal-alisg.tiktokv.com",
                    "user-agent": "Dart/3.4 (dart:io)"
                }
            ).json()['data']
        except Exception as e:
            return False

    def proccess_result(self, checked_line: str, response):
        with self.lock:
            self.checked += 1
            if response:
                if 'error_code' not in response:
                    if response['username'] and response['username'] != '':
                        with open("Valids.txt", "a", encoding="utf-8") as w:
                            w.write(f"{response['username']}:{checked_line}\n")
                            self.valid += 1
                    else:
                        with open("MightBeBanned.txt", "a", encoding="utf-8") as w:
                            w.write(f"{checked_line}\n")
                            self.mightbebanned += 1
                else:
                    with open("Bads.txt", "a", encoding="utf-8") as w:
                        w.write(f"{checked_line}\n")
                    self.bad += 1
            else:
                with open("toCheckAgain[Error].txt", "a", encoding="utf-8") as w:
                    w.write(f"{checked_line}\n")
                self.errors += 1

    def console(self):
        while True:
            with self.lock:
                remaining = self.total - self.checked
                print(
                    f"{Fore.GREEN}Valid: {self.valid:,} {Fore.RED}| Bad: {self.bad:,} {Fore.YELLOW}| Errors: {self.errors:,} {Fore.CYAN}| Remaining: {remaining:,} lines{Style.RESET_ALL}",
                    end="\r"
                )
                if self.checked >= self.total:
                    print()
                    break
            time.sleep(1)

    def main(self, list_: list[str]):
        httpClient = httpx.Client()
        for line in list_:
            sessionid = line.split(":")[2] if len(line.split(":")) > 2 else ""
            result = self.checkApi(sessionid=sessionid, client=httpClient)
            self.proccess_result(line, result)

    def run(self):
        chunked_file = self.__chunkify(self.sessions_list, self.threads)
        
        threads = []
        console_thread = threading.Thread(target=self.console)
        console_thread.start()

        for accounts_chunk in chunked_file:
            t = threading.Thread(target=self.main, args=[accounts_chunk])
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        console_thread.join()
        input("Press Enter To Exit :>")

TikTok(
    file_path=input(f"{Style.BRIGHT}Enter accounts-file-path [ex-> sessions.txt]: {Style.RESET_ALL}"),
    threads=10
).run()
