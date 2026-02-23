<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSearchStore } from '../stores/search'

const route = useRoute()
const router = useRouter()
const searchStore = useSearchStore()

const localQuery = ref((route.query.q as string) || '')
const sortBy = ref('stars')

const triggerSearch = () => {
  if (localQuery.value.trim()) {
    router.replace({ query: { q: localQuery.value } })
    searchStore.performSearch(localQuery.value, sortBy.value)
  }
}

watch(sortBy, () => {
  searchStore.performSearch(localQuery.value, sortBy.value)
})

onMounted(() => {
  if (localQuery.value) {
    searchStore.performSearch(localQuery.value, sortBy.value)
  }
})
</script>

<template>
  <div class="pb-12">
    <header class="border-b border-gray-700 px-5 py-2.5 text-gray-500">
      <div>~ ~ ~ ~ ~</div>
    </header>

    <div class="flex flex-col items-center gap-5 my-7.5">
      <div class="flex items-center gap-2.5 cursor-pointer" @click="router.push('/')">
        <h2 class="text-3xl font-light m-0">SEARCHME</h2>
      </div>
      
      <form @submit.prevent="triggerSearch" class="w-full max-w-md relative">
        <input 
          v-model="localQuery" 
          type="text" 
          class="w-full px-3.75 py-2.5 bg-transparent border-2 transition-all focus:border-blue-500 border-white text-white outline-none"
        />
        <button type="submit" class="absolute right-2.5 top-1/2 -translate-y-1/2 bg-none border-none text-white cursor-pointer">🔍</button>
      </form>
    </div>

    <main class="max-w-3xl mx-auto px-5">
      <div class="flex justify-between items-center mb-5 text-sm">
        <div class="flex items-center gap-2">
          <span>⇃ sort by: </span>
          <select v-model="sortBy" class="bg-transparent text-white border-none outline-none cursor-pointer">
            <option value="stars">stars</option>
            <option value="forks">forks</option>
            <option value="updated">recently updated</option>
          </select>
        </div>
        <div class="text-xs text-gray-400">{{ searchStore.totalResults }} results</div>
      </div>

      <div v-if="searchStore.isSearchLoading" class="text-center py-8">Loading...</div>

      <div v-else class="space-y-0">
        <div 
          v-for="repo in searchStore.results" 
          :key="repo.id" 
          class="border-t-2 border-b-2 border-gray-500 py-5 -mb-0.5"
        >
          <div class="flex justify-between items-baseline mb-1.25">
            <h3 class="text-xl font-medium m-0">
              <span>⑂</span> {{ repo.repo_name }}
            </h3>
            <span class="text-xs text-gray-500">last updated: {{ repo.last_updated }}</span>
          </div>
          
          <div class="text-gray-400 text-sm mb-2">👤 {{ repo.owner }}</div>
          
          <div class="flex gap-3.75 text-gray-400 text-sm mb-3.75">
            <span>☆ {{ repo.stars }}</span>
            <span>⑂ {{ repo.forks }}</span>
          </div>
          
          <p class="text-gray-300 text-xs leading-relaxed m-0 mb-3.75 max-w-11/12">{{ repo.description }}</p>
          
          <div class="text-right text-gray-500 text-xl cursor-pointer">≡</div>
        </div>
      </div>
    </main>
  </div>
</template>
