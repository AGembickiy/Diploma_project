<template>
  <div class="main-layout">
    <Header />
    <div class="main-body">
      <ContentArea>
        <slot />
      </ContentArea>
      <Sidebar />
    </div>
    <Footer />
    <!-- LoginDialog удалён, теперь он только в App.vue через Teleport -->
  </div>
</template>

<script setup lang="ts">
import Header from '@/components/layout/Header.vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import Footer from '@/components/layout/Footer.vue'
import ContentArea from '@/components/layout/ContentArea.vue'
// import LoginDialog from '@/components/ui/LoginDialog.vue'
// import { useUiStore } from '@/stores/ui'
// import { useUserStore } from '@/stores/user'

// const ui = useUiStore()
// const user = useUserStore()

// const handleLogin = ({ login, _password }: { login: string; password: string }) => {
//   user.login(login)
//   ui.closeLoginDialog()
// }

// const handleRegister = ({ login, _password }: { login: string; password: string }) => {
//   user.login(login)
//   ui.closeLoginDialog()
// }
</script>

<style src="@/assets/styles/layout.css" scoped /> 