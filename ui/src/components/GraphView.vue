<template>
    <h1>Miejsce na Twój {{ appName }}</h1>
</template>

<script>
export default {
  props: {
    appName: String
  }
}
</script>

<style scoped>
h1 {
  margin: 40px 0 0;
}
</style>
