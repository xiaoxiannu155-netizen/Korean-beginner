import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/letter.dart';
import '../services/api_client.dart';
import '../services/letter_service.dart';

final letterListProvider = FutureProvider.family<List<Letter>, String?>((ref, type) async {
  final client = ref.watch(apiClientProvider);
  final service = LetterService(client);
  final data = await service.getLetters(type: type);
  return data.map((j) => Letter.fromJson(j)).toList();
});

final letterDetailProvider = FutureProvider.family<Letter, String>((ref, id) async {
  final client = ref.watch(apiClientProvider);
  final service = LetterService(client);
  final data = await service.getLetter(id);
  return Letter.fromJson(data);
});
