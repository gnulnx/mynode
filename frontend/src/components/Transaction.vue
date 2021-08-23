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
            <div class="column is-3"></div>
            <div class="column">
                <span v-if="txn.coinbase" class="is-size-5">(Coinbase)</span>
            </div>
            <div class="column is-1"> => </div>
            <div class="column is-4">
                <ul>
                    <li v-for="v in txn.vout" :key="v.txid">
                        <div class="columns">
                            <div class="column is-9">{{v.scriptPubKey.addresses[0]}}</div> 
                            <div class="column is-3">{{v.value}}</div>
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
export default {
    name: "Transaction",
    props: ["txn"],
    mounted() {
        console.log("Transaction mounted")
    }
}
</script>
