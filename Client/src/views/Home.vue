<template>
  <div class="home">
    <Settings />
  </div>
</template>

<script>
// @ is an alias to /src
import Settings from "@/components/Settings.vue";

export default {
  name: "Home",
  components: {
    Settings,
  },
};
</script>
