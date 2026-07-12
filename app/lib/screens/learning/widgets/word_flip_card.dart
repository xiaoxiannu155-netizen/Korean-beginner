import 'package:flutter/material.dart';
import '../../../models/word.dart';
import '../../../config/theme.dart';

class WordFlipCard extends StatefulWidget {
  final Word word;
  const WordFlipCard({super.key, required this.word});

  @override
  State<WordFlipCard> createState() => _WordFlipCardState();
}

class _WordFlipCardState extends State<WordFlipCard> with SingleTickerProviderStateMixin {
  bool _isFlipped = false;
  late final AnimationController _controller;
  late final Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(duration: const Duration(milliseconds: 400), vsync: this);
    _animation = Tween(begin: 0.0, end: 1.0).animate(CurvedAnimation(parent: _controller, curve: Curves.easeInOut));
  }

  void _flip() {
    setState(() => _isFlipped = !_isFlipped);
    _isFlipped ? _controller.forward() : _controller.reverse();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: _flip,
      child: AnimatedBuilder(
        animation: _animation,
        builder: (_, child) {
          final isFront = _animation.value < 0.5;
          return Transform(
            alignment: Alignment.center,
            transform: Matrix4.identity()..setEntry(3, 2, 0.001)..rotateY(_animation.value * 3.14159),
            child: Container(
              width: 300, height: 400,
              decoration: BoxDecoration(
                color: isFront ? Colors.white : const Color(0xFFF8F7FF),
                borderRadius: BorderRadius.circular(16),
                boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 10, offset: const Offset(0, 4))],
              ),
              child: Center(
                child: Transform(
                  alignment: Alignment.center,
                  transform: Matrix4.identity()..rotateY(_animation.value > 0.5 ? 3.14159 : 0),
                  child: isFront ? _buildFront() : _buildBack(),
                ),
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildFront() {
    final w = widget.word;
    return Padding(padding: const EdgeInsets.all(24), child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
      Text(w.korean, style: const TextStyle(fontSize: 48, fontWeight: FontWeight.bold)),
      const SizedBox(height: 12),
      Text('[${w.romanization ?? ""}]', style: const TextStyle(fontSize: 20, color: AppTheme.primary)),
      const SizedBox(height: 8),
      const Text('👆 点击翻转', style: TextStyle(color: AppTheme.textSecondary)),
    ]));
  }

  Widget _buildBack() {
    final w = widget.word;
    return Padding(padding: const EdgeInsets.all(24), child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
      Text(w.chinese ?? '', style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
      const SizedBox(height: 16),
      if (w.examples.isNotEmpty)
        Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(color: const Color(0xFFFFF5F5), borderRadius: BorderRadius.circular(10), border: const Border(left: BorderSide(color: Color(0xFFE84393), width: 3))),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            if (w.examples.first.sourceName != null)
              Text('📺 ${w.examples.first.sourceName}', style: const TextStyle(fontSize: 10, color: Color(0xFFE84393), fontWeight: FontWeight.bold)),
            const SizedBox(height: 4),
            Text(w.examples.first.koreanSentence, style: const TextStyle(fontSize: 16)),
            const SizedBox(height: 4),
            if (w.examples.first.chineseTranslation != null)
              Text(w.examples.first.chineseTranslation!, style: const TextStyle(fontSize: 12, color: AppTheme.textSecondary)),
          ]),
        ),
    ]));
  }

  @override
  void dispose() { _controller.dispose(); super.dispose(); }
}
