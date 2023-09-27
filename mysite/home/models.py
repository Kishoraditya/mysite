from django.db import models
from django.shortcuts import render
from wagtail.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, PageChooserPanel, MultipleChooserPanel, InlinePanel
from wagtail.images.blocks import ImageChooserBlock
from streams import blocks
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.api import APIField
from rest_framework.fields import Field


class BannerCTASerializer(Field):
    def to_representation(self, page):
        return {
            'id': page.id,
            'title': page.title,
            'first_published_at': page.first_published_at,
            'owner': page.owner.username,
            'slug': page.slug,
            'url': page.url,
        }
class HomePage(RoutablePageMixin,Page):
    """Home page model."""
    #max_count = 1
    subpage_types = [
        'blog.BlogIndexPage',
        'contact.ContactPage',
        'flex.FlexPage',
    ]
    parent_page_type = [
        'wagtailcore.Page'
    ]

    banner_title = models.CharField(max_length=100, blank=False, null=True)
    banner_subtitle = RichTextField(features=["bold", "italic"])
    content = StreamField([("cta", blocks.CTABlock()),], null=True, blank=True,use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("banner_title"),
        FieldPanel("banner_subtitle"),
        InlinePanel(
            "images", 
            label="Banner Images",
        ),
        FieldPanel("content"),
        InlinePanel("carousel_images", 
                    max_num=5, 
                    min_num=1, 
                    label="Image",
            heading="Carousel Images",
            ),
    ]
    
    api_fields = [
        APIField("banner_title"),
        APIField("banner_subtitle"),
        APIField("content"),
        APIField("carousel_images"),
        APIField("banner_cta", serializer=BannerCTASerializer()),
        APIField("a_custom_api_response"),
    ]
    
    @property
    def a_custom_api_response(self):
        # return ["SOMETHING CUSTOM", 3.14, [1, 2, 3, 'a', 'b', 'c']]
        # logic goes in here
        return f"Banner Title Is: {self.banner_title}"

    class Meta:

        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"
      
    @path('subscribe/')
    def the_subscribe_page(self, request, *args, **kwargs):
        return self.render(
            request, 
            context_overrides={
                'context' : self.get_context(request, *args, **kwargs),
            },
            template="home/subscribe.html",
        )
    
    def get_admin_display_title(self):
        return "Custom Home Page Title"




class HomeImage(Orderable, models.Model):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='images')
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    banner_cta = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
   )
    panels=[
        FieldPanel("banner_image"),
        FieldPanel("banner_cta"),
    ]

class HomePageCarouselImages(Orderable):
    """Between 1 and 5 images for the home page carousel."""

    page = ParentalKey(HomePage, related_name="carousel_images")
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [FieldPanel("carousel_image")]
    



# # This will change the "title" field 's verbose name to "Custom Name".
# # But you'd still reference it in the template as `page.title`
#HomePage._meta.get_field("title").verbose_name = "Custom Name"
# # Here we are removing the help text. But to change it, simply change None to a string.
#HomePage._meta.get_field("title").help_text = None
# # Below is the new default title for a Home Page.
# # This only appears when you create a new page.
# HomePage._meta.get_field("title").default = "Default HomePage Title"
# # Lastly, we're adding a default `slug` value to the page.
# # This does not need to reflect the same (or similar) value that the `title` field has.
# HomePage._meta.get_field("slug").default = "default-homepage-title"
