<script setup>
import { ref, computed } from 'vue'
import PageIntro from '../components/PageIntro.vue'
import { works } from '../data/site'
import CommentThread from '../components/CommentThread.vue'

const selected = ref(works[0])
const tab = ref('story')
const archiveOpen = ref(false)
const copied = ref(false)
const shared = ref(false)
const familyStory = ref('')
const storySaved = ref(false)
const tabs = [{ key: 'story', label: '故事' }, { key: 'pattern', label: '纹样' }, { key: 'asset', label: '数字档案' }]
const tabCopy = computed(() => ({ story: '双龙守护、祥瑞相逢。作品记录了共同创作的想象，也把家族对于团聚与守望的愿望放入屋脊之上。', pattern: '以作品中的龙鳞、祥云与朱红为灵感生成的衍生色彩，适用于壁纸、海报与文创包装。', asset: '数字档案把作品信息、工艺寓意和家族故事放在一起，方便保存、补充与分享。' }[tab.value]))
const credentialCode = computed(() => `${selected.value.id}-2024-CY`)
const copyCredential = async () => { try { await navigator.clipboard?.writeText(credentialCode.value) } catch {} copied.value = true; setTimeout(() => { copied.value = false }, 1800) }
const saveStory = () => { storySaved.value = true }
const shareArchive = async () => { try { if (navigator.share) await navigator.share({ title: `${selected.value.title} · 嵌瓷数字档案`, text: selected.value.meaning, url: window.location.href }); else await navigator.clipboard?.writeText(window.location.href); shared.value = true } catch {} }
</script>

<template>
  <div>
    <PageIntro eyebrow="03 / DIGITAL EXPERIENCE" title="打开一份数字传家宝" intro="选择一件作品，查看它的故事、纹样与数字档案。" image="/assets/chaozhou-2.webp" />
    <section class="section-pad experience-section"><div class="container"><div class="demo-note"><span>数字传家宝体验</span> 展示嵌瓷作品的故事、纹样与数字档案。</div><div class="experience-layout"><aside class="work-picker"><span class="eyebrow">WORKS / 作品选择</span><button v-for="work in works" :key="work.id" type="button" :class="{ active: selected.id === work.id }" @click="selected = work; tab = 'story'; archiveOpen = false"><span>{{ work.id }}</span><strong>{{ work.title }}</strong><small>{{ work.creator }}</small></button></aside><div class="work-detail"><div class="work-image"><img :src="selected.image" :alt="selected.title"/><div class="image-stamp">潮<br /><small>韵</small></div></div><div class="work-meta"><div><span class="eyebrow">{{ selected.id }} / {{ selected.year }}</span><h2>{{ selected.title }}</h2><p>{{ selected.meaning }}</p></div><div class="pattern-dots"><i v-for="color in selected.pattern" :key="color" :style="{ background: color }"></i></div></div><div class="experience-tabs"><button v-for="item in tabs" :key="item.key" type="button" :class="{ active: tab === item.key }" @click="tab = item.key">{{ item.label }}</button></div><div class="tab-panel"><p>{{ tabCopy }}</p><div v-if="tab === 'pattern'" class="pattern-preview"><i v-for="color in selected.pattern" :key="color" :style="{ background: color }"></i><span>智能纹样生成 / 纹样设计展示</span></div><div v-if="tab === 'asset'" class="asset-preview credential-card archive-card"><div class="archive-mark">档案<small>CY</small></div><div class="archive-content"><span class="eyebrow">DIGITAL ARCHIVE</span><h3>{{ selected.title }} · 数字作品档案</h3><div class="archive-meta"><span>唯一编号 <b>{{ credentialCode }}</b></span><span>创作年份 <b>{{ selected.year }}</b></span><span>记录状态 <b>持续更新</b></span></div><div class="archive-actions"><button class="text-link" type="button" @click="archiveOpen = !archiveOpen">{{ archiveOpen ? '收起完整档案' : '查看完整档案' }} <span>→</span></button><button class="text-link" type="button" @click="shareArchive">{{ shared ? '分享链接已复制' : '分享作品' }} <span>↗</span></button><button class="text-link" type="button" @click="copyCredential">{{ copied ? '编号已复制' : '复制作品编号' }} <span>↗</span></button></div><div v-if="archiveOpen" class="archive-detail"><p><strong>文化寓意：</strong>{{ selected.meaning }}</p><p><strong>工艺信息：</strong>潮州嵌瓷 · 屋脊装饰 · 彩瓷拼贴</p><p><strong>传承记录：</strong>作品资料、创作过程与家族记忆可持续补充。</p><label>补充家族故事<textarea v-model="familyStory" rows="3" placeholder="写下这件作品与你的家庭、城市或节日有关的记忆"></textarea></label><button class="button button-dark archive-save" type="button" @click="saveStory">{{ storySaved ? '故事已保存' : '保存家族故事' }}</button></div></div></div><button v-if="tab === 'story'" class="text-link" type="button" @click="tab = 'asset'">查看数字档案 <span>→</span></button></div></div></div></div></section>
    <div class="experience-community container"><CommentThread page-key="experience" anchor="archive" title="分享你的数字传家宝体验" /></div><section class="content-expansion alt"><div class="container"><div class="expansion-heading"><span class="eyebrow">A DIGITAL STORY ROOM</span><h2>一次体验，打开四个入口</h2><p>资料调研显示，87.95% 的受访者愿意亲手制作嵌瓷，54.91% 的受访者认可 AR 等数字展示方式。因此体验页不只是展示成品，而是把观看、参与、生成和分享连成一条路径。</p></div><div class="metric-strip"><div><strong>87.95%</strong><span>愿意亲手制作嵌瓷</span></div><div><strong>83.71%</strong><span>喜欢文创产品展示</span></div><div><strong>54.91%</strong><span>接受 AR / 建模展示</span></div><div><strong>743</strong><span>有效调研样本</span></div></div></div></section>
    <section class="content-expansion"><div class="container"><div class="expansion-heading"><span class="eyebrow">OFFLINE TO ONLINE</span><h2>从古城工坊进入数字世界</h2></div><div class="detail-grid"><article class="detail-card"><span class="detail-index">01 / 工坊</span><h3>亲手完成一片瓷</h3><p>在传承人指导下完成选片、拼贴和装饰，感受嵌瓷从材料到作品的真实过程。</p></article><article class="detail-card"><span class="detail-index">02 / AR 展示</span><h3>扫描后看见工艺</h3><p>通过 AR 底座和实景导览查看作品拆解、工艺讲解与潮州建筑中的文化语境。</p></article><article class="detail-card"><span class="detail-index">03 / 社群分享</span><h3>把作品带回家</h3><p>上传家风故事、生成专属纹样，邀请家人和朋友共同完成一份可持续更新的档案。</p></article></div></div></section>
  </div>
</template>

