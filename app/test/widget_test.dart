import 'package:flutter_test/flutter_test.dart';
import 'package:korean_app/app.dart';

void main() {
  testWidgets('App renders with bottom navigation', (WidgetTester tester) async {
    await tester.pumpWidget(const KoreanApp());
    expect(find.text('首页'), findsOneWidget);
    expect(find.text('学习'), findsOneWidget);
    expect(find.text('AI'), findsOneWidget);
    expect(find.text('我的'), findsOneWidget);
  });
}
