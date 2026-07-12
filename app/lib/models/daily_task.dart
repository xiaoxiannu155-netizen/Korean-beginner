class DailyTask {
  final int wordsCompleted;
  final bool grammarCompleted;
  final bool listeningCompleted;
  final bool speakingCompleted;

  const DailyTask({
    this.wordsCompleted = 0,
    this.grammarCompleted = false,
    this.listeningCompleted = false,
    this.speakingCompleted = false,
  });

  factory DailyTask.fromJson(Map<String, dynamic> json) => DailyTask(
    wordsCompleted: json['words_completed'] as int? ?? 0,
    grammarCompleted: json['grammar_completed'] as bool? ?? false,
    listeningCompleted: json['listening_completed'] as bool? ?? false,
    speakingCompleted: json['speaking_completed'] as bool? ?? false,
  );

  double get progress {
    int done = 0;
    if (wordsCompleted >= 5) done++;
    if (grammarCompleted) done++;
    if (listeningCompleted) done++;
    if (speakingCompleted) done++;
    return done / 4.0;
  }

  List<TaskItem> get items => [
    TaskItem(label: '5个新单词', xp: 30, completed: wordsCompleted >= 5, progress: wordsCompleted / 5),
    TaskItem(label: '1个语法点', xp: 20, completed: grammarCompleted),
    TaskItem(label: '1次听力练习', xp: 15, completed: listeningCompleted),
    TaskItem(label: '1次口语练习', xp: 25, completed: speakingCompleted),
  ];
}

class TaskItem {
  final String label;
  final int xp;
  final bool completed;
  final double? progress;

  const TaskItem({required this.label, required this.xp, this.completed = false, this.progress});
}
