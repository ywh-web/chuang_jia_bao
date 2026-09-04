<script setup>
import { computed, ref } from 'vue'

const activeChapter = ref(0)
const spotlight = ref({ x: 50, y: 50 })
const comparison = ref(46)
const activeDetail = ref(0)
const visitedChapters = ref([true, false, false])
const archiveVisible = ref(false)
const archiveDownloaded = ref(false)

const chapters = [
  { tag: '01 / 团队启程', title: '一群大学生，第一次把目光投向潮州屋脊', text: '2023 年，广东财经大学跨年级、跨专业学生组建“潮韵嵌行”。团队从嵌瓷的文化与文旅价值调研出发，让会计、设计、计算机、文旅等十余个专业在同一门老手艺前相遇。', source: '项目档案 · 团队概况（2023）' },
  { tag: '02 / 走进校园', title: '孩子们动手，把屋脊上的艺术带回课堂', text: '2024 年暑期实践中，团队推动“嵌瓷进校园”。活动反馈显示，93.33% 的参与反馈认可动手能力得到锻炼，80% 认可创造能力得到提升，非遗从课本名词变成了手中的作品。', source: '项目档案 · 嵌瓷进校园实践（2024）' },
  { tag: '03 / 数字传承', title: '从一次实践，走向持续更新的数字传承', text: '团队随后开发嵌瓷文旅 AI 助手“瓷嘟嘟”，整理 200 多条专业语料并融合 AR 导览；2025 年起继续探索数字传家宝，让匠人经验、纹样与青年共创被长期记录。', source: '项目档案 · 数字化研发记录（2024—2025）' },
]

const details = [
  { label: '屋脊', title: '屋脊上的立体叙事', text: '嵌瓷依附在屋脊之上，把家族祈愿、乡土故事与建筑轮廓连成一条可以远望的叙事线。' },
  { label: '凤凰', title: '凤凰的吉祥寓意', text: '凤凰象征和美与新生。匠人会依据屋脊朝向、观看距离和日照，调整羽翼的层次与颜色。' },
  { label: '贴饶', title: '一片碎瓷的落点', text: '每片瓷都要经过选色、剪裁、试位与粘贴。微小的角度变化，决定鳞羽在阳光下如何闪动。' },
]

const exploredCount = computed(() => visitedChapters.value.filter(Boolean).length)
const archiveReady = computed(() => exploredCount.value === chapters.length)
const remainingChapters = computed(() => chapters.length - exploredCount.value)

const selectChapter = (index) => {
  activeChapter.value = index
  const nextVisited = visitedChapters.value.map((visited, itemIndex) => visited || itemIndex === index)
  visitedChapters.value = nextVisited
  if (nextVisited.every(Boolean)) archiveVisible.value = true
}

const selectDetail = (index) => {
  activeDetail.value = index
}

const moveSpotlight = (event) => {
  const rect = event.currentTarget.getBoundingClientRect()
  spotlight.value = { x: ((event.clientX - rect.left) / rect.width) * 100, y: ((event.clientY - rect.top) / rect.height) * 100 }
}

const touchSpotlight = (event) => {
  const touch = event.touches[0]
  if (touch) moveSpotlight({ currentTarget: event.currentTarget, clientX: touch.clientX, clientY: touch.clientY })
}

const showArchive = () => {
  if (archiveReady.value) archiveVisible.value = true
}

const downloadArchive = () => {
  if (!archiveReady.value) return

  const canvas = document.createElement('canvas')
  canvas.width = 1400
  canvas.height = 900
  const context = canvas.getContext('2d')
  const gradient = context.createLinearGradient(0, 0, 1400, 900)
  gradient.addColorStop(0, '#07191c')
  gradient.addColorStop(.58, '#103336')
  gradient.addColorStop(1, '#6a2422')
  context.fillStyle = gradient
  context.fillRect(0, 0, canvas.width, canvas.height)
  context.strokeStyle = '#78ddd5'
  context.lineWidth = 3
  context.strokeRect(40, 40, 1320, 820)
  context.strokeStyle = 'rgba(232, 200, 120, .5)'
  context.strokeRect(58, 58, 1284, 784)

  context.fillStyle = '#78ddd5'
  context.font = '24px sans-serif'
  context.fillText('CY · DIGITAL HEIRLOOM ARCHIVE', 90, 125)
  context.fillStyle = '#e8c878'
  context.font = '700 74px serif'
  context.fillText('潮韵嵌行 · 青年传承实录', 90, 235)
  context.fillStyle = '#f7f0e3'
  context.font = '34px sans-serif'
  context.fillText('一群广财青年与潮州嵌瓷共同走过的数字化实践', 90, 300)

  context.fillStyle = 'rgba(247, 240, 227, .72)'
  context.font = '22px sans-serif'
  context.fillText('地点  广东潮州 · CHAOZHOU', 90, 370)
  context.fillText('记录  实地调研 / 校园实践 / 数字研发', 90, 410)
  context.fillText('时间  2023—2025 · 状态持续行动', 90, 450)

  const archiveSteps = ['团队启程', '走进校园', '数字传承']
  archiveSteps.forEach((step, index) => {
    const x = 90 + index * 420
    context.fillStyle = index === 2 ? '#e8c878' : '#78ddd5'
    context.font = '700 34px sans-serif'
    context.fillText('0' + (index + 1), x, 565)
    context.fillStyle = '#f7f0e3'
    context.font = '700 30px sans-serif'
    context.fillText(step, x, 620)
    context.fillStyle = 'rgba(247, 240, 227, .55)'
    context.fillRect(x, 660, 330, 2)
  })

  context.fillStyle = 'rgba(247, 240, 227, .68)'
  context.font = '24px sans-serif'
  context.fillText('“从看见一门手艺，到让更多年轻人参与其中。”', 90, 760)
  context.fillStyle = '#e8c878'
  context.font = '20px monospace'
  context.fillText('ARCHIVE NO. CY-2023-2025  ·  潮韵青年传承实录', 90, 815)

  const link = document.createElement('a')
  link.download = '潮韵数字传家宝-青年传承实录.png'
  link.href = canvas.toDataURL('image/png')
  link.click()
  archiveDownloaded.value = true
}
</script>

<template>
  <section id="digital-story" class="immersive-story">
    <div class="container">
      <div class="immersive-heading">
        <span class="eyebrow">DIGITAL STORY / 数字故事</span>
        <h2>一群青年，怎样把屋脊上的非遗带进数字时代</h2>
        <p>这不是虚构人物的故事，而是“潮韵嵌行”从调研、校园实践到数字化研发的真实轨迹。点击三个章节，查看项目在 2023—2025 年间留下的记录。</p>
      </div>

      <div class="immersive-stage digital-story-stage" :style="{ '--spot-x': `${spotlight.x}%`, '--spot-y': `${spotlight.y}%` }" @pointermove="moveSpotlight" @touchmove.prevent="touchSpotlight">
        <div class="digital-story-surface" aria-hidden="true">
          <div class="digital-story-grid"></div>
          <div class="digital-scan-image">
            <img src="/assets/chaozhou-6.webp" alt="" />
            <span class="scan-line"></span>
            <small>FIELD RECORD · CHAOZHOU</small>
          </div>
          <div class="digital-orbit orbit-one"></div>
          <div class="digital-orbit orbit-two"></div>
          <div class="digital-route">
            <i v-for="(_, index) in chapters" :key="index" :class="{ active: activeChapter === index }"></i>
          </div>
          <div class="digital-index">
            <span>CY · PROJECT ARCHIVE</span>
            <strong>潮州 / CHAOZHOU</strong>
            <small>23.662° N · 116.622° E</small>
          </div>
          <div class="digital-data-stream">
            <span>TEAM_2023</span><span>CAMPUS_2024</span><span>AI_GUIDE</span><span>HEIRLOOM_2025</span>
          </div>
          <div class="digital-chapter-echo">0{{ activeChapter + 1 }}</div>
        </div>
        <div class="immersive-light"></div>
        <div class="immersive-copy">
          <span>{{ chapters[activeChapter].tag }}</span>
          <h3>{{ chapters[activeChapter].title }}</h3>
          <p>{{ chapters[activeChapter].text }}</p>
          <small class="story-source">{{ chapters[activeChapter].source }}</small>
        </div>
        <img class="immersive-ip" src="/assets/ip-characters-hero.webp" alt="潮州嵌瓷数字传家宝 IP 形象" />
        <button v-for="(chapter, index) in chapters" :key="chapter.tag" class="story-hotspot" :class="`hotspot-${index + 1}`" type="button" :aria-label="chapter.title" :aria-pressed="activeChapter === index" @click="selectChapter(index)"><i></i><span>{{ index + 1 }}</span></button>
        <div class="immersive-controls"><button v-for="(_, index) in chapters" :key="index" type="button" :class="{ active: activeChapter === index, visited: visitedChapters[index] }" @click="selectChapter(index)">0{{ index + 1 }}</button></div>
      </div>

      <section class="story-toolkit" aria-labelledby="story-toolkit-title">
        <div class="story-toolkit-heading">
          <div>
            <span class="eyebrow">EXPLORE THE ARCHIVE / 探索档案</span>
            <h3 id="story-toolkit-title">从观看故事，到亲手留下记忆</h3>
          </div>
          <p>对比一帧实地影像，读懂三个文化细节，再完成这段青年实践的数字档案。</p>
        </div>

        <div class="story-tool-grid">
          <article class="story-tool restoration-tool">
            <header><span>01 / 影像修复</span><h4>拖动，唤回屋脊的颜色</h4></header>
            <div class="restoration-frame">
              <img class="restoration-after" src="/assets/chaozhou-6.webp" alt="数字修复后的彩色嵌瓷屋脊" />
              <img class="restoration-before" src="/assets/chaozhou-6.webp" alt="修复前的褪色嵌瓷屋脊" :style="{ clipPath: 'inset(0 ' + (100 - comparison) + '% 0 0)' }" />
              <span class="restoration-label label-before">实地记录 · 原始影像</span>
              <span class="restoration-label label-after">数字增色</span>
              <i class="restoration-divider" :style="{ left: 'calc(' + comparison + '% - 1px)' }"><b>↔</b></i>
            </div>
            <label class="restoration-slider">
              <span>原始影像</span>
              <input v-model.number="comparison" type="range" min="0" max="100" aria-label="拖动查看照片修复前后对比" />
              <span>修复结果</span>
            </label>
            <p>数字增色用于辅助观看，纹样名称、工艺与文化寓意仍以匠人和项目调研记录为准。</p>
          </article>

          <article class="story-tool detail-tool">
            <header><span>02 / 文化细节</span><h4>点一点，读懂屋脊上的故事</h4></header>
            <div class="detail-map">
              <img src="/assets/chaozhou-6.webp" alt="带有文化细节探索点的潮州嵌瓷屋脊" />
              <button v-for="(detail, index) in details" :key="detail.label" type="button" class="detail-point" :class="['detail-point-' + (index + 1), { active: activeDetail === index }]" :aria-label="'查看' + detail.label + '文化细节'" @click="selectDetail(index)"><span>{{ index + 1 }}</span></button>
            </div>
            <div class="detail-reading" aria-live="polite">
              <span>{{ details[activeDetail].label }}</span>
              <h5>{{ details[activeDetail].title }}</h5>
              <p>{{ details[activeDetail].text }}</p>
            </div>
          </article>
        </div>

        <article class="archive-maker" :class="{ ready: archiveReady }">
          <div class="archive-maker-progress">
            <span>03 / 数字档案卡</span>
            <strong>{{ exploredCount }} / {{ chapters.length }} 章已阅读</strong>
            <div class="archive-progress-track"><i v-for="(_, index) in chapters" :key="index" :class="{ complete: visitedChapters[index] }"></i></div>
          </div>

          <div v-if="!archiveVisible" class="archive-maker-prompt" aria-live="polite">
            <h4>读完故事，档案卡会自动生成</h4>
            <p v-if="!archiveReady">还需阅读 {{ remainingChapters }} 个章节。点击上方场景中的数字节点，补齐这份记忆。</p>
            <p v-else>三段记忆已经汇合，可以生成数字传家宝档案。</p>
            <button class="story-action" type="button" :disabled="!archiveReady" @click="showArchive">生成档案卡</button>
          </div>

          <div v-else class="archive-result" aria-live="polite">
            <div class="archive-card-preview">
              <span>CY · DIGITAL HEIRLOOM ARCHIVE</span>
              <h4>潮韵嵌行 · 青年传承实录</h4>
              <p>一群广财青年与潮州嵌瓷共同走过的数字化实践</p>
              <dl><div><dt>地点</dt><dd>广东潮州</dd></div><div><dt>记录</dt><dd>调研 · 校园实践 · 数字研发</dd></div><div><dt>时间</dt><dd>2023—2025</dd></div></dl>
              <div class="archive-card-steps"><span>01 团队启程</span><span>02 走进校园</span><span>03 数字传承</span></div>
              <small>ARCHIVE NO. CY-2023-2025</small>
            </div>
            <div class="archive-download-copy">
              <span class="eyebrow">YOUR STORY CARD</span>
              <h4>这份记忆，已经可以带走</h4>
              <p>下载高清 PNG 实录卡，保存这段有项目资料支撑的青年非遗实践。</p>
              <button class="story-action" type="button" @click="downloadArchive">{{ archiveDownloaded ? '档案卡已下载，再次保存' : '下载数字档案卡' }}</button>
            </div>
          </div>
        </article>
      </section>
    </div>
  </section>
</template>

