from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from wagtail.contrib.forms.models import AbstractFormField, AbstractForm

class FormField(AbstractFormField):
    page= ParentalKey(
        'UrlInputPage',
        on_delete=models.CASCADE,
        related_name='form_fields',
    )

class UrlInputPage(AbstractForm):
    # You can add any additional fields you need here
    content = RichTextField(blank=True)

    content_panels = AbstractForm.content_panels + [
        # Define how this page model will be displayed in the admin panel
        FieldPanel('content', classname="full"),
        InlinePanel('form_fields', label ="Form Fields")
    ]
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        print("Start")
        # Get information about form fields
        data_fields = [
            (field.clean_name, field.label)
            for field in self.get_form_fields()
        ]
        submissions = self.get_submission_class().objects.filter(page=self)
        for submission in submissions:
            data = submission.get_data()
            for name, label in data_fields:
                answer = data.get(name)
                if answer is None:
                    # Something wrong with data.
                    # Probably you have changed questions
                    # and now we are receiving answers for old questions.
                    # Just skip them.
                    answer = "Error"
                    continue
                print("Success")
                print(f"Answer for {name}: {answer}")
        print("Successfully")
        context.update({
            'answer': answer,
        })
        return context

class UrlInputPageLanding(Page):
    content = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('content', classname="full"),
    ]
    
    
    

