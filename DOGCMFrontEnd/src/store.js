import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);


export default new Vuex.Store({
    state: {
        userName: '',
       // email:'',
        token: '',
        group: -1,
        passwd:'',
        pswMD5: '',
        pushAddr: ''
    },
    mutations: {

    },
    actions: {

    }
})
