from django.db import models
from django.shortcuts import render
from wagtail.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, PageChooserPanel, MultipleChooserPanel, InlinePanel
from wagtail.images.blocks import ImageChooserBlock
from streams import blocks
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
class HomePage(RoutablePageMixin,Page):
    """Home page model."""
    max_count = 1

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

