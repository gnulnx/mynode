<template>
<b-navbar>
        <template #brand>
            <b-navbar-item>
                <h1 class="title">Node</h1>
            </b-navbar-item>
        </template>
        <template #start>
            <b-navbar-item>
                <router-link to="/">Home</router-link>
                <!-- <b-navbar-item href="#">Home</b-navbar-item> -->
            <b-navbar-item>
                <!-- Exploror -->
                <div class="column">
                         <router-link to="/explorer">Explorer</router-link>
                        <!-- <a>Exploror</a> -->
                    </div>
                    <!-- <div class="column is-three-quarters">
                        <input class="input" size=50 placeholder="address or transaction" v-model="q" @change="$emit('submit-query', q)" />
                    </div>
                    <div class="column">
                        <a class="button is-primary" v-on:click="$emit('submit-query', q)">Submit</a>
                    </div> -->
            </b-navbar-item>
                <!-- <div class="columns">
                    <div class="column">
                        <a>Exploror</a>
                    </div>
                    <div class="column is-three-quarters">
                        <input class="input" size=50 placeholder="address or transaction" v-model="q" @change="$emit('submit-query', q)" />
                    </div>
                    <div class="column">
                        <a class="button is-primary" v-on:click="$emit('submit-query', q)">Submit</a>
                    </div>
                </div> -->
            </b-navbar-item>
        </template>

        <!-- <template #end>
            <b-navbar-item tag="div">
                <div class="buttons">
                    <a class="button is-primary">
                        <strong>Sign up</strong>
                    </a>
                    <a class="button is-light">
                        Log in
                    </a>
                </div>
            </b-navbar-item>
        </template> -->
    </b-navbar>
</template>

<style lang="scss">
.title {
    font-family: "Leckerli One";
    font-size: 48px;
}
</style>

<script>
import { defineComponent } from '@vue/composition-api'

export default defineComponent({
    props: ['qp'],
    data() {
      return {
          q: '',
      }
    },
    watch: { 
        qp: function(newVal, oldVal) { // watch it
            this.q = newVal
            console.log('Prop changed: ', newVal, ' | was: ', oldVal)
        }
    },
    mounted() {
        console.log("Here in mounted")
        if (this.qp)
            this.q = this.qp
        this.window = window
    }
})
</script>
