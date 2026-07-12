import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../providers/joy_provider.dart';
import '../../widgets/joy_sprite.dart';
import '../../config/theme.dart';

class JoySettingsScreen extends ConsumerStatefulWidget {
  const JoySettingsScreen({super.key});
  @override
  ConsumerState<JoySettingsScreen> createState() => _JoySettingsScreenState();
}

class _JoySettingsScreenState extends ConsumerState<JoySettingsScreen> {
  late TextEditingController _nameCtrl;
  @override
  void initState() { super.initState(); _nameCtrl = TextEditingController(text: ref.read(joyProvider.notifier).config.name); }

  @override
  Widget build(BuildContext context) {
    final notifier = ref.read(joyProvider.notifier);
    final config = notifier.config;
    return Scaffold(
      appBar: AppBar(title: const Text('🧚 AI小精灵设置')),
      body: SingleChildScrollView(padding: const EdgeInsets.all(16), child: Column(children: [
        const JoySprite(size: 100), const SizedBox(height: 16),
        Text(config.name, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)), const SizedBox(height: 24),
        TextField(controller: _nameCtrl, decoration: const InputDecoration(labelText: '📝 名字', border: OutlineInputBorder()),
          onChanged: (v) => notifier.updateConfig(JoyConfig(name: v, gender: config.gender, personality: config.personality, displayMode: config.displayMode))),
        const SizedBox(height: 16),
        Row(children: [
          Expanded(child: _GenderBtn(label: '👧 女生', sel: config.gender == 'female', onTap: () => notifier.updateConfig(JoyConfig(name: config.name, gender: 'female', personality: config.personality, displayMode: config.displayMode)))),
          const SizedBox(width: 8),
          Expanded(child: _GenderBtn(label: '👦 男生', sel: config.gender == 'male', onTap: () => notifier.updateConfig(JoyConfig(name: config.name, gender: 'male', personality: config.personality, displayMode: config.displayMode)))),
          const SizedBox(width: 8),
          Expanded(child: _GenderBtn(label: '🧒 中性', sel: config.gender == 'neutral', onTap: () => notifier.updateConfig(JoyConfig(name: config.name, gender: 'neutral', personality: config.personality, displayMode: config.displayMode)))),
        ]),
        const SizedBox(height: 16),
        DropdownButtonFormField<JoyPersonality>(value: config.personality, decoration: const InputDecoration(labelText: '🎭 性格', border: OutlineInputBorder()),
          items: const [DropdownMenuItem(value: JoyPersonality.gentle, child: Text('🌸 温柔陪伴型')), DropdownMenuItem(value: JoyPersonality.lively, child: Text('⚡ 活泼鼓励型')), DropdownMenuItem(value: JoyPersonality.strict, child: Text('📐 严格老师型')), DropdownMenuItem(value: JoyPersonality.humorous, child: Text('😆 幽默朋友型'))],
          onChanged: (v) => notifier.updateConfig(JoyConfig(name: config.name, gender: config.gender, personality: v!, displayMode: config.displayMode))),
        const SizedBox(height: 16),
        DropdownButtonFormField<JoyDisplayMode>(value: config.displayMode, decoration: const InputDecoration(labelText: '👁️ 显示模式', border: OutlineInputBorder()),
          items: const [DropdownMenuItem(value: JoyDisplayMode.always, child: Text('🟢 始终显示')), DropdownMenuItem(value: JoyDisplayMode.autoHide, child: Text('🟡 学习时自动隐藏 (推荐)')), DropdownMenuItem(value: JoyDisplayMode.hidden, child: Text('⚫ 完全隐藏'))],
          onChanged: (v) => notifier.updateConfig(JoyConfig(name: config.name, gender: config.gender, personality: config.personality, displayMode: v!))),
      ])),
    );
  }
  @override
  void dispose() { _nameCtrl.dispose(); super.dispose(); }
}

class _GenderBtn extends StatelessWidget {
  final String label; final bool sel; final VoidCallback onTap;
  const _GenderBtn({required this.label, required this.sel, required this.onTap});
  @override
  Widget build(BuildContext context) {
    return GestureDetector(onTap: onTap, child: Container(
      padding: const EdgeInsets.symmetric(vertical: 12),
      decoration: BoxDecoration(color: sel ? const Color(0xFFF8F7FF) : Colors.white, borderRadius: BorderRadius.circular(10), border: Border.all(color: sel ? AppTheme.primary : const Color(0xFFDDDDDD), width: sel ? 2 : 1)),
      child: Text(label, textAlign: TextAlign.center, style: TextStyle(color: sel ? AppTheme.primary : AppTheme.textSecondary, fontWeight: FontWeight.w600)),
    ));
  }
}
