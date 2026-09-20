import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'services/notifications.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  await NotificationService.init('demo-user');
  runApp(const MaterialApp(home: Scaffold(body: Center(child: Text('Xandrosyn Jobs')))));
}
