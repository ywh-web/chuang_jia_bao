<script setup>
import PageIntro from '../components/PageIntro.vue'
import SectionHeading from '../components/SectionHeading.vue'
import { storyTimeline } from '../data/site'
import InteractiveStory from '../components/InteractiveStory.vue'
import CommentThread from '../components/CommentThread.vue'
import UgcWall from '../components/UgcWall.vue'
</script>
<template>
  <div><PageIntro eyebrow="04 / INTANGIBLE HERITAGE" title="屋脊上的故事，正在继续" intro="潮州嵌瓷把地方文化塑成立体的色彩，也把一代代人的愿望安放在建筑之上。" image="/assets/chaozhou-1.webp"/><section class="section-pad"><div class="container"><SectionHeading eyebrow="A LIVING CRAFT" title="看见一门工艺的时间感" text="龙、凤、花鸟、人物，不只是装饰；它们是潮州人对秩序、吉祥与生活的想象。"/><div class="timeline"> <article v-for="item in storyTimeline" :key="item.year" class="timeline-item"><div class="timeline-image"><img :src="item.image" :alt="item.title"/></div><div class="timeline-copy"><span class="timeline-year">{{ item.year }}</span><h2>{{ item.title }}</h2><p>{{ item.text }}</p></div></article></div></div></section><InteractiveStory /><section class="content-expansion alt"><div class="container"><div class="expansion-heading"><span class="eyebrow">CRAFT NOTES</span><h2>一片瓷为什么能成为潮州的文化符号</h2><p>嵌瓷以碎瓷片重构立体叙事，龙凤、麒麟、花鸟和戏曲人物既是装饰，也是潮汕民间对吉祥、家族和秩序的共同想象。它的价值不只在于“好看”，还在于每一次观看都能重新进入地方生活。</p></div><div class="detail-grid"><article class="detail-card"><span class="detail-index">01 / 技艺</span><h3>十二道工序的耐心</h3><p>塑坯、剪饶、贴饶、微调等工序依赖经验和手上功夫，匠人培养周期长，构成不可替代的技艺壁垒。</p></article><article class="detail-card"><span class="detail-index">02 / 题材</span><h3>民间故事的立体化</h3><p>龙凤、麒麟送子、红头船与戏曲人物，将潮汕宗族文化、商贸历史和祈福愿望凝结为可见的形象。</p></article><article class="detail-card"><span class="detail-index">03 / 传承</span><h3>从师徒到共创</h3><p>面对传承人老龄化，项目用校园课程、青年创作和数字档案让更多人以自己的方式进入工艺现场。</p></article></div></div></section><section class="content-expansion"><div class="container"><div class="expansion-heading"><span class="eyebrow">STORY ARCHIVE</span><h2>把公共文化，转成私人记忆</h2></div><div class="prose-columns"><div><h3>匠人的声音</h3><p>记录传承人的创作初心、工艺判断和地方经验，配合方言保护与 AI 配音，让口述内容可以被家庭成员反复聆听。</p></div><div><h3>家族的回应</h3><p>用户可以补充家族照片、成长片段和祝福文字，让作品从“潮州的一件工艺品”变成“我家的一段文化记忆”。</p></div></div></div></section><section class="quote-section"><div class="container"><span class="eyebrow">THE NEXT CHAPTER</span><blockquote>让年轻人不只是观看非遗，<br /><em>而是进入它、理解它，再创造它。</em></blockquote><RouterLink class="text-link" to="/experience">体验数字化共创 <span>→</span></RouterLink></div></section><div class="story-community-stack container"><UgcWall /><CommentThread page-key="story" anchor="craft" title="说说你看到的嵌瓷故事" /></div></div>
</template>


