import 'package:flutter/material.dart';
import '../../../config/theme.dart';

class LearningPathBar extends StatelessWidget {
  final int currentStage;

  const LearningPathBar({super.key, this.currentStage = 2});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('🗺️ 学习路径',
          style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: AppTheme.textPrimary)),
        const SizedBox(height: 10),
        SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          child: Row(
            children: [
              _PathNode(icon: '🏆', label: '字母完成', active: true, locked: false),
              const Padding(
                padding: EdgeInsets.symmetric(horizontal: 4),
                child: Icon(Icons.arrow_forward_ios, size: 14, color: AppTheme.textSecondary),
              ),
              _PathNode(icon: '🔤', label: '拼读进行中', active: currentStage == 2, locked: false),
              const Padding(
                padding: EdgeInsets.symmetric(horizontal: 4),
                child: Icon(Icons.arrow_forward_ios, size: 14, color: AppTheme.textSecondary),
              ),
              _PathNode(icon: '🔒', label: '词汇', active: false, locked: true),
              const Padding(
                padding: EdgeInsets.symmetric(horizontal: 4),
                child: Icon(Icons.arrow_forward_ios, size: 14, color: AppTheme.textSecondary),
              ),
              _PathNode(icon: '🔒', label: '实战', active: false, locked: true),
            ],
          ),
        ),
      ],
    );
  }
}

class _PathNode extends StatelessWidget {
  final String icon, label;
  final bool active;
  final bool locked;

  const _PathNode({required this.icon, required this.label, this.active = false, this.locked = false});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          width: 48, height: 48,
          decoration: BoxDecoration(
            color: locked ? const Color(0xFFDFE6E9) : (active ? AppTheme.primary : AppTheme.success),
            shape: BoxShape.circle,
          ),
          child: Center(child: Text(icon, style: const TextStyle(fontSize: 20))),
        ),
        const SizedBox(height: 4),
        Text(label, style: TextStyle(
          fontSize: 10,
          color: locked ? AppTheme.textSecondary : (active ? AppTheme.primary : AppTheme.textPrimary),
        )),
      ],
    );
  }
}
