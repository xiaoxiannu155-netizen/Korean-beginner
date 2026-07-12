import 'package:flutter/material.dart';
import 'config/theme.dart';
import 'widgets/main_scaffold.dart';

class KoreanApp extends StatelessWidget {
  const KoreanApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '韩语启蒙助手',
      theme: AppTheme.lightTheme,
      home: const MainScaffold(),
      debugShowCheckedModeBanner: false,
    );
  }
}
