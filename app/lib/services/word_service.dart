import 'api_client.dart';

class WordService {
  final ApiClient _client;
  WordService(this._client);

  Future<Map<String, dynamic>> getWords({String? category, int page = 1, int pageSize = 20}) async {
    final resp = await _client.dio.get('/words', queryParameters: {'category': category, 'page': page, 'page_size': pageSize});
    return resp.data;
  }

  Future<Map<String, dynamic>> getWord(String id) async {
    final resp = await _client.dio.get('/words/$id');
    return resp.data;
  }

  Future<Map<String, dynamic>> reviewWord(String wordId, bool isCorrect) async {
    final resp = await _client.dio.post('/words/$wordId/review', data: {'is_correct': isCorrect});
    return resp.data;
  }
}
