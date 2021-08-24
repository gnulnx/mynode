<template>
    <div v-if="tx" class="txn_panel">
        <!-- <div class="container">Hello</div> -->
        <!-- header -->

        <div class="container">
            <div class="columns">
                <div class="column is-1"></div>
                <div class="column left">hash</div>
                <a class="column" @click="fetch()">{{txid}}</a>
                <div class="column right">date</div>
                <div class="column is-1"></div>
            </div>
        </div>

        <div class="columns">
            <div class="column"></div>
            <div class="column">
                <ul>
                    <li v-for="(txid, idx) in tx.inputs" :key="idx">
                        <div class="columns">
                            <div class="column left">{{txid.address}}</div>
                            <div class="column is-1 right">{{txid.value.toFixed(2)}}</div>
                        </div>
                    </li>
                </ul>
            </div>
            <div class="column"> => </div>

            <div class="column">
                <ul>
                    <li v-for="(txid, idx) in tx.outputs" :key="idx">
                        <div class="columns">
                            <div class="column left">{{txid.address}}</div>
                            <div class="column is-1 right">{{txid.value.toFixed(2)}}</div>
                        </div>
                    </li>
                </ul>
            </div>

            <div class="column"></div>
        </div>

        <!-- <h1 class="title">{{txid}}</h1> -->
        <!-- <div v-if="tx">
            <pre>{{JSON.stringify(tx)}}</pre>
        </div> -->
    </div>
</template>

<script>
import { defineComponent } from '@vue/composition-api'
import axios from 'axios'
import { EventBus } from '@/event-bus';

export default defineComponent({
    setup() {
        
    },
    props: ["txid"],
    data() {
        return {
            tx: null
        }
    },
    mounted() {
        var self = this;
        if (this.txid) {
            // Fetch transaction data for each panel
            axios
                .get(`/api/?q=${self.txid}`)
                .then(resp => {
                    self.tx= resp.data;
                    console.log(`Mounted with ${self.txid}`)
                })
                .catch(err => console.log(err))
        }
        // console.log(`Mounted with ${this.txid}`)
    },
    methods: {
        fetch() {
            EventBus.$emit('fetch', this.txid);
        }
    }
    // watch: { 
    //     txid: function(newVal, oldVal) { // watch it
    //         console.log('Prop changed: ', newVal, ' | was: ', oldVal)
    //     }
    // }
})
</script>

<style lang="scss" scoped>
.txn_panel {
    border: solid 1px black;
    border-radius: 5px;
    width: 100%;
    margin-top: 10px;
    margin-bottom: 10px;
}

.left {
    text-align: left;;
}
.right {
    text-align: right;;
}
.banner {
    background-color: rgb(208, 255, 204);
    border: solid 1px black;
    border-radius: 5px;
    width: 100%;
//     margin-top: 10px;
//     margin-bottom: 10px; 
}
.container {
    border: solid 1px black;
    padding-top: 10px;
    padding-bottom: 10px;
    background-color: rgb(208, 255, 204);
}
</style>
