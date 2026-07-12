import 'api_client.dart';

class LetterService {
  final ApiClient _client;
  LetterService(this._client);

  Future<List<dynamic>> getLetters({String? type}) async {
    final resp = await _client.dio.get('/letters', queryParameters: {'type': type});
    return resp.data as List<dynamic>;
  }

  Future<Map<String, dynamic>> getLetter(String id) async {
    final resp = await _client.dio.get('/letters/$id');
    return resp.data as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> submitPractice(String letterId, double score, bool mastered) async {
    final resp = await _client.dio.post('/letters/$letterId/practice', data: {'score': score, 'mastered': mastered});
    return resp.data;
  }
}
