import { createStore } from 'vuex'

export default createStore({
  state: {
    currentApp: null,
    currentSession: null
  },
  mutations: {
    setCurrentApp(state, app) {
      state.currentApp = app
    },
    setCurrentSession(state, session) {
      state.currentSession = session
    }
  },
  actions: {
    setCurrentApp({ commit }, app) {
      commit('setCurrentApp', app)
    },
    setCurrentSession({ commit }, session) {
      commit('setCurrentSession', session)
    }
  },
  getters: {
    currentApp: state => state.currentApp,
    currentSession: state => state.currentSession
  }
})