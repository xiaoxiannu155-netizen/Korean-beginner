import 'dart:math';
import 'package:flutter/material.dart';
import '../config/theme.dart';

/// Joy animation states using pure Flutter animations (no Lottie dependency needed initially)
class JoyAnimation extends StatefulWidget {
  final JoyAnimState animState;
  final double size;
  final VoidCallback? onTap;

  const JoyAnimation({super.key, this.animState = JoyAnimState.idle, this.size = 80, this.onTap});

  @override
  State<JoyAnimation> createState() => _JoyAnimationState();
}

enum JoyAnimState { idle, sleeping, waking, celebrating, encouraging, listening }

class _JoyAnimationState extends State<JoyAnimation> with TickerProviderStateMixin {
  late AnimationController _bounceController;
  late AnimationController _zzzController;
  late Animation<double> _bounceAnim;
  late Animation<double> _zzzOpacity;

  @override
  void initState() {
    super.initState();
    _bounceController = AnimationController(duration: const Duration(milliseconds: 1200), vsync: this);
    _bounceAnim = Tween(begin: 0.0, end: 1.0).animate(CurvedAnimation(parent: _bounceController, curve: Curves.easeInOut));
    _zzzController = AnimationController(duration: const Duration(milliseconds: 2000), vsync: this);
    _zzzOpacity = Tween(begin: 0.0, end: 1.0).animate(CurvedAnimation(parent: _zzzController, curve: Curves.easeInOut));

    if (widget.animState == JoyAnimState.idle || widget.animState == JoyAnimState.celebrating) {
      _bounceController.repeat(reverse: true);
    }
    if (widget.animState == JoyAnimState.sleeping) {
      _zzzController.repeat(reverse: true);
    }
  }

  @override
  void didUpdateWidget(JoyAnimation oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.animState != widget.animState) {
      _bounceController.stop();
      _zzzController.stop();
      if (widget.animState == JoyAnimState.idle || widget.animState == JoyAnimState.celebrating) {
        _bounceController.repeat(reverse: true);
      }
      if (widget.animState == JoyAnimState.sleeping) {
        _zzzController.repeat(reverse: true);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: widget.onTap,
      child: AnimatedBuilder(
        animation: Listenable.merge([_bounceAnim, _zzzOpacity]),
        builder: (_, child) {
          final bounce = sin(_bounceAnim.value * 2 * pi) * 5;
          return Transform.translate(
            offset: Offset(0, widget.animState != JoyAnimState.sleeping ? bounce : 0),
            child: Stack(
              clipBehavior: Clip.none,
              children: [
                // Joy body
                _buildJoyBody(widget.size, widget.animState),
                // Zzz for sleeping
                if (widget.animState == JoyAnimState.sleeping)
                  Positioned(
                    top: -20, right: -30,
                    child: Opacity(
                      opacity: _zzzOpacity.value,
                      child: const SleepZzz(),
                    ),
                  ),
                // Sparkles for celebrating
                if (widget.animState == JoyAnimState.celebrating)
                  ..._buildSparkles(),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildJoyBody(double s, JoyAnimState state) {
    final mouthCurve = state == JoyAnimState.celebrating ? 0.6 : (state == JoyAnimState.sleeping ? 0.05 : 0.4);
    return Container(
      width: s, height: s * 0.9,
      decoration: BoxDecoration(
        gradient: const LinearGradient(colors: [Color(0xFFFFEAA7), Color(0xFFFDCB6E)]),
        borderRadius: BorderRadius.only(
          topLeft: Radius.circular(s * 0.5), topRight: Radius.circular(s * 0.5),
          bottomLeft: Radius.circular(s * 0.45), bottomRight: Radius.circular(s * 0.45),
        ),
      ),
      child: Stack(children: [
        // Ears
        Positioned(top: -s*0.15, left: s*0.08, child: Transform.rotate(angle: -0.3, child: Container(width: s*0.22, height: s*0.3, decoration: BoxDecoration(gradient: const LinearGradient(colors: [Color(0xFFFFEAA7), Color(0xFFFDCB6E)]), borderRadius: BorderRadius.circular(s*0.12))))),
        Positioned(top: -s*0.15, right: s*0.08, child: Transform.rotate(angle: 0.3, child: Container(width: s*0.22, height: s*0.3, decoration: BoxDecoration(gradient: const LinearGradient(colors: [Color(0xFFFFEAA7), Color(0xFFFDCB6E)]), borderRadius: BorderRadius.circular(s*0.12))))),
        // Eyes
        Positioned(top: s*0.3, left: s*0.18, child: _buildEye(s*0.2, state)),
        Positioned(top: s*0.3, right: s*0.18, child: _buildEye(s*0.2, state)),
        // Mouth
        Positioned(top: s*0.55, left: s*0.3, child: Container(width: s*0.4, height: s*0.12, decoration: BoxDecoration(
          border: Border(bottom: BorderSide(color: const Color(0xFF2D3436), width: max(s*0.03, 1.5))),
          borderRadius: BorderRadius.only(bottomLeft: Radius.circular(s*mouthCurve), bottomRight: Radius.circular(s*mouthCurve)),
        ))),
        // Blush
        Positioned(top: s*0.5, left: s*0.08, child: Container(width: s*0.13, height: s*0.07, decoration: BoxDecoration(color: const Color(0x66FF7675), borderRadius: BorderRadius.circular(s*0.1)))),
        Positioned(top: s*0.5, right: s*0.08, child: Container(width: s*0.13, height: s*0.07, decoration: BoxDecoration(color: const Color(0x66FF7675), borderRadius: BorderRadius.circular(s*0.1)))),
      ]),
    );
  }

  Widget _buildEye(double s, JoyAnimState state) {
    final eyeHeight = state == JoyAnimState.sleeping ? s * 0.1 : s * 1.1;
    return Container(
      width: s, height: eyeHeight,
      decoration: const BoxDecoration(color: Color(0xFF2D3436), shape: BoxShape.circle),
      child: state != JoyAnimState.sleeping
        ? Align(alignment: Alignment.topLeft, child: Padding(padding: EdgeInsets.all(s*0.15), child: Container(width: s*0.35, height: s*0.35, decoration: const BoxDecoration(color: Colors.white, shape: BoxShape.circle))))
        : null,
    );
  }

  List<Widget> _buildSparkles() {
    return [
      Positioned(top: -10, left: -10, child: _sparkle(12)),
      Positioned(top: -15, right: -5, child: _sparkle(10)),
      Positioned(bottom: -5, left: 10, child: _sparkle(8)),
    ];
  }

  Widget _sparkle(double s) {
    return Container(width: s, height: s, decoration: const BoxDecoration(color: AppTheme.accent, shape: BoxShape.circle));
  }

  @override
  void dispose() {
    _bounceController.dispose();
    _zzzController.dispose();
    super.dispose();
  }
}

class SleepZzz extends StatelessWidget {
  const SleepZzz({super.key});
  @override
  Widget build(BuildContext context) {
    return const Row(mainAxisSize: MainAxisSize.min, children: [
      Text('Z', style: TextStyle(fontSize: 12, color: Colors.grey, fontWeight: FontWeight.bold)),
      SizedBox(width: 2),
      Text('z', style: TextStyle(fontSize: 16, color: Colors.grey, fontWeight: FontWeight.bold)),
      SizedBox(width: 2),
      Text('z', style: TextStyle(fontSize: 20, color: Colors.grey, fontWeight: FontWeight.bold)),
    ]);
  }
}
