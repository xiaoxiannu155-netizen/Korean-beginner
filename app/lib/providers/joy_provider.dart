import 'package:flutter_riverpod/flutter_riverpod.dart';

enum JoyState { idle, sleeping, active }

enum JoyPersonality { gentle, lively, strict, humorous }

enum JoyDisplayMode { always, autoHide, hidden }

class JoyConfig {
  String name;
  String gender;
  JoyPersonality personality;
  JoyDisplayMode displayMode;

  JoyConfig({
    this.name = 'Joy',
    this.gender = 'female',
    this.personality = JoyPersonality.gentle,
    this.displayMode = JoyDisplayMode.autoHide,
  });
}

class JoyNotifier extends StateNotifier<JoyState> {
  JoyConfig config;

  JoyNotifier() : config = JoyConfig(), super(JoyState.idle);

  void wakeUp() {
    if (state == JoyState.sleeping) {
      state = JoyState.active;
    }
  }

  void goToSleep() {
    if (config.displayMode == JoyDisplayMode.autoHide && state == JoyState.idle) {
      state = JoyState.sleeping;
    }
  }

  void activate() => state = JoyState.active;
  void deactivate() => state = JoyState.idle;

  void updateConfig(JoyConfig newConfig) {
    config = newConfig;
    if (config.displayMode == JoyDisplayMode.hidden) {
      state = JoyState.sleeping;
    }
  }
}

final joyProvider = StateNotifierProvider<JoyNotifier, JoyState>((ref) => JoyNotifier());
