<template>
    <div>
        <div class="columns">
            <div class="column"></div> 
            <div class="column">
                <p class="is-size-1">Transaction</p>
            </div>
            <div class="column"></div>
        </div>

        <div v-if="txn.coinbase" class="columns">
            <div class="column is-1"></div>
            <div class="column">
                <span v-if="txn.coinbase" class="is-size-5">(Coinbase)</span>
            </div>
            <div class="column is-1"> => </div>
            <div class="column">
                <ul>
                    <li v-for="v in txn.outputs" :key="v.address">
                        <div class="columns">
                            <div class="column is-9">{{v.address}}</div> 
                            <div class="column is-3">{{v.value.toFixed(8)}}</div>
                        </div>
                    </li>
                </ul>
            </div>
            <div class="column is-3"></div>
        </div>

       <div v-if="!txn.coinbase" class="columns">
            <div class="column is-1"></div>
            <div class="column">
                <ul>
                    <li v-for="v in txn.inputs" :key="v.address">
                        <div class="columns">
                            <a class="column is-9" @click="bus.$emit('fetch', v.address)" >{{v.address}}</a> 
                            <div class="column is-3">{{v.value.toFixed(8)}}</div>
                        </div>
                    </li>
                </ul>
            </div>
            <div class="column is-1"> => </div>
            <div class="column">
                <ul>
                    <li v-for="v in txn.outputs" :key="v.address">
                        <div class="columns">
                            <a class="column is-9" @click="bus.$emit('fetch', v.address)" >{{v.address}}</a> 
                            <div class="column is-3">{{v.value.toFixed(8)}}</div>
                        </div>
                    </li>
                </ul>
            </div>
            <div class="column is-3"></div>
        </div> 
        <!-- <div v-if="txn.coinbase">
        <span v-if="txn.coinbase" class="is-size-5">(Coinbase)</span> -->
        
    </div>
</template>

<script>
import { EventBus } from '@/event-bus';
export default {
    name: "Transaction",
    props: ["txn"],
    data() {
        return {
            bus: EventBus
        }
    },
    mounted() {
        console.log("Transaction mounted")
    }
}
</script>
