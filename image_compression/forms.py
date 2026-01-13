from django import forms
from .models  import CompressImage

class CompressImageForm(forms.ModelForm):
    class Meta:
        model = CompressImage
        fields = ('original_img' , 'quality')

    original_img = forms.ImageField(label='Upload Image')

    # ✅ validate supported formats
    def clean_original_img(self):
        img = self.cleaned_data.get("original_img")

        allowed_types = [
            "image/jpeg",
            "image/png",
            "image/webp",
        ]

        if img.content_type not in allowed_types:
            raise forms.ValidationError(
                "Only JPG, PNG, and WEBP images are supported."
            )

        return img