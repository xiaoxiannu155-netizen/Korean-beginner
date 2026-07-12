import 'package:sqflite/sqflite.dart' as sql;
import 'package:shared_preferences/shared_preferences.dart';
import 'api_client.dart';

class SyncService {
  final ApiClient _client;
  SyncService(this._client);

  Future<void> syncProgress() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final lastSync = prefs.getString('last_sync_time');
      final resp = await _client.dio.get('/sync/checkpoint');
      prefs.setString('last_sync_time', DateTime.now().toIso8601String());
    } catch (_) {}
  }

  Future<void> syncContentUpdates() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final since = prefs.getString('last_content_update') ?? DateTime(2026, 1, 1).toIso8601String();
      await _client.dio.get('/sync/content-updates', queryParameters: {'since': since});
      prefs.setString('last_content_update', DateTime.now().toIso8601String());
    } catch (_) {}
  }
}
