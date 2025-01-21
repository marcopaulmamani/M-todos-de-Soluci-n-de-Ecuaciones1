import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración general de la página
st.set_page_config(page_title="Solución de Ecuaciones Lineales", page_icon="🧮", layout="wide")

# Función para calcular el determinante
def determinante(matrix):
    return np.linalg.det(matrix)

# Método de Cramer
def metodo_cramer(A, b):
    A_inv = np.linalg.inv(A)
    x = np.dot(A_inv, b)
    return x

# Método de Jordan
def metodo_jordan(A, b):
    n = len(A)
    augmented_matrix = np.hstack((A, b.reshape(-1, 1)))
    
    for i in range(n):
        augmented_matrix[i] = augmented_matrix[i] / augmented_matrix[i, i]
        for j in range(n):
            if i != j:
                factor = augmented_matrix[j, i]
                augmented_matrix[j] -= factor * augmented_matrix[i]
    
    return augmented_matrix[:, -1]

# Método de sustitución
def metodo_sustitucion(A, b):
    n = len(A)
    x = np.zeros(n)
    
    for i in range(n):
        sum = b[i]
        for j in range(i):
            sum -= A[i][j] * x[j]
        x[i] = sum / A[i][i]
    
    return x

# Título principal con estilo
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Métodos de Solución de Ecuaciones</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: gray;'>MÉTODOS DE OPTIMIZACIÓN</h2>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; font-size: 16px;">
Bienvenido al sistema de resolución de ecuaciones lineales. Selecciona un método y proporciona los datos para resolver tu sistema.
</div>
""", unsafe_allow_html=True)

# Separador decorativo
st.markdown("---")

# Sidebar con opciones
st.sidebar.header("Configuración")
metodo = st.sidebar.radio("Selecciona un Método", ("Método de Cramer", "Método de Jordan", "Método de Sustitución"))
n = st.sidebar.number_input("Número de variables (n)", min_value=2, max_value=10, value=3)

# Entrada dinámica de datos
st.sidebar.subheader("Ingresa los datos")
def ingresar_matriz(n):
    matriz = []
    for i in range(n):
        row = st.sidebar.text_input(f"Fila {i+1} de A (valores separados por espacio)", key=f"row_{i}")
        if row:
            matriz.append(list(map(float, row.split())))
    return matriz

def ingresar_vector_b(n):
    b_input = st.sidebar.text_input("Vector de resultados b (valores separados por espacio)", key="vector_b")
    if b_input:
        return list(map(float, b_input.split()))
    return []

A = ingresar_matriz(n)
b = ingresar_vector_b(n)

# Información del método seleccionado
if metodo == "Método de Cramer":
    st.subheader("Calculadora Método de Cramer")
    st.markdown("""
    El **Método de Cramer** utiliza determinantes para resolver sistemas lineales. Resuelve ecuaciones con:
    \\[
    x_i = \\frac{det(A_i)}{det(A)}
    \\]
    """, unsafe_allow_html=True)

elif metodo == "Método de Jordan":
    st.subheader("Calculadora Método de Jordan")
    st.markdown("""
    El **Método de Jordan** usa la eliminación Gauss-Jordan para transformar la matriz en su forma escalonada reducida.
    """, unsafe_allow_html=True)

else:
    st.subheader("Calculadora Método de Sustitución")
    st.markdown("""
    El **Método de Sustitución** despeja variables de una en una, sustituyéndolas en las demás ecuaciones.
    """)

# Botón para calcular
col1, col2 = st.columns([1, 3])

if st.button("Calcular Solución"):
    if len(A) == n and len(b) == n:
        A = np.array(A)
        b = np.array(b)

        # Validar y calcular
        if metodo == "Método de Cramer":
            if determinante(A) != 0:
                resultado = metodo_cramer(A, b)
                col1.success("¡Solución encontrada!")
                col2.write("Resultado (Método de Cramer):")
                col2.write(resultado)
            else:
                col1.error("El determinante es cero. No hay solución única.")

        elif metodo == "Método de Jordan":
            resultado = metodo_jordan(A, b)
            col1.success("¡Solución encontrada!")
            col2.write("Resultado (Método de Jordan):")
            col2.write(resultado)

        elif metodo == "Método de Sustitución":
            resultado = metodo_sustitucion(A, b)
            col1.success("¡Solución encontrada!")
            col2.write("Resultado (Método de Sustitución):")
            col2.write(resultado)

        # Gráfico
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(range(1, n + 1), resultado, color="#4CAF50", alpha=0.7)
        ax.set_title("Resultados de las Variables", fontsize=14)
        ax.set_xlabel("Variables", fontsize=12)
        ax.set_ylabel("Valor", fontsize=12)
        ax.set_xticks(range(1, n + 1))
        ax.grid(alpha=0.3)
        st.pyplot(fig)
    else:
        st.error("Por favor, ingresa correctamente la matriz A y el vector b.")
else:
    st.info("Introduce los datos en la barra lateral y presiona 'Calcular Solución'.")
