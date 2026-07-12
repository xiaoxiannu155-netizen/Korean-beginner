class Letter {
  final String id;
  final String char;
  final String type;
  final String? romanization;
  final String? chineseHint;
  final String? pronunciationAudioUrl;
  final String? strokeAnimationUrl;
  final String? mouthShapeUrl;
  final int orderIndex;
  final String? pronunciationTip;

  const Letter({required this.id, required this.char, required this.type, this.romanization, this.chineseHint, this.pronunciationAudioUrl, this.strokeAnimationUrl, this.mouthShapeUrl, this.orderIndex = 0, this.pronunciationTip});

  factory Letter.fromJson(Map<String, dynamic> json) => Letter(
    id: json['id'] as String, char: json['char'] as String, type: json['type'] as String,
    romanization: json['romanization'] as String?, chineseHint: json['chinese_hint'] as String?,
    pronunciationAudioUrl: json['pronunciation_audio_url'] as String?,
    strokeAnimationUrl: json['stroke_animation_url'] as String?,
    mouthShapeUrl: json['mouth_shape_url'] as String?,
    orderIndex: json['order_index'] as int? ?? 0,
    pronunciationTip: json['pronunciation_tip'] as String?,
  );

  String get categoryLabel {
    switch (type) { case 'basic_vowel': return '基础元音'; case 'compound_vowel': return '复合元音'; case 'consonant': return '基础辅音'; case 'double_consonant': return '双辅音'; case 'syllable_rule': return '拼读规则'; default: return '其他'; }
  }
}
