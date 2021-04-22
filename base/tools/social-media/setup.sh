if [ "$PREFIX" == '' ];then
    ROOT='sudo'
    PREFIX="/usr"
    
else
    ROOT=''
fi

if [ -f "$PREFIX/bin/dart" ];then
	dart pub get
	dart compile exe dart_main.dart
	$ROOT chmod +x dart_main.exe
fi