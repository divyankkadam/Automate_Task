from django.contrib import admin
from .models import CompressImage
from django.utils.html import format_html


class CompressImageAdmin(admin.ModelAdmin):

    def thumbnail(self, obj):
        if obj.compressed_img:
            return format_html(
                '<img src="{}" width="40" height="40" />',
                obj.compressed_img.url
            )
        return "-"
    
    def org_img_size(self, obj):
        if obj.original_img:
            size_mb = obj.original_img.size / (1024 * 1024)
            size_text = f"{size_mb:.2f} MB"
            return format_html("{}", size_text)
        return "-"


    def comp_img_size(self, obj):
        if obj.compressed_img:
            size_mb = obj.compressed_img.size / (1024 * 1024)
            if size_mb >1:
                size_text = f"{size_mb:.2f} MB"
                return format_html("{}", size_text)
            else:
                size_kb = obj.compressed_img.size/1024
                size_text = f"{size_mb:.2f} KB"
                return format_html("{}", size_text)

            
        return "-"


    thumbnail.short_description = "Preview"
    org_img_size.short_description = "Original Size"
    comp_img_size.short_description = "Compressed Size"


    list_display = ('user', 'thumbnail', 'org_img_size', 'comp_img_size', 'compressed_at')


admin.site.register(CompressImage, CompressImageAdmin)
