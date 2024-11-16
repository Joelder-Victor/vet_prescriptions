import streamlit as st
from auth import authenticate_user, register_user
from register_vet import get_veterinarian_info, get_logo, get_signature
from register_animal import register_animal, register_guardian
from register_prescriptions import register_medicine,register_prescription
from jinja2 import Template
from weasyprint import HTML
import base64
from register_animal import register_animal

st.set_page_config(
    page_title="VetOne",  # Define o título da aba do navegador
    layout="centered",  # Layout centralizado
    initial_sidebar_state="expanded",  # Estado inicial da sidebar
)
hide_streamlit_style = """
            <style>
            /* Oculta o menu principal (hamburger menu) */
            #MainMenu {visibility: hidden;}
            
            /* Oculta o cabeçalho "Made with Streamlit" */
            footer {visibility: hidden;}
            
            /* Oculta o cabeçalho superior */
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if "animal_form_loaded" not in st.session_state:
    st.session_state["animal_form_loaded"] = False

if "route_count" not in st.session_state:
    st.session_state["route_count"] = 1


def add_route():
    st.session_state["route_count"] += 1


def remove_route():
    if st.session_state["route_count"] > 1:
        st.session_state["route_count"] -= 1


logo_path = ""
signature_path = ""
# Interface principal
st.title("Autenticação")

# Seleção entre Login e Cadastro
auth_option = st.selectbox("Selecione a opção", ["Login", "Cadastro"])

if auth_option == "Login":
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        token = authenticate_user(email, password)
        if token:
            st.session_state["auth_token"] = token
            st.session_state["email"] = email
            st.session_state["logo_path"] = ""
            st.session_state["signature_path"] = ""
            st.success("Login realizado com sucesso!")

elif auth_option == "Cadastro":
    name = st.text_input("Nome")
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")
    crmv = st.text_input("CRMV")
    phone = st.text_input("Telefone (opcional)")
    if st.button("Cadastrar"):
        register_user(name, email, password, crmv, phone)

# Conteúdo do aplicativo após autenticação
if "auth_token" in st.session_state:
    # Carrega o HTML template
    with open('templates/template.html', 'r', encoding='utf-8') as file:
        html_template = file.read()
    st.write("Autenticado")

    # Inicializa as informações do veterinário
    if "vet_info" not in st.session_state:
        vet_info = get_veterinarian_info(
            st.session_state["email"], st.session_state["auth_token"])
        if vet_info:
            st.session_state["vet_info"] = vet_info
        else:
            st.error("Erro ao carregar informações do veterinário.")

    with st.expander("Informações do Veterinário", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            if "vet_info" in st.session_state:
                vet = st.session_state["vet_info"]
                st.write(f"**Nome:** {vet['name']}")
                st.write(f"**CRMV:** {vet['crmv']}")
                st.write(f"**Email:** {vet['email']}")
                st.write(f"**Telefone:** {vet['phone']}")

        if st.session_state.get("logo_path") == "":
            logo_path = get_logo(
                st.session_state["email"], st.session_state["auth_token"])
            st.session_state["logo_path"] = logo_path
        with col2:
            if st.session_state["logo_path"]:
                st.image(st.session_state["logo_path"],
                         width=100, caption="Logo")
                with open(st.session_state["logo_path"], "rb") as logo_file:
                    logo_bytes = logo_file.read()
                encoded_logo = base64.b64encode(logo_bytes).decode('utf-8')
                logo_src = f"data:image/png;base64,{encoded_logo}"

        if st.session_state.get("signature_path") == "":
            signature_path = get_signature(
                st.session_state["email"], st.session_state["auth_token"])
            st.session_state["signature_path"] = signature_path

        with col3:
            if st.session_state["signature_path"]:
                st.image(st.session_state["signature_path"],
                         width=100, caption="signature")
                with open(st.session_state["signature_path"], "rb") as signature_file:
                    signature_bytes = signature_file.read()
                encoded_signature = base64.b64encode(
                    signature_bytes).decode('utf-8')
                signature_src = f"data:image/png;base64,{encoded_signature}"

    if "animal_form_loaded" not in st.session_state:
        st.session_state["animal_form_loaded"] = False

    # Header e formulário
    st.header("Cadastro do Animal e do Tutor")
    with st.expander("Informações do Tutor e Animal", expanded=st.session_state.get("animal_form_loaded")):
        # Preenchendo dados do tutor e animal
        tutor = st.text_input("Tutor", value=st.session_state.get("tutor", ""))
        address = st.text_input(
            "Endereço", value=st.session_state.get("address", ""))
        animal_name = st.text_input(
            "Nome do Animal", value=st.session_state.get("animal_name", ""))
        species = st.text_input(
            "Espécie", value=st.session_state.get("species", ""))
        breed = st.text_input("Raça", value=st.session_state.get("breed", ""))
        age = st.text_input("Idade", value=st.session_state.get("age", ""))
        gender = st.selectbox("Sexo", ["Macho", "Fêmea"], index=[
                              "Macho", "Fêmea"].index(st.session_state.get("gender", "Macho")))
        weight = st.text_input(
            "Peso (kg)", value=st.session_state.get("weight", ""))

        # Apenas registrando o animal quando o botão é clicado
        if st.button("Cadastrar Animal"):
            # Aqui você pode chamar a função `register_animal` para registrar
            # os dados e atualizar o estado da sessão
            tutor_id = register_guardian(
                name=tutor, address=address)
            st.session_state["tutor_id"] = tutor_id
            animal_id = register_animal(
                name=animal_name,
                weight=weight,
                breed=breed,
                gender=gender,
                species=species,
                age=age,
                tutor_id=tutor_id
            )
            st.session_state["animal_id"] = animal_id
            # Atualizando os valores no session_state
            st.session_state["tutor"] = tutor
            st.session_state["address"] = address
            st.session_state["animal_name"] = animal_name
            st.session_state["species"] = species
            st.session_state["breed"] = breed
            st.session_state["age"] = age
            st.session_state["gender"] = gender
            st.session_state["weight"] = weight

        # Indicando que o formulário foi enviado
        st.session_state["animal_form_loaded"] = True

        # Exibindo os dados do animal para o usuário após o envio
    if st.session_state.get("animal_name"):
        st.success("Cadastro do Animal realizado com sucesso!")
        col1, col2 = st.columns(2)
        with col1:
            # Exibe os dados que foram preenchidos no formulário
            st.write("**Dados do Animal Cadastrado:**")
            st.write(f"**Tutor:** {tutor}")
            st.write(f"**Endereço:** {address}")
            st.write(f"**Nome do Animal:** {animal_name}")
        with col2:
            st.write(f"**Espécie:** {species}")
            st.write(f"**Raça:** {breed}")
            st.write(f"**Idade:** {age}")
            st.write(f"**Sexo:** {gender}")
            st.write(f"**Peso:** {weight}")

    # Cadastro de Receita
    st.header("Cadastro da Receita")

    if 'route_count' not in st.session_state:
        st.session_state['route_count'] = 1

    # Buttons to add or remove routes
    col_add, col_remove = st.columns([1, 1])
    with col_add:
        st.button("Adicionar Via", on_click=add_route)
    with col_remove:
        st.button("Remover Via", on_click=remove_route)

    prescriptions = []
    for i in range(st.session_state['route_count']):
        with st.expander(f"Via de Administração {i+1}", expanded=True):
            administration_route = st.text_input(
                f"Via de Administração", key=f'administration_route_{i}')

            # Initialize session state for medications
            if f'med_count_{i}' not in st.session_state:
                st.session_state[f'med_count_{i}'] = 1

            def add_medication(route_index=i):
                st.session_state[f'med_count_{route_index}'] += 1

            def remove_medication(route_index=i):
                if st.session_state[f'med_count_{route_index}'] > 1:
                    st.session_state[f'med_count_{route_index}'] -= 1

            col_add_med, col_remove_med = st.columns([1, 1])
            with col_add_med:
                st.button(f"Adicionar Medicamento na Via {i+1}", key=f'add_med_{i}', on_click=add_medication)
            with col_remove_med:
                st.button(f"Remover Medicamento da Via {i+1}", key=f'remove_med_{i}', on_click=remove_medication)

            medications = []
            for j in range(st.session_state[f'med_count_{i}']):
                st.subheader(f"Medicamento {j+1} na Via {i+1}")
                medication_name = st.text_input(
                    "Nome do Medicamento", key=f'medication_name_{i}_{j}')
                quantity = st.text_input("Quantidade", key=f'quantity_{i}_{j}')
                dosage = st.text_area("Posologia", key=f'dosage_{i}_{j}')
                medications.append({
                    'medication_name': medication_name,
                    'quantity': quantity,
                    'dosage': dosage
                })
            prescriptions.append({
                'administration_route': administration_route,
                'medications': medications
            })
            st.session_state["prescriptions"] = prescriptions
        medicines_ids = []
        if st.button("Cadastrar Prescrição"):
            if not prescriptions:
                st.error("Nenhuma prescrição foi adicionada.")
            else:
                st.success("Prescrição cadastrada com sucesso!")
                st.write("**Detalhes da Prescrição:**")
                for idx, prescription in enumerate(prescriptions, start=1):
                    st.write(
                        f"**Via de Administração {idx}:** {prescription['administration_route']}")
                    for med_idx, medication in enumerate(prescription['medications'], start=1):
                        medicines_ids.append(register_medicine(
                            medication['medication_name'], medication['quantity'], medication['dosage']))
                        
                        st.write(f"  - **Medicamento {med_idx}:**")
                        st.write(f"    Nome: {medication['medication_name']}")
                        st.write(f"    Quantidade: {medication['quantity']}")
                        st.write(f"    Posologia: {medication['dosage']}")
                tutor_id = st.session_state.get("tutor_id")
                animal_id = st.session_state.get("animal_id")
                prescription_id = register_prescription(vet["id"],tutor_id,animal_id,medicines_ids)

    # Geração de PDF
    if st.button("Gerar PDF"):
        with open('templates/template.html', 'r', encoding='utf-8') as file:
            html_template = file.read()

        template = Template(html_template)
        html_filled = template.render(
            crmv=vet['crmv'],
            phone=vet['phone'],
            email=vet['email'],
            veterinarian_name=vet['name'],
            tutor=tutor,
            address=address,
            animal_name=animal_name,
            species=species,
            breed=breed,
            age=age,
            gender=gender,
            weight=weight,
            logo_src=logo_src or "https://via.placeholder.com/200x200.png?text=Logo",
            signature_src=signature_src or "https://via.placeholder.com/200x200.png?text=Logo",
            prescriptions=st.session_state.get("prescriptions")
        )

        pdf_file = HTML(string=html_filled).write_pdf()
        b64 = base64.b64encode(pdf_file).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="receita_{animal_name}.pdf">Clique aqui para baixar o PDF</a>'
        st.markdown(href, unsafe_allow_html=True)
