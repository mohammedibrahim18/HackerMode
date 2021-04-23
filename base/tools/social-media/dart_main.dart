import 'dart:io';
import 'dart:convert';
import 'package:http/http.dart' as http;

class SocialMedia{
  String userName;
  List urls200 = [];
  int _counter = 0;
  Map<String,dynamic> contentsAsMap = {};

  SocialMedia(this.userName);

  void startLoop() async {
    String contents = await File('data.json').readAsString();
    this.contentsAsMap = json.decode(contents);
    contentsAsMap.forEach((hostName,info){
      String url = info["url"].replaceAll("%s",this.userName);

      this.getRequest(Uri.parse(url)).then((value) {
        _counter++;
        stdout.write("\r# Loading [$_counter/${contentsAsMap.keys.length}]");
        if (value) {
          this.urls200.add(hostName);
        }
        if (_counter == contentsAsMap.keys.length){
          this.showData();
        }

      });
    });
  }

  Future<bool> getRequest(url) async {
    try{
      var req = await http.get(url).timeout(Duration(seconds: 3));
      if (req.statusCode == 200) {
        return true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }

  void showData(){
    //print("[\x1B[32m+\x1B[0m] \x1B[32m$hostName: \x1B[0m$url");
    this.urls200.sort();
    this.urls200.forEach((hostName){
    print("[\x1B[32m+\x1B[0m] \x1B[32m$hostName: \x1B[0m${contentsAsMap[hostName]["url"].replaceAll('%s',this.userName)}");
    });
    exit(-1);
  }
}

String input(text){
  // simple input
  stdout.write(text);
  return stdin.readLineSync();
}

void main() async {
  var username = input('\x1B[33mUsername\x1B[32m~\x1B[31m/\x1B[0m\$ ');
  SocialMedia Obj = new SocialMedia(username);
  Obj.startLoop();
}