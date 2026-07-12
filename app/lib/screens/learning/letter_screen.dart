import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../models/letter.dart';
import '../../providers/letter_provider.dart';
import '../../providers/joy_provider.dart';
import '../../widgets/joy_sprite.dart';
import '../../widgets/joy_bottom_panel.dart';
import '../../config/theme.dart';

class LetterScreen extends ConsumerStatefulWidget {
  final String letterId;
  const LetterScreen({super.key, required this.letterId});

  @override
  ConsumerState<LetterScreen> createState() => _LetterScreenState();
}

class _LetterScreenState extends ConsumerState<LetterScreen> {
  @override
  Widget build(BuildContext context) {
    final letterAsync = ref.watch(letterDetailProvider(widget.letterId));
    final joyState = ref.watch(joyProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('字母学习')),
      body: letterAsync.when(
        data: (letter) => Stack(children: [
          SingleChildScrollView(padding: const EdgeInsets.all(24), child: Column(children: [
            Text(letter.char, style: const TextStyle(fontSize: 120, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text('[${letter.romanization ?? ""}]', style: const TextStyle(fontSize: 24, color: AppTheme.primary)),
            Text(letter.chineseHint ?? '', style: const TextStyle(fontSize: 16, color: AppTheme.textSecondary)),
            const SizedBox(height: 24),
            if (letter.pronunciationTip != null) ...[
              const Text('💡 发音技巧', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              Container(padding: const EdgeInsets.all(16), decoration: BoxDecoration(color: const Color(0xFFF8F7FF), borderRadius: BorderRadius.circular(12)), child: Text(letter.pronunciationTip!, style: const TextStyle(fontSize: 14, height: 1.6))),
            ],
          ])),
          Positioned(bottom: joyState == JoyState.active ? 200 : 16, right: 16, child: Column(mainAxisSize: MainAxisSize.min, children: [
            if (joyState == JoyState.sleeping) const SleepZzz(),
            const JoySprite(),
          ])),
          if (joyState == JoyState.active) Positioned(bottom: 0, left: 0, right: 0, child: JoyBottomPanel(currentContent: letter.char, contextType: JoyContext.letter)),
        ]),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(child: Text('加载失败: $e')),
      ),
    );
  }
}
