import { createStore } from 'vuex';
import { jwtDecode } from 'jwt-decode';

export default createStore({
  state: {
    accessToken: localStorage.getItem('access_token') || '',
    userRole: null,
    user_id: null,
    sessionExpiration: null,
    tokenExpiration: null,
  },
  mutations: {
    setToken(state, token) {
      state.accessToken = token;
      localStorage.setItem('access_token', token);
      const decoded = jwtDecode(token);
      state.userRole = decoded.role;
      state.user_id = decoded.user_id
      state.sessionExpiration = decoded.exp;
      state.tokenExpiration = 1800;
      state.sessionExpiration = Math.floor(Date.now() / 1000) + state.tokenExpiration; // * 60;
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
      state.sessionExpiration = Math.floor(Date.now() / 1000) + state.tokenExpiration; // * 60;
    },
  },
  actions: {
    // async extendTokenExp({ commit }) {
    //   try {
    //     const response = await apiClient.post('/refresh-token-interval', {
    //       sub: this.state.user_id,
    //       role: this.state.userRole,
    //       user_id: this.state.user_id,
    //       tokenExp: this.state.tokenExpiration,
    //     });
    //     commit('setToken', response.data.updated_token);
    //   } catch (error) {
    //     console.error('Error refreshing token:', error.response.data.detail);
    //     console.error('Status code:', error.response.status);
    //   }
    // },
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
