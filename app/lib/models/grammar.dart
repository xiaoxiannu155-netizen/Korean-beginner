class GrammarPoint {
  final String id;
  final String? title, structureFormula, explanation, usageScenario;
  final int? level, orderIndex;
  final List<GrammarExample> examples;

  GrammarPoint({required this.id, this.title, this.level, this.structureFormula, this.explanation, this.usageScenario, this.orderIndex, this.examples = const []});

  factory GrammarPoint.fromJson(Map<String, dynamic> json) => GrammarPoint(
    id: json['id'] as String, title: json['title'] as String?, level: json['level'] as int?,
    structureFormula: json['structure_formula'] as String?, explanation: json['explanation'] as String?,
    usageScenario: json['usage_scenario'] as String?, orderIndex: json['order_index'] as int?,
    examples: (json['examples'] as List<dynamic>?)?.map((e) => GrammarExample.fromJson(e)).toList() ?? [],
  );
}

class GrammarExample {
  final String id;
  final String? koreanSentence, chineseTranslation;
  final bool isWrongExample;

  GrammarExample({required this.id, this.koreanSentence, this.chineseTranslation, this.isWrongExample = false});
  factory GrammarExample.fromJson(Map<String, dynamic> json) => GrammarExample(
    id: json['id'] as String, koreanSentence: json['korean_sentence'] as String?,
    chineseTranslation: json['chinese_translation'] as String?, isWrongExample: json['is_wrong_example'] as bool? ?? false,
  );
}
