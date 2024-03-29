from django.shortcuts import render, redirect
from django.contrib.auth import logout
import requests
from . models import Search
from django.http import JsonResponse, HttpResponse
import requests
import json


# Create your views here.

HUNTER_API_KEY = 'f682560568da2d1e777425be0d561920ba8ba909'


def index(request):
    search_confirm = False 
    if request.method == 'POST':
        search = request.POST.get('search')

        if not search:
            return HttpResponse("Nenhum termo de pesquisa fornecido.")

        api_result = requests.get(f'https://api.hunter.io/v2/domain-search?domain={search}&api_key={HUNTER_API_KEY}')

        if api_result.status_code == 200:
            response_data = api_result.json()

            # Exibindo o JSON retornado pela API no console do Django
            print(json.dumps(response_data, indent=2))

            # Processar os dados para obter informações relevantes dos e-mails
            if 'data' in response_data and 'emails' in response_data['data']:
                emails_data = response_data['data']['emails']
            else:
                emails_data = []

            emails_list = []
            for email_data in emails_data:
                email_info = {
                    'value': email_data['value'],
                    'type': email_data['type'],
                    'confidence': email_data['confidence'],
                    'sources': email_data['sources'],
                    # Adicione outras informações sobre o e-mail, se necessário
                }
                emails_list.append(email_info)

            search_confirm = True    

            # Contexto para enviar para o template
            context = {
                'domain': response_data['data']['domain'],
                'industry': response_data['data']['industry'],
                'emails': emails_list,
                'search_confirm': search_confirm,
                'search': search,

            }


            return JsonResponse(context)
        else:
            return JsonResponse({'error': f"Erro da API: {api_result.status_code}"})

        '''
            return render(request, 'new_index.html', context)
        else:
            print(f"Erro da API: {api_result.status_code}")
            return HttpResponse("Erro da API: Não foi possível obter os dados.")
        '''

    else:
        return render(request, 'home.html')
