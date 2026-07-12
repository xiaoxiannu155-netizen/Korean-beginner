import 'package:flutter_test/flutter_test.dart';
import 'package:korean_app/models/daily_task.dart';

void main() {
  group('DailyTask', () {
    test('default values are all zero/false', () {
      final task = DailyTask();
      expect(task.wordsCompleted, 0);
      expect(task.grammarCompleted, false);
      expect(task.listeningCompleted, false);
      expect(task.speakingCompleted, false);
    });

    test('fromJson parses correctly', () {
      final json = {
        'words_completed': 3,
        'grammar_completed': true,
        'listening_completed': false,
        'speaking_completed': true,
      };
      final task = DailyTask.fromJson(json);
      expect(task.wordsCompleted, 3);
      expect(task.grammarCompleted, true);
      expect(task.speakingCompleted, true);
    });

    test('progress is 0.0 when nothing completed', () {
      expect(DailyTask().progress, 0.0);
    });

    test('progress is 1.0 when all completed', () {
      final task = DailyTask(
        wordsCompleted: 5,
        grammarCompleted: true,
        listeningCompleted: true,
        speakingCompleted: true,
      );
      expect(task.progress, 1.0);
    });

    test('progress is 0.5 when 2 of 4 done', () {
      final task = DailyTask(wordsCompleted: 5, grammarCompleted: true);
      expect(task.progress, 0.5);
    });

    test('items list has 4 entries', () {
      expect(DailyTask().items.length, 4);
    });

    test('words task not complete if less than 5', () {
      final task = DailyTask(wordsCompleted: 3);
      expect(task.items[0].completed, false);
    });

    test('words task complete at exactly 5', () {
      final task = DailyTask(wordsCompleted: 5);
      expect(task.items[0].completed, true);
    });
  });

  group('TaskItem', () {
    test('properties are correct', () {
      final item = TaskItem(label: 'Test', xp: 10, completed: false);
      expect(item.label, 'Test');
      expect(item.xp, 10);
      expect(item.completed, false);
      expect(item.progress, isNull);
    });
  });
}
