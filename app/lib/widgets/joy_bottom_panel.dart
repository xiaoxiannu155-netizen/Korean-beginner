import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/joy_provider.dart';
import '../config/theme.dart';

enum JoyContext { word, letter, grammar, batchim, unknown }

class JoyBottomPanel extends ConsumerWidget {
  final String currentContent;
  final String? currentSentence;
  final JoyContext contextType;
  final void Function()? onPlay, onSlowPlay, onSyllableBreakdown, onExample, onExplain, onSpeechEvaluate;

  const JoyBottomPanel({super.key, required this.currentContent, this.currentSentence, this.contextType = JoyContext.unknown, this.onPlay, this.onSlowPlay, this.onSyllableBreakdown, this.onExample, this.onExplain, this.onSpeechEvaluate});

  String get _contextLabel {
    switch (contextType) {
      case JoyContext.word: return '单词';
      case JoyContext.letter: return '字母';
      case JoyContext.grammar: return '语法';
      case JoyContext.batchim: return '收音';
      case JoyContext.unknown: return '内容';
    }
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: const BoxDecoration(color: Colors.white, borderRadius: BorderRadius.vertical(top: Radius.circular(16)), boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 10, offset: Offset(0, -2))]),
      child: Column(mainAxisSize: MainAxisSize.min, children: [
        Row(children: [
          const JoySprite(size: 36), const SizedBox(width: 8),
          Expanded(child: RichText(text: TextSpan(style: const TextStyle(color: AppTheme.textPrimary, fontSize: 13), children: [
            const TextSpan(text: 'Joy 已识别当前', style: TextStyle(fontWeight: FontWeight.normal)),
            TextSpan(text: _contextLabel, style: const TextStyle(color: AppTheme.primary, fontWeight: FontWeight.bold)),
            const TextSpan(text: ': '),
            TextSpan(text: currentContent, style: const TextStyle(color: AppTheme.primary, fontWeight: FontWeight.bold)),
          ]))),
          IconButton(icon: const Icon(Icons.close, size: 18), onPressed: () => ref.read(joyProvider.notifier).deactivate()),
        ]),
        const SizedBox(height: 12),
        Wrap(spacing: 8, runSpacing: 8, children: [
          _ActionChip(label: '🔊 朗读', isPrimary: true, onTap: onPlay),
          _ActionChip(label: '🐢 慢速', onTap: onSlowPlay),
          _ActionChip(label: '✂️ 音节拆分', onTap: onSyllableBreakdown),
        ]),
        const SizedBox(height: 8),
        Wrap(spacing: 8, runSpacing: 8, children: [
          _ActionChip(label: '📖 例句朗读', onTap: onExample),
          _ActionChip(label: '📝 AI解释', onTap: onExplain),
          _ActionChip(label: '🎤 跟读评分', onTap: onSpeechEvaluate),
        ]),
      ]),
    );
  }
}

class _ActionChip extends StatelessWidget {
  final String label; final bool isPrimary; final VoidCallback? onTap;
  const _ActionChip({required this.label, this.isPrimary = false, this.onTap});
  @override
  Widget build(BuildContext context) {
    return GestureDetector(onTap: onTap, child: Container(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
      decoration: BoxDecoration(color: isPrimary ? AppTheme.primary : Colors.white, borderRadius: BorderRadius.circular(8), border: isPrimary ? null : Border.all(color: const Color(0xFFDDDDDD))),
      child: Text(label, style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: isPrimary ? Colors.white : AppTheme.textPrimary)),
    ));
  }
}
