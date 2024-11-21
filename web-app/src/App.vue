<template>
  <div @mousemove="resetTimer" @keypress="resetTimer">
    <router-view />
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['sessionExp', 'isAuthenticated']),
  },
  mounted() {
    this.fetchTokenData();
    this.checkExpiredToken();

    this.tokenInterval = setInterval(() => {
      this.checkExpiredToken();
    }, 1000);
  },
  methods: {
    ...mapActions(['logout', 'extendExpiration', 'fetchTokenData']),

    resetTimer() {
      if (this.isAuthenticated) {
        console.log(this.sessionExp);
        this.extendExpiration();
      }
    },
    checkExpiredToken() {

      if(this.isAuthenticated) {
        console.log("Checking token expiration...");
        console.log(Date.now() + " >= " + this.sessionExp * 1000);

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
