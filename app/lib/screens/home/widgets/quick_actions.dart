import 'package:flutter/material.dart';
import '../../../config/theme.dart';

class QuickActions extends StatelessWidget {
  const QuickActions({super.key});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              gradient: const LinearGradient(colors: [Color(0xFFFD79A8), Color(0xFFE84393)]),
              borderRadius: BorderRadius.circular(10),
            ),
            child: const Column(
              children: [
                Text('🔍', style: TextStyle(fontSize: 24)),
                SizedBox(height: 4),
                Text('查单词/翻译', style: TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w600)),
              ],
            ),
          ),
        ),
        const SizedBox(width: 10),
        Expanded(
          child: Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              gradient: const LinearGradient(colors: [Color(0xFF00CEC9), Color(0xFF00B894)]),
              borderRadius: BorderRadius.circular(10),
            ),
            child: const Column(
              children: [
                Text('🤖', style: TextStyle(fontSize: 24)),
                SizedBox(height: 4),
                Text('AI 口语陪练', style: TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w600)),
              ],
            ),
          ),
        ),
      ],
    );
  }
}
