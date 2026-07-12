import 'package:flutter_test/flutter_test.dart';
import 'package:korean_app/providers/joy_provider.dart';

void main() {
  group('JoyNotifier', () {
    test('initial state is idle', () {
      final notifier = JoyNotifier();
      expect(notifier.state, JoyState.idle);
    });

    test('activate sets state to active', () {
      final notifier = JoyNotifier();
      notifier.activate();
      expect(notifier.state, JoyState.active);
    });

    test('deactivate returns to idle from active', () {
      final notifier = JoyNotifier();
      notifier.activate();
      notifier.deactivate();
      expect(notifier.state, JoyState.idle);
    });

    test('wakeUp from sleeping goes to active', () {
      final notifier = JoyNotifier();
      notifier.state = JoyState.sleeping;
      notifier.wakeUp();
      expect(notifier.state, JoyState.active);
    });

    test('goToSleep in autoHide mode transitions from idle', () {
      final notifier = JoyNotifier();
      notifier.config.displayMode = JoyDisplayMode.autoHide;
      notifier.state = JoyState.idle;
      notifier.goToSleep();
      expect(notifier.state, JoyState.sleeping);
    });

    test('goToSleep in always mode does NOT transition', () {
      final notifier = JoyNotifier();
      notifier.config.displayMode = JoyDisplayMode.always;
      notifier.state = JoyState.idle;
      notifier.goToSleep();
      expect(notifier.state, JoyState.idle);
    });

    test('hidden display mode sets state to sleeping', () {
      final notifier = JoyNotifier();
      notifier.updateConfig(JoyConfig(displayMode: JoyDisplayMode.hidden));
      expect(notifier.state, JoyState.sleeping);
    });

    test('default config values', () {
      final notifier = JoyNotifier();
      expect(notifier.config.name, 'Joy');
      expect(notifier.config.gender, 'female');
      expect(notifier.config.personality, JoyPersonality.gentle);
      expect(notifier.config.displayMode, JoyDisplayMode.autoHide);
    });

    test('updateConfig changes all settings', () {
      final notifier = JoyNotifier();
      notifier.updateConfig(JoyConfig(
        name: 'Coco', gender: 'male',
        personality: JoyPersonality.strict,
        displayMode: JoyDisplayMode.always,
      ));
      expect(notifier.config.name, 'Coco');
      expect(notifier.config.gender, 'male');
    });
  });
}
