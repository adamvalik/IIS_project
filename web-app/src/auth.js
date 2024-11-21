import { createStore } from 'vuex';
import { jwtDecode } from 'jwt-decode';
import apiClient from '@/api';

export default createStore({
  state: {
    accessToken: localStorage.getItem('access_token') || '',
    userRole: null,
    user_id: null,
    sessionExpiration: null,
    sub: null,
  },
  mutations: {
    setToken(state, token) {
      state.accessToken = token;
      localStorage.setItem('access_token', token);
      const decoded = jwtDecode(token);
      state.userRole = decoded.role;
      state.user_id = decoded.user_id;
      state.sessionExpiration = decoded.exp;
      state.sub = decoded.sub;
    },
    clearToken(state) {
      state.accessToken = '';
      state.userRole = null;
      state.user_id = null;
      state.sessionExpiration = null;
      localStorage.removeItem('access_token');
    },
  },
  actions: {
    async extendTokenExp({ commit, state }) {
      try {
        const response = await apiClient.post('/refresh-token-interval', {
          sub: state.sub,
          role: state.userRole,
          user_id: state.user_id,
        });

        commit('setToken', response.data.access_token);
      } catch (error) {
        console.error('Error refreshing token:', error);
      }
    },
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
    sessionExp: state => state.sessionExpiration,
    user_id: state => state.user_id,
  }
});
