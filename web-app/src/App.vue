<template>
  <div @mousemove="detectActivity" @keypress="detectActivity">
    <router-view />
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  data() {
    return {
      ActivityDetected: false,
    };
  },
  computed: {
    ...mapGetters(['sessionExp', 'isAuthenticated', 'isTokenExpired']),
  },
  mounted() {
    // Load token data to Vuex store
    this.fetchTokenData();

    // Check token expiration for the first time
    this.checkExpiredToken();

    // Check for token expiration every minute
    this.tokenInterval = setInterval(() => {
      this.checkExpiredToken();
    }, 60000);
  },
  methods: {
    ...mapActions(['logout', 'extendExpiration', 'fetchTokenData', 'extendTokenExp']),

    detectActivity() {
      this.ActivityDetected = true;
    },
    checkExpiredToken() {

      //If user is logged in
      if(this.isAuthenticated){
        //If activity was detected, extend token expiration
        if(this.ActivityDetected) {
          console.log("Extending token expiration...");
          console.log(this.sessionExp * 1000);
          this.extendTokenExp();
          this.ActivityDetected = false;
        } 
      
        //Check if token has expired
        if((Date.now() >= this.sessionExp * 1000)) {
          alert("Your session has expired. Please log in again.");
          this.logout();
          this.$router.push('/');
        }

      }
    }

  },
  beforeUnmount() {
    clearInterval(this.tokenInterval);
  },
}
</script>
