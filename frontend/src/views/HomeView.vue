<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const searchInput = ref('')

const submitSearch = () => {
  if (searchInput.value.trim()) {
    router.push({ name: 'results', query: { q: searchInput.value.trim() } })
  }
}
</script>

<template>
  <div class="flex flex-col items-center justify-center min-h-[70vh]">
    <div class="flex items-center gap-4 mb-8">
      <h1 class="text-6xl tracking-wider font-light">SEARCHME</h1>
    </div>

    <form @submit.prevent="submitSearch" class="w-full max-w-2xl">
      <div class="relative">
        <input 
          v-model="searchInput" 
          type="text" 
          placeholder="Search repositories..." 
          class="w-full px-5 py-4 pr-16 bg-transparent border-2 transition-all focus:border-blue-500 border-white text-white text-lg outline-none"
        />
        <button 
          type="submit" 
          class="absolute right-4 top-1/2 -translate-y-1/2 bg-none border-none text-white text-xl cursor-pointer"
        >
          🔍
        </button>
      </div>
    </form>
  </div>
</template>
