import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface RepoResult {
  repo_name: string
  owner: string
  stars: number
  license: string | null
  readme_snippet: string | null
}

const error = ref<string | null>(null)

export const useSearchStore = defineStore('search', () => {
  const query = ref('')
  const results = ref<RepoResult[]>([])
  const totalResults = ref(0)
  const isSearchLoading = ref(false)
  const sortBy = ref('relevance')
  const queryTime = ref(0)

  const sortedResults = computed(() => {
    const r = [...results.value]
    if (sortBy.value === 'stars') return r.sort((a, b) => b.stars - a.stars)
    return r
  })

  async function performSearch(searchQuery: string) {
    if (!searchQuery) return
    isSearchLoading.value = true
    error.value = null
    query.value = searchQuery
    try {
      const apiUrl =
        import.meta.env.VITE_API_URL ||
        'https://searchme-api-217336954570.us-central1.run.app/api/search'
      const response = await fetch(`${apiUrl}?q=${encodeURIComponent(searchQuery)}`)
      const data = await response.json()
      results.value = data.results
      totalResults.value = data.total_results
      queryTime.value = data.query_time
    } catch (e) {
      error.value = 'Something went wrong. Please try again.'
      results.value = []
      totalResults.value = 0
    } finally {
      isSearchLoading.value = false
    }
  }

  return {
    query,
    results,
    sortedResults,
    totalResults,
    isSearchLoading,
    sortBy,
    error,
    performSearch,
    queryTime,
  }
})
