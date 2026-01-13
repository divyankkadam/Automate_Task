from django.http import HttpResponse
from django.shortcuts import redirect, render
from . forms import CompressImageForm
from PIL import Image
import io

def compress(request):
    user = request.user
    if request.method == 'POST':
        form = CompressImageForm(request.POST , request.FILES)
        if form.is_valid():
            original_img = form.cleaned_data['original_img']
            quality = form.cleaned_data['quality']

            compressed_img = form.save(commit=False)
            compressed_img.user = user

            # Perform compression
            img = Image.open(original_img)
            buffer = io.BytesIO()
            # print('curser position at the beginning =>',buffer.tell())

            # detect original format
            format = img.format  # 'JPEG', 'PNG', 'WEBP', etc.

            save_kwargs = {}

            # formats that support quality
            if format in ["JPEG", "WEBP"]:
                save_kwargs["quality"] = quality
                save_kwargs["optimize"] = True

            # PNG uses compression level instead of quality
            elif format == "PNG":
                # convert quality (1–100) to compression level (0–9)
                compression_level = int((100 - quality) / 10)
                save_kwargs["compress_level"] = compression_level

            img.save(buffer, format=format, **save_kwargs)
            # print('curser position after image compression =>',buffer.tell())

            buffer.seek(0)
            # print('curser position after setting back to 0 =>',buffer.tell())

            # save the compressed img inside the model
            compressed_img.compressed_img.save(
                f'compressed_{original_img}',buffer,save=True
            )

            response = HttpResponse(buffer.getvalue(), content_type=f"image/{format.lower()}")
            response['Content-Disposition'] = f'attachment; filename=compressed_{original_img}'
            return response
    else:
        form = CompressImageForm()
        context = {
            'form' : form,
        }
        return render(request , 'image_compression/compress.html', context)



