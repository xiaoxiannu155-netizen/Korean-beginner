import 'api_client.dart';

class AuthService {
  final ApiClient _client;

  AuthService(this._client);

  Future<Map<String, dynamic>> register(String email, String username, String password) async {
    final resp = await _client.dio.post('/auth/register', data: {
      'email': email,
      'username': username,
      'password': password,
    });
    await _client.saveTokens(resp.data['access_token'], resp.data['refresh_token']);
    return resp.data;
  }

  Future<Map<String, dynamic>> login(String email, String password) async {
    final resp = await _client.dio.post('/auth/login', data: {
      'email': email,
      'password': password,
    });
    await _client.saveTokens(resp.data['access_token'], resp.data['refresh_token']);
    return resp.data;
  }

  Future<void> logout() async {
    await _client.clearTokens();
  }

  Future<Map<String, dynamic>> getProfile() async {
    final resp = await _client.dio.get('/users/me');
    return resp.data;
  }

  Future<Map<String, dynamic>> getProgress() async {
    final resp = await _client.dio.get('/users/me/progress');
    return resp.data;
  }
}
