<template>
    <div v-if="address">
        <div class="columns is-flex is-horz-center"> 
            <div class="column">
                <h1 class="title is-flex is-horz-center">Address</h1>
            </div>
        </div>
       <div class="columns is-flex is-horz-center"> 
           <div class="column is-3 is-flex is-horz-center">
                <img class="qr" :src="address.qr">
            </div>

            <div class="column is-3">
                <div class="columns bot-brd ">
                    <div class="column is-3">Address</div>
                    <div class="column">{{address.address}}</div>
                </div>
                <div class="columns bot-brd ">
                    <div class="column is-3">Balance</div>
                    <div class="column">{{address.total}}</div>
                </div>
                <div class="columns bot-brd ">
                    <div class="column is-3">Transactions</div>
                    <div v-if="address" class="column">{{address.utxos.length}}</div>
                </div>
            </div>
            <div class="column is-4"></div>

        </div> 

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
                                <a :href='utxo.txnid'>{{utxo.txnid}}</a>
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
                <!-- <pre v-if="address">{{ JSON.stringify(address,undefined,2) }}</pre>  -->
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
    </div>
</template>

<script>
export default {
    name: "Address",
    props: ["address"],
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
</style>
