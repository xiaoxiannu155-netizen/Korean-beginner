import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../services/api_client.dart';
import '../../config/theme.dart';

class TranslateScreen extends ConsumerStatefulWidget {
  const TranslateScreen({super.key});
  @override
  ConsumerState<TranslateScreen> createState() => _TranslateScreenState();
}

class _TranslateScreenState extends ConsumerState<TranslateScreen> {
  final _inputCtrl = TextEditingController();
  String? _result, _pronunciation;
  bool _isLoading = false, _zhToKo = true;

  Future<void> _translate() async {
    final text = _inputCtrl.text.trim();
    if (text.isEmpty) return;
    setState(() => _isLoading = true);
    try {
      final client = ref.read(apiClientProvider);
      final resp = await client.dio.post('/ai/translate', data: {'text': text, 'direction': _zhToKo ? 'zh-ko' : 'ko-zh'});
      setState(() { _result = resp.data['result']; _pronunciation = resp.data['pronunciation']; });
    } catch (_) {
      setState(() => _result = '翻译失败');
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('🤖 AI 翻译')),
      body: SingleChildScrollView(padding: const EdgeInsets.all(16), child: Column(children: [
        Row(children: [
          _LangBtn(label: '中→韩', selected: _zhToKo, onTap: () => setState(() => _zhToKo = true)),
          const SizedBox(width: 8),
          _LangBtn(label: '韩→中', selected: !_zhToKo, onTap: () => setState(() => _zhToKo = false)),
        ]),
        const SizedBox(height: 12),
        TextField(controller: _inputCtrl, maxLines: 4, decoration: InputDecoration(hintText: _zhToKo ? '输入中文...' : '한국어를 입력하세요...', border: const OutlineInputBorder())),
        const SizedBox(height: 12),
        SizedBox(width: double.infinity, child: ElevatedButton(onPressed: _isLoading ? null : _translate, child: Text(_isLoading ? '翻译中...' : '翻译', style: const TextStyle(fontSize: 16)))),
        if (_result != null) ...[
          const SizedBox(height: 16),
          Container(width: double.infinity, padding: const EdgeInsets.all(16), decoration: BoxDecoration(color: const Color(0xFFF8F7FF), borderRadius: BorderRadius.circular(12)),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(_result!, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
              if (_pronunciation != null) ...[const SizedBox(height: 4), Text('[$_pronunciation]', style: const TextStyle(fontSize: 14, color: AppTheme.primary))],
            ])),
        ],
      ])),
    );
  }

  @override
  void dispose() { _inputCtrl.dispose(); super.dispose(); }
}

class _LangBtn extends StatelessWidget {
  final String label; final bool selected; final VoidCallback onTap;
  const _LangBtn({required this.label, required this.selected, required this.onTap});
  @override
  Widget build(BuildContext context) {
    return GestureDetector(onTap: onTap, child: Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(color: selected ? AppTheme.primary : Colors.white, borderRadius: BorderRadius.circular(20), border: Border.all(color: selected ? AppTheme.primary : const Color(0xFFDDDDDD))),
      child: Text(label, style: TextStyle(color: selected ? Colors.white : AppTheme.textPrimary, fontWeight: FontWeight.w600)),
    ));
  }
}
