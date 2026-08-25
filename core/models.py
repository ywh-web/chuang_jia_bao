from django.db import models


class ContactInquiry(models.Model):
    class CooperationType(models.TextChoices):
        SCHOOL = 'school', 'B 端校园研学'
        FAMILY = 'family', 'C 端家庭体验'
        TOURISM = 'tourism', 'G 端文旅合作'
        LICENSING = 'licensing', 'B2B 纹样授权'

    class Status(models.TextChoices):
        PENDING = 'pending', '待处理'
        CONTACTED = 'contacted', '已联系'
        CLOSED = 'closed', '已完成'

    name = models.CharField('称呼', max_length=80)
    contact = models.CharField('联系方式', max_length=160)
    cooperation_type = models.CharField('合作方向', max_length=20, choices=CooperationType.choices)
    message = models.TextField('合作留言', blank=True)
    status = models.CharField('处理状态', max_length=20, choices=Status.choices, default=Status.PENDING)
    admin_note = models.TextField('管理员备注', blank=True)
    created_at = models.DateTimeField('提交时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = '合作意向'
        verbose_name_plural = '合作意向'

    def __str__(self):
        return f'{self.name} · {self.get_cooperation_type_display()}'


class Comment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', '待审核'
        APPROVED = 'approved', '已通过'
        REJECTED = 'rejected', '已拒绝'

    page_key = models.CharField('页面标识', max_length=80)
    anchor = models.CharField('内容锚点', max_length=80, blank=True)
    author_name = models.CharField('留言昵称', max_length=80)
    content = models.TextField('留言内容')
    parent = models.ForeignKey('self', verbose_name='回复对象', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    status = models.CharField('审核状态', max_length=20, choices=Status.choices, default=Status.PENDING)
    like_count = models.PositiveIntegerField('点赞数', default=0)
    created_at = models.DateTimeField('提交时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = '评论与回复'
        verbose_name_plural = '评论与回复'

    def __str__(self):
        return f'{self.author_name} · {self.content[:24]}'


class UGCSubmission(models.Model):
    class Category(models.TextChoices):
        STORY = 'story', '家族故事'
        SHOWCASE = 'showcase', '买家秀 / 搭配指南'
        MEMORY = 'memory', '老照片与城市记忆'

    class Status(models.TextChoices):
        PENDING = 'pending', '待审核'
        APPROVED = 'approved', '已通过'
        REJECTED = 'rejected', '已拒绝'

    title = models.CharField('投稿标题', max_length=120)
    author_name = models.CharField('投稿人', max_length=80)
    contact = models.CharField('联系方式', max_length=160, blank=True)
    category = models.CharField('投稿类型', max_length=20, choices=Category.choices, default=Category.STORY)
    story = models.TextField('投稿内容')
    image = models.ImageField('图片', upload_to='ugc/%Y/%m/', blank=True, null=True)
    status = models.CharField('审核状态', max_length=20, choices=Status.choices, default=Status.PENDING)
    like_count = models.PositiveIntegerField('点赞数', default=0)
    featured = models.BooleanField('精选展示', default=False)
    created_at = models.DateTimeField('提交时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        ordering = ('-featured', '-created_at')
        verbose_name = '用户共创投稿'
        verbose_name_plural = '用户共创投稿'

    def __str__(self):
        return f'{self.title} · {self.author_name}'
