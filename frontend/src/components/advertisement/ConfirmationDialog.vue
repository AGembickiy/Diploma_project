<template>
  <div v-if="isVisible" class="confirmation-overlay" @click="closeDialog">
    <div class="confirmation-dialog" @click.stop>
      <div class="confirmation-header">
        <h3 class="confirmation-title">✅ Успешно!</h3>
      </div>
      
      <div class="confirmation-content">
        <p class="confirmation-message">{{ message }}</p>
      </div>
      
      <div class="confirmation-actions">
        <button class="btn btn-primary" @click="handleOk">
          OK
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  isVisible: boolean
  message: string
}

interface Emits {
  (e: 'close'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const closeDialog = () => {
  emit('close')
}

const handleOk = () => {
  console.log('🔘 Кнопка OK нажата в ConfirmationDialog')
  // Закрываем диалог подтверждения
  emit('close')
}
</script>

<style scoped>
.confirmation-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
}

.confirmation-dialog {
  background: #1a1a1a;
  border: 2px solid #4a4a4a;
  border-radius: 12px;
  padding: 24px;
  max-width: 400px;
  width: 90%;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.8);
  text-align: center;
}

.confirmation-header {
  margin-bottom: 16px;
}

.confirmation-title {
  color: #28a745;
  font-size: 1.5rem;
  margin: 0;
  font-family: 'MedievalSharp', cursive;
  text-shadow: 0 0 10px rgba(40, 167, 69, 0.5);
}

.confirmation-content {
  margin-bottom: 24px;
}

.confirmation-message {
  color: #e0e0e0;
  font-size: 1.1rem;
  margin: 0;
  line-height: 1.5;
}

.confirmation-actions {
  display: flex;
  justify-content: center;
}

.btn {
  padding: 12px 32px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'MedievalSharp', cursive;
}

.btn-primary {
  background: #28a745;
  color: white;
  border: 2px solid #218838;
}

.btn-primary:hover {
  background: #218838;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(40, 167, 69, 0.4);
}
</style>
