import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/joy_provider.dart';

class JoySprite extends ConsumerWidget {
  final double size;
  const JoySprite({super.key, this.size = 48});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(joyProvider);
    final notifier = ref.read(joyProvider.notifier);

    return GestureDetector(
      onTap: () {
        if (state == JoyState.sleeping || state == JoyState.idle) {
          notifier.activate();
        } else {
          notifier.deactivate();
        }
      },
      child: AnimatedOpacity(
        duration: const Duration(milliseconds: 500),
        opacity: state == JoyState.sleeping ? 0.35 : 1.0,
        child: AnimatedScale(
          duration: const Duration(milliseconds: 500),
          scale: state == JoyState.sleeping ? 0.6 : 1.0,
          child: _buildJoyBody(size),
        ),
      ),
    );
  }

  Widget _buildJoyBody(double s) {
    return Container(
      width: s,
      height: s * 0.9,
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          begin: Alignment.topCenter, end: Alignment.bottomCenter,
          colors: [Color(0xFFFFEAA7), Color(0xFFFDCB6E)],
        ),
        borderRadius: BorderRadius.only(
          topLeft: Radius.circular(s * 0.5), topRight: Radius.circular(s * 0.5),
          bottomLeft: Radius.circular(s * 0.45), bottomRight: Radius.circular(s * 0.45),
        ),
        boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.1), blurRadius: 4)],
      ),
      child: Stack(
        children: [
          // Left ear
          Positioned(top: -s * 0.15, left: s * 0.08,
            child: Transform.rotate(angle: -0.3,
              child: Container(width: s * 0.25, height: s * 0.35,
                decoration: BoxDecoration(gradient: const LinearGradient(colors: [Color(0xFFFFEAA7), Color(0xFFFDCB6E)]), borderRadius: BorderRadius.circular(s * 0.15))))),
          // Right ear
          Positioned(top: -s * 0.15, right: s * 0.08,
            child: Transform.rotate(angle: 0.3,
              child: Container(width: s * 0.25, height: s * 0.35,
                decoration: BoxDecoration(gradient: const LinearGradient(colors: [Color(0xFFFFEAA7), Color(0xFFFDCB6E)]), borderRadius: BorderRadius.circular(s * 0.15))))),
          // Eyes
          Positioned(top: s * 0.3, left: s * 0.18, child: _buildEye(s * 0.2)),
          Positioned(top: s * 0.3, right: s * 0.18, child: _buildEye(s * 0.2)),
          // Blush
          Positioned(top: s * 0.5, left: s * 0.08, child: Container(width: s * 0.15, height: s * 0.08, decoration: BoxDecoration(color: const Color(0x66FF7675), borderRadius: BorderRadius.circular(s * 0.1)))),
          Positioned(top: s * 0.5, right: s * 0.08, child: Container(width: s * 0.15, height: s * 0.08, decoration: BoxDecoration(color: const Color(0x66FF7675), borderRadius: BorderRadius.circular(s * 0.1)))),
          // Mouth
          Positioned(top: s * 0.55, left: s * 0.3,
            child: Container(width: s * 0.4, height: s * 0.12,
              decoration: BoxDecoration(border: Border(bottom: BorderSide(color: const Color(0xFF2D3436), width: s * 0.04)), borderRadius: BorderRadius.only(bottomLeft: Radius.circular(s * 0.2), bottomRight: Radius.circular(s * 0.2))))),
        ],
      ),
    );
  }

  Widget _buildEye(double size) {
    return Container(width: size, height: size * 1.2, decoration: const BoxDecoration(color: Color(0xFF2D3436), shape: BoxShape.circle),
      child: Align(alignment: Alignment.topLeft,
        child: Padding(padding: EdgeInsets.all(size * 0.15),
          child: Container(width: size * 0.38, height: size * 0.38, decoration: const BoxDecoration(color: Colors.white, shape: BoxShape.circle)))));
  }
}

class SleepZzz extends StatelessWidget {
  const SleepZzz({super.key});
  @override
  Widget build(BuildContext context) {
    return const Row(mainAxisSize: MainAxisSize.min, children: [
      Text('Z', style: TextStyle(fontSize: 10, color: Colors.grey, fontWeight: FontWeight.bold)),
      SizedBox(width: 2),
      Text('z', style: TextStyle(fontSize: 14, color: Colors.grey, fontWeight: FontWeight.bold)),
      SizedBox(width: 2),
      Text('z', style: TextStyle(fontSize: 18, color: Colors.grey, fontWeight: FontWeight.bold)),
    ]);
  }
}
