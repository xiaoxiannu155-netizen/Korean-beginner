import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/daily_task.dart';
import '../services/api_client.dart';

final dailyTaskProvider = FutureProvider<DailyTask>((ref) async {
  final client = ref.watch(apiClientProvider);
  try {
    final resp = await client.dio.get('/daily-tasks/today');
    return DailyTask.fromJson(resp.data);
  } catch (_) {
    return const DailyTask();
  }
});
