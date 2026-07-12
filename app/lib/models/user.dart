class User {
  final String id;
  final String email;
  final String? username;
  final String? avatarUrl;

  User({required this.id, required this.email, this.username, this.avatarUrl});

  factory User.fromJson(Map<String, dynamic> json) => User(
    id: json['id'] as String,
    email: json['email'] as String,
    username: json['username'] as String?,
    avatarUrl: json['avatar_url'] as String?,
  );
}

class UserProgress {
  final int stage;
  final int totalXp;
  final int level;
  final int streakDays;
  final String joyName;
  final String joyGender;
  final String joyPersonality;
  final String joyDisplayMode;

  const UserProgress({
    this.stage = 1,
    this.totalXp = 0,
    this.level = 1,
    this.streakDays = 0,
    this.joyName = 'Joy',
    this.joyGender = 'female',
    this.joyPersonality = 'gentle',
    this.joyDisplayMode = 'auto_hide',
  });

  factory UserProgress.fromJson(Map<String, dynamic> json) => UserProgress(
    stage: json['stage'] as int? ?? 1,
    totalXp: json['total_xp'] as int? ?? 0,
    level: json['level'] as int? ?? 1,
    streakDays: json['streak_days'] as int? ?? 0,
    joyName: json['joy_name'] as String? ?? 'Joy',
    joyGender: json['joy_gender'] as String? ?? 'female',
    joyPersonality: json['joy_personality'] as String? ?? 'gentle',
    joyDisplayMode: json['joy_display_mode'] as String? ?? 'auto_hide',
  );

  String get levelName {
    if (totalXp >= 2500) return '💎 钻石';
    if (totalXp >= 1500) return '🥇 金 II';
    if (totalXp >= 1000) return '🥇 金';
    if (totalXp >= 600) return '🥈 银 II';
    if (totalXp >= 300) return '🥈 银';
    if (totalXp >= 100) return '🥉 铜 II';
    return '🥉 铜';
  }
}
