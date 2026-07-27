import router from '@/router'
import { useAuthStore } from '@/stores/auth'

export async function demoLogin() {
  const auth = useAuthStore()
  await auth.login('demo', 'demo123')
  const target = router.currentRoute.value.query.redirect || '/'
  await router.push(target)
}
