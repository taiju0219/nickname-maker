<script setup lang="ts">
import { ref } from 'vue';
interface NicknameResponse {
  nickname: string;
}
const userName = ref<string>('')
const title = ref<string>('')
const nickname = ref<string>('')
const getNickname = async() => {
  if (!userName.value) {
    alert('名前を入力してね')
    return
  }
  try {
    const response = await fetch ('https://localhost:8000/nickname')
    const data: NicknameResponse = await response.json()
    title.value = data.nickname
    nickname.value = `${title.value} ${userName.value}`
  } catch (error) {
    console.error('エラー', error)
    alert('サーバーとの通信に失敗しました')
  }
}
</script>

<template>
  <div class = "container">
    <h1>あだ名メーカー</h1>
    <p>あなたの名前を教えてください！</p>
    <div class = "input-area">
      <input type = "text" v-model = "userName" placeholder = "名前を入力" @keyup.enter = "getNickname">
      <button @click = "getNickname">作成</button>
    </div>
    <div v-if = "nickname" class = "result">
      あなたのあだ名は<br>
      <span class = "nickname-text">「{{ nickname }}」</span>です！

    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
  font-family: sans-serif;
  padding-top: 50px;
}

.input-area {
  margin: 20px 0;
}

input {
  padding: 10px;
  font-size: 16px;
  margin-right: 10px;
  border: 2px solid #ddd;
  border-radius: 4px;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #3aa876;
}

.result {
  margin-top: 30px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  color: #35495e;
}

.nickname-text {
  font-size: 32px;
  font-weight: bold;
  color: #42b983;
  display: block;
  margin-top: 10px;
}
</style>