<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/explorer">Explorer</router-link>
    </div>
    <router-view/>
  </div>
</template>

<script>
import Vue from 'vue'
import Buefy from 'buefy'
import VueRouter from 'vue-router'
import 'buefy/dist/buefy.css'
Vue.use(Buefy)
Vue.use(VueRouter)

export default {
  name: 'App', 
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
