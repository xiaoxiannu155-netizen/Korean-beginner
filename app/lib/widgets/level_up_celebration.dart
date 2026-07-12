import 'dart:math';
import 'package:flutter/material.dart';
import '../config/theme.dart';

/// Full-screen level up celebration overlay
class LevelUpCelebration extends StatefulWidget {
  final String message;
  final String oldLevel;
  final String newLevel;
  final VoidCallback onDismiss;

  const LevelUpCelebration({super.key, required this.message, required this.oldLevel, required this.newLevel, required this.onDismiss});

  @override
  State<LevelUpCelebration> createState() => _LevelUpCelebrationState();
}

class _LevelUpCelebrationState extends State<LevelUpCelebration> with TickerProviderStateMixin {
  late AnimationController _scaleController;
  late AnimationController _confettiController;
  late Animation<double> _scaleAnim;
  final _random = Random();

  @override
  void initState() {
    super.initState();
    _scaleController = AnimationController(duration: const Duration(milliseconds: 600), vsync: this);
    _scaleAnim = Tween(begin: 0.3, end: 1.0).animate(CurvedAnimation(parent: _scaleController, curve: Curves.elasticOut));
    _confettiController = AnimationController(duration: const Duration(milliseconds: 2000), vsync: this);
    _scaleController.forward();
    _confettiController.forward();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: widget.onDismiss,
      child: Container(
        color: Colors.black54,
        child: Center(
          child: AnimatedBuilder(
            animation: Listenable.merge([_scaleAnim, _confettiController]),
            builder: (_, __) {
              return Stack(
                clipBehavior: Clip.none,
                children: [
                  // Confetti particles
                  ...List.generate(20, (i) {
                    final x = (_random.nextDouble() - 0.5) * 300 * _confettiController.value;
                    final y = -200 * _confettiController.value + (_random.nextDouble() * 100);
                    return Positioned(
                      left: 150 + x, top: y,
                      child: Container(
                        width: 8, height: 8,
                        decoration: BoxDecoration(
                          color: [AppTheme.primary, AppTheme.accent, AppTheme.success, AppTheme.error][i % 4],
                          shape: BoxShape.circle,
                        ),
                      ),
                    );
                  }),
                  // Main card
                  Transform.scale(
                    scale: _scaleAnim.value,
                    child: Container(
                      padding: const EdgeInsets.all(32),
                      decoration: BoxDecoration(
                        gradient: const LinearGradient(colors: [AppTheme.primary, Color(0xFFA29BFE)]),
                        borderRadius: BorderRadius.circular(20),
                        boxShadow: [BoxShadow(color: AppTheme.primary.withOpacity(0.3), blurRadius: 20)],
                      ),
                      child: Column(mainAxisSize: MainAxisSize.min, children: [
                        const Text('🎉', style: TextStyle(fontSize: 64)),
                        const SizedBox(height: 12),
                        Text(widget.message, style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 8),
                        Text('${widget.oldLevel} → ${widget.newLevel}', style: const TextStyle(color: AppTheme.accent, fontSize: 28, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 12),
                        const Text('点击继续', style: TextStyle(color: Colors.white70, fontSize: 12)),
                      ]),
                    ),
                  ),
                ],
              );
            },
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _scaleController.dispose();
    _confettiController.dispose();
    super.dispose();
  }
}
