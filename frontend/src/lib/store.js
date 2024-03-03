import { writable } from 'svelte/store';

// localStorage에 저장하는 store
const persist_storage = (key, initValue) => {
  const storedValueStr = localStorage.getItem(key)
  const store = writable(storedValueStr != null ? JSON.parse(storedValueStr) : initValue)
  store.subscribe((val) => {
      localStorage.setItem(key, JSON.stringify(val))
  })
  return store
}

export const page = persist_storage("page", 0)
export const access_token = persist_storage("access_token", "")
export const email = persist_storage("email", "")
export const is_login = persist_storage("is_login", false)



// sessionStorage에 저장하는 store
const session_storage = (key, initValue) => {
  const storedValueStr = sessionStorage.getItem(key)
  const store = writable(storedValueStr != null ? JSON.parse(storedValueStr) : initValue)
  store.subscribe((val) => {
    sessionStorage.setItem(key, JSON.stringify(val))
  })
  return store
}

export const selectedItems = session_storage('selectedItems', {'spirits': [], 'materials': []})
export const searchQuery = session_storage('searchQuery', '')
