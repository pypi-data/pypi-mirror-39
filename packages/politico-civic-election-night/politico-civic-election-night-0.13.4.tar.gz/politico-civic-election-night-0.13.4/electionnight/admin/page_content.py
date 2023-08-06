from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from election.models import ElectionDay
from electionnight.models import PageContentBlock


class BlockAdminForm(forms.ModelForm):
    # content = forms.CharField(widget=CKEditorWidget()) # TODO: To markdown

    class Meta:
        model = PageContentBlock
        fields = ("content_type", "content")


class PageContentBlockInline(admin.StackedInline):
    model = PageContentBlock
    extra = 0
    form = BlockAdminForm


class ElectionDayFilter(admin.SimpleListFilter):
    title = _("Election date")
    parameter_name = "date"

    def lookups(self, request, model_admin):
        return (
            (e.date, e.date.strftime("%Y-%m-%d"))
            for e in ElectionDay.objects.all()
        )

    def queryset(self, request, queryset):
        if self.value() == "":
            return queryset
        return queryset.filter(election_day__date=self.value())


class PageContentAdmin(admin.ModelAdmin):
    inlines = [PageContentBlockInline]
    list_filter = ("content_type", ElectionDayFilter)
    list_display = ("page_location",)
    search_fields = ("page_location",)
    filter_horizontal = ("featured",)
    # actions = None
    readonly_fields = (
        "election_day",
        "page_location",
        "content_object",
        "division",
    )
    fieldsets = (
        (None, {"fields": ("page_location",)}),
        (
            "Page Meta",
            {"fields": ("election_day", "content_object", "division")},
        ),
        ("Relationships", {"fields": ("featured",)}),
    )
