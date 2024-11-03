import { createStore } from 'vuex';
import { jwtDecode } from 'jwt-decode';

export default createStore({
  state: {
    accessToken: localStorage.getItem('access_token') || '',
    userRole: localStorage.getItem('access_token') ? jwtDecode(localStorage.getItem('access_token')).role : null,
    sessionExpiration: localStorage.getItem('access_token') ? jwtDecode(localStorage.getItem('access_token')).exp : null,
    user_id: localStorage.getItem('access_token') ? jwtDecode(localStorage.getItem('access_token')).user_id : null,
    tokenExpiration: localStorage.getItem('access_token') ? jwtDecode(localStorage.getItem('access_token')).tokenExp : null,
  },
  mutations: {
    setToken(state, token) {
      state.accessToken = token;
      localStorage.setItem('access_token', token);
      const decoded = jwtDecode(token);
      state.userRole = decoded.role;
      state.user_id = decoded.user_id
      state.sessionExpiration = decoded.exp;
      state.tokenExpiration = decoded.tokenExp;
    },
    clearToken(state) {
      state.accessToken = '';
      state.userRole = null;
      state.user_id = null;
      state.sessionExpiration = null;
      state.tokenExpiration = null;
      localStorage.removeItem('access_token');
    },
    resetExpiration(state) {
      state.sessionExpiration = Math.floor(Date.now() / 1000) + state.tokenExpiration * 60;
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
      commit('resetExpiration');
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
