from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

PROJETOS_CIENTIFICOS = [
    {
        'id': 1,
        'titulo': "Densidade óssea e muscular em microgravidade",
        'descricao': "Este experimento tem como objetivo analisar os efeitos da microgravidade na densidade óssea e muscular dos astronautas que ficam por longos períodos a bordo da ISS. A pesquisa busca entender como a falta de gravidade afeta o corpo humano e quais são as consequências a longo prazo.",
        'pais': "EUA",
        'status': "intacto",
        'imagem_placeholder': "Projeto+Osseo",
        'imagem_bandeira': "eua_flag.png",
        'passos_de_reparo': []
    },
    {
        'id': 2,
        'titulo': "Materiais resistentes à radiação espacial",
        'descricao': "Estudo sobre o desenvolvimento de novos materiais capazes de suportar os altos níveis de radiação encontrados no espaço profundo, protegendo equipamentos e tripulantes. Essencial para missões de longa duração, este projeto busca otimizar a segurança e a durabilidade das estruturas espaciais.",
        'pais': "Brasil",
        'status': "avariado",
        'imagem_placeholder': "Materiais+Radiacao",
        'imagem_bandeira': "brazil_flag.png",
        'passos_de_reparo': [
            {'descricao': "Verificar vazamentos nos sistemas de tubulação.", 'concluido': False},
            {'descricao': "Substituir válvulas defeituosas e refazer as conexões.", 'concluido': False},
            {'descricao': "Testar a integridade do sistema após o reparo.", 'concluido': False}
        ]
    },
    {
        'id': 3,
        'titulo': "Comportamento de fluidos em microgravidade",
        'descricao': "Análise do comportamento de líquidos em ambiente de microgravidade para otimizar sistemas de suporte à vida, propulsão e gerenciamento de resíduos em missões espaciais. A compreensão aprofundada desses fenômenos é vital para a engenharia de naves e estações espaciais futuras.",
        'pais': "Alemanha",
        'status': "avariado",
        'imagem_placeholder': "Fluidos+Espaco",
        'imagem_bandeira': "alemanha_flag.png",
        'passos_de_reparo': [
            "Verificar vazamentos nos sistemas de tubulação.",
            "Substituir válvulas defeituosas e refazer as conexões.",
            "Testar a integridade do sistema após o reparo."
        ]
    },
    {
        'id': 4,
        'titulo': "Microrganismos em ambiente extremo",
        'descricao': "Pesquisa sobre a sobrevivência e adaptação de microrganismos em condições extremas do espaço, com implicações para a astrobiologia e busca por vida extraterrestre. Entender sua resiliência pode revelar segredos sobre a origem e a distribuição da vida no universo.",
        'pais': "EUA",
        'status': "intacto",
        'imagem_placeholder': "Microrganismos",
        'imagem_bandeira': "eua_flag.png",
        'passos_de_reparo': []
    },
    {
        'id': 5,
        'titulo': "Crescimento de plantas em microgravidade",
        'descricao': "Estudo sobre o cultivo de vegetais em ambientes de microgravidade para garantir fontes de alimento fresco em missões de longa duração e futuras colônias espaciais. Este projeto é fundamental para a autossuficiência de habitats fora da Terra.",
        'pais': "Brasil",
        'status': "intacto",
        'imagem_placeholder': "Plantas+Espaco",
        'imagem_bandeira': "brazil_flag.png",
        'passos_de_reparo': []
    },
    {
        'id': 6,
        'titulo': "Regeneração de tecidos em microgravidade",
        'descricao': "Investigação sobre a capacidade de regeneração de tecidos e órgãos em condições de microgravidade, buscando avanços na medicina espacial e tratamentos terrestres. Os resultados podem revolucionar a recuperação de lesões e doenças.",
        'pais': "Alemanha",
        'status': "avariado",
        'imagem_placeholder': "Regeneracao+Tecidos",
        'imagem_bandeira': "alemanha_flag.png",
        'passos_de_reparo': [
            {'descricao': "Analisar amostras de tecido danificado.", 'concluido': False},
            {'descricao': "Aplicar protocolo de bio-regeneração com fatores de crescimento.", 'concluido': False},
            {'descricao': "Monitorar a resposta celular e a formação de novo tecido.", 'concluido': False}
        ]
    },
    {
        'id': 7,
        'titulo': "Comunicação por rádio no espaço",
        'descricao': "Pesquisa sobre a otimização de sistemas de comunicação por rádio para garantir transmissões estáveis e de alta velocidade entre a Terra e missões espaciais distantes. A clareza e a confiabilidade da comunicação são cruciais para o sucesso de qualquer exploração espacial.",
        'pais': "EUA",
        'status': "intacto",
        'imagem_placeholder': "Comunicacao+Radio",
        'imagem_bandeira': "eua_flag.png",
        'passos_de_reparo': []
    },
    {
        'id': 8,
        'titulo': "Cristalização de proteínas em microgravidade",
        'descricao': "Estudo da formação de cristais de proteínas em ambiente de microgravidade para obter cristais maiores e mais puros, essenciais para a pesquisa farmacêutica e o desenvolvimento de novas drogas. A qualidade desses cristais impacta diretamente a descoberta de novos medicamentos.",
        'pais': "Brasil",
        'status': "avariado",
        'imagem_placeholder': "Proteinas+Microgravidade",
        'imagem_bandeira': "brazil_flag.png",
        'passos_de_reparo': [
            {'descricao': "Verificar a temperatura do cristalizador e ajustar se necessário.", 'concluido': False},
            {'descricao': "Limpar o sistema de filtragem de partículas para evitar impurezas.", 'concluido': False},
            {'descricao': "Reiniciar o processo de cristalização com novas amostras.", 'concluido': False}
        ]
    },
]

def lista_cartoes(request):
    context = {
        'projetos': PROJETOS_CIENTIFICOS
    }
    return render(request, 'index.html', context)

def detalhes_projeto(request, projeto_id):
    projeto_encontrado = None
    for projeto in PROJETOS_CIENTIFICOS:
        if projeto['id'] == projeto_id:
            projeto_encontrado = projeto
            break

    if projeto_encontrado is None:
        from django.http import Http404
        raise Http404("Projeto não encontrado")

    context = {
        'projeto': projeto_encontrado
    }
    return render(request, 'detail.html', context)

@csrf_exempt # APENAS PARA DESENVOLVIMENTO, NUNCA EM PRODUÇÃO SEM O CSRF!
def add_repair_step(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            project_id = data.get('project_id')
            step_description = data.get('step_description')

            if not project_id or not step_description:
                return JsonResponse({'success': False, 'message': 'Dados incompletos.'}, status=400)

            projeto_encontrado = None
            for p in PROJETOS_CIENTIFICOS:
                if p['id'] == project_id:
                    projeto_encontrado = p
                    break

            if projeto_encontrado is None:
                return JsonResponse({'success': False, 'message': 'Projeto não encontrado.'}, status=404)

            # Adiciona o novo passo como um dicionário com 'concluido': False
            projeto_encontrado['passos_de_reparo'].append({'descricao': step_description, 'concluido': False})

            return JsonResponse({'success': True, 'message': 'Passo adicionado com sucesso!'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Requisição inválida (JSON malformado).'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erro interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=405)
    
@csrf_exempt # APENAS PARA DESENVOLVIMENTO, NUNCA EM PRODUÇÃO SEM O CSRF!
def update_repair_step_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            project_id = data.get('project_id')
            step_index = data.get('step_index') # Usaremos o índice do passo na lista
            is_checked = data.get('is_checked') # O novo estado do checkbox

            if project_id is None or step_index is None or is_checked is None:
                return JsonResponse({'success': False, 'message': 'Dados incompletos.'}, status=400)

            projeto_encontrado = None
            for p in PROJETOS_CIENTIFICOS:
                if p['id'] == project_id:
                    projeto_encontrado = p
                    break

            if projeto_encontrado is None:
                return JsonResponse({'success': False, 'message': 'Projeto não encontrado.'}, status=404)

            passos = projeto_encontrado['passos_de_reparo']

            if 0 <= step_index < len(passos):
                # Atualiza o estado 'concluido' do passo específico
                passos[step_index]['concluido'] = is_checked
                return JsonResponse({'success': True, 'message': 'Status do passo atualizado com sucesso!'})
            else:
                return JsonResponse({'success': False, 'message': 'Índice do passo inválido.'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Requisição inválida (JSON malformado).'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erro interno: {str(e)}'}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=405)