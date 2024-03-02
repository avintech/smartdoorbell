import 'package:firebase_database/firebase_database.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
/// A placeholder class that represents an entity or model.
class Item {
  const Item(this.name,this.url);
  final String name;
  final String url;
}

class rtdatabase {
  Future<Object?> get() async {
    try {
      final storage = FlutterSecureStorage();
      final uuid = await storage.read(key: 'uuid');
      final data = await FirebaseDatabase.instance
          .ref()
          .child(uuid!)
          .child('unknownfaces').orderByKey()
          .get();
      return data;
    } catch (e) {
      return e.toString();
    }
  }

  Future<String> uploadKey(String token) async {
    try{
      final storage = FlutterSecureStorage();
      final uuid = await storage.read(key: 'uuid');
      await FirebaseDatabase.instance
          .ref()
          .child(uuid!)
          .child('token')
          .set(token);
      return 'Success';
    } catch (e) {
      return e.toString();
    }
  }
}