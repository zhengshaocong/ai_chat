/// <reference types="vite/client" />

declare module '*.vue' {
    import type { DefineComponent } from 'vue'
    const component: DefineComponent<{}, {}, any>
    export default component
  }
  
// 声明 Vue 3 的全局类型
declare module 'vue' {
  interface ComponentCustomProperties {
    $router: any
    $route: any
  }
}
  