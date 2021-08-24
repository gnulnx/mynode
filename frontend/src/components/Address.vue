<template>
    <div v-if="address">
        <div class="columns is-flex is-horz-center"> 
            <div class="column">
                <h1 class="title is-flex is-horz-center">Address</h1>
            </div>
        </div>
       <div class="columns is-flex is-horz-center"> 
           <div class="column is-3 is-flex is-horz-center">
                <img class="qr" :src="address.qrcode">
            </div>

            <div class="column is-5">
                <ul>
                    <li>
                        <div class="columns">
                            <div class="column left">Address</div>
                            <div class="column left">{{address.address}}</div>
                        </div>
                    </li>
                     <li>
                        <div class="columns">
                            <div class="column left">Total Transactions</div>
                            <div class="column left">{{address.inputs.length}}</div>
                        </div>
                    </li>
                    <!-- <li>
                        <div class="columns">
                            <div class="column">Spend</div>
                            <div class="column">{{address.outputs.length}}</div>
                        </div>
                    </li> -->
                </ul>
                
            </div>
            <div class="column is-4"></div>

        </div> 

        <div class="columns">
            <div class="column"></div>
            
            <div class="column is-horz-center bot-brd">
            </div>
            <div class="column"></div>
        </div>
        <!-- <div class="vert-space"></div>
        <div class="columns">
            <div class="column"></div> 
            <div class="column is-horz-center bot-brd">
                <h1 class="title">UTXO's</h1>
                <br>
                <ul id='utxo-list'>
                    <li v-for="utxo in address.utxos" :key="utxo.txnid">
                        <div class="utxo bot-brd">
                            <div class="columns">
                                <div class="column">Tx</div>
                                <div class="column">
                                <a :href="utxo.txnid">{{utxo.txnid}}</a>
                                </div>
                            </div>
                            <div class="columns">
                                <div class="column">outnum</div>
                                <div class="column">{{utxo.outnum}}</div>
                            </div>
                            <div class="columns">
                                <div class="column">cionbase</div>
                                <div class="column">{{utxo.coinbase}}</div>
                            </div>
                            <div class="columns">
                                <div class="column">amount</div>
                                <div class="column">{{utxo.amount}}</div>
                            </div>
                            <div class="columns">
                                <div class="column">type</div>
                                <div class="column">{{utxo.type}}</div>
                            </div>
                        </div>
                    </li>
                </ul>
            </div>
            <div class="column"></div> 
        </div> -->

        <div class="columns">
            <div class="column"></div> 
            <div class="column is-10 is-horz-center bot-brd">
                <h1 class="title">Transactions ({{address.inputs.length}})</h1>
                <TransactionPanel v-for="txid in address.inputs" :key="txid" :txid="txid" v-on:fetch="$emit('fetch')" />
            </div>
            <div class="column"></div> 
        </div>

    </div>
</template>

<script>
import TransactionPanel from "./TransactionPanel.vue"
export default {
    name: "Address",
    props: ["address"],
    components: {
        TransactionPanel
    },
    mounted() {
        console.log("Created new address")
        console.log(this.address)
    }
}
</script>

<style lang="scss" scoped>
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
.qr {
    width: 50%;
    height: auto;
}
.left {
    text-align: left;;
}
.right {
    text-align: right;;
}
</style>
