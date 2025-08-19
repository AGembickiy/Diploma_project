<template>
  <div class="card-list" :class="listClass">
    <div v-if="items.length === 0" class="empty-state">
      <div class="empty-icon">{{ emptyIcon }}</div>
      <h3 class="empty-title">{{ emptyTitle }}</h3>
      <p class="empty-description">
        {{ emptyDescription }}
      </p>
    </div>

    <div v-else class="list-container">
      <slot 
        v-for="(item, index) in sortedItems" 
        :key="getItemKey(item, index)"
        :item="item"
        :index="index"
      >
        <!-- Слот для карточки -->
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  items: any[]
  sortBy?: 'date-desc' | 'date-asc' | 'name' | 'none'
  sortField?: string
  emptyIcon?: string
  emptyTitle?: string
  emptyDescription?: string
  listClass?: string
}

const props = withDefaults(defineProps<Props>(), {
  sortBy: 'none',
  sortField: 'created_at',
  emptyIcon: '📝',
  emptyTitle: 'Нет элементов',
  emptyDescription: 'Пока нет элементов для отображения.',
  listClass: ''
})

const sortedItems = computed(() => {
  if (props.sortBy === 'none') {
    return props.items
  }

  const items = [...props.items]
  
  switch (props.sortBy) {
    case 'date-desc':
      return items.sort((a, b) => {
        const dateA = new Date(a[props.sortField]).getTime()
        const dateB = new Date(b[props.sortField]).getTime()
        return dateB - dateA
      })
    case 'date-asc':
      return items.sort((a, b) => {
        const dateA = new Date(a[props.sortField]).getTime()
        const dateB = new Date(b[props.sortField]).getTime()
        return dateA - dateB
      })
    case 'name':
      return items.sort((a, b) => {
        const nameA = a.name || a.title || a.authorName || ''
        const nameB = b.name || b.title || b.authorName || ''
        return nameA.localeCompare(nameB)
      })
    default:
      return items
  }
})

const getItemKey = (item: any, index: number): string | number => {
  return item.id || item.key || index
}
</script>

<style scoped>
.card-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
  overflow-y: auto;
  max-height: calc(100vh - 200px);
  padding-right: 8px;
}

.list-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.card-list::-webkit-scrollbar {
  width: 8px;
}

.card-list::-webkit-scrollbar-track {
  background: var(--bg-secondary, #2c2c44);
  border-radius: 4px;
}

.card-list::-webkit-scrollbar-thumb {
  background: var(--border-color, #4a4a6a);
  border-radius: 4px;
}

.card-list::-webkit-scrollbar-thumb:hover {
  background: var(--primary-color, #a29bfe);
}

.empty-state {
  text-align: center;
  padding: 2rem 1rem;
  color: var(--text-muted, #8a8a8a);
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.empty-title {
  color: var(--text-secondary, #b8b8b8);
  font-family: 'MedievalSharp', cursive;
  font-size: 1.25rem;
  margin: 0 0 0.25rem 0;
}

.empty-description {
  color: var(--text-muted, #8a8a8a);
  font-size: 0.875rem;
  margin: 0 0 1rem 0;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .card-list {
    max-height: calc(100vh - 180px);
  }
}
</style> 