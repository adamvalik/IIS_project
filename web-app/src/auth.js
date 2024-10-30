import { createStore } from 'vuex';
import { jwtDecode } from 'jwt-decode';

export default createStore({
  state: {
    accessToken: localStorage.getItem('access_token') || '',
    userRole: localStorage.getItem('access_token') ? jwtDecode(localStorage.getItem('access_token')).role : null,
  },
  mutations: {
    setToken(state, token) {
      state.accessToken = token;
      localStorage.setItem('access_token', token);
      const decoded = jwtDecode(token);
      state.userRole = decoded.role;
    },
    clearToken(state) {
      state.accessToken = '';
      state.userRole = null;
      localStorage.removeItem('access_token');
    }
  },
  actions: {
    login({ commit }, token) {
      commit('setToken', token);
    },
    logout({ commit }) {
      commit('clearToken');
    }
  },
  getters: {
    isAuthenticated: state => !!state.accessToken,
    userRole: state => state.userRole,
  }
});
