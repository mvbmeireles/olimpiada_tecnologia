from django.shortcuts import render

# Create your views here.
def lista_cartoes(request):
    # Por enquanto, vamos retornar uma mensagem simples para testar.
    # Mais tarde, vamos renderizar um template HTML.
    return render(request, 'index.html', {'mensagem': 'Olá do Django!'})