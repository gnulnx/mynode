<template>
  <div class="home">
    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
    <!-- <Home msg="Welcome to Your Vue.js App"/> -->
    <div class="columns">
        <div class="column is-1"></div>
        <div class="column page-title">
            <h1 class="title">Node Info</h1>
        </div>
        <div class="column is-1"></div>
    </div>

    
    <div v-if="info">
        <div class="columns">
            <div class="column is-1"></div>

            <!-- BlockChain Section --> 
            <div class="column is-6 panel">
                <div class="columns">
                    <div class="column header"><strong>Block Chain</strong></div>
                </div> 
                <div class="columns">
                    <div class="column">Chain</div>
                    <div class="column">{{info.blockchain.chain}}</div>
                </div>
                <div class="columns">
                    <div class="column">Block Height</div>
                    <div class="column">{{info.blockchain.blocks}}</div>
                </div>
                <div class="columns">
                    <div class="column">Pruned</div>
                    <div class="column">{{info.blockchain.pruned}}</div>
                </div>
                <div class="columns">
                    <div class="column">Last Block Time</div>
                    <div class="column">{{get_date(info.blockchain.mediantime)}}</div>
                </div>
            </div>

            <!-- Network Section --> 
            <div class="column panel">
                <div class="columns">
                    <div class="column header"><strong>Network</strong></div>
                </div> 
                <div class="columns">
                    <div class="column">Version</div>
                    <div class="column">{{info.network.subversion}}</div>
                </div>
                <div class="columns">
                    <div class="column">Connections</div>
                    <div class="column">{{info.network.connections}}</div>
                </div>
            </div>
            <div class="column is-1"></div> 
        </div>
 
        <div class="columns">
            <div class="column is-1"></div>
            <!-- Memory Section --> 
            <!-- <div class="column panel">
                <div class="columns">
                    <div class="column header"><strong>Memory</strong></div>
                </div> 
                <div class="columns">
                    <div class="column">Usage</div>
                    <div class="column">{{info.memory.locked.used}}</div>
                </div>
            </div> -->

            <!-- mempool Section --> 
            <div class="column panel is-5">
                <div class="columns">
                    <div class="column header"><strong>Mempool</strong></div>
                </div> 
                <div class="columns">
                    <div class="column">Memory Usage</div>
                    <div class="column">{{bytes_to_mb(info.mempool.usage)}}</div>
                </div>
                <div class="columns">
                    <div class="column">Current # of Txn's</div>
                    <div class="column">{{info.mempool.size}}</div>
                </div>
                <div class="columns">
                    <div class="column">Memory Used</div>
                    <div class="column">{{bytes_to_mb(info.mempool.bytes)}}</div>
                </div>
            </div>

            <!-- Softforks Section  -->
            <div class="column panel is-5">
                <div class="columns">
                    <div class="column header"><strong>Soft Forks</strong></div>
                </div> 
                <div class="columns">
                    <div class="column"><strong>Name</strong></div>
                    <div class="column"><strong>Block</strong></div>
                    <div class="column"><strong>Type</strong></div>
                    <div class="column"><strong>Active</strong></div>
                </div>
                <div class="columns" v-for="(item, key, index) in info.blockchain.softforks" :key="index">
                    <div class="column">{{key}}</div>
                    <div class="column">{{item.height}}</div>
                    <div class="column">{{item.type}}</div>
                    <div class="column">{{item.active}}</div>
                </div>
            </div>

            <div class="column is-1"></div> 
        </div> 


        <!-- <div class="columns">
            <div class="column is-1"></div>
            <div class="column panel">
                <div class="columns">
                    <div class="column header"><strong>Soft Forks</strong></div>
                </div> 
                <div class="columns">
                    <div class="column"><strong>Name</strong></div>
                    <div class="column"><strong>Block</strong></div>
                    <div class="column"><strong>Type</strong></div>
                    <div class="column"><strong>Active</strong></div>
                </div>
                <div class="columns" v-for="(item, key, index) in info.blockchain.softforks" :key="index">
                    <div class="column">{{key}}</div>
                    <div class="column">{{item.height}}</div>
                    <div class="column">{{item.type}}</div>
                    <div class="column">{{item.active}}</div>
                </div>
            </div>
            <div class="column is-1"></div>
        </div> -->
        <!-- Uncomment if you need to see the full data dump on screen -->
        <!-- <div>{{info}}</div> -->
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Home',
    data () {
        return {
            info: ''
        }
    },
    methods: {
        bytes_to_mb: function(q) {
            return (parseInt(q)/1000000).toString() +" MB"
        },

        get_date: function(ts) {
            var date = new Date(ts * 1000);
            console.log(date)
            return date
        }
    },
    mounted() {
        var self = this
        axios
            .get("/api/info")
            .then(resp => self.info = resp.data)
            .catch(err => console.log(err))

        setInterval(function() {
            axios
                .get("/api/info")
                .then(resp => self.info = resp.data)
                .catch(err => console.log(err))
        }, 15000)
    }
}
</script>

<style lang="scss" scoped>

strong {
    font-size: 24px;
}
.panel {
    border: 1px solid rgb(215, 213, 213);
    border-radius: 5px;
    margin: 5px 5px 10px 5px
}
.title {
    margin-top: 25px;
    margin-bottom: 25px;
}
.header {
    background-color:  #42b983;
}
.page-title {
    // padding: 2px 2px 2px 2px;
    // border-radius: 5px;
    // font-size: 36px;
    // background-color: rgb(234, 234, 234)
}
</style>