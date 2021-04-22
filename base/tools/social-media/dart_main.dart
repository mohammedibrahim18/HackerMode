import 'dart:io';
import 'dart:convert';
import 'package:sprintf/sprintf.dart' as sprintf;
import 'package:http/http.dart' as http;

class SocialMedia{
  var userName;

  SocialMedia(userName) {
    this.userName = userName;
  }

  void startLoop(){
    // to start search
    new File('data.json').readAsString().then((String contents) {
      var jsonData = json.decode(contents);
      jsonData.forEach((hostName,Info){
        var url = sprintf.sprintf(Info["url"],[this.userName]);
        this.getRequest(url).then((value) {
          if (value) {
            print("[\x1B[32m+\x1B[0m] \x1B[32m$hostName: \x1B[0m$url");
          }
        }).catchError((e){
        });
      });
    });
  }

  Future<bool> getRequest(url) async {
    // To make request
    var req = await http.get(url);
    if (req.statusCode == 200) {
      return true;
    }
    return false;
  }
}

String input(text){
  // simple input
  stdout.write(text);
  return stdin.readLineSync();
}

void main() {
  var username = input('\x1B[33mUsername\x1B[32m~\x1B[31m/\x1B[0m\$ ');
  SocialMedia Obj = new SocialMedia(username);
  Obj.startLoop();
}