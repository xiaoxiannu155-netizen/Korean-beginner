import 'package:just_audio/just_audio.dart';

class AudioService {
  final _player = AudioPlayer();

  Future<void> play(String url, {double speed = 1.0}) async {
    try {
      await _player.setUrl(url);
      await _player.setSpeed(speed);
      await _player.play();
    } catch (_) {}
  }

  Future<void> playSlow(String url) => play(url, speed: 0.5);
  Future<void> pause() => _player.pause();
  Future<void> stop() => _player.stop();
  void dispose() => _player.dispose();
}
