<template>
  <div id="app">
      <!-- <Header v-on:submit-query="get_address" :qp="q" /> -->
    <!-- <Explorer v-if="exp" /> -->
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/explorer">Explorer</router-link>
    </div>
    <router-view/>
  </div>
</template>

<script>
import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import Buefy from 'buefy'
import VueRouter from 'vue-router'
// import Header from './components/Header.vue'
import 'buefy/dist/buefy.css'
Vue.use(Buefy)
Vue.use(VueRouter)
Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    address: '',
    txn: '',
  },
  mutations: {
    address (state, n) {
        state.txn = ''
        state.address = n
    },
    txn(state, n) {
        state.address = ''
        state.txn = n
    }
  }
})

export default {
  name: 'App',
  components: {
    //   Header
  },
  store: store,
  data() {
      return {
          exp: false,
          address: "",
          q: ""
      }
  },
  mounted() {
        console.log("Explorer.vue mounted")
        this.href = window.location.href
        var lastpart = this.href.substring(this.href.lastIndexOf('/') + 1)

        if (lastpart.length > 10) {
            this.q=lastpart
            this.get_data(lastpart)
        }
    },
  methods: {
    get_address: function(q) {
        // Example addresses
        // 1PaPFX6idr3zCfk3uCq8m1dWC8hZuoy6gg
        // 1NQ44Qv7ckBdup1kesYcP1kPTrFLaa98xU
        console.log(`App.get_address: ${store}`)
        var self = this;
        axios
            .get(`/api/?q=${q}`)
            .then(resp => self.address = resp.data)

        store.commit("address", this.address)
        console.log("store.state.address below")
        console.log(store.state.address)
    },
  }
}
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
  border-bottom: solid 1px rgb(188, 187, 187);
  margin-bottom: 15px;
}
</style>
