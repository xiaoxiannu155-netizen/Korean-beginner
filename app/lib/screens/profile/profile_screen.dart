import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../providers/auth_provider.dart';
import '../../config/theme.dart';
import 'widgets/stats_card.dart';
import 'badge_collection_screen.dart';
import 'joy_settings_screen.dart';

class ProfileScreen extends ConsumerWidget {
  const ProfileScreen({super.key});
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final auth = ref.watch(authProvider);
    return Scaffold(
      appBar: AppBar(title: const Text('👤 我的')),
      body: SingleChildScrollView(padding: const EdgeInsets.all(16), child: Column(children: [
        CircleAvatar(radius: 40, backgroundColor: AppTheme.primary, child: Text(auth.user?.username?.isNotEmpty == true ? auth.user!.username![0].toUpperCase() : '👤', style: const TextStyle(fontSize: 32, color: Colors.white))),
        const SizedBox(height: 12),
        Text(auth.user?.username ?? '同学', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
        Text(auth.progress?.levelName ?? '🥉 铜', style: const TextStyle(color: AppTheme.textSecondary)),
        const SizedBox(height: 24),
        StatsCard(progress: auth.progress),
        const SizedBox(height: 24),
        _Item(icon: '🧚', label: 'AI 小精灵设置', onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const JoySettingsScreen()))),
        _Item(icon: '🏆', label: '勋章收集', onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const BadgeCollectionScreen()))),
        _Item(icon: '🎯', label: '学习目标', onTap: () {}),
        _Item(icon: '🔔', label: '提醒设置', onTap: () {}),
        _Item(icon: 'ℹ️', label: '关于', onTap: () {}),
      ])),
    );
  }
}

class _Item extends StatelessWidget {
  final String icon, label; final VoidCallback onTap;
  const _Item({required this.icon, required this.label, required this.onTap});
  @override
  Widget build(BuildContext context) => ListTile(leading: Text(icon, style: const TextStyle(fontSize: 24)), title: Text(label), trailing: const Icon(Icons.chevron_right), onTap: onTap);
}
