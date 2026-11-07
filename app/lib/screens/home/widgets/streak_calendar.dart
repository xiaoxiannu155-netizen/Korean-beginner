import 'package:flutter/material.dart';
import '../../../config/theme.dart';

class StreakCalendar extends StatelessWidget {
  final List<Map<String, dynamic>> weekData;
  const StreakCalendar({super.key, required this.weekData});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(12)),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Text('📅 本周学习记录', style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        Row(mainAxisAlignment: MainAxisAlignment.spaceEvenly, children: weekData.map((day) {
          final studied = day['studied'] == true;
          final dateStr = (day['date'] as String?) ?? '';
          final dayLabel = dateStr.length >= 10 ? dateStr.substring(8, 10) : '--';
          return Column(children: [
            Text(dayLabel, style: const TextStyle(fontSize: 12, color: AppTheme.textSecondary)),
            const SizedBox(height: 6),
            Container(
              width: 36, height: 36,
              decoration: BoxDecoration(
                color: studied ? AppTheme.success : const Color(0xFFF0F0F0),
                shape: BoxShape.circle,
              ),
              child: Center(child: studied ? const Text('🔥', style: TextStyle(fontSize: 16)) : const Text('·', style: TextStyle(color: AppTheme.textSecondary))),
            ),
          ]);
        }).toList()),
      ]),
    );
  }
}
