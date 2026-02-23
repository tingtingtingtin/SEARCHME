import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface RepoResult {
  id: string
  repo_name: string
  owner: string
  stars: number
  forks: number
  last_updated: string
  description: string
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
      const response = await fetch(`http://localhost:8000/api/search?q=${encodeURIComponent(searchQuery)}&sort=${sortBy}`)
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