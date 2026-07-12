import 'package:flutter/material.dart';
import '../../../models/user.dart';
import '../../../config/theme.dart';

class StatsCard extends StatelessWidget {
  final UserProgress? progress;
  const StatsCard({super.key, this.progress});
  @override
  Widget build(BuildContext context) {
    return Container(padding: const EdgeInsets.all(16), decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(12), boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 8)]),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Text('📊 学习统计', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        Row(mainAxisAlignment: MainAxisAlignment.spaceAround, children: [
          _Stat(icon: '🔥', value: '${progress?.streakDays ?? 0}', label: '连续天数'),
          _Stat(icon: '⭐', value: '${progress?.totalXp ?? 0}', label: '总 XP'),
          _Stat(icon: '📖', value: '阶段${progress?.stage ?? 1}', label: '学习阶段'),
        ]),
      ]));
  }
}

class _Stat extends StatelessWidget {
  final String icon, value, label;
  const _Stat({required this.icon, required this.value, required this.label});
  @override
  Widget build(BuildContext context) => Column(children: [Text('$icon $value', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)), const SizedBox(height: 4), Text(label, style: const TextStyle(fontSize: 11, color: AppTheme.textSecondary))]);
}
