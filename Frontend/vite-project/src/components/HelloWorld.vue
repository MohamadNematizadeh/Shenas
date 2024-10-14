<script setup lang="ts">
</script>
<template>
  <div class="welcome-page">
    <h1>Welcome to the eKYC System</h1>
    <p>This is the user interface for uploading and verifying documents.</p>
    <button >شروع تشخیص چهره</button>
  </div>
</template>

<style scoped>
.welcome-page {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  text-align: center;
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 15px 20px;
  border: none;
  cursor: pointer;
  font-size: 18px;
}

button:hover {
  background-color: #45a049;
}
</style>
