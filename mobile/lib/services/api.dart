import 'dart:convert';
import 'package:http/http.dart' as http;
class ApiService {
  static const baseUrl=String.fromEnvironment('API_URL',defaultValue:'http://10.0.2.2:8000/api');
  static Future<void> registerToken(String userId,String token) async {
    await http.post(Uri.parse('$baseUrl/devices'),
      headers:{'Content-Type':'application/json'},
      body:jsonEncode({'user_id':userId,'token':token,'platform':'android'}));
  }
}
