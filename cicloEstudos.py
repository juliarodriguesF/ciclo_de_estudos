import flet as ft
from fpdf import FPDF


def main(page: ft.Page):
    page.title = "Ciclo de Estudos"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    disciplinas = []
    multiplicadores = {
        1: 5,  # Péssimo
        2: 4,  # Ruim
        3: 3,  # Mais ou menos
        4: 2,  # Bom
        5: 1   # Ótimo
    }

    def adicionar_disciplina(e):
        nome = nome_input.value
        prioridade = int(prioridade_input.value)
        disciplinas.append({"nome": nome, "prioridade": prioridade,
                           "multiplicador": multiplicadores[prioridade]})
        atualizar_tabela()
        nome_input.value = ""
        prioridade_input.value = ""
        page.update()

    def calcular_ciclo(e):
        total_multiplicadores = sum(d["multiplicador"] for d in disciplinas)
        horas_diarias = int(horas_diarias_input.value)
        dias_semana = int(dias_semana_input.value)
        horas_totais = horas_diarias * dias_semana
        coeficiente = horas_totais / total_multiplicadores

        for d in disciplinas:
            d["horas_semanais"] = coeficiente * d["multiplicador"]

        mostrar_ciclo(disciplinas)

    def mostrar_ciclo(disciplinas):
        resultados.value = ""
        for disciplina in disciplinas:
            resultados.value += f"{disciplina['nome']} - Prioridade: {
                disciplina['prioridade']} - Horas Semanais: {disciplina['horas_semanais']:.2f}\n"
        page.update()

    def limpar():
        disciplinas.clear()
        nome_input.value = ""
        prioridade_input.value = ""
        resultados.value = ""
        horas_diarias_input.value = ""
        dias_semana_input.value = ""
        page.update()

    def atualizar_tabela():
        rows = []
        for disciplina in disciplinas:
            horas_semanais = disciplina.get("horas_semanais", "N/A")
            rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(disciplina["nome"])),
                    ft.DataCell(ft.Text(str(disciplina["prioridade"]))),
                    ft.DataCell(ft.Text(str(disciplina["multiplicador"]))),
                    ft.DataCell(ft.Text(str(horas_semanais)))
                ]
            ))

        tabela.rows = rows
        page.update()

    def show_message_dialog(title, content):
        message_dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(content),
            actions=[
                ft.TextButton("OK", on_click=close_message_dialog)
            ],
        )
        page.dialog = message_dialog
        message_dialog.open = True
        page.update()

    def close_message_dialog(e):
        page.dialog.open = False
        page.update()

    def show_help_dialog(e):
        show_message_dialog("Prioridades", "As prioridades devem ser definidas considerando os seguintes critérios: "
                            "Prioridade 1: 'Me considero muito ruim nesta disciplina'. "
                            "Prioridade 2: 'Me considero ruim nesta disciplina'. "
                            "Prioridade 3: 'Me considero mais ou menos nesta disciplina'. "
                            "Prioridade 4: 'Me considero bom nesta disciplina'. "
                            "Prioridade 5: 'Me considero muito bom nesta disciplina'.")

    nome_input = ft.TextField(label="Nome da Disciplina")
    prioridade_input = ft.TextField(
        label="Prioridade (1-5)", keyboard_type=ft.KeyboardType.NUMBER)

    adicionar_button = ft.ElevatedButton(
        text="Adicionar Disciplina", on_click=adicionar_disciplina)

    horas_diarias_input = ft.TextField(
        label="Horas Diárias", keyboard_type=ft.KeyboardType.NUMBER)
    dias_semana_input = ft.TextField(
        label="Dias da Semana", keyboard_type=ft.KeyboardType.NUMBER)
    calcular_button = ft.ElevatedButton(
        text="Calcular Ciclo", on_click=calcular_ciclo)

    help_button = ft.IconButton(
        icon=ft.icons.HELP_OUTLINE, on_click=show_help_dialog)

    limpar_button = ft.ElevatedButton(
        text="Limpar", on_click=limpar
    )

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Disciplina")),
            ft.DataColumn(ft.Text("Prioridade")),
            ft.DataColumn(ft.Text("Multiplicador")),
            ft.DataColumn(ft.Text("Horas Semanais")),
        ],
        rows=[],
    )

    resultados = ft.Text()

    page.add(
        ft.Row([ft.Text("Ciclo de Estudos"), help_button],
               alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        nome_input,
        prioridade_input,
        adicionar_button,
        ft.Divider(),
        horas_diarias_input,
        dias_semana_input,
        calcular_button,
        tabela,
        ft.Divider(),
        limpar_button,
        resultados
    )


ft.app(target=main)
