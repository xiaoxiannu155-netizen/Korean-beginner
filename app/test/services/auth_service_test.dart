import 'package:flutter_test/flutter_test.dart';
import 'package:korean_app/models/user.dart';

void main() {
  group('User model', () {
    test('fromJson parses correctly', () {
      final json = {
        'id': 'test-id',
        'email': 'test@example.com',
        'username': 'tester',
        'avatar_url': null,
      };
      final user = User.fromJson(json);
      expect(user.id, 'test-id');
      expect(user.email, 'test@example.com');
      expect(user.username, 'tester');
    });
  });

  group('UserProgress model', () {
    test('fromJson parses with defaults', () {
      final json = <String, dynamic>{};
      final progress = UserProgress.fromJson(json);
      expect(progress.stage, 1);
      expect(progress.totalXp, 0);
      expect(progress.joyName, 'Joy');
    });

    test('levelName returns correct level', () {
      expect(UserProgress(totalXp: 0).levelName, '🥉 铜');
      expect(UserProgress(totalXp: 500).levelName, '🥈 银 II');
      expect(UserProgress(totalXp: 1500).levelName, '🥇 金 II');
      expect(UserProgress(totalXp: 3000).levelName, '💎 钻石');
    });
  });
}
