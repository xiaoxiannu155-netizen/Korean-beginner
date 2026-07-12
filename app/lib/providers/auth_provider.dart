import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/user.dart';
import '../services/api_client.dart';
import '../services/auth_service.dart';

final apiClientProvider = Provider<ApiClient>((ref) => ApiClient());

final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier(ref.watch(apiClientProvider));
});

class AuthState {
  final bool isAuthenticated;
  final User? user;
  final UserProgress? progress;
  final bool isLoading;
  final String? error;

  const AuthState({
    this.isAuthenticated = false,
    this.user,
    this.progress,
    this.isLoading = false,
    this.error,
  });

  AuthState copyWith({
    bool? isAuthenticated,
    User? user,
    UserProgress? progress,
    bool? isLoading,
    String? error,
  }) {
    return AuthState(
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
      user: user ?? this.user,
      progress: progress ?? this.progress,
      isLoading: isLoading ?? this.isLoading,
      error: error,
    );
  }
}

class AuthNotifier extends StateNotifier<AuthState> {
  final ApiClient _client;
  late final AuthService _service;

  AuthNotifier(this._client) : super(const AuthState()) {
    _service = AuthService(_client);
  }

  Future<void> checkAuth() async {
    if (await _client.hasToken()) {
      try {
        await loadProfile();
      } catch (_) {
        await _client.clearTokens();
        state = const AuthState();
      }
    }
  }

  Future<void> register(String email, String username, String password) async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      await _service.register(email, username, password);
      await loadProfile();
    } catch (e) {
      state = state.copyWith(isLoading: false, error: '注册失败: ${e.toString()}');
    }
  }

  Future<void> login(String email, String password) async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      await _service.login(email, password);
      await loadProfile();
    } catch (e) {
      state = state.copyWith(isLoading: false, error: '登录失败: 邮箱或密码错误');
    }
  }

  Future<void> logout() async {
    await _service.logout();
    state = const AuthState();
  }

  Future<void> loadProfile() async {
    try {
      final userData = await _service.getProfile();
      final progressData = await _service.getProgress();
      state = AuthState(
        isAuthenticated: true,
        user: User.fromJson(userData),
        progress: UserProgress.fromJson(progressData),
      );
    } catch (e) {
      state = state.copyWith(isLoading: false, error: '加载用户信息失败');
    }
  }
}
