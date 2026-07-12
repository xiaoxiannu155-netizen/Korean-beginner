import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../services/api_client.dart';
import '../../config/theme.dart';
import '../../widgets/pronunciation_player.dart';

class SpeechEvalScreen extends ConsumerStatefulWidget {
  final String? initialText;
  const SpeechEvalScreen({super.key, this.initialText});

  @override
  ConsumerState<SpeechEvalScreen> createState() => _SpeechEvalScreenState();
}

class _SpeechEvalScreenState extends ConsumerState<SpeechEvalScreen> {
  final _textCtrl = TextEditingController();
  Map<String, dynamic>? _result;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    if (widget.initialText != null) _textCtrl.text = widget.initialText!;
  }

  Future<void> _evaluate() async {
    final text = _textCtrl.text.trim();
    if (text.isEmpty) return;
    setState(() => _isLoading = true);
    try {
      final client = ref.read(apiClientProvider);
      final resp = await client.dio.post('/speech/evaluate', data: {'text': text});
      setState(() => _result = resp.data);
    } catch (_) {
      setState(() => _result = {'error': '评估失败'});
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('🎤 跟读评分')),
      body: SingleChildScrollView(padding: const EdgeInsets.all(16), child: Column(children: [
        TextField(controller: _textCtrl, decoration: const InputDecoration(labelText: '输入要练习的韩文', border: OutlineInputBorder(), hintText: '例如: 사랑해요')),
        const SizedBox(height: 12),
        SizedBox(width: double.infinity, child: ElevatedButton(onPressed: _isLoading ? null : _evaluate, child: Text(_isLoading ? '评估中...' : '开始评估', style: const TextStyle(fontSize: 16)))),
        if (_result != null) ...[
          const SizedBox(height: 24),
          // Score ring
          if (_result!['overall_score'] != null)
            _ScoreRing(score: (_result!['overall_score'] as num).toDouble()),
          const SizedBox(height: 16),
          // Syllable scores
          if (_result!['syllable_scores'] != null)
            Wrap(spacing: 8, alignment: WrapAlignment.center, children: (_result!['syllable_scores'] as List).map<Widget>((s) {
              final score = (s['score'] as num).toDouble();
              final status = s['status'] ?? 'ok';
              final color = score >= 0.8 ? AppTheme.success : (score >= 0.6 ? AppTheme.accent : AppTheme.error);
              return Container(padding: const EdgeInsets.all(8), decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(8), border: Border.all(color: color.withOpacity(0.3))),
                child: Column(children: [Text(s['syllable'] ?? '', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: color)), Text('${(score * 100).toInt()}%', style: TextStyle(fontSize: 11, color: color))]));
            }).toList()),
          // Feedback
          if (_result!['feedback'] != null) ...[
            const SizedBox(height: 16),
            ...(_result!['feedback'] as List).map((f) => Padding(padding: const EdgeInsets.only(bottom: 4), child: Text(f.toString(), style: const TextStyle(fontSize: 13)))),
          ],
          // XP
          if (_result!['xp_earned'] != null)
            Container(margin: const EdgeInsets.only(top: 12), padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8), decoration: BoxDecoration(color: AppTheme.accent.withOpacity(0.1), borderRadius: BorderRadius.circular(20)),
              child: Text('+${_result!['xp_earned']} XP', style: const TextStyle(color: AppTheme.accent, fontWeight: FontWeight.bold, fontSize: 16))),
          // Pronunciation player
          if (_textCtrl.text.trim().isNotEmpty) ...[
            const SizedBox(height: 16),
            PronunciationPlayer(text: _textCtrl.text.trim()),
          ],
        ],
      ])),
    );
  }

  @override
  void dispose() { _textCtrl.dispose(); super.dispose(); }
}

class _ScoreRing extends StatelessWidget {
  final double score;
  const _ScoreRing({required this.score});

  Color get _color => score >= 0.9 ? AppTheme.success : (score >= 0.7 ? AppTheme.accent : (score >= 0.5 ? Colors.orange : AppTheme.error));

  @override
  Widget build(BuildContext context) {
    final pct = (score * 100).toInt();
    return Column(children: [
      SizedBox(width: 100, height: 100, child: Stack(fit: StackFit.expand, children: [
        CircularProgressIndicator(value: score, strokeWidth: 8, backgroundColor: Colors.grey.shade200, color: _color),
        Center(child: Text('$pct', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: _color))),
      ])),
      const SizedBox(height: 4),
      Text(pct >= 90 ? '🏆 完美!' : (pct >= 70 ? '👍 很好!' : (pct >= 50 ? '📖 继续加油' : '💪 多练习')), style: TextStyle(fontSize: 16, color: _color, fontWeight: FontWeight.bold)),
    ]);
  }
}
