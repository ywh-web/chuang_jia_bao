<script setup>
import { onMounted, ref } from 'vue'
import { createUgc, likeUgc, listUgc } from '../api/community'
const items = ref([])
const loading = ref(true)
const submitting = ref(false)
const notice = ref('')
const form = ref({ title: '', authorName: '', category: 'story', story: '', contact: '', image: null })
const categories = [{ value: 'story', label: '家族故事' }, { value: 'showcase', label: '买家秀 / 搭配指南' }, { value: 'memory', label: '老照片与城市记忆' }]
const load = async () => { try { items.value = (await listUgc()).items || [] } catch (error) { notice.value = error.message } finally { loading.value = false } }
const submit = async () => {
  if (!form.value.title.trim() || !form.value.authorName.trim() || !form.value.story.trim()) { notice.value = '请至少填写标题、投稿人和故事内容。'; return }
  submitting.value = true; notice.value = ''
  const data = new FormData(); Object.entries(form.value).forEach(([key, value]) => { if (value) data.append(key, value) })
  try { const result = await createUgc(data); items.value.unshift(result.item); form.value = { title: '', authorName: '', category: 'story', story: '', contact: '', image: null }; notice.value = result.message } catch (error) { notice.value = error.message } finally { submitting.value = false }
}
const like = async (item) => { const key = `ugc-liked-${item.id}`; if (localStorage.getItem(key)) return; try { const result = await likeUgc(item.id); item.likeCount = result.likeCount; localStorage.setItem(key, '1') } catch (error) { notice.value = error.message } }
const onFile = (event) => { form.value.image = event.target.files?.[0] || null }
onMounted(load)
</script>

<template>
  <section class="ugc-wall"><div class="ugc-intro"><div><span class="eyebrow">OPEN ARCHIVE / 共创档案</span><h2>把你的嵌瓷记忆放进来</h2><p>一张老照片、一段家族故事，或一次文创搭配，都可以成为数字传家宝的下一页。</p></div><div class="ugc-rule"><b>投稿规则</b><span>内容审核后公开展示</span><span>图片建议小于 5MB</span><span>请尊重他人隐私与版权</span></div></div><div class="ugc-layout"><form class="ugc-form" @submit.prevent="submit"><label>投稿标题<input v-model="form.title" maxlength="120" placeholder="例如：我家屋脊上的那只凤凰"/></label><label>你的名字<input v-model="form.authorName" maxlength="80" placeholder="可以使用昵称"/></label><label>投稿类型<select v-model="form.category"><option v-for="item in categories" :key="item.value" :value="item.value">{{ item.label }}</option></select></label><label>故事或说明<textarea v-model="form.story" maxlength="3000" rows="6" placeholder="讲讲这件作品、这张照片与你的关系"></textarea></label><label>联系方式（选填）<input v-model="form.contact" maxlength="160" placeholder="方便项目团队联系你"/></label><label>上传图片（选填）<input type="file" accept="image/*" @change="onFile"/></label><button class="button button-dark" type="submit" :disabled="submitting">{{ submitting ? '提交中…' : '提交我的故事' }}</button><p v-if="notice" class="community-notice" role="status">{{ notice }}</p></form><div class="ugc-list"><div v-if="loading" class="community-empty">正在打开共创档案……</div><div v-else-if="!items.length" class="community-empty">还没有公开投稿，来留下第一份记忆吧。</div><article v-for="item in items" :key="item.id" class="ugc-card"><img v-if="item.imageUrl" :src="item.imageUrl" :alt="item.title"/><div class="ugc-card-body"><span class="ugc-category">{{ item.categoryLabel }}</span><h3>{{ item.title }}</h3><p>{{ item.story }}</p><div class="ugc-meta"><span>by {{ item.authorName }}</span><button type="button" @click="like(item)">赞 {{ item.likeCount }}</button></div></div></article></div></div></section>
</template>
