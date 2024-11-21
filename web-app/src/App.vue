<template>
  <div @mousemove="resetTimer" @keypress="resetTimer">
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
    this.fetchTokenData();
    this.checkExpiredToken();

    this.tokenInterval = setInterval(() => {
      this.checkExpiredToken();
    }, 60000);
  },
  methods: {
    ...mapActions(['logout', 'extendExpiration', 'fetchTokenData', 'extendTokenExp']),

    resetTimer() {
      this.ActivityDetected = true;
    },
    checkExpiredToken() {

      if(this.isAuthenticated){
        if(this.ActivityDetected) {
          console.log("Extending token expiration...");
          console.log(this.sessionExp * 1000);
          this.extendTokenExp();
          this.ActivityDetected = false;
      } 
        if((Date.now() >= this.sessionExp * 1000)) {
          alert("Your session has expired. Please log in again.");
          this.logout();
          this.$router.push('/');
        }

      }

        // if(this.isTokenExpired) {
        //   alert("Your session has expired. Please log in again.");
        //   this.logout();
        //   this.$router.push('/');
        // }

        // console.log("Checking token expiration...");
        // console.log(Date.now() + " >= " + this.sessionExp * 1000);

        // if((Date.now() >= this.sessionExp * 1000)) {
        //   alert("Your session has expired. Please log in again.");
        //   this.logout();
        //   this.$router.push('/');
        // }
      //}
    }

  },
  beforeUnmount() {
    clearInterval(this.tokenInterval);
  },
}
</script>
