import 'dart:io';


String kivyPath = File(Platform.script.toFilePath()).parent.parent.path + "/tools/kivy";
String currentPath = Directory.current.path;

class KivyApp{
  String appName = "MyApp";

  void build(){
    this.createAppFolders();
    this.createMainFile();
  }

  void createMainFile(){
     this.getDateFromFile("main_debug").then((data) {
       data = data.replaceAll("\$appName",appName);
       File("main.py").writeAsString(data);
    });
  }

  void createAppFolders(){
    List<String> appFolders = [
      'app',
      'app/assets',
      'app/backend',
      'app/backend/manager_screens',
      'app/backend/manager_screens/main_screen',
      'app/GUI',
    ];
    appFolders.forEach((folder) {
      Directory myDir = Directory(folder);
      myDir.exists().then( (isExists) {
        if (!isExists) {
          myDir.create();
        }
      });
    });
  }

  Future getDateFromFile(String filePath) async {
    File file = File("$kivyPath/kivy_files/$filePath");
    return await file.readAsString();
  }

}


void main(List<String> args) {
  KivyApp kivyApp = new KivyApp();

  if (args.length > 0) {
    args.skip(0).forEach((arg) {
      if (arg.startsWith("build[") && arg.endsWith("]")) {
        kivyApp.appName = arg.substring(6, arg.length - 1);
        kivyApp.build();
        print(kivyApp.appName);
      }

      if (arg == "build") {
          kivyApp.build();
      }

      if (arg.startsWith("screen[") && arg.endsWith("]")) {
        String screenName = arg.substring(7, arg.length - 1);
        print(screenName);
      }
    });
  }
}