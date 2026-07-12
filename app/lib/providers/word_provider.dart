import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/word.dart';
import '../services/api_client.dart';
import '../services/word_service.dart';

final wordListProvider = FutureProvider.family<WordListResult, String?>((ref, category) async {
  final client = ref.watch(apiClientProvider);
  final service = WordService(client);
  final data = await service.getWords(category: category);
  final items = (data['items'] as List).map((j) => Word.fromJson(j)).toList();
  return WordListResult(items: items, total: data['total'] as int);
});

class WordListResult {
  final List<Word> items;
  final int total;
  const WordListResult({required this.items, required this.total});
}

final wordDetailProvider = FutureProvider.family<Word, String>((ref, id) async {
  final client = ref.watch(apiClientProvider);
  final service = WordService(client);
  final data = await service.getWord(id);
  return Word.fromJson(data);
});
