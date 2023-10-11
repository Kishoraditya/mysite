from django import forms
from django.db import models
from django.shortcuts import render

# Add these:
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.models import Page, Orderable, PreviewableMixin
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, TabbedInterface, ObjectList
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from .amp_utils import PageAMPTemplateMixin
from django.utils.translation import gettext_lazy as _
#from wagtailcodeblock.blocks import CodeBlock
from wagtail.contrib.routable_page.models import RoutablePageMixin, re_path
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from wagtail.api import APIField
from rest_framework.fields import Field
from wagtail.images.api.fields import ImageRenditionField
from django_comments_xtd.models import XtdComment

class BlogChildPagesSerializer(Field):
    def to_representation(self, child_pages):
        # logic in here
        return_posts = []
        for child in child_pages:
            post_dict = {
                'id': child.id,
                'title': child.title,
                'slug': child.slug,
                'url': child.url,
            }
            return_posts.append(post_dict)
        return return_posts
        # Pythonic comprehensions
        # return [
        #     {
        #         'id': child.id,
        #         'title': child.title,
        #         'slug': child.slug,
        #         'url': child.url,
        #     } for child in child_pages
        # ]


class BlogIndexPage(RoutablePageMixin, Page):
    max_count = 1
    subpage_types = ['blog.VideoBlogPage', 'blog.ArticleBlogPage']
    intro = RichTextField(blank=True)
    template = "blog/blog_index_page.html"
    ajax_template = "blog/blog_index_page_ajax.html"
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        posts = self.get_children().live().order_by('-first_published_at')
#        if request.GET.get('tag', None):
#            tags = request.GET.get('tag')
#            posts = posts.filter(tags__slug__in=[tags])
        paginator = Paginator(posts, 1)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            blogpages = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            blogpages = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            blogpages = paginator.page(paginator.num_pages)
        context['blogpages'] = blogpages
        context["categories"] = BlogCategory.objects.all()
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
    @re_path(r"^july-2019/$", name="july_2019")
    @re_path(r"^year/(\d+)/(\d+)/$", name="blogs_by_year")
    def blogs_by_year(self, request, year=None, month=None):
        context = self.get_context(request)
        # Implement your BlogDetailPage filter. Maybe something like this:
        # if year is not None and month is not None:
        #     posts = BlogDetailPage.objects.live().public().filter(year=year, month=month)
        # else:
        #     # No year and no month were set, assume this is july-2019 only posts
        #     posts = BlogDetailPage.objects.live().public().filter(year=2019, month=07)
        # print(year)
        # print(month)
        # context["posts"] = posts

        # Note: The below template (latest_posts.html) will need to be adjusted
        return render(request, "blog/latest_posts.html", context)

    @re_path(r"^category/(?P<cat_slug>[-\w]*)/$", name="category_view")
    def category_view(self, request, cat_slug):
        """Find blog posts based on a category."""
        context = self.get_context(request)

        try:
            # Look for the blog category by its slug.
            category = BlogCategory.objects.get(slug=cat_slug)
        except Exception:
            # Blog category doesnt exist (ie /blog/category/missing-category/)
            # Redirect to self.url, return a 404.. that's up to you!
            category = None

        if category is None:
            # This is an additional check.
            # If the category is None, do something. Maybe default to a particular category.
            # Or redirect the user to /blog/ ¯\_(ツ)_/¯
            pass

        context["posts"] = BlogPage.objects.live().public().filter(categories__in=[category])

        # Note: The below template (latest_posts.html) will need to be adjusted
        return render(request, "blog/latest_posts.html", context)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Add extra variables and return the updated context
        context['blog_entries'] = BlogPage.objects.child_of(self).live()
        return context
    
    @re_path(r'^latest/$', name="latest_posts")
    def latest_blog_posts_only_shows_last_5(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context["blog_entries"] = context["blog_entries"][:1]
        return render(request, "blog/latest_posts.html", context)
    
    def get_sitemap_urls(self, request):
        # Uncomment to have no sitemap for this page
        # return []
        sitemap = super().get_sitemap_urls(request)
        sitemap.append(
            {
                "location": self.full_url + self.reverse_subpage("latest_posts"),
                "lastmod": (self.last_published_at or self.latest_revision_created_at),
                "priority": 0.9,
            }
        )
        return sitemap
    api_fields = [
        APIField("posts", serializer=BlogChildPagesSerializer(source='get_child_pages')),
    ]

    @property
    def get_child_pages(self):
        return self.get_children().public().live()
        # return self.get_children().public().live().values("id", "title", "slug")



class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )
    
class PersonBlock(blocks.StructBlock):
    first_name = blocks.CharBlock()
    surname = blocks.CharBlock()
    photo = ImageChooserBlock(required=False)
    biography = blocks.RichTextBlock()
    
    class Meta:
        template = 'blog/person.html'
        icon = 'user'

class CommonContentBlock(blocks.StreamBlock):
    heading = blocks.CharBlock(form_classname="title")
    paragraph = blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'h4', 'h5', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'image', 'code', 'blockquote'])
    #code = blocks.CodeBlock(label=_("Code"))
    image = ImageChooserBlock()
    
    class Meta:
        block_counts = {
            'heading': {'min_num': 1, 'max_num': 3},
        }

class BlogPage(PageAMPTemplateMixin, Page):
    
    subpage_types = []
    parent_page_types = ['blog.BlogIndexPage']

    page_description = "Use this page for converting users"
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = StreamField([
        ('person', PersonBlock()),
        ('gallery', blocks.ListBlock(ImageChooserBlock())),
        ('carousel', blocks.StreamBlock([
            ('image', ImageChooserBlock()),
            ('video', EmbedBlock()),
        ], icon='image')),
        ('common_content', CommonContentBlock()),
    ], min_num=2, max_num=7, use_json_field=True)
    authors = ParentalManyToManyField('blog.Author', blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+', 
        verbose_name=_("Image")
    )
    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)
    
    def get_absolute_url(self):
        return self.get_url()
    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None
        
    def save(self, *args, **kwargs):
        """Create a template fragment key.
        Then delete the key."""
        key = make_template_fragment_key(
            "blog_post_preview",
            [self.id]
        )
        cache.delete(key)
        return super().save(*args, **kwargs)

    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.FilterField('date'),
        #index.SearchField('body'),
    ]
    
    # Editor panels configuration

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('authors', widget=forms.CheckboxSelectMultiple),
            FieldPanel('tags'),
            FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
        ], heading="Blog information"),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
        InlinePanel('customcomments', label=_("Comments")),
    ]
    
    sidebar_content_panels = [
        #FieldPanel('advert'),
        InlinePanel('related_links', heading="Related links", label="Related link"),
    ]
    
    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel('feed_image'),
    ]
    
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(sidebar_content_panels, heading='Sidebar content'),
        ObjectList(Page.promote_panels, heading='Promote'),
    ])
    # Parent page / subpage type rules

    parent_page_types = ['blog.BlogIndexPage']
    subpage_types = []
    
    #ajax_template = 'other_template_fragment.html'
    #template = 'other_template.html'
    #amp_template = 'my_custom_amp_template.html'
    

class BlogPageRelatedLink(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]
#class Advert(PreviewableMixin, models.Model):
#    url = models.URLField(null=True, blank=True)
#    text = models.CharField(max_length=255)

#    panels = [
#        FieldPanel('url'),
#        FieldPanel('text'),
#    ]
#    search_fields = [
#        index.SearchField('text'),
#        index.AutocompleteField('text'),
#   ]

#   def get_preview_template(self, request, mode_name):
#        return "blog/templates/blog/advert.html"
    
class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]
    
    #@property
    #def image(self):
    #    return self.image

    #api_fields = [
    #    APIField("caption"),
    
    # This is using a custom django rest framework serializer
    #    APIField("image", serializer=ImageSerializedField()),
    # The below APIField is using a Wagtail-built DRF Serializer that supports
    # custom image rendition sizes
    #APIField(
    #        "image",
    #        serializer=ImageRenditionField(
    #            'fill-200x250',
    #            source="image"
    #        )
    #    ),
    #]

@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('author_image'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Authors'

class BlogTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context

class BlogCategory(models.Model):
    """Blog catgory for a snippet."""

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text='A slug to identify posts by this category',
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


register_snippet(BlogCategory)


class ArticleBlogPage(BlogPage):
    """A subclassed blog post page for articles."""

    template = "blog/article_blog_page.html"

    subtitle = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    intro_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Best size for this image will be 1400x400'
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('authors', widget=forms.CheckboxSelectMultiple),
            FieldPanel('tags'),
            FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
        ], heading="Blog information"),
        FieldPanel('intro'),
        FieldPanel("subtitle"),
        ImageChooserBlock("intro_image"),
        FieldPanel('body'),
        
    ]


# Second subclassed page
class VideoBlogPage(BlogPage):
    """A video subclassed page."""

    template = "blog/video_blog_page.html"

    youtube_video_id = models.CharField(max_length=30)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('authors', widget=forms.CheckboxSelectMultiple),
            FieldPanel('tags'),
            FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
            
        ], heading="Blog information"),
        FieldPanel('intro'),
        FieldPanel("youtube_video_id"),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
        
    ]

class ImageSerializedField(Field):
    """A custom serializer used in Wagtails v2 API."""

    def to_representation(self, value):
        """Return the image URL, title and dimensions."""
        return {
            "url": value.file.url,
            "title": value.title,
            "width": value.width,
            "height": value.height,
        }

class CustomComment(XtdComment):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='customcomments')

    def save(self, *args, **kwargs):
        if self.user:
            self.user_name = self.user.display_name
        self.page = BlogPage.objects.get(pk=self.object_pk)
        super(CustomComment, self).save(*args, **kwargs)

