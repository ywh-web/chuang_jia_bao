<script setup>
import { ref } from 'vue'
const activeChapter = ref(0)
const spotlight = ref({ x: 50, y: 50 })
const chapters = [
  { tag: '01 / 选片', title: '先让一片瓷，找到自己的位置', text: '碎瓷不是废料。颜色、弧度和光泽被重新判断，成为屋脊故事里的一个停顿。' },
  { tag: '02 / 贴饶', title: '手上的经验，决定故事如何站起来', text: '匠人用一双手把平面的愿望变成立体的守护，让龙凤和花鸟在阳光里有了方向。' },
  { tag: '03 / 传家', title: '当你伸手触碰，它就进入你的记忆', text: '今天的观看、留言和分享，会成为下一位家人理解潮州文化的入口。' },
]
const moveSpotlight = (event) => {
  const rect = event.currentTarget.getBoundingClientRect()
  spotlight.value = { x: ((event.clientX - rect.left) / rect.width) * 100, y: ((event.clientY - rect.top) / rect.height) * 100 }
}
const touchSpotlight = (event) => { const touch = event.touches[0]; if (touch) moveSpotlight({ currentTarget: event.currentTarget, clientX: touch.clientX, clientY: touch.clientY }) }
</script>

<template>
  <section class="immersive-story"><div class="container"><div class="immersive-heading"><span class="eyebrow">IMMERSIVE STORY / 沉浸式叙事</span><h2>把鼠标交给屋脊，让故事显影</h2><p>移动光标或手指，照亮一段工艺记忆；点击场景中的章节，查看它如何从一片碎瓷走进家庭。</p></div><div class="immersive-stage" :style="{ '--spot-x': `${spotlight.x}%`, '--spot-y': `${spotlight.y}%` }" @pointermove="moveSpotlight" @touchmove.prevent="touchSpotlight"><div class="immersive-depth depth-back"></div><div class="immersive-depth depth-mid"></div><div class="immersive-light"></div><div class="immersive-copy"><span>{{ chapters[activeChapter].tag }}</span><h3>{{ chapters[activeChapter].title }}</h3><p>{{ chapters[activeChapter].text }}</p></div><img class="immersive-ip" src="/assets/ip-characters-hero.webp" alt="潮州嵌瓷数字传家宝 IP 形象"/><button v-for="(chapter, index) in chapters" :key="chapter.tag" class="story-hotspot" :class="`hotspot-${index + 1}`" type="button" :aria-label="chapter.title" :aria-pressed="activeChapter === index" @click="activeChapter = index"><i></i><span>{{ index + 1 }}</span></button><div class="immersive-controls"><button v-for="(_, index) in chapters" :key="index" type="button" :class="{ active: activeChapter === index }" @click="activeChapter = index">0{{ index + 1 }}</button></div></div></div></section>
</template>
