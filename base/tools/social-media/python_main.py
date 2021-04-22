import json
import requests

from typing import List
from N4Tools.Design import ThreadAnimation
from N4Tools.Design import Color


class SocialMedia:
    status_200: List[str] = []

    def __init__(self):
        self.username: str = input('\033[33mUsername\033[32m~\033[31m/\033[0m$ ')

    def get_request(self, url: str) -> bool:
        try:
            req = requests.get(url, timeout=5)
        except:
            return False
        if req.status_code == 200:
            return True
        return False

    def data(self) -> dict:
        with open("data.json") as f:
            data = json.load(f)
        return data

    @ThreadAnimation(kwargs={"text":"Loading [0/168] ..."})
    def start_loop(thread, self) -> None:
        counter: int = 0
        for website_name, website_data in self.data().items():
            counter += 1
            if website_data.get("type") == "statusCode":
                status: bool = self.get_request(
                    website_data.get("url").replace("%s",self.username),
                )
                thread.set_kwargs(text=f"Loading [{counter}/168] ...")
                if status:
                    self.status_200.append(website_name)
        thread.kill()
        self.show_data()

    def show_data(self) -> None:
        websites_names: List[str] = sorted(self.status_200)
        data: dict = self.data()
        for name in websites_names:
            print(f"[\x1B[32m+\x1B[0m] \x1B[32m{name}: \x1B[0m{data.get(name).get('url').replace('%s',self.username)}");

if __name__ == "__main__":
    Obj = SocialMedia()
    Obj.start_loop()