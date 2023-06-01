<template>
    <div id="building">
  <transition name="transitionRouter">
    <router-view></router-view>
  </transition>
    </div>
</template>

<script>

export default {
  // name: 'app',
  // components: {
  //   Login,
  //   // HelloWorld
  // }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}
body{
  margin:0;
  padding:0;
  border:0
}
#building {
  background: url("~@/assets/background.jpg");
  width: 100%;
  height: 100%;
  position: fixed;
  background-size: cover;
  background-position: 0px -70px;
}
</style>
