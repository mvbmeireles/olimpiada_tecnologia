document.addEventListener('DOMContentLoaded', function() {
    const addStepButton = document.getElementById('add-step-button');
    const newStepDescriptionInput = document.getElementById('new-step-description');
    const repairStepsList = document.querySelector('.repair-steps'); // A lista <ul> dos passos

    // Função auxiliar para obter o token CSRF do cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // --- Lógica para ADICIONAR novo passo (já existente, apenas ajustada a criação do item) ---
    if (addStepButton && newStepDescriptionInput && repairStepsList) {
        const projectId = parseInt(repairStepsList.dataset.projectId); // Pega o ID do projeto do atributo data-project-id

        addStepButton.addEventListener('click', async function() {
            const newStepText = newStepDescriptionInput.value.trim();

            if (newStepText) {
                if (isNaN(projectId)) {
                    console.error('Não foi possível obter o ID do projeto do atributo data-project-id.');
                    alert('Erro: ID do projeto não encontrado.');
                    return;
                }

                const data = {
                    project_id: projectId,
                    step_description: newStepText,
                    csrfmiddlewaretoken: getCookie('csrftoken')
                };

                try {
                    const response = await fetch('/api/add_repair_step/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-Requested-With': 'XMLHttpRequest',
                        },
                        body: JSON.stringify(data)
                    });

                    if (response.ok) {
                        const result = await response.json();
                        if (result.success) {
                            // Adicionar o novo passo visualmente à lista
                            const newStepItem = document.createElement('li');
                            newStepItem.classList.add('repair-step-item');
                            // Usamos repairStepsList.children.length - 1 para o índice,
                            // pois o formulário de adição é o último filho e não conta como passo.
                            // Mas é mais seguro calcular o índice dos itens de passo.
                            const currentStepCount = repairStepsList.querySelectorAll('.repair-step-item').length;
                            const newIndex = currentStepCount; // O próximo índice será o total atual de passos

                            newStepItem.innerHTML = `
                                <input type="checkbox" id="step${currentStepCount + 1}" data-index="${newIndex}">
                                <label for="step${currentStepCount + 1}">${newStepText}</label>
                            `;

                            // Insere o novo item ANTES do formulário de adição
                            const addForm = document.querySelector('.add-new-item-form');
                            if (addForm) {
                                repairStepsList.insertBefore(newStepItem, addForm);
                            } else {
                                repairStepsList.appendChild(newStepItem); // Caso o form não exista, adiciona no final
                            }

                            newStepDescriptionInput.value = ''; // Limpa o campo de input

                            // Adiciona o event listener ao NOVO checkbox
                            const newCheckbox = newStepItem.querySelector('input[type="checkbox"]');
                            if (newCheckbox) {
                                newCheckbox.addEventListener('change', handleCheckboxChange);
                            }

                        } else {
                            alert('Erro ao adicionar passo: ' + result.message);
                        }
                    } else {
                        alert('Erro no servidor ao adicionar passo. Status: ' + response.status);
                    }
                } catch (error) {
                    console.error('Erro ao enviar requisição:', error);
                    alert('Ocorreu um erro ao tentar adicionar o passo.');
                }
            } else {
                alert('Por favor, digite a descrição do novo passo.');
            }
        });
    }

    // --- NOVA Lógica para PERSISTIR o estado do checkbox ---

    // Função para lidar com a mudança de estado de qualquer checkbox
    async function handleCheckboxChange(event) {
        const checkbox = event.target;
        const isChecked = checkbox.checked;
        const stepIndex = parseInt(checkbox.dataset.index); // Pega o índice do atributo data-index
        const projectId = parseInt(repairStepsList.dataset.projectId); // Pega o ID do projeto do atributo data-project-id

        if (isNaN(projectId) || isNaN(stepIndex)) {
            console.error('Dados de projeto/passo inválidos para atualização.');
            alert('Erro: Não foi possível identificar o passo para atualização.');
            return;
        }

        const data = {
            project_id: projectId,
            step_index: stepIndex,
            is_checked: isChecked,
            csrfmiddlewaretoken: getCookie('csrftoken')
        };

        try {
            const response = await fetch('/api/update_repair_step_status/', { // Endpoint para atualizar status
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                const result = await response.json();
                if (!result.success) {
                    alert('Erro ao atualizar status: ' + result.message);
                    // Opcional: Reverter o estado do checkbox se o servidor retornar erro
                    checkbox.checked = !isChecked;
                }
            } else {
                alert('Erro no servidor ao atualizar status. Status: ' + response.status);
                // Opcional: Reverter o estado do checkbox se o servidor retornar erro
                checkbox.checked = !isChecked;
            }
        } catch (error) {
            console.error('Erro ao enviar requisição de atualização de status:', error);
            alert('Ocorreu um erro ao tentar atualizar o status do passo.');
            // Opcional: Reverter o estado do checkbox
            checkbox.checked = !isChecked;
        }
    }

    // Adiciona event listener a TODOS os checkboxes existentes ao carregar a página
    const checkboxes = document.querySelectorAll('.repair-step-item input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', handleCheckboxChange);
    });

});