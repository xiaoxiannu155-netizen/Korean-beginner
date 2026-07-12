import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../services/api_client.dart';
import '../../config/theme.dart';

class SpellingGameScreen extends ConsumerStatefulWidget {
  const SpellingGameScreen({super.key});
  @override
  ConsumerState<SpellingGameScreen> createState() => _SpellingGameScreenState();
}

class _SpellingGameScreenState extends ConsumerState<SpellingGameScreen> {
  int _level = 1;
  String _question = '';
  String _decomposition = '';
  List<String> _options = [];
  int _score = 0;
  int _streak = 0;
  bool _isLoading = true;
  String? _feedback;
  bool? _lastCorrect;

  @override
  void initState() {
    super.initState();
    _loadQuestion();
  }

  Future<void> _loadQuestion() async {
    setState(() => _isLoading = true);
    try {
      final client = ref.read(apiClientProvider);
      final resp = await client.dio.get('/spelling/question', queryParameters: {'level': _level});
      setState(() {
        _question = resp.data['answer'];
        _decomposition = resp.data['decomposition'];
        _options = List<String>.from(resp.data['options']);
        _feedback = null;
        _isLoading = false;
      });
    } catch (_) {
      setState(() => _isLoading = false);
    }
  }

  void _selectOption(String option) async {
    final client = ref.read(apiClientProvider);
    final resp = await client.dio.post('/spelling/check', queryParameters: {
      'user_input': option, 'correct_answer': _question,
    });
    final correct = resp.data['is_correct'] as bool;
    setState(() {
      _lastCorrect = correct;
      _feedback = correct ? '✅ 正确! +${resp.data['xp_earned']}XP' : '❌ 再试一次!';
      if (correct) {
        _score += resp.data['xp_earned'];
        _streak++;
        if (_streak >= 5) { _streak = 0; _level = (_level % 4) + 1; }
        Future.delayed(const Duration(milliseconds: 800), _loadQuestion);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('🔤 拼读闯关 Lv.$_level')),
      body: _isLoading
        ? const Center(child: CircularProgressIndicator())
        : Padding(
            padding: const EdgeInsets.all(24),
            child: Column(children: [
              // Score bar
              Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
                Text('⭐ $_score', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: AppTheme.accent)),
                Text('🔥 连对 $_streak', style: const TextStyle(color: AppTheme.primary)),
              ]),
              const SizedBox(height: 40),
              // Decomposition display
              Container(
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(color: const Color(0xFFF8F7FF), borderRadius: BorderRadius.circular(16)),
                child: Column(children: [
                  const Text('音节拆分', style: TextStyle(fontSize: 12, color: AppTheme.textSecondary)),
                  const SizedBox(height: 8),
                  Text(_decomposition, style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: AppTheme.primary)),
                ]),
              ),
              const SizedBox(height: 24),
              const Text('选择正确的拼写:', style: TextStyle(fontSize: 14)),
              const SizedBox(height: 16),
              // Options grid
              Wrap(spacing: 12, runSpacing: 12, alignment: WrapAlignment.center, children: _options.map((opt) => GestureDetector(
                onTap: () => _selectOption(opt),
                child: Container(
                  width: 100, padding: const EdgeInsets.symmetric(vertical: 16),
                  decoration: BoxDecoration(
                    color: _lastCorrect == null ? Colors.white : (_question == opt ? AppTheme.success.withOpacity(0.1) : Colors.white),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: const Color(0xFFDDDDDD)),
                  ),
                  child: Text(opt, textAlign: TextAlign.center,
                    style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold)),
                ),
              )).toList()),
              const SizedBox(height: 24),
              if (_feedback != null)
                Text(_feedback!, style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: _lastCorrect == true ? AppTheme.success : AppTheme.error)),
            ]),
          ),
    );
  }
}
