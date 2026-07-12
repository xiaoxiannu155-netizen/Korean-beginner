class BatchimRule {
  final String id;
  final String? title, ruleType, description, animationUrl;
  final int? orderIndex;
  final List<BatchimExample> examples;

  BatchimRule({required this.id, this.title, this.ruleType, this.description, this.animationUrl, this.orderIndex, this.examples = const []});

  factory BatchimRule.fromJson(Map<String, dynamic> json) => BatchimRule(
    id: json['id'] as String, title: json['title'] as String?, ruleType: json['rule_type'] as String?,
    description: json['description'] as String?, animationUrl: json['animation_url'] as String?,
    orderIndex: json['order_index'] as int?,
    examples: (json['examples'] as List<dynamic>?)?.map((e) => BatchimExample.fromJson(e)).toList() ?? [],
  );
}

class BatchimExample {
  final String id;
  final String? writtenForm, pronouncedForm, processDescription, audioUrl;

  BatchimExample({required this.id, this.writtenForm, this.pronouncedForm, this.processDescription, this.audioUrl});
  factory BatchimExample.fromJson(Map<String, dynamic> json) => BatchimExample(
    id: json['id'] as String, writtenForm: json['written_form'] as String?,
    pronouncedForm: json['pronounced_form'] as String?, processDescription: json['process_description'] as String?,
    audioUrl: json['audio_url'] as String?,
  );
}
