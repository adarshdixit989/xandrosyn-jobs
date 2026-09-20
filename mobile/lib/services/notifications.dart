import 'package:firebase_messaging/firebase_messaging.dart';
import 'api.dart';

@pragma('vm:entry-point')
Future<void> backgroundHandler(RemoteMessage message) async {}

class NotificationService {
  static Future<void> init(String userId) async {
    FirebaseMessaging.onBackgroundMessage(backgroundHandler);
    final m=FirebaseMessaging.instance;
    await m.requestPermission(alert:true,badge:true,sound:true);
    final token=await m.getToken();
    if(token!=null) await ApiService.registerToken(userId,token);
    m.onTokenRefresh.listen((t)=>ApiService.registerToken(userId,t));
    FirebaseMessaging.onMessage.listen((message){});
  }
}
