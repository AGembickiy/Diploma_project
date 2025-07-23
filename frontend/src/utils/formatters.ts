export const formatDate = (date: string): string => {
  return new Date(date).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

export const formatPrice = (price: number): string => {
  return price.toLocaleString('ru-RU')
} 