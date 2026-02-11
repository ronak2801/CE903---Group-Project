# Frontend Description
This repository contains the code for the frontend demo application.

# Requirements
- flutter: 3.7.1

# How to run
1. Ensure that you have flutter installed.
```bash
flutter --version
```
2. Run the project.
``` bash
flutter run
```

# How to create Reusable Widgets
1. Add a file to the `lib/widgets/`. (Ex. `my_resuable_widget.dart`)
2. Create a state less of stateful widget.
```dart
// state less widget
class MyReusableWidget extends StatelessWidget {
  const MyReusableWidget({ Key key }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Text("MyResuableWidget");
  }

}

// stateful widget
class MyResuableWidgetStateful extends StatefulWidget {
  const MyResuableWidgetStateful({ Key key }) : super(key: key);
  
  @override
  State<MyResuableWidgetStateful> createState() => _MyResuableWidgetStatefulState();
}

class _MyResuableWidgetStatefulState extends State<MyResuableWidgetStateful> {
  
  @override
  Widget build(BuildContext context) {
    return Text("MyReusableWidgetStateful");
  }

}
```
3. Use your resuable widget in a screen.
```dart
// e.g. login_screen_ui.dart
import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:flutter/src/widgets/placeholder.dart';

// import the reusable widget here
import '../../widgets/my_reusable_widget.dart';

class LoginScreenUI extends StatelessWidget {
  const LoginScreenUI({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: MyResuableWidget(), // use it as one of the children in the screen.
    );
  }
}
```
