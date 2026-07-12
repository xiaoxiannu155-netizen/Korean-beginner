import 'package:flutter/material.dart';
import '../../../models/daily_task.dart';
import '../../../config/theme.dart';

class DailyTaskList extends StatelessWidget {
  final List<TaskItem> tasks;
  final void Function(int index)? onTaskTap;

  const DailyTaskList({super.key, required this.tasks, this.onTaskTap});

  @override
  Widget build(BuildContext context) {
    final completed = tasks.where((t) => t.completed).length;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('📋 今日任务',
          style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppTheme.textPrimary)),
        const SizedBox(height: 4),
        Text('预计 10 分钟 · 完成 $completed/${tasks.length}',
          style: const TextStyle(fontSize: 12, color: AppTheme.textSecondary)),
        const SizedBox(height: 12),
        ...List.generate(tasks.length, (i) => _TaskRow(
          task: tasks[i],
          onTap: onTaskTap != null ? () => onTaskTap!(i) : null,
        )),
      ],
    );
  }
}

class _TaskRow extends StatefulWidget {
  final TaskItem task;
  final VoidCallback? onTap;

  const _TaskRow({required this.task, this.onTap});

  @override
  State<_TaskRow> createState() => _TaskRowState();
}

class _TaskRowState extends State<_TaskRow> with SingleTickerProviderStateMixin {
  late final AnimationController _animController;
  late final Animation<double> _strikethroughAnim;
  bool _wasCompleted = false;

  @override
  void initState() {
    super.initState();
    _wasCompleted = widget.task.completed;
    _animController = AnimationController(
      duration: const Duration(milliseconds: 600),
      vsync: this,
    );
    _strikethroughAnim = Tween(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _animController, curve: Curves.easeInOut),
    );
    if (widget.task.completed) {
      _animController.value = 1.0;
    }
  }

  @override
  void didUpdateWidget(_TaskRow oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (!oldWidget.task.completed && widget.task.completed) {
      _animController.forward();
    }
  }

  @override
  Widget build(BuildContext context) {
    final task = widget.task;
    final completed = task.completed;
    final screenWidth = MediaQuery.of(context).size.width;

    return GestureDetector(
      onTap: widget.onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 300),
        margin: const EdgeInsets.only(bottom: 8),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
        decoration: BoxDecoration(
          color: completed ? const Color(0xFFF0FDF4) : Colors.white,
          borderRadius: BorderRadius.circular(10),
          border: Border.all(
            color: completed ? const Color(0xFFBBF7D0) : const Color(0xFFEEEEEE),
          ),
        ),
        child: Row(
          children: [
            AnimatedContainer(
              duration: const Duration(milliseconds: 300),
              width: 22, height: 22,
              decoration: BoxDecoration(
                color: completed ? AppTheme.success : Colors.transparent,
                shape: BoxShape.circle,
                border: completed ? null : Border.all(color: const Color(0xFFDDDDDD), width: 2),
              ),
              child: completed
                ? const Icon(Icons.check, color: Colors.white, size: 14)
                : null,
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Stack(
                children: [
                  Text(
                    task.label,
                    style: TextStyle(
                      fontSize: 14,
                      color: completed ? AppTheme.textSecondary : AppTheme.textPrimary,
                    ),
                  ),
                  if (completed)
                    Positioned(
                      top: 12,
                      left: 0,
                      child: AnimatedBuilder(
                        animation: _strikethroughAnim,
                        builder: (_, child) => Container(
                          height: 2,
                          width: (screenWidth - 120) * _strikethroughAnim.value,
                          color: AppTheme.textSecondary.withOpacity(0.4),
                        ),
                      ),
                    ),
                ],
              ),
            ),
            Text(
              '+${task.xp}XP',
              style: TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w600,
                color: completed ? AppTheme.success : AppTheme.textSecondary,
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _animController.dispose();
    super.dispose();
  }
}
