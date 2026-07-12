import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../services/api_client.dart';
import '../config/theme.dart';

/// Reusable pronunciation player with speed control and syllable breakdown
class PronunciationPlayer extends ConsumerStatefulWidget {
  final String text;
  final bool showSpeedControl;
  final bool showBreakdown;
  final VoidCallback? onPlay;

  const PronunciationPlayer({super.key, required this.text, this.showSpeedControl = true, this.showBreakdown = true, this.onPlay});

  @override
  ConsumerState<PronunciationPlayer> createState() => _PronunciationPlayerState();
}

class _PronunciationPlayerState extends ConsumerState<PronunciationPlayer> {
  double _speed = 1.0;
  List<Map<String, dynamic>> _breakdown = [];
  bool _showBreakdown = false;

  Future<void> _loadBreakdown() async {
    if (!widget.showBreakdown || _breakdown.isNotEmpty) return;
    try {
      final client = ref.read(apiClientProvider);
      final resp = await client.dio.get('/ai/pronounce/${Uri.encodeComponent(widget.text)}', queryParameters: {'speed': _speed});
      setState(() => _breakdown = List<Map<String, dynamic>>.from(resp.data['breakdown'] ?? []));
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    return Column(mainAxisSize: MainAxisSize.min, children: [
      // Speed selector
      if (widget.showSpeedControl)
        Row(mainAxisAlignment: MainAxisAlignment.center, children: [
          _SpeedBtn(speed: 1.0, current: _speed, onTap: () => setState(() => _speed = 1.0)),
          const SizedBox(width: 4),
          _SpeedBtn(speed: 0.75, current: _speed, onTap: () => setState(() => _speed = 0.75)),
          const SizedBox(width: 4),
          _SpeedBtn(speed: 0.5, current: _speed, onTap: () => setState(() => _speed = 0.5)),
        ]),
      const SizedBox(height: 8),
      // Play button
      GestureDetector(
        onTap: () {
          widget.onPlay?.call();
          _loadBreakdown();
        },
        child: Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(color: AppTheme.primary, shape: BoxShape.circle),
          child: const Icon(Icons.volume_up, color: Colors.white, size: 28),
        ),
      ),
      // Syllable breakdown
      if (widget.showBreakdown && _breakdown.isNotEmpty) ...[
        const SizedBox(height: 8),
        GestureDetector(
          onTap: () => setState(() => _showBreakdown = !_showBreakdown),
          child: Text(_showBreakdown ? '收起音节拆分 ▲' : '查看音节拆分 ▼', style: const TextStyle(fontSize: 11, color: AppTheme.primary)),
        ),
        if (_showBreakdown)
          Wrap(spacing: 6, runSpacing: 6, children: _breakdown.map((s) {
            final comp = s['components'] ?? '';
            final hint = s['pronunciation_hint'] ?? '';
            return Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              decoration: BoxDecoration(color: const Color(0xFFF8F7FF), borderRadius: BorderRadius.circular(6)),
              child: Column(children: [
                Text(s['syllable'] ?? '', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                Text(comp, style: const TextStyle(fontSize: 10, color: AppTheme.textSecondary)),
                if (hint.isNotEmpty) Text(hint, style: const TextStyle(fontSize: 9, color: AppTheme.primary)),
              ]),
            );
          }).toList()),
      ],
    ]);
  }
}

class _SpeedBtn extends StatelessWidget {
  final double speed, current;
  final VoidCallback onTap;
  const _SpeedBtn({required this.speed, required this.current, required this.onTap});

  String get label => speed == 1.0 ? '1×' : '${speed}×';

  @override
  Widget build(BuildContext context) {
    final selected = speed == current;
    return GestureDetector(onTap: onTap, child: Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(color: selected ? AppTheme.primary : const Color(0xFFF0EDFF), borderRadius: BorderRadius.circular(16)),
      child: Text(label, style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: selected ? Colors.white : AppTheme.primary)),
    ));
  }
}
