import { createStore } from 'vuex';
import { jwtDecode } from 'jwt-decode';
import apiClient from '@/api';

export default createStore({
  state: {
    accessToken: '',
    userRole: null,
    user_id: null,
    sessionExpiration: null,
    mail: null,
  },
  mutations: {
    //Set all states in the store based on the token when user logs in
    setUserToken(state, token) {
      state.accessToken = token;
      localStorage.setItem('access_token', token);
      const decoded = jwtDecode(token);
      state.userRole = decoded.role;
      state.user_id = decoded.user_id;
      state.sessionExpiration = decoded.exp;
      state.mail = decoded.mail;
    },
    // Clear the token from vuex store when user logs out
    clearUserToken(state) {
      state.accessToken = '';
      state.userRole = null;
      state.user_id = null;
      state.sessionExpiration = null;
      localStorage.removeItem('access_token');
    },
  },
  actions: {
    // Extend the token expiration time when activity is detected
    async extendTokenExp({ commit, state }) {
      try {
        const response = await apiClient.post('/refresh-token-interval', {
          mail: state.mail,
          role: state.userRole,
          user_id: state.user_id,
        });
        //Set the new token with extended time in the store
        commit('setUserToken', response.data.access_token);
      } catch (error) {
        console.error('Error refreshing token:', error);
      }
    },

    // Login action to set the token in the store
    login({ commit }, token) {
      commit('setUserToken', token);
    },

    // Logout action to clear the token from the store
    logout({ commit }) {
      commit('clearUserToken');
    },

    // Fetch the token data from local storage when user refreshes the page
    fetchTokenData({ commit }) {
      const token = localStorage.getItem('access_token');
      if (token) {
        commit('setUserToken', token);
      }
    }
  },

  // Getters to access the states in the store
  getters: {
    isAuthenticated: state => !!state.accessToken,
    userRole: state => state.userRole,
    sessionExp: state => state.sessionExpiration,
    user_id: state => state.user_id,
  }
});
