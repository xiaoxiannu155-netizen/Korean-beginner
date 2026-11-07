import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../services/api_client.dart';
import '../../config/theme.dart';

class ScenarioListScreen extends ConsumerStatefulWidget {
  const ScenarioListScreen({super.key});
  @override
  ConsumerState<ScenarioListScreen> createState() => _ScenarioListScreenState();
}

class _ScenarioListScreenState extends ConsumerState<ScenarioListScreen> {
  List<Map<String, dynamic>> _scenarios = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final client = ref.read(apiClientProvider);
      final resp = await client.dio.get('/scenarios');
      setState(() { _scenarios = List<Map<String, dynamic>>.from(resp.data); _isLoading = false; });
    } catch (_) { setState(() => _isLoading = false); }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('🎭 情景对话')),
      body: _isLoading ? const Center(child: CircularProgressIndicator()) : ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: _scenarios.length,
        itemBuilder: (_, i) {
          final s = _scenarios[i];
          final difficulty = s['difficulty'] as int? ?? 1;
          return Card(
            margin: const EdgeInsets.only(bottom: 12),
            child: ListTile(
              leading: Text(s['title']?.toString().substring(0, 2) ?? '🎭', style: const TextStyle(fontSize: 28)),
              title: Text(s['title']?.toString() ?? '', style: const TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(s['description']?.toString() ?? '', style: const TextStyle(fontSize: 12, color: AppTheme.textSecondary)),
                const SizedBox(height: 4),
                Row(children: List.generate(3, (j) => Icon(Icons.star, size: 14, color: j < difficulty ? AppTheme.accent : const Color(0xFFDDDDDD)))),
              ]),
              trailing: const Icon(Icons.arrow_forward_ios, size: 16),
              onTap: () {
                Navigator.push(context, MaterialPageRoute(
                  builder: (_) => ScenarioChatScreen(scenarioId: s['id'] as String, title: s['title'] as String),
                ));
              },
            ),
          );
        },
      ),
    );
  }
}

class ScenarioChatScreen extends ConsumerStatefulWidget {
  final String scenarioId;
  final String title;
  const ScenarioChatScreen({super.key, required this.scenarioId, required this.title});

  @override
  ConsumerState<ScenarioChatScreen> createState() => _ScenarioChatScreenState();
}

class _ScenarioChatScreenState extends ConsumerState<ScenarioChatScreen> {
  final _msgCtrl = TextEditingController();
  final _scrollCtrl = ScrollController();
  final List<Map<String, String>> _messages = [];
  Map<String, dynamic>? _scenario;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadScenario();
  }

  Future<void> _loadScenario() async {
    try {
      final client = ref.read(apiClientProvider);
      final resp = await client.dio.get('/scenarios/${widget.scenarioId}');
      setState(() { _scenario = resp.data; _isLoading = false; });
      // Add starter message
      if (_scenario != null) {
        _messages.add({
          'role': 'ai', 'ko': _scenario!['starter'] ?? '',
          'zh': _scenario!['starter_zh'] ?? '',
        });
      }
    } catch (_) { setState(() => _isLoading = false); }
  }

  Future<void> _send() async {
    final text = _msgCtrl.text.trim();
    if (text.isEmpty) return;
    _msgCtrl.clear();

    setState(() => _messages.add({'role': 'user', 'ko': text, 'zh': ''}));
    _scrollToBottom();

    try {
      final client = ref.read(apiClientProvider);
      final resp = await client.dio.post('/scenarios/${widget.scenarioId}/chat', data: {'message': text});
      setState(() {
        _messages.add({
          'role': 'ai',
          'ko': resp.data['reply'] ?? '',
          'zh': resp.data['reply_zh'] ?? '',
        });
      });
      _scrollToBottom();
    } catch (_) {
      setState(() => _messages.add({'role': 'ai', 'ko': '죄송합니다, 다시 시도해 주세요.', 'zh': '抱歉，请重试。'}));
    }
  }

  void _scrollToBottom() {
    Future.delayed(const Duration(milliseconds: 100), () {
      if (_scrollCtrl.hasClients) _scrollCtrl.animateTo(_scrollCtrl.position.maxScrollExtent, duration: const Duration(milliseconds: 300), curve: Curves.easeOut);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.title)),
      body: _isLoading ? const Center(child: CircularProgressIndicator()) : Column(children: [
        // Context card
        Container(
          width: double.infinity, margin: const EdgeInsets.all(12), padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(color: const Color(0xFFFFF8E1), borderRadius: BorderRadius.circular(8)),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            const Text('💡 场景说明', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
            Text(_scenario?['context'] ?? '', style: const TextStyle(fontSize: 11)),
            if (_scenario?['tips'] != null) ...[
              const SizedBox(height: 4),
              Wrap(spacing: 4, children: (_scenario!['tips'] as List).map((t) => Container(padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2), decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(4)), child: Text(t.toString(), style: const TextStyle(fontSize: 10)))).toList()),
            ],
          ]),
        ),
        // Messages
        Expanded(child: ListView.builder(controller: _scrollCtrl, padding: const EdgeInsets.symmetric(horizontal: 12), itemCount: _messages.length, itemBuilder: (_, i) {
          final msg = _messages[i];
          final isUser = msg['role'] == 'user';
          return Align(
            alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
            child: Container(
              margin: const EdgeInsets.only(bottom: 8),
              padding: const EdgeInsets.all(12),
              constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.75),
              decoration: BoxDecoration(
                color: isUser ? AppTheme.primary : Colors.white,
                borderRadius: BorderRadius.circular(12),
                border: isUser ? null : Border.all(color: const Color(0xFFEEEEEE)),
              ),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(msg['ko'] ?? '', style: TextStyle(fontSize: 16, color: isUser ? Colors.white : AppTheme.textPrimary)),
                if ((msg['zh'] ?? '').isNotEmpty) ...[
                  const SizedBox(height: 4),
                  Text(msg['zh'] ?? '', style: TextStyle(fontSize: 12, color: isUser ? Colors.white70 : AppTheme.textSecondary)),
                ],
              ]),
            ),
          );
        })),
        // Input
        Container(padding: const EdgeInsets.all(12), decoration: BoxDecoration(color: Colors.white, boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 5, offset: const Offset(0, -2))]),
          child: Row(children: [
            Expanded(child: TextField(controller: _msgCtrl, decoration: const InputDecoration(hintText: '输入韩语...', border: OutlineInputBorder(), contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 10)), onSubmitted: (_) => _send())),
            const SizedBox(width: 8),
            IconButton(onPressed: _send, icon: const Icon(Icons.send, color: AppTheme.primary)),
          ]),
        ),
      ]),
    );
  }

  @override
  void dispose() { _msgCtrl.dispose(); _scrollCtrl.dispose(); super.dispose(); }
}
