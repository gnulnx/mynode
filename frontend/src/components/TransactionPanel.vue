<template>
    <div v-if="tx" class="txn_panel">
        <h1 class="title">{{txid}}</h1>
        <div v-if="tx">
            <pre>{{JSON.stringify(tx)}}</pre>
        </div>
    </div>
</template>

<script>
import { defineComponent } from '@vue/composition-api'
import axios from 'axios'

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
    margin-top: 10px;
    margin-bottom: 10px;
}
</style>
