import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../services/api_client.dart';
import '../../config/theme.dart';

class BadgeCollectionScreen extends ConsumerStatefulWidget {
  const BadgeCollectionScreen({super.key});
  @override
  ConsumerState<BadgeCollectionScreen> createState() => _BadgeCollectionScreenState();
}

class _BadgeCollectionScreenState extends ConsumerState<BadgeCollectionScreen> {
  List<Map<String, dynamic>> _badges = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadBadges();
  }

  Future<void> _loadBadges() async {
    try {
      final client = ref.read(apiClientProvider);
      final resp = await client.dio.get('/badges');
      setState(() { _badges = List<Map<String, dynamic>>.from(resp.data); _isLoading = false; });
    } catch (_) {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final earned = _badges.where((b) => b['earned'] == true).length;
    return Scaffold(
      appBar: AppBar(title: Text('🏆 勋章收集 ($earned/${_badges.length})')),
      body: _isLoading
        ? const Center(child: CircularProgressIndicator())
        : GridView.builder(
            padding: const EdgeInsets.all(16),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 3, crossAxisSpacing: 12, mainAxisSpacing: 12, childAspectRatio: 0.85),
            itemCount: _badges.length,
            itemBuilder: (_, i) => _BadgeTile(badge: _badges[i]),
          ),
    );
  }
}

class _BadgeTile extends StatelessWidget {
  final Map<String, dynamic> badge;
  const _BadgeTile({required this.badge});

  @override
  Widget build(BuildContext context) {
    final earned = badge['earned'] == true;
    return Container(
      decoration: BoxDecoration(
        color: earned ? Colors.white : const Color(0xFFF5F5F5),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: earned ? AppTheme.accent : const Color(0xFFEEEEEE), width: earned ? 2 : 1),
      ),
      child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
        Text(badge['icon'] ?? '🏅', style: TextStyle(fontSize: 32, color: earned ? null : Colors.grey.withOpacity(0.4))),
        const SizedBox(height: 6),
        Text(badge['name'] ?? '', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: earned ? AppTheme.textPrimary : const Color(0xFFBBBBBB)), textAlign: TextAlign.center),
        Text(badge['condition'] ?? '', style: TextStyle(fontSize: 8, color: earned ? AppTheme.textSecondary : const Color(0xFFDDDDDD)), textAlign: TextAlign.center, maxLines: 2),
      ]),
    );
  }
}
