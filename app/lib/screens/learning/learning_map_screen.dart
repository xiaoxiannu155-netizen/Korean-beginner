import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../config/theme.dart';

class LearningMapScreen extends StatelessWidget {
  const LearningMapScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('🗺️ 学习地图')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(children: [
          _StageCard(stage: 1, title: '阶段1: 字母', subtitle: '元音 → 辅音 → 双辅音 → 复合元音 · 约2-3周', progress: 0.0, status: _NodeStatus.active),
          _StageCard(stage: 2, title: '阶段2: 拼读', subtitle: '音节结构 → 收音 → 连读 → 音变规则 · 约3-4周', progress: 0.0, status: _NodeStatus.locked),
          _StageCard(stage: 3, title: '阶段3: 词汇语法', subtitle: '分类单词 → 基础语法 → 生活对话 · 约4-6周', progress: 0.0, status: _NodeStatus.locked),
          _StageCard(stage: 4, title: '阶段4: 实战', subtitle: '听力训练 → AI陪练 → 真实交流', progress: 0.0, status: _NodeStatus.locked),
        ]),
      ),
    );
  }
}

enum _NodeStatus { active, completed, locked }

class _StageCard extends StatelessWidget {
  final int stage;
  final String title, subtitle;
  final double progress;
  final _NodeStatus status;

  const _StageCard({required this.stage, required this.title, required this.subtitle, required this.progress, required this.status});

  @override
  Widget build(BuildContext context) {
    final isLocked = status == _NodeStatus.locked;
    final isCompleted = status == _NodeStatus.completed;

    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isLocked ? const Color(0xFFF5F5F5) : Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: isLocked ? const Color(0xFFEEEEEE) : (isCompleted ? AppTheme.success : AppTheme.primary)),
      ),
      child: Row(children: [
        Container(
          width: 48, height: 48,
          decoration: BoxDecoration(
            color: isLocked ? const Color(0xFFDFE6E9) : (isCompleted ? AppTheme.success : AppTheme.accent),
            shape: BoxShape.circle,
          ),
          child: Center(child: isLocked ? const Icon(Icons.lock, color: Colors.white) : (isCompleted ? const Icon(Icons.check, color: Colors.white) : Text('$stage', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 20)))),
        ),
        const SizedBox(width: 16),
        Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(title, style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: isLocked ? const Color(0xFFBBBBBB) : AppTheme.textPrimary)),
          const SizedBox(height: 4),
          Text(subtitle, style: TextStyle(fontSize: 12, color: isLocked ? const Color(0xFFDDDDDD) : AppTheme.textSecondary)),
          if (!isLocked) ...[
            const SizedBox(height: 8),
            ClipRRect(
              borderRadius: BorderRadius.circular(4),
              child: LinearProgressIndicator(value: progress, backgroundColor: const Color(0xFFF0EDFF), color: AppTheme.primary, minHeight: 4),
            ),
          ],
        ])),
      ]),
    );
  }
}
