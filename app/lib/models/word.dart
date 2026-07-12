class Word {
  final String id, korean;
  final String? chinese, romanization, pronunciationAudioUrl, category, subCategory;
  final int difficultyLevel;
  final List<WordExample> examples;

  Word({required this.id, required this.korean, this.chinese, this.romanization, this.pronunciationAudioUrl, this.category, this.subCategory, this.difficultyLevel = 1, this.examples = const []});

  factory Word.fromJson(Map<String, dynamic> json) => Word(
    id: json['id'] as String, korean: json['korean'] as String,
    chinese: json['chinese'] as String?, romanization: json['romanization'] as String?,
    pronunciationAudioUrl: json['pronunciation_audio_url'] as String?,
    category: json['category'] as String?, subCategory: json['sub_category'] as String?,
    difficultyLevel: json['difficulty_level'] as int? ?? 1,
    examples: (json['examples'] as List<dynamic>?)?.map((e) => WordExample.fromJson(e)).toList() ?? [],
  );
}

class WordExample {
  final String koreanSentence;
  final String? chineseTranslation, sourceType, sourceName;

  WordExample({required this.koreanSentence, this.chineseTranslation, this.sourceType, this.sourceName});
  factory WordExample.fromJson(Map<String, dynamic> json) => WordExample(
    koreanSentence: json['korean_sentence'] as String,
    chineseTranslation: json['chinese_translation'] as String?,
    sourceType: json['source_type'] as String?,
    sourceName: json['source_name'] as String?,
  );
}
