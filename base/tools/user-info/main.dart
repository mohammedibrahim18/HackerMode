import 'dart:io';
import 'package:http/http.dart' as http;

String input(text){
  stdout.write(text);
  return stdin.readLineSync();
}

class SocialMedia{
  var urls;
  var userName;

  SocialMedia(userName){
    this.userName = userName;
    this.urls= {
    "github":"https://github.com/$userName",
    "youtube":"https://www.youtube.com/c/$userName",
    "instagram":"https://www.instagram.com/$userName",
    "reddit":"https://www.reddit.com/r/$userName",
    "pypi":"https://pypi.org/user/$userName",
    "tiktok":"https://www.tiktok.com/@$userName?",
    "twitter":"https://twitter.com/$userName",
    };
  }

  void startLoop(){
    this.urls.forEach((hostName,url){
      this.getRequest(url).then((value) {
        if (value) {
          print("[+] ${this.userName} has an accout in $hostName");
        }
        else {
          print("[-] ${this.userName} does not have an accout in $hostName");
        }
      }
      ).catchError((e){
          print("error");
      });
    });
  }

  Future<bool> getRequest(url) async {
    var req = await http.get(url);
    if (req.statusCode == 200) {
      return true;
    }
    return false;
  }
}

void main() {
  var username = input('Enter username: ');
  SocialMedia Obj = new SocialMedia(username);
  Obj.startLoop();
}