<script setup>
import { onMounted, ref } from 'vue'
import { createComment, likeComment, listComments } from '../api/community'

defineOptions({ name: 'CommentThread' })
const props = defineProps({
  pageKey: { type: String, required: true },
  anchor: { type: String, default: '' },
  title: { type: String, default: '留下你的观察' },
})
const items = ref([])
const loading = ref(true)
const submitting = ref(false)
const notice = ref('')
const replyTo = ref(null)
const form = ref({ authorName: '', content: '' })

const load = async () => {
  loading.value = true
  try { items.value = (await listComments(props.pageKey, props.anchor)).items || [] } catch (error) { notice.value = error.message } finally { loading.value = false }
}
const submit = async () => {
  if (!form.value.authorName.trim() || !form.value.content.trim()) { notice.value = '请填写昵称和留言内容。'; return }
  submitting.value = true; notice.value = ''
  try {
    const result = await createComment({ pageKey: props.pageKey, anchor: props.anchor, parentId: replyTo.value?.id || null, ...form.value })
    if (!replyTo.value) items.value.unshift(result.item)
    else { const parent = items.value.find((item) => item.id === replyTo.value.id); if (parent) parent.replies = [...(parent.replies || []), result.item] }
    form.value = { authorName: '', content: '' }; replyTo.value = null; notice.value = result.message
  } catch (error) { notice.value = error.message } finally { submitting.value = false }
}
const like = async (item) => {
  const key = `comment-liked-${item.id}`
  if (localStorage.getItem(key)) return
  try { const result = await likeComment(item.id); item.likeCount = result.likeCount; localStorage.setItem(key, '1') } catch (error) { notice.value = error.message }
}
onMounted(load)
</script>

<template>
  <section class="community-comments" :aria-labelledby="`comments-${pageKey}-${anchor}`">
    <div class="community-heading"><div><span class="eyebrow">COMMUNITY / 互动留言</span><h2 :id="`comments-${pageKey}-${anchor}`">{{ title }}</h2></div><span class="community-count">{{ items.length }} 条公开留言</span></div>
    <div v-if="loading" class="community-empty">正在加载大家的留言……</div>
    <div v-else-if="!items.length" class="community-empty">这里还没有留言，欢迎成为第一个分享观察的人。</div>
    <div v-else class="comment-list">
      <article v-for="item in items" :key="item.id" class="comment-card">
        <div class="comment-avatar">{{ item.authorName.slice(0, 1) }}</div>
        <div class="comment-body"><div class="comment-meta"><strong>{{ item.authorName }}</strong><time>{{ new Date(item.createdAt).toLocaleDateString('zh-CN') }}</time></div><p>{{ item.content }}</p><div class="comment-actions"><button class="like-button" type="button" @click="like(item)" aria-label="给这条留言点赞"><span class="action-thumb" aria-hidden="true">👍</span><span>{{ item.likeCount }}</span></button><button class="reply-button" type="button" @click="replyTo = item" aria-label="回复这条留言"><span class="action-reply" aria-hidden="true">↩</span><span>回复 {{ item.replies?.length || 0 }}</span></button></div>
          <div v-for="reply in item.replies" :key="reply.id" class="comment-reply"><strong>{{ reply.authorName }}</strong><p>{{ reply.content }}</p><button class="like-button" type="button" @click="like(reply)" aria-label="给这条回复点赞"><span class="action-thumb" aria-hidden="true">👍</span><span>{{ reply.likeCount }}</span></button></div>
        </div>
      </article>
    </div>
    <form class="comment-form" @submit.prevent="submit"><div class="replying" v-if="replyTo">正在回复 {{ replyTo.authorName }} · <button type="button" @click="replyTo = null">取消</button></div><div class="comment-form-grid"><input v-model="form.authorName" maxlength="80" placeholder="你的昵称" aria-label="你的昵称"/><textarea v-model="form.content" maxlength="1000" rows="3" :placeholder="replyTo ? '写下你的回复……' : '分享你对这段内容的观察……'" aria-label="留言内容"></textarea><button class="button button-dark" type="submit" :disabled="submitting">{{ submitting ? '提交中…' : '发布留言' }}</button></div><p v-if="notice" class="community-notice" role="status">{{ notice }}</p></form>
  </section>
</template>

