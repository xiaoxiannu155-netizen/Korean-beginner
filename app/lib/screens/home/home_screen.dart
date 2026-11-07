import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../models/daily_task.dart';
import '../../providers/auth_provider.dart';
import '../../providers/daily_task_provider.dart';
import 'widgets/greeting_header.dart';
import 'widgets/daily_task_list.dart';
import 'widgets/learning_path_bar.dart';
import 'widgets/quick_actions.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final auth = ref.watch(authProvider);
    final tasksAsync = ref.watch(dailyTaskProvider);

    return Scaffold(
      body: RefreshIndicator(
        onRefresh: () async {
          ref.invalidate(dailyTaskProvider);
          await ref.read(dailyTaskProvider.future);
        },
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          child: Column(
            children: [
              GreetingHeader(user: auth.user, progress: auth.progress),
              Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    tasksAsync.when(
                      data: (task) => DailyTaskList(tasks: task.items),
                      loading: () => const Center(child: CircularProgressIndicator()),
                      error: (_, __) => DailyTaskList(tasks: const DailyTask().items),
                    ),
                    const SizedBox(height: 20),
                    const QuickActions(),
                    const SizedBox(height: 20),
                    LearningPathBar(currentStage: auth.progress?.stage ?? 1),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
