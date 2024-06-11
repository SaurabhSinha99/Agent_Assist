from django.shortcuts import render
def index(request):
    return render(request, 'index.html')

# # Create your views here.


# import uuid
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.core.files.storage import default_storage
# from django.utils.timezone import now

# def get_context_id(request):
#     context_id = uuid.uuid4()
#     return JsonResponse({'context_id': str(context_id)})

# @csrf_exempt
# def upload_audio(request):
#     if request.method == 'POST':
#         context_id = request.POST.get('context_id')
#         audio_file = request.FILES['audio']
#         timestamp = now().strftime("%Y%m%d%H%M%S")
#         file_name = f'audio/{context_id}/{timestamp}_{audio_file.name}'
#         file_path = default_storage.save(file_name, audio_file)
#         return JsonResponse({'message': 'File uploaded successfully', 'file_path': file_path})
#     return JsonResponse({'error': 'Invalid request'}, status=400)



import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.utils.timezone import now
import whisper
import torch

# Load the Whisper model
model = whisper.load_model("base").to("cuda")

# Global dictionary to store transcriptions by context ID
transcriptions = {}

def index(request):
    return render(request, 'index.html')

def get_context_id(request):
    context_id = uuid.uuid4()
    # Initialize an empty transcription for the new context ID
    transcriptions[str(context_id)] = ""
    return JsonResponse({'context_id': str(context_id)})

@csrf_exempt
def upload_audio(request):
    if request.method == 'POST':
        context_id = request.POST.get('context_id')
        audio_file = request.FILES['audio']
        timestamp = now().strftime("%Y%m%d%H%M%S")
        file_name = f'audio/{context_id}/{timestamp}_{audio_file.name}'
        file_path = default_storage.save(file_name, audio_file)

        # Transcribe the audio file
        transcription = transcribe_audio(file_path)

        # Append the transcription to the existing context transcription
        if context_id in transcriptions:
            transcriptions[context_id] += transcription

        return JsonResponse({'message': 'File uploaded and transcribed successfully', 'file_path': file_path, 'transcription': transcriptions[context_id]})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def transcribe_audio(file_path):
    # Load the audio file
    audio = whisper.load_audio(file_path)
    # Perform the transcription
    result = model.transcribe(audio)
    print(result['text'])
    return result['text']


