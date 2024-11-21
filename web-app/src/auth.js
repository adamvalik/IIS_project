import { createStore } from 'vuex';
import { jwtDecode } from 'jwt-decode';

export default createStore({
  state: {
    accessToken: localStorage.getItem('access_token') || '',
    userRole: null,
    user_id: null,
    sessionExpiration: null,
  },
  mutations: {
    setToken(state, token) {
      state.accessToken = token;
      localStorage.setItem('access_token', token);
      const decoded = jwtDecode(token);
      state.userRole = decoded.role;
      state.user_id = decoded.user_id;
      state.sessionExpiration = Math.floor(Date.now() / 1000) + 10 * 60;
    },
    clearToken(state) {
      state.accessToken = '';
      state.userRole = null;
      state.user_id = null;
      state.sessionExpiration = null;
      localStorage.removeItem('access_token');
    },
    setNewSessionExp(state) {
      state.sessionExpiration = Math.floor(Date.now() / 1000) + 10 * 60;
    },
  },
  actions: {
    login({ commit }, token) {
      commit('setToken', token);
    },
    logout({ commit }) {
      commit('clearToken');
    },
    extendExpiration({ commit }) {
      commit('setNewSessionExp');
    },
    fetchTokenData({ commit }) {
      const token = localStorage.getItem('access_token');
      if (token) {
        commit('setToken', token);
      }
    }
  },
  getters: {
    isAuthenticated: state => !!state.accessToken,
    userRole: state => state.userRole,
    tokenExp: state => state.tokenExpiration,
    sessionExp: state => state.sessionExpiration,
    user_id: state => state.user_id
  }
});
