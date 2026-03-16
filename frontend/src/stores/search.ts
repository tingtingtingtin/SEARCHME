import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface RepoResult {
  repo_name: string
  owner: string
  stars: number
  license: string | null
}

export const useSearchStore = defineStore('search', () => {
  const query = ref('')
  const results = ref<RepoResult[]>([])
  const totalResults = ref(0)
  const isSearchLoading = ref(false)

  async function performSearch(searchQuery: string, sortBy: string = 'stars') {
    if (!searchQuery) return

    isSearchLoading.value = true
    query.value = searchQuery

    try {
      const response = await fetch(`https://searchme-api-217336954570.us-central1.run.app/api/search?q=${encodeURIComponent(searchQuery)}&sort=${sortBy}`)
      const data = await response.json()

      results.value = data.results
      totalResults.value = data.total_results
    } catch (error) {
      console.error("Failed to fetch search results:", error)
    } finally {
      isSearchLoading.value = false
    }
  }

  return { query, results, totalResults, isSearchLoading, performSearch }
})