import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../services/api_client.dart';
import '../../config/theme.dart';

class SoundChangeDemoScreen extends ConsumerStatefulWidget {
  const SoundChangeDemoScreen({super.key});
  @override
  ConsumerState<SoundChangeDemoScreen> createState() => _SoundChangeDemoScreenState();
}

class _SoundChangeDemoScreenState extends ConsumerState<SoundChangeDemoScreen> {
  List<Map<String, dynamic>> _rules = [];
  int _currentIndex = 0;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadRules();
  }

  Future<void> _loadRules() async {
    try {
      final client = ref.read(apiClientProvider);
      final resp = await client.dio.get('/batchim', queryParameters: {'rule_type': 'liaison'});
      // Also fetch other types
      var rules = List<Map<String, dynamic>>.from(resp.data);
      final nasalResp = await client.dio.get('/batchim', queryParameters: {'rule_type': 'nasalization'});
      rules.addAll(List<Map<String, dynamic>>.from(nasalResp.data));
      final tensResp = await client.dio.get('/batchim', queryParameters: {'rule_type': 'tensification'});
      rules.addAll(List<Map<String, dynamic>>.from(tensResp.data));
      final aspResp = await client.dio.get('/batchim', queryParameters: {'rule_type': 'aspiration'});
      rules.addAll(List<Map<String, dynamic>>.from(aspResp.data));
      final latResp = await client.dio.get('/batchim', queryParameters: {'rule_type': 'lateralization'});
      rules.addAll(List<Map<String, dynamic>>.from(latResp.data));
      setState(() { _rules = rules; _isLoading = false; });
    } catch (_) {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) return Scaffold(appBar: AppBar(title: const Text('🔄 音变规则')), body: const Center(child: CircularProgressIndicator()));
    if (_rules.isEmpty) return Scaffold(appBar: AppBar(title: const Text('🔄 音变规则')), body: const Center(child: Text('暂无数据')));

    final rule = _rules[_currentIndex];

    return Scaffold(
      appBar: AppBar(title: Text('🔄 ${rule['title'] ?? "音变规则"}')),
      body: SingleChildScrollView(padding: const EdgeInsets.all(24), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(color: const Color(0xFFF8F7FF), borderRadius: BorderRadius.circular(12)),
          child: Text(rule['description'] ?? '', style: const TextStyle(fontSize: 14, height: 1.6)),
        ),
        const SizedBox(height: 24),
        Text('${_currentIndex + 1} / ${_rules.length}', style: const TextStyle(color: AppTheme.textSecondary)),
        const SizedBox(height: 12),
        Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
          ElevatedButton(onPressed: _currentIndex > 0 ? () => setState(() => _currentIndex--) : null, child: const Text('← 上一规则')),
          ElevatedButton(onPressed: _currentIndex < _rules.length - 1 ? () => setState(() => _currentIndex++) : null, child: const Text('下一规则 →')),
        ]),
      ])),
    );
  }
}
