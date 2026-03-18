<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSearchStore } from '../stores/search'
import { marked } from 'marked'

const route = useRoute()
const router = useRouter()
const searchStore = useSearchStore()
const localQuery = ref((route.query.q as string) || '')

const triggerSearch = () => {
  if (localQuery.value.trim()) {
    router.replace({ query: { q: localQuery.value } })
    searchStore.performSearch(localQuery.value)
  }
}

const renderSnippet = (text: string | null) => {
  if (!text) return ''
  const cleaned = text.replace(/\[!\[.*?\]\(.*?\)\]\(.*?\)/g, '').replace(/!\[.*?\]\(.*?\)/g, '')
  return marked.parse(cleaned) as string
}

onMounted(() => {
  if (localQuery.value) searchStore.performSearch(localQuery.value)
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
        <button
          type="submit"
          class="absolute right-2.5 top-1/2 -translate-y-1/2 bg-none border-none text-white cursor-pointer"
        >
          🔍
        </button>
      </form>
    </div>

    <main class="max-w-3xl mx-auto px-5">
      <div class="flex justify-between items-center mb-5 text-sm">
        <div class="flex items-center gap-2">
          <span>⇃ Sort by: </span>
          <select
            v-model="searchStore.sortBy"
            class="bg-transparent text-white border-none outline-none cursor-pointer"
            style="background-color: #111827"
          >
            <option value="relevance" style="background-color: #111827; color: white">Relevance</option>
            <option value="stars" style="background-color: #111827; color: white">Stars</option>
          </select>
        </div>
        <div class="text-xs text-gray-400">{{ searchStore.totalResults }} results</div>
        <div v-if="searchStore.results.length > 0" class="text-xs text-gray-500 mt-1">
          {{ searchStore.queryTime.toPrecision(1) }}ms
        </div>
      </div>

      <div v-if="searchStore.isSearchLoading" class="space-y-0">
        <div
          v-for="i in 5"
          :key="i"
          class="border-t-2 border-b-2 border-gray-500 py-5 -mb-0.5 animate-pulse"
        >
          <div class="h-6 bg-gray-700 w-1/3 mb-2"></div>
          <div class="h-4 bg-gray-700 w-1/4 mb-3"></div>
          <div class="h-3 bg-gray-700 w-full mb-1"></div>
          <div class="h-3 bg-gray-700 w-5/6"></div>
        </div>
      </div>

      <div v-else-if="searchStore.results.length === 0" class="text-center py-8 text-gray-500">
        No results found for "{{ searchStore.query }}"
      </div>

      <div v-else-if="searchStore.error" class="text-center py-8 text-red-400">
        {{ searchStore.error }}
      </div>

      <div v-else class="space-y-0">
        <div
          v-for="(repo, index) in searchStore.sortedResults"
          :key="repo.repo_name"
          class="border-t-2 border-b-2 border-gray-500 py-5 -mb-0.5"
        >
          <div class="flex justify-between items-baseline mb-1.25">
            <a
              :href="`https://github.com/${repo.repo_name}`"
              target="_blank"
              class="text-xl font-medium transition-colors"
            >
              <span class="text-gray-400">{{ repo.owner }}</span>
              <span class="text-gray-500">/</span>
              <span class="text-white">{{ repo.repo_name.split('/')[1] }}</span>
            </a>
            <span class="text-xs text-gray-600">#{{ index + 1 }}</span>
          </div>

          <div class="flex gap-3.75 text-gray-400 text-sm mb-3.75 mt-2">
            <span
              >{{ repo.stars >= 1000 ? (repo.stars / 1000).toFixed(1) + 'k' : repo.stars }} ☆</span
            >
            <span
              v-if="repo.license"
              class="text-xs border border-gray-600 px-1.5 py-0.5 text-gray-400"
            >
              {{ repo.license }}
            </span>
          </div>

          <p
            v-if="repo.readme_snippet"
            class="text-gray-300 text-xs leading-relaxed m-0 mb-3.75 max-w-11/12 prose prose-invert prose-xs"
            v-html="renderSnippet(repo.readme_snippet)"
          />
        </div>
      </div>
    </main>
  </div>
</template>
