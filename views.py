import sys
import requests
from django.shortcuts import render
from django.http import JsonResponse
from TextToImgSearch.models import ImageSearchDetail  
from nltk.metrics.distance import edit_distance  # editing distance
from EB.models import Topic, TopicDetail
from pathlib import Path 
import subprocess


def text_to_art_home(request):
    """Renders the TextToArt home page."""
    return render(request, 'TextToArt.html')

def run_script(script_name, script_path, script_arg):  # script_arg 
    venvpath = Path('/home/metacomp/python_virtualenv/py3.11.4_ml/bin/activate')  # ml env path
    scriptpath = Path(script_path) / script_name  # script path
    description = Path(' --description')

    # command
    cmd = f'source {venvpath}; python {scriptpath} {description} "{script_arg.strip()}"'

    print(f"RUN_SCRIPT CALLED: cmd: >>{cmd}<<")  # output
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable='/bin/bash')

    # Waiting for it to be done
    stdout, stderr = process.communicate()
    print(f"STDOUT: {stdout.decode()}")
    print(f"STDERR: {stderr.decode()}")

    return stdout.decode().strip()


# def text_to_art_search(request):
#     """Handles the search functionality for TextToArt."""
#     if request.method == 'POST':
#         query = request.POST.get('query', '').strip().lower()  # Extract and sanitize query
#         # Filter images by tagtext containing the query
#         matching_images = ImageSearchDetail.objects.filter(tagtext__icontains=query)[:5]  # Limit to 5 results
#         # Serialize the data to send as JSON
#         serialized_images = list(matching_images.values('id', 'imageurl', 'tagtext'))
#         return JsonResponse({'images': serialized_images})
#     return JsonResponse({'error': 'Invalid request method.'}, status=400)

# def text_to_art_search(request):
#     """Handles the search functionality for TextToArt."""
#     if request.method == 'POST':
#         query = request.POST.get('search', '').strip().lower()  # Extract and sanitize query
#         if not query:
#             return render(request, 'TextToArt.html', {'error': 'Search query cannot be empty.'})
#         print(query)
#         query = run_script('llm_test.py', '/home/ncdbproj/CadillacDBProj/TextToArt', query)

#         # Filter images by tagtext containing the query
#         matching_images = ImageSearchDetail.objects.filter(tagtext__icontains=query)[:10]  # Limit to 10 results

#         # Render the search results on the same page
#         return render(request, 'TextToArt.html', {
#             'search_query': query,
#             'matching_images': matching_images,
#         })
    
#     # If not a POST request, render the search page without results
#     return render(request, 'TextToArt.html')

# def text_to_art_search(request):
#     """Handles the search functionality for TextToArt."""
#     if request.method == 'POST':
#         query = request.POST.get('search', '').strip().lower()
#         if not query:
#             return render(request, 'TextToArt.html', {'error': 'Search query cannot be empty.'})

#         print(f"User Query: {query}")
        
#         # calls the script
#         script_result = run_script('llm_test.py', '/home/ncdbproj/CadillacDBProj/TextToArt', query)

#         # checks script result
#         if not script_result or "Error" in script_result:  # script fails
#             return render(request, 'TextToArt.html', {'error': script_result or "Script did not produce any result."})

#         # makes sure scripts returns right result
#         print(f"Script Result: {script_result}")

#         # searches database using script result
#         matching_images = ImageSearchDetail.objects.filter(tagtext__icontains=script_result)[:10]

#         return render(request, 'TextToArt.html', {
#             'search_query': query,
#             'matching_images': matching_images,
#         })

#     return render(request, 'TextToArt.html')


def text_to_art_search(request):
    """Handles the search functionality for TextToArt."""
    if request.method == 'POST':
        query = request.POST.get('search', '').strip().lower()
        if not query:
            return render(request, 'TextToArt.html', {'error': 'Search query cannot be empty.'})
        
        query = run_script('llm_test.py', '/home/ncdbproj/CadillacDBProj/TextToArt', query)

        # 获取所有图像记录
        all_images = ImageSearchDetail.objects.all()

        # 定义相似度计算函数
        def calculate_similarity(tagtext, query):
            max_length = max(len(tagtext), len(query))
            return 1 - edit_distance(tagtext, query) / max_length  # 归一化到 [0, 1]

        # 计算相似度并排序
        scored_images = [
            (image, calculate_similarity(image.tagtext, query)) for image in all_images
        ]

        # 按相似度降序排序并选取前10条
        scored_images = sorted(scored_images, key=lambda x: x[1], reverse=True)[:10]

        # 提取匹配的图像对象
        matching_images = [image for image, score in scored_images]

        # 渲染结果到前端
        return render(request, 'TextToArt.html', {
            'search_query': query,
            'matching_images': matching_images,
        })

    # 非POST请求时，渲染默认页面
    return render(request, 'TextToArt.html')

def text_to_art_image_page(request, image_id):
    """Renders the individual image page for TextToArt."""
    image = get_object_or_404(ImageSearchDetail, id=image_id)  # Fetch the image by ID
    similar_images = ImageSearchDetail.objects.filter(tagtext__icontains=image.tagtext).exclude(id=image_id)[:4]
    return render(request, 'TextToArtImagePage.html', {
        'image': image,
        'similar_images': similar_images
    })

def select_image(request, image_id):
    """Handles image selection and forwards to the styling function."""
    # Fetch the image based on its ID
    image = ImageSearchDetail.objects.get(id=image_id)
    # Redirect to the Car Hallucination function (adjust this path as needed)
    return render(request, 'TextToArt/StyleSelection.html', {'image': image})


