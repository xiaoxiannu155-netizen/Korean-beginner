import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:korean_app/app.dart';

void main() {
  testWidgets('App renders with bottom navigation', (WidgetTester tester) async {
    await tester.pumpWidget(const ProviderScope(child: KoreanApp()));
    await tester.pump(const Duration(milliseconds: 100));
    expect(find.text('首页'), findsOneWidget);
    expect(find.text('学习'), findsOneWidget);
    expect(find.text('AI'), findsOneWidget);
    expect(find.text('我的'), findsOneWidget);
    // 清空组件树，让 Dio 超时定时器随 ProviderScope 销毁
    await tester.pumpWidget(const SizedBox.shrink());
    await tester.pump(const Duration(seconds: 11));
  });
}
