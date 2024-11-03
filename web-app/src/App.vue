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
    this.checkExpiredToken();

    this.tokenInterval = setInterval(() => {
      this.checkExpiredToken();
    }, 120000);
  },
  methods: {
    ...mapActions(['logout', 'extendExpiration']),

    resetTimer() {
      if (this.isAuthenticated) {
        this.extendExpiration();
      }
    },
    checkExpiredToken() {

      if(this.isAuthenticated) {
        console.log("Checking token expiration...");
        console.log(Date.now());
        console.log(this.sessionExp);

        if((Date.now() >= this.sessionExp * 1000)) {
          alert("Your session has expired. Please log in again.");
          this.logout();
        }
      }
    }

  },
  beforeUnmount() {
    clearInterval(this.tokenInterval);
  },
}
</script>
