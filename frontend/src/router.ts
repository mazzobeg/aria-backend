import ScrapersRoot from './components/ScrapersRoot.vue'
import ArticlesRoot from './components/ArticlesRoot.vue'
import { createRouter, createWebHistory} from 'vue-router'
const routes = [
    {
        path: '/scrapers',
        name: 'Scrapers',
        component: ScrapersRoot
    },
    {
        path: '/articles',
        name: 'Articles',
        component: ArticlesRoot
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
  })
  
export default router