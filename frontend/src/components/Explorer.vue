<template>
  <div id="explorer">
        <!-- <Header v-on:submit-query="get_address" :qp="q" /> -->
        <div class="columns">
            <div class="column"></div>
            <div class="column"><h1 class="title">Block Explorer</h1></div>
            <div class="column"></div>
        </div> 
        <div class="columns">
            <div class="column"></div>
            <div class="column is-three-quarters">
                <input class="input" size=50 placeholder="address or transaction" v-model="q" @change="get_data(q)" />
            </div>
            <div class="column">
                <a class="button is-primary" v-on:click="get_data(q)">Submit</a>
            </div>
            <div class="column"></div>
        </div>
        <Address v-if="this.$store.state.address" :address="this.$store.state.address" />
        <Home v-if="home" :data="home" />
        <Transaction v-if="txn" :txn="txn" />
  </div>
</template>

 <script>
import axios from 'axios'
// import Header from './Header.vue'
import Address from './Address.vue'
import Home from './Home.vue'
import Transaction from './Transaction.vue'

export default {
    name: 'Explorer',
    components: {
    // Header,
    Address,
    Transaction,
    Home
    },
    data() {
        return {
            q: '',
            address: '',
            txn: '',
            home: '',
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
            var self = this;
            axios
                .get(`/api/?q=${q}`)
                .then(resp => self.address = resp.data)

            console.log(this.address)
        },
        get_data: function(q) {
            var self = this;
            axios
                .get(`/api/?q=${q}`)
                .then(resp => {
                    console.log("RETURNED")
                    console.log(JSON.stringify(resp.data, null, 2))
                    if (resp.data.data_type == 'address') {
                        self.$store.commit("address", resp.data)
                        // self.address = resp.data
                    } else if (resp.data.data_type == 'txn') {
                        self.$store.commit("txn", resp.data)
                        self.txn = resp.data
                        console.log(JSON.stringify(self.txn, null, 2))
                    }
                })
        }
    }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.button {
    background-color: #42b983
}
.qr {
    width: 50%;
    height: auto;
}
.column {
    /* border-style: solid; */
}
.bot-brd {
    border-bottom: 1px solid grey;
}
.is-horz-center {
    justify-content: center;
}
.vert-space {
    margin-top: 50px;
}
.utxo {
    background-color:rgb(245, 246, 246);
    margin-top:10px;
    margin-bottom: 10px;
    padding: 5px 5px 5px 5px;
    border-radius: 5px;
}
#explorer {
    /* margin-top: 10px; */
}
</style>
