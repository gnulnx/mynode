<template>
  <div id="explorer">
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
        <Address v-if="address" :address="address" />
        <Home v-if="home" :data="home" />
        <Transaction v-if="txn" :txn="txn" />
  </div>
</template>

 <script>
//  import Vue from 'vue'
import axios from 'axios'
// import Header from './Header.vue'
import Address from './Address.vue'
import Home from './Home.vue'
import Transaction from './Transaction.vue'
import { EventBus } from '@/event-bus';



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

        EventBus.$on('fetch', (q) => {
            this.q = q;
            console.log("Fetch new data baby")
            this.get_data(q)
        });
    },
    methods: {
        get_data: function(q) {
            var self = this;
            // this.q = ''
            this.address = ''
            this.txn = ''
            this.home = ''
            axios
                .get(`/api/?q=${q}`)
                .then(resp => {
                    if (resp.data.data_type == 'address') {
                        self.address = resp.data
                        self.txn = null;
                        console.log("Address state has been saved")
                    } else if (resp.data.data_type == 'txn') {
                        self.txn = resp.data
                        self.address = null
                        console.log(JSON.stringify(self.txn, null, 2))
                    }
                })

            console.log("get_data")
            console.log(this.address)
            console.log(this.txn)
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
