import 'package:flutter/material.dart';
import '../../../models/user.dart';
import '../../../config/theme.dart';

class GreetingHeader extends StatelessWidget {
  final User? user;
  final UserProgress? progress;

  const GreetingHeader({super.key, this.user, this.progress});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.fromLTRB(20, 48, 20, 24),
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [Color(0xFF6C5CE7), Color(0xFFA29BFE)],
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('🇰🇷 안녕하세요!',
                    style: TextStyle(color: Colors.white70, fontSize: 12)),
                  const SizedBox(height: 4),
                  Text('${user?.username ?? "同学"}, 继续加油! 🔥',
                    style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
                ],
              ),
              CircleAvatar(
                radius: 22,
                backgroundColor: Colors.white24,
                child: Text(
                  user?.username?.isNotEmpty == true ? user!.username![0].toUpperCase() : '👤',
                  style: const TextStyle(color: Colors.white),
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _StatBadge(icon: '🔥', value: '${progress?.streakDays ?? 0}', label: '连续天数'),
              _StatBadge(icon: '⭐', value: '${progress?.totalXp ?? 0}', label: '经验值'),
              _StatBadge(icon: '🏆', value: progress?.levelName ?? '🥉 铜', label: '等级'),
            ],
          ),
        ],
      ),
    );
  }
}

class _StatBadge extends StatelessWidget {
  final String icon, value, label;
  const _StatBadge({required this.icon, required this.value, required this.label});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('$icon $value',
          style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
        const SizedBox(height: 2),
        Text(label, style: const TextStyle(color: Colors.white60, fontSize: 10)),
      ],
    );
  }
}
