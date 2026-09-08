# Accesibilidad web para personas ciegas en contenidos digitales del Boletín Oficial de la UNMDP

Repositorio asociado a la tesina de grado de la **Licenciatura en Gestión Universitaria**, Facultad de Ciencias Económicas y Sociales, Universidad Nacional de Mar del Plata (UNMDP).

## Tema de la tesina

**“Accesibilidad web para personas ciegas en contenidos digitales del Boletín Oficial de la UNMDP”**

El trabajo analiza la accesibilidad de los contenidos digitales publicados en el **Boletín Oficial de la UNMDP** durante el ciclo académico 2025, considerando el marco normativo aplicable, las acciones institucionales relacionadas con la accesibilidad digital y las barreras que pueden experimentar las personas ciegas al acceder a dichos contenidos.

## Objetivo general

Analizar la accesibilidad de los contenidos digitales publicados en el Boletín Oficial de la UNMDP durante el ciclo académico 2025, considerando el marco normativo aplicable, las acciones institucionales y las barreras de acceso que pueden experimentar las personas ciegas.

## Objetivos específicos

* Caracterizar el marco normativo nacional y de la UNMDP relacionado con la accesibilidad digital.
* Describir las acciones institucionales destinadas a promover la accesibilidad de los contenidos digitales para personas ciegas.
* Identificar y analizar las barreras de navegación, lectura e interacción que pueden presentarse al acceder a los contenidos digitales del Boletín Oficial de la UNMDP.
* Aplicar procedimientos automatizados y manuales para obtener evidencia sobre determinados aspectos de accesibilidad de las páginas web y documentos PDF analizados.
* Sistematizar los resultados obtenidos mediante herramientas de consolidación que permitan facilitar su análisis e interpretación.

## Marco normativo y técnico

### Marco normativo argentino

El análisis se desarrolla considerando el marco normativo argentino relacionado con la accesibilidad de la información en páginas web.

Entre las normas de referencia se encuentra la **Ley 26.653 de Accesibilidad de la Información en las Páginas Web**, su reglamentación mediante el **Decreto 656/2019** y la **Disposición ONTI 6/2019**.

La Disposición ONTI 6/2019 aprueba las **Pautas de Accesibilidad de Contenido Web 2.0** y los correspondientes criterios de conformidad adoptados por la República Argentina. La disposición establece un conjunto de 38 criterios de conformidad y determina niveles mínimos de cumplimiento para los organismos alcanzados por la normativa.

La elección de **WCAG 2.1** como marco técnico para el análisis de esta investigación responde a la necesidad de disponer de un conjunto de criterios técnicos actualizado respecto de las pautas adoptadas por la normativa argentina, manteniendo a su vez la referencia normativa nacional establecida por la ONTI.

Por lo tanto, en esta investigación se diferencia entre:

* **marco normativo nacional:** Disposición ONTI 6/2019 y normativa relacionada;
* **marco técnico utilizado para el análisis:** WCAG 2.1.

Esta distinción permite utilizar WCAG 2.1 como referencia técnica sin atribuir a la Disposición ONTI 6/2019 la adopción normativa de dicha versión.

### Selección de criterios WCAG 2.1

El análisis se concentra en criterios de conformidad **WCAG 2.1 de niveles A y AA**, seleccionados por su pertinencia para estudiar aspectos relacionados con la percepción, comprensión, navegación e interacción de los contenidos digitales desde la perspectiva de personas ciegas.

La evaluación no pretende determinar la conformidad integral de los contenidos con la totalidad de WCAG 2.1, sino analizar los criterios seleccionados para los objetivos específicos de la investigación.

> **Nota metodológica:** los resultados producidos por las herramientas automatizadas constituyen evidencia de apoyo para el análisis de accesibilidad. No deben interpretarse como una certificación automática de conformidad WCAG. Los criterios que requieren apreciación humana deben complementarse mediante evaluación manual y, cuando corresponde, pruebas con lectores de pantalla.

## Herramientas desarrolladas

El repositorio contiene scripts y herramientas HTML desarrollados específicamente para automatizar parte de la evaluación y sistematizar los resultados obtenidos durante la investigación.

---

## 1. Evaluación automatizada de contenidos HTML

**Archivo:** `evaluar_wcag_ceguera_v3.py`

Script desarrollado en **Python 3.7 o superior**, utilizando principalmente bibliotecas de la biblioteca estándar de Python.

El script procesa las URL de los contenidos del Boletín Oficial incluidas en su código. Para el procesamiento de las páginas HTML utiliza `HTMLParser`, permitiendo identificar y analizar distintos elementos de la estructura de los documentos.

La herramienta implementa una evaluación automatizada de determinados aspectos correspondientes a **13 criterios WCAG 2.1 de niveles A y AA**, seleccionados para el análisis de accesibilidad desde la perspectiva de personas ciegas.

Los criterios contemplados por el script son:

| Criterio                       | Nivel | Modalidad prevista      |
| ------------------------------ | ----: | ----------------------- |
| 1.1.1 Contenido no textual     |     A | Automatizada            |
| 1.3.1 Información y relaciones |     A | Automatizada            |
| 1.3.2 Secuencia significativa  |     A | Manual                  |
| 1.4.5 Imágenes de texto        |    AA | Automatizada/heurística |
| 2.4.1 Evitar bloques           |     A | Automatizada            |
| 2.4.2 Página titulada          |     A | Automatizada            |
| 2.4.3 Orden del foco           |     A | Manual                  |
| 2.4.4 Propósito de los enlaces |     A | Automatizada/manual     |
| 2.4.6 Encabezados y etiquetas  |    AA | Automatizada            |
| 3.1.1 Idioma de la página      |     A | Automatizada            |
| 3.1.2 Idioma de las partes     |    AA | Manual                  |
| 4.1.1 Procesamiento            |     A | Automatizada            |
| 4.1.2 Nombre, función, valor   |     A | Automatizada            |

En aquellos casos en los que el criterio requiere apreciación humana, el procedimiento contempla la realización de pruebas mediante **NVDA (NonVisual Desktop Access)**.

La evaluación automatizada debe interpretarse como una identificación preliminar de determinados aspectos del contenido y no como una comprobación exhaustiva de la conformidad WCAG.

### Consideración sobre el criterio 1.4.5

En el caso del criterio **1.4.5 – Imágenes de texto**, el procedimiento implementado realiza una identificación heurística de posibles situaciones relacionadas con imágenes que contienen texto.

Por tratarse de una detección automatizada, los resultados deben ser posteriormente interpretados teniendo en cuenta el contexto del contenido y las excepciones contempladas por WCAG 2.1.

### Consideración sobre 4.1.1 y 4.1.2

El análisis HTML mantiene los criterios 4.1.1 y 4.1.2 debido a que el trabajo utiliza **WCAG 2.1** como marco técnico.

En la documentación actualizada de WCAG, W3C señala que 4.1.1 *Parsing* debe considerarse siempre satisfecho para contenido HTML o XML desde el punto de vista de la conformidad y que posteriormente fue eliminado de WCAG 2.2. El criterio 4.1.2 *Name, Role, Value* continúa siendo un criterio de nivel A en WCAG 2.1.

Por este motivo, los resultados correspondientes a estos criterios deben interpretarse dentro del contexto de **WCAG 2.1**, que es el marco técnico adoptado para esta investigación.

---

## 2. Consolidación de resultados de la evaluación HTML

**Archivo:** `consolidador_wcag_ceguera_v4.html`

Herramienta HTML destinada a consolidar los resultados obtenidos mediante la evaluación automatizada y las verificaciones manuales.

Permite:

* cargar archivos CSV con resultados automatizados;
* incorporar resultados de evaluaciones manuales;
* asociar los resultados a los documentos evaluados;
* obtener indicadores globales;
* visualizar los resultados mediante gráficos;
* consultar los resultados por criterio;
* distinguir entre resultados de cumplimiento, incumplimiento, resultados parciales y casos no evaluados;
* exportar los resultados consolidados.

La herramienta admite tanto resultados provenientes de archivos CSV como la incorporación manual de resultados para los criterios que requieren verificación humana.
La herramienta contempla los mismos **13 criterios WCAG 2.1** utilizados en la evaluación HTML.

---

# Evaluación de documentos PDF

## 3. Evaluación automatizada de documentos PDF

**Archivo:** `evaluar_pdf_pdfa_wcag_ultimo.py`

Este script permite procesar los documentos PDF seleccionados para el análisis a partir de las URL correspondientes al Boletín Oficial.

El procedimiento se desarrolla en tres etapas principales.

### Etapa 1 — Descarga de documentos

El script identifica y descarga los archivos PDF correspondientes a las URL analizadas y los almacena localmente para su procesamiento posterior.

También verifica que el archivo descargado corresponda efectivamente a un documento PDF antes de continuar con la evaluación.

### Etapa 2 — Validación mediante veraPDF

Los documentos son procesados mediante **veraPDF**, utilizando el perfil **PDF/A-1a**, correspondiente a la familia de estándares PDF/A definida por ISO 19005.

La validación permite obtener información sobre el cumplimiento de determinadas reglas y comprobaciones estructurales del documento PDF.

### Etapa 3 — Procesamiento y mapeo metodológico

Los resultados generados por veraPDF son procesados por el script para identificar reglas y comprobaciones que presentan incumplimientos.

A partir de determinados resultados se realiza un **mapeo metodológico hacia criterios WCAG 2.1 seleccionados**.

Por lo tanto, el procedimiento utilizado puede representarse de la siguiente manera:

```text
Documento PDF
     ↓
Validación mediante veraPDF
     ↓
Perfil PDF/A-1a
     ↓
Identificación de reglas y comprobaciones fallidas
     ↓
Mapeo metodológico
     ↓
Criterios WCAG 2.1 seleccionados
```

Es importante señalar que **veraPDF no realiza directamente una evaluación de conformidad con WCAG 2.1**. Su función dentro de este trabajo consiste en validar determinados aspectos del documento conforme al perfil PDF/A utilizado.

El vínculo entre los resultados PDF/A y los criterios WCAG constituye, por lo tanto, un **procedimiento metodológico implementado específicamente para esta investigación**, y no debe interpretarse como una equivalencia normativa entre PDF/A y WCAG.

El propio procedimiento utiliza correspondencias entre resultados relacionados con el modelo Matterhorn, cláusulas de PDF/A y criterios WCAG seleccionados.

### Criterios analizados en los documentos PDF

La evaluación PDF utiliza un conjunto específico de correspondencias entre resultados de la validación PDF/A y criterios WCAG 2.1.

Este conjunto **no debe confundirse con los 13 criterios utilizados en la evaluación HTML**, ya que ambos procedimientos tienen implementaciones y alcances diferentes.

En consecuencia:

> La evaluación HTML utiliza 13 criterios WCAG 2.1 seleccionados, mientras que la evaluación PDF utiliza un subconjunto de criterios mediante un procedimiento específico de mapeo entre resultados de la validación PDF/A y criterios WCAG.

Esta diferenciación permite evitar la interpretación de que ambos procedimientos realizan exactamente la misma evaluación.

### Alcance del análisis PDF

Los resultados de la evaluación PDF permiten identificar determinadas características estructurales de los documentos, como el etiquetado, información de idioma, metadatos, estructura y otros aspectos contemplados en las reglas utilizadas para el mapeo. Por ejemplo, el código establece correspondencias relacionadas con el etiquetado del documento, la secuencia del contenido y el idioma.
Sin embargo, estos resultados **no permiten por sí solos determinar la experiencia real de lectura o navegación de una persona ciega**.

Por esta razón, los resultados automatizados deben considerarse evidencia técnica complementaria al análisis cualitativo y, cuando corresponda, a las pruebas mediante tecnologías de asistencia.

---

## 4. Consolidación de resultados PDF

**Archivo:** `consolidador_pdf_pdfa_ultimo.html`

Herramienta HTML destinada a consolidar y visualizar los resultados generados por el script de evaluación PDF.

La herramienta recibe el archivo `resultados_pdf_wcag.csv` y permite visualizar:

* cantidad de documentos evaluados;
* porcentaje y cantidad de documentos que cumplen;
* porcentaje y cantidad de documentos con cumplimiento parcial;
* documentos que no cumplen;
* resultados N/A o con error;
* cantidad total de reglas PDF/A fallidas;
* cantidad total de comprobaciones fallidas;
* porcentaje de cumplimiento por criterio WCAG;
* distribución global de los resultados;
* detalle de los resultados por documento;
* estado de los criterios WCAG asociados a cada documento.

La herramienta genera un gráfico de cumplimiento por criterio y un gráfico de distribución global de los documentos.

También presenta una tabla detallada por documento con el estado global, la conformidad PDF/A, las reglas y comprobaciones fallidas y los resultados correspondientes a los criterios WCAG incluidos en el CSV.

---

# Diferenciación entre las evaluaciones HTML y PDF

Las herramientas desarrolladas para el análisis de contenidos HTML y documentos PDF cumplen funciones relacionadas, pero no equivalentes.

| Aspecto               | Contenidos HTML                     | Documentos PDF                                   |
| --------------------- | ----------------------------------- | ------------------------------------------------ |
| Archivo principal     | `evaluar_wcag_ceguera_v3.py`        | `evaluar_pdf_pdfa_wcag_ultimo.py`                |
| Tecnología            | Python                              | Python + veraPDF                                 |
| Marco técnico         | WCAG 2.1                            | PDF/A-1a + mapeo metodológico a WCAG 2.1         |
| Cantidad de criterios | 13 criterios seleccionados          | Subconjunto de criterios mediante mapeo          |
| Evaluación manual     | Sí                                  | Complementaria                                   |
| Lector de pantalla    | NVDA                                | Puede utilizarse como complemento                |
| Resultado principal   | Resultados por criterio WCAG        | PDF/A + reglas/checks + criterios WCAG asociados |
| Consolidación         | `consolidador_wcag_ceguera_v4.html` | `consolidador_pdf_pdfa_ultimo.html`              |

Esta diferenciación constituye una decisión metodológica del trabajo y evita considerar que la validación PDF/A sea, por sí misma, una evaluación WCAG.

---

# Criterios metodológicos

Las herramientas desarrolladas en este repositorio tienen como finalidad **automatizar parte del proceso de evaluación y sistematizar evidencia para la investigación**.

No sustituyen la evaluación humana de accesibilidad.

La evaluación automatizada presenta limitaciones inherentes: determinados aspectos de accesibilidad solamente pueden determinarse mediante inspección humana, análisis del contexto, navegación con teclado, utilización de lectores de pantalla y valoración de la experiencia de uso.

Por este motivo, los resultados obtenidos mediante los scripts deben interpretarse conjuntamente con:

* evaluación manual;
* revisión de la estructura y del contenido;
* pruebas de navegación;
* pruebas mediante lectores de pantalla cuando corresponda;
* análisis del contexto de cada contenido;
* interpretación de los resultados dentro del marco metodológico de la tesina.

La ONTI también señala que sus recomendaciones y herramientas sirven como apoyo para favorecer el cumplimiento de las normas, pero no sustituyen las propias normas ni aseguran por sí mismas su cumplimiento.

---

# Limitaciones

Los procedimientos implementados presentan las siguientes limitaciones:

* La evaluación automatizada no permite determinar por sí sola la accesibilidad integral de un contenido.
* La identificación automática de determinados problemas puede requerir interpretación humana.
* Los resultados HTML corresponden a los criterios WCAG 2.1 seleccionados para la investigación y no a la totalidad de WCAG 2.1.
* La evaluación PDF no constituye una evaluación directa de WCAG por parte de veraPDF.
* El mapeo entre resultados PDF/A y criterios WCAG constituye un procedimiento metodológico aplicado en esta investigación.
* La validación PDF/A no permite determinar por sí sola la experiencia de lectura de una persona ciega.
* Los resultados deben interpretarse en conjunto con las evaluaciones manuales y el análisis desarrollado en la tesina.

En consecuencia, los resultados producidos por estas herramientas **no deben interpretarse como una certificación oficial de accesibilidad ni como una declaración general de conformidad WCAG**.

---

# Reproducibilidad

Las herramientas fueron desarrolladas para ejecutarse en un entorno Linux.

## Evaluación HTML

### Requisitos

* Linux.
* Python 3.7 o superior.
* No requiere la instalación de paquetes externos para el funcionamiento del script.

### Ejecución

```bash
python3 evaluar_wcag_ceguera_v3.py
```

El script procesa las URL definidas en su código y genera los archivos de resultados correspondientes.

## Evaluación PDF

### Requisitos

* Linux.
* Python 3.7 o superior.
* veraPDF instalado y disponible para su ejecución desde el sistema.

### Ejecución

```bash
python3 evaluar_pdf_pdfa_wcag_ultimo.py
```

El script descarga los documentos, ejecuta la validación mediante veraPDF, procesa los resultados y genera los archivos de salida.

---

# Estructura del repositorio

```text
.
├── evaluar_wcag_ceguera_v3.py
├── consolidador_wcag_ceguera_v4.html
├── evaluar_pdf_pdfa_wcag_ultimo.py
├── consolidador_pdf_pdfa_ultimo.html
└── README.md
```

---

# Referencias normativas y técnicas

* **Ley 26.653** — Accesibilidad de la Información en las Páginas Web.
* **Decreto 656/2019** — Reglamentación de la Ley 26.653.
* **Disposición ONTI 6/2019** — Pautas de Accesibilidad de Contenido Web 2.0 y criterios de conformidad adoptados por la República Argentina.
* **WCAG 2.1 — Web Content Accessibility Guidelines**, World Wide Web Consortium (W3C).
* **ISO 19005 — PDF/A**, utilizada como referencia para la validación de los documentos PDF mediante veraPDF.
* **Matterhorn Protocol**, utilizado como referencia para las correspondencias metodológicas aplicadas en el análisis de los documentos PDF.
* **NVDA — NonVisual Desktop Access**, utilizado para las pruebas manuales de navegación y lectura mediante lector de pantalla.

---

# Autoría
Técnicos Marcelo Alejandro Algamiz y Edgardo Damián Emiliano
Repositorio desarrollado como parte de la tesina de grado de la **Licenciatura en Gestión Universitaria**, Facultad de Ciencias Económicas y Sociales, Universidad Nacional de Mar del Plata.
