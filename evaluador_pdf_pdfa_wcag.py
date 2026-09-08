#!/usr/bin/env python3
# =============================================================================
# evaluar_pdf_pdfa_wcag.py  v3
# Evaluación por lote de PDFs — veraPDF perfil PDF/A-1a (ISO 19005-1:2005)
# Criterios WCAG 2.1 mapeados via Protocolo Matterhorn
# Cláusulas ISO 19005-1 confirmadas con veraPDF 1.30.2
# Boletín Oficial UNMdP — Tesina LGU — Algamiz & Emiliano 2025/2026
#
# USO:   python evaluar_pdf_pdfa_wcag.py
# REQUISITOS: Python 3.7+ y veraPDF en el PATH
# SALIDA:
#   pdfs/                    PDFs descargados
#   resultados_pdf_wcag.csv  para importar al consolidador HTML
#   resultados_pdf_wcag.txt  reporte legible
# =============================================================================

import urllib.request, subprocess, xml.etree.ElementTree as ET
import csv, os, re, time, sys
from datetime import datetime
from html.parser import HTMLParser

DOCUMENTOS = [
    ("92309",      "https://digesto.mdp.edu.ar/archivos/92309.pdf",                     "pdf"),
    ("92383",      "https://digesto.mdp.edu.ar/archivos/92383.pdf",                     "pdf"),
    ("94838",      "https://digesto.mdp.edu.ar/archivos/94838.pdf",                     "pdf"),
    ("94881",      "https://digesto.mdp.edu.ar/archivos/94881.pdf",                     "pdf"),
    ("95518",      "https://digesto.mdp.edu.ar/archivos/95518.pdf",                     "pdf"),
    ("95638",      "https://digesto.mdp.edu.ar/archivos/95638.pdf",                     "pdf"),
    ("96549",      "https://digesto.mdp.edu.ar/archivos/96549.pdf",                     "pdf"),
    ("96731",      "https://digesto.mdp.edu.ar/archivos/96731.pdf",                     "pdf"),
    ("97706",      "https://digesto.mdp.edu.ar/archivos/97706.pdf",                     "pdf"),
    ("97815",      "https://digesto.mdp.edu.ar/archivos/97815.pdf",                     "pdf"),
    ("98047",      "https://digesto.mdp.edu.ar/archivos/98047.pdf",                     "pdf"),
    ("98353",      "https://digesto.mdp.edu.ar/archivos/98353.pdf",                     "pdf"),
    ("99132",      "https://digesto.mdp.edu.ar/archivos/99132.pdf",     		"pdf"),
    ("99216",      "https://digesto.mdp.edu.ar/archivos/99216.pdf",                     "pdf"),
    ("100361",     "https://digesto.mdp.edu.ar/archivos/100361.pdf",                    "pdf"),
    ("100631",     "https://digesto.mdp.edu.ar/archivos/100631.pdf",                    "pdf"),
    ("102085",     "https://digesto.mdp.edu.ar/archivos/102085.pdf",                    "pdf"),
    ("102148",     "https://digesto.mdp.edu.ar/archivos/102148.pdf",                    "pdf"),
    ("102161",     "https://digesto.mdp.edu.ar/archivos/102161.pdf",                    "pdf"),
    ("102522",     "https://digesto.mdp.edu.ar/archivos/102522.pdf",                    "pdf"),
    ("102797",     "https://digesto.mdp.edu.ar/archivos/102797.pdf",                    "pdf"),
    ("103295",     "https://digesto.mdp.edu.ar/archivos/103295.pdf",                    "pdf"),
]

FLAVOUR      = "1a"
FLAVOUR_NOME = "PDF/A-1a"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/pdf,text/html,*/*;q=0.8",
    "Accept-Language": "es-AR,es;q=0.9",
}

# =============================================================================
# MAPEO WCAG ↔ MATTERHORN ↔ CLÁUSULAS ISO 19005-1:2005
# Cláusulas confirmadas con veraPDF 1.30.2 sobre documentos reales del BO.
#
# Estructura ISO 19005-1:
#   6.1     Requisitos generales de conformidad
#   6.2     Gráficos (imágenes, espacios de color)
#   6.2.3.3 Espacios de color DeviceRGB/CMYK sin perfil ICC embebido
#   6.3     Fuentes
#   6.3.4   Fuentes no embebidas en el archivo
#   6.4     Transparencia y efectos visuales
#   6.5     Anotaciones
#   6.6     Acciones
#   6.7     Metadatos XMP
#   6.7.2   Ausencia o malformación del stream de metadatos XMP
#   6.7.3   Entradas obligatorias en metadatos XMP (título, fechas, etc.)
#   6.7.11  Idioma del documento en el catálogo (Lang entry)
#   6.8     Estructura lógica y etiquetado (Tagged PDF)
#   6.8.2   MarkInfo — documento etiquetado
#   6.8.3   Estructura lógica completa (árbol de etiquetas)
#   6.8.4   Orden de lectura y mapeo de caracteres
#   6.9     Contenido alternativo (texto alternativo en figuras)
#
# NOTA METODOLÓGICA:
#   Las cláusulas 6.2.3.3, 6.3.4, 6.4, 6.7.2, 6.7.3 corresponden a
#   requisitos técnicos de preservación (colores, fuentes, metadatos) que
#   NO tienen correlato directo con los criterios WCAG de accesibilidad para
#   ceguera total, por lo que se reportan como "No aplica" en el mapeo WCAG.
# =============================================================================

CRITERIOS_WCAG = [
    {
        "wcag":               "1.1.1",
        "nivel":              "A",
        "nombre_wcag":        "Contenido no textual",
        "matterhorn":         "14-001",
        "clausulas":          {"6.9"},
        "descripcion":        (
            "Todo elemento gráfico o imagen debe tener texto alternativo "
            "que describa su contenido. Sin esta descripción, el lector de "
            "pantalla omite la imagen sin informar al usuario ciego."
        ),
        "descripcion_matterhorn": (
            "14-001: Los elementos de tipo Figura deben tener texto alternativo "
            "definido en el atributo /Alt de su etiqueta de estructura."
        ),
    },
    {
        "wcag":               "1.3.1",
        "nivel":              "A",
        "nombre_wcag":        "Información y relaciones",
        "matterhorn":         "01-001 / 01-002",
        "clausulas":          {"6.8.2", "6.8.3"},
        "descripcion":        (
            "El documento debe estar completamente etiquetado (Tagged PDF) "
            "con una estructura lógica que refleje la jerarquía del contenido. "
            "Sin etiquetado, el lector de pantalla no puede identificar "
            "títulos, párrafos, listas ni tablas."
        ),
        "descripcion_matterhorn": (
            "01-001 / 01-002: El documento completo debe estar marcado como "
            "Etiquetado (Tagged PDF) en el diccionario MarkInfo del catálogo."
        ),
    },
    {
        "wcag":               "1.3.2",
        "nivel":              "A",
        "nombre_wcag":        "Secuencia significativa",
        "matterhorn":         "01-006",
        "clausulas":          {"6.8.3", "6.8.4"},
        "descripcion":        (
            "El orden de lectura definido en el árbol de etiquetas debe "
            "coincidir con el orden visual y semántico del contenido. "
            "Un orden incorrecto hace que el lector de pantalla lea el "
            "documento en una secuencia sin sentido."
        ),
        "descripcion_matterhorn": (
            "01-006: El orden de lectura en el árbol de etiquetas del PDF "
            "debe coincidir con el significado lógico del contenido."
        ),
    },
    {
        "wcag":               "1.4.5",
        "nivel":              "AA",
        "nombre_wcag":        "Imágenes de texto",
        "matterhorn":         "14-002",
        "clausulas":          {"6.9", "6.8.3"},
        "descripcion":        (
            "No se debe presentar texto mediante imágenes escaneadas sin "
            "incluir el texto real en la estructura del documento. Un PDF "
            "escaneado sin capa de texto subyacente es completamente "
            "ilegible para el lector de pantalla."
        ),
        "descripcion_matterhorn": (
            "14-002: Está prohibido usar texto escaneado dentro de una imagen "
            "sin su texto real estructurado en el árbol de etiquetas."
        ),
    },
    {
        "wcag":               "2.4.1",
        "nivel":              "A",
        "nombre_wcag":        "Saltar bloques",
        "matterhorn":         "09-001",
        "clausulas":          {"6.8.3"},
        "descripcion":        (
            "El documento debe usar etiquetas de encabezado (H1 a H6) que "
            "permitan al lector de pantalla navegar directamente entre "
            "secciones, omitiendo bloques de contenido repetido o no relevante."
        ),
        "descripcion_matterhorn": (
            "09-001: Obligación de usar etiquetas de encabezado (H1 a H6) "
            "para permitir la navegación estructural rápida entre secciones."
        ),
    },
    {
        "wcag":               "2.4.2",
        "nivel":              "A",
        "nombre_wcag":        "Título de página",
        "matterhorn":         "06-002",
        "clausulas":          {"6.7.3"},
        "descripcion":        (
            "El título del documento debe estar definido en los metadatos "
            "del archivo. El lector de pantalla anuncia este título al abrir "
            "el PDF; su ausencia impide identificar el documento sin explorar "
            "su contenido."
        ),
        "descripcion_matterhorn": (
            "06-002: El título del documento debe estar explícitamente "
            "definido en las propiedades de metadatos del archivo PDF."
        ),
    },
    {
        "wcag":               "2.4.3",
        "nivel":              "A",
        "nombre_wcag":        "Orden de foco",
        "matterhorn":         "01-005",
        "clausulas":          {"6.8.3", "6.8.4"},
        "descripcion":        (
            "El orden de tabulación entre elementos interactivos (enlaces, "
            "campos de formulario) debe ser lógico y coherente. Un orden "
            "de foco incorrecto desorienta al usuario ciego al navegar "
            "con teclado entre los elementos del documento."
        ),
        "descripcion_matterhorn": (
            "01-005: El orden de tabulación de las anotaciones o enlaces "
            "interactivos debe ser lógico y preservar el significado."
        ),
    },
    {
        "wcag":               "2.4.4",
        "nivel":              "A",
        "nombre_wcag":        "Propósito de los enlaces",
        "matterhorn":         "18-001",
        "clausulas":          {"6.8.3"},
        "descripcion":        (
            "Las etiquetas de los hipervínculos deben describir de manera "
            "comprensible la acción o el destino del enlace. Textos genéricos "
            "como 'clic aquí' o 'ver más' no permiten al usuario ciego "
            "entender el propósito del enlace sin leer el contexto."
        ),
        "descripcion_matterhorn": (
            "18-001: Las etiquetas de los hipervínculos deben describir "
            "claramente la acción o el destino al que apuntan."
        ),
    },
    {
        "wcag":               "2.4.6",
        "nivel":              "AA",
        "nombre_wcag":        "Encabezados y etiquetas",
        "matterhorn":         "09-003",
        "clausulas":          {"6.8.3"},
        "descripcion":        (
            "Los niveles de encabezado deben seguir una jerarquía progresiva "
            "sin saltos artificiales. Pasar de H1 directamente a H4 rompe la "
            "estructura que el lector de pantalla usa para anunciar la "
            "organización del documento."
        ),
        "descripcion_matterhorn": (
            "09-003: Los niveles de encabezado no deben tener saltos "
            "artificiales (por ejemplo, pasar de H1 directamente a H4)."
        ),
    },
    {
        "wcag":               "3.1.1",
        "nivel":              "A",
        "nombre_wcag":        "Idioma de la página",
        "matterhorn":         "11-001",
        "clausulas":          {"6.7.11"},
        "descripcion":        (
            "El diccionario raíz del catálogo del PDF debe declarar el "
            "idioma principal del documento. El lector de pantalla usa esta "
            "declaración para seleccionar el sintetizador de voz correcto; "
            "su ausencia produce pronunciación incorrecta del texto."
        ),
        "descripcion_matterhorn": (
            "11-001: El diccionario raíz del catálogo del PDF debe declarar "
            "el idioma principal del archivo (ej. es-AR)."
        ),
    },
    {
        "wcag":               "3.1.2",
        "nivel":              "AA",
        "nombre_wcag":        "Idioma de las partes",
        "matterhorn":         "11-002",
        "clausulas":          {"6.8.3"},
        "descripcion":        (
            "Los fragmentos de texto redactados en un idioma diferente al "
            "declarado para el documento deben tener asignado su propio "
            "atributo de lenguaje. Sin esta marca, el lector de pantalla "
            "los pronuncia con las reglas fonéticas del idioma principal."
        ),
        "descripcion_matterhorn": (
            "11-002: Los fragmentos de texto en un idioma secundario deben "
            "tener asignado su propio atributo de lenguaje en la etiqueta."
        ),
    },
    {
        "wcag":               "4.1.2",
        "nivel":              "A",
        "nombre_wcag":        "Nombre, función, valor",
        "matterhorn":         "05-001",
        "clausulas":          {"6.8.3", "6.8.5"},
        "descripcion":        (
            "Las tablas deben tener sus filas, columnas y celdas de "
            "encabezado correctamente marcadas con etiquetas semánticas. "
            "Sin esta estructura, el lector de pantalla no puede relacionar "
            "cada celda con su encabezado correspondiente."
        ),
        "descripcion_matterhorn": (
            "05-001: Las filas, columnas y celdas de encabezado de las "
            "tablas deben estar técnicamente marcadas de forma correcta."
        ),
    },
]

# Índice cláusula → criterios WCAG (para lookup rápido)
# Usamos prefijo: "6.8" cubre "6.8.2", "6.8.3", etc.
def clausula_coincide(clausula_real, clausulas_criterio):
    """
    Verifica si una cláusula real del XML coincide con alguna del criterio.
    Soporta coincidencia exacta y por prefijo (ej. "6.8" cubre "6.8.2.2.1").
    """
    for cl in clausulas_criterio:
        if clausula_real == cl:
            return True
        if clausula_real.startswith(cl + ".") or clausula_real.startswith(cl):
            return True
    return False


# ── Utilidades de red ─────────────────────────────────────────────────────────
class PDFLinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.pdf_links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a":
            href = a.get("href", "")
            if href.lower().endswith(".pdf"):
                self.pdf_links.append(href)
        if tag in ("iframe","embed","object"):
            src = a.get("src","") or a.get("data","")
            if src.lower().endswith(".pdf"):
                self.pdf_links.append(src)

def extraer_pdf_desde_html(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        cs = r.headers.get_content_charset() or "utf-8"
        html = r.read().decode(cs, errors="replace")
    p = PDFLinkParser(); p.feed(html)
    if not p.pdf_links: return None
    link = p.pdf_links[0]
    if link.startswith("http"): return link
    return "/".join(url.split("/")[:3]) + "/" + link.lstrip("/")

def descargar_pdf(url, destino):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        content = r.read()
    if not content.startswith(b"%PDF"):
        raise ValueError(f"No es un PDF válido (primeros bytes: {content[:8]})")
    with open(destino, "wb") as f: f.write(content)
    return os.path.getsize(destino)

def verificar_verapdf():
    for cmd in ["verapdf","verapdf.bat","verapdf.sh"]:
        try:
            r = subprocess.run([cmd,"--version"], capture_output=True, text=True, timeout=10)
            out = (r.stdout + r.stderr).strip()
            if "veraPDF" in out:
                return True, cmd, out.split("\n")[0]
        except: continue
    return False, None, "veraPDF no encontrado en el PATH"

def ejecutar_verapdf(cmd, pdf_path):
    r = subprocess.run(
        [cmd,"--format","xml","-f",FLAVOUR,"--maxfailuresdisplayed","-1",pdf_path],
        capture_output=True, text=True, timeout=120
    )
    return r.stdout, r.stderr, r.returncode


# ── Parser XML ────────────────────────────────────────────────────────────────
def parsear_xml(xml_str):
    res = {
        "is_compliant": None, "profile": "",
        "passed_rules": 0, "failed_rules": 0, "total_rules": 0,
        "passed_checks": 0, "failed_checks": 0, "total_checks": 0,
        "failures": [], "error": None,
    }
    if not xml_str or not xml_str.strip():
        res["error"] = "Sin salida XML de veraPDF"; return res
    xml_clean = xml_str
    for marker in ["<?xml","<report"]:
        idx = xml_str.find(marker)
        if idx > 0: xml_clean = xml_str[idx:]; break
    try:
        root = ET.fromstring(xml_clean)
        vr = root.find(".//validationReport")
        if vr is None:
            res["error"] = "No se encontró validationReport en el XML"; return res
        res["is_compliant"] = vr.get("isCompliant","").lower() == "true"
        res["profile"]      = vr.get("profileName","")
        det = vr.find("details")
        if det is not None:
            res["passed_rules"]  = int(det.get("passedRules",  0))
            res["failed_rules"]  = int(det.get("failedRules",  0))
            res["passed_checks"] = int(det.get("passedChecks", 0))
            res["failed_checks"] = int(det.get("failedChecks", 0))
            res["total_rules"]   = res["passed_rules"] + res["failed_rules"]
            res["total_checks"]  = res["passed_checks"] + res["failed_checks"]
        for rule in root.findall(".//rule"):
            if rule.get("status","").lower() != "failed": continue
            clause  = rule.get("clause","")
            test_n  = rule.get("testNumber","")
            rule_id = f"{clause}.{test_n}".strip(".")
            f_chks  = int(rule.get("failedChecks", rule.get("occurrences",1)))
            desc_el = rule.find("description")
            desc    = desc_el.text.strip()[:150] if desc_el is not None and desc_el.text else ""
            err_el  = rule.find(".//errorMessage")
            err_msg = err_el.text.strip()[:120] if err_el is not None and err_el.text else ""
            res["failures"].append({
                "clause": clause, "test_n": test_n, "rule_id": rule_id,
                "description": desc, "failed_checks": f_chks, "error_msg": err_msg,
            })
    except ET.ParseError as e:
        res["error"] = f"Error parseando XML: {e}"
        m = re.search(r'isCompliant="(true|false)"', xml_str)
        if m: res["is_compliant"] = m.group(1) == "true"
        m = re.search(r'failedRules="(\d+)"', xml_str)
        if m: res["failed_rules"] = int(m.group(1))
        m = re.search(r'passedRules="(\d+)"', xml_str)
        if m: res["passed_rules"] = int(m.group(1))
        res["total_rules"] = res["passed_rules"] + res["failed_rules"]
    return res


# ── Mapeo fallos → criterios WCAG ─────────────────────────────────────────────
def evaluar_criterios_wcag(failures):
    """
    Para cada criterio WCAG, busca si alguna cláusula fallida
    corresponde a las cláusulas mapeadas (por prefijo).
    """
    resultados = {}
    for c in CRITERIOS_WCAG:
        fallos_rel = [
            f for f in failures
            if clausula_coincide(f["clause"], c["clausulas"])
        ]
        resultados[c["wcag"]] = {
            "resultado":          "No cumple" if fallos_rel else "Cumple",
            "fallos":             fallos_rel,
            "nombre_wcag":        c["nombre_wcag"],
            "nivel":              c["nivel"],
            "matterhorn":         c["matterhorn"],
            "descripcion":        c["descripcion"],
            "desc_matterhorn":    c["descripcion_matterhorn"],
        }
    return resultados


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 65)
    print(f"  EVALUACIÓN PDF — veraPDF — {FLAVOUR_NOME} — Criterios WCAG")
    print(f"  {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"  Documentos: {len(DOCUMENTOS)}  |  Criterios WCAG: {len(CRITERIOS_WCAG)}")
    print("=" * 65)

    ok, vera_cmd, ver_str = verificar_verapdf()
    if not ok:
        print(f"\n  ⚠  {ver_str}")
        print("  Instalá veraPDF desde https://verapdf.org/software/\n")
        sys.exit(1)
    print(f"\n  veraPDF: {ver_str} | Perfil: -{FLAVOUR} ({FLAVOUR_NOME})\n")

    pdf_dir = "pdfs"
    os.makedirs(pdf_dir, exist_ok=True)
    all_results = []

    for i, (doc_id, url, tipo) in enumerate(DOCUMENTOS, 1):
        print(f"[{i:02d}/{len(DOCUMENTOS)}] {doc_id}")
        result = {
            "doc_id": doc_id, "url": url, "pdf_path": None,
            "raw": {}, "wcag_resultados": {},
            "estado_global": "N/A", "obs": "", "error": None,
        }

        # ── Descarga ──────────────────────────────────────────────────────
        pdf_path = os.path.join(pdf_dir, f"{doc_id}.pdf")
        pdf_url  = url
        try:
            if tipo == "html":
                print(f"  → Extrayendo PDF desde HTML...", end=" ", flush=True)
                pdf_url = extraer_pdf_desde_html(url)
                if not pdf_url: raise ValueError("No se encontró link a PDF en la página.")
                print(f"OK → {pdf_url}")
            if os.path.exists(pdf_path):
                print(f"  → PDF ya descargado ({os.path.getsize(pdf_path)//1024} KB), reutilizando.")
            else:
                print(f"  → Descargando...", end=" ", flush=True)
                size = descargar_pdf(pdf_url, pdf_path)
                print(f"OK ({size//1024} KB)")
            result["pdf_path"] = pdf_path
        except Exception as e:
            print(f"  ERROR: {e}")
            result["error"] = str(e); result["obs"] = f"Error al obtener PDF: {e}"
            all_results.append(result); continue
        time.sleep(0.2)

        # ── veraPDF ───────────────────────────────────────────────────────
        print(f"  → veraPDF [{FLAVOUR_NOME}]...", end=" ", flush=True)
        try:
            stdout, stderr, rc = ejecutar_verapdf(vera_cmd, pdf_path)
            raw = parsear_xml(stdout)
            if raw["error"] and raw["is_compliant"] is None:
                raw2 = parsear_xml(stderr)
                if raw2["is_compliant"] is not None: raw = raw2
            result["raw"] = raw
            if raw["error"] and raw["is_compliant"] is None:
                print(f"Error XML: {raw['error']}")
            else:
                fallos_str = f"✗ {raw.get('failed_rules',0)} reglas fallidas ({raw.get('failed_checks',0)} checks)"
                print("✓ CONFORME" if raw["is_compliant"] else fallos_str)
        except subprocess.TimeoutExpired:
            print("TIMEOUT")
            result["raw"] = {"error":"Timeout","is_compliant":None,"failures":[],"failed_rules":0,"failed_checks":0}
        except Exception as e:
            print(f"ERROR: {e}")
            result["raw"] = {"error":str(e),"is_compliant":None,"failures":[],"failed_rules":0,"failed_checks":0}

        # ── Mapeo WCAG ────────────────────────────────────────────────────
        failures = result["raw"].get("failures", [])
        if result["raw"].get("is_compliant") is not None or failures is not None:
            result["wcag_resultados"] = evaluar_criterios_wcag(failures)
            cumple = sum(1 for v in result["wcag_resultados"].values() if v["resultado"]=="Cumple")
            total  = len(result["wcag_resultados"])
            result["estado_global"] = (
                "Cumple"     if cumple == total else
                "Parcial"    if cumple > 0      else
                "No cumple"
            )
            result["obs"] = (
                f"{FLAVOUR_NOME}: {cumple}/{total} criterios WCAG cumplen | "
                f"Reglas PDF/A: {result['raw'].get('failed_rules',0)} fallidas, "
                f"{result['raw'].get('failed_checks',0)} checks fallidos"
            )
        else:
            result["estado_global"] = "N/A"
            result["obs"] = result["raw"].get("error","Sin datos")

        print(f"  → Estado WCAG: {result['estado_global']} "
              f"({sum(1 for v in result['wcag_resultados'].values() if v['resultado']=='No cumple')} criterios no cumplen)\n")
        all_results.append(result)

    # ── CSV ───────────────────────────────────────────────────────────────────
    # Formato: una fila por documento (no por criterio),
    # con columnas separadas para cada criterio WCAG → más fácil de graficar.
    csv_path = "resultados_pdf_wcag.csv"
    wcag_codes = [c["wcag"] for c in CRITERIOS_WCAG]

    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        # Encabezado
        header = ["Documento", "URL_PDF", "Estado_Global",
                  "PDFA_Conforme", "PDFA_Reglas_Fallidas", "PDFA_Checks_Fallidos",
                  "Criterios_Cumplen", "Criterios_NoCumplen"]
        for code in wcag_codes:
            header.append(f"WCAG_{code.replace('.','_')}")
        w.writerow(header)

        for r in all_results:
            wres = r["wcag_resultados"]
            raw  = r["raw"]
            cumple   = sum(1 for v in wres.values() if v["resultado"]=="Cumple")
            nocumple = sum(1 for v in wres.values() if v["resultado"]=="No cumple")
            conf = ("Sí" if raw.get("is_compliant") is True
                    else "No" if raw.get("is_compliant") is False
                    else "Error")
            row = [
                r["doc_id"], r["url"], r["estado_global"],
                conf,
                raw.get("failed_rules",""),
                raw.get("failed_checks",""),
                cumple, nocumple,
            ]
            for code in wcag_codes:
                row.append(wres.get(code,{}).get("resultado","N/A"))
            w.writerow(row)

    # ── CSV detallado (criterio × documento) para análisis profundo ───────────
    csv_det_path = "resultados_pdf_wcag_detalle.csv"
    with open(csv_det_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow([
            "Documento","URL_PDF",
            "Criterio_WCAG","Nombre_WCAG","Nivel","Matterhorn",
            "Descripcion_WCAG","Descripcion_Matterhorn",
            "Resultado","Clausulas_Fallidas","Observacion",
        ])
        for r in all_results:
            for c in CRITERIOS_WCAG:
                ev      = r["wcag_resultados"].get(c["wcag"], {})
                fallos  = ev.get("fallos", [])
                obs_err = "; ".join(
                    f"[{f['rule_id']}] {f['failed_checks']} ocurrencias"
                    for f in fallos[:3]
                )
                w.writerow([
                    r["doc_id"], r["url"],
                    c["wcag"], c["nombre_wcag"], c["nivel"], c["matterhorn"],
                    c["descripcion"], c["descripcion_matterhorn"],
                    ev.get("resultado","N/A"), len(fallos), obs_err,
                ])

    # ── TXT ───────────────────────────────────────────────────────────────────
    txt_path = "resultados_pdf_wcag.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"EVALUACIÓN PDF — veraPDF — {FLAVOUR_NOME} — Criterios WCAG\n")
        f.write(f"Fecha:      {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write(f"Documentos: {len(all_results)}  |  Criterios WCAG: {len(CRITERIOS_WCAG)}\n")
        f.write("=" * 65 + "\n\n")
        for r in all_results:
            f.write(f"DOCUMENTO: {r['doc_id']}\nURL: {r['url']}\n")
            if r["error"]:
                f.write(f"  ⚠ Error: {r['error']}\n\n"); continue
            raw = r["raw"]
            f.write(f"  Estado global:   {r['estado_global']}\n")
            f.write(f"  PDF/A-1a:        {'✓ Conforme' if raw.get('is_compliant') else '✗ No conforme'}\n")
            f.write(f"  Reglas fallidas: {raw.get('failed_rules',0)} ({raw.get('failed_checks',0)} checks)\n")
            f.write(f"  Cláusulas fallidas en XML: {', '.join(sorted(set(f['clause'] for f in raw.get('failures',[]))))}\n")
            f.write(f"  {'─'*50}\n")
            for c in CRITERIOS_WCAG:
                ev    = r["wcag_resultados"].get(c["wcag"], {})
                marca = "✓" if ev.get("resultado")=="Cumple" else "✗"
                f.write(f"  {marca} [{c['nivel']}] {c['wcag']} — {c['nombre_wcag']}\n")
                f.write(f"      Matterhorn: {c['matterhorn']}\n")
                f.write(f"      {c['descripcion_matterhorn']}\n")
                fallos = ev.get("fallos",[])
                if fallos:
                    f.write(f"      Fallos: {len(fallos)} regla/s\n")
                    for fl in fallos[:3]:
                        f.write(f"        · [{fl['rule_id']}] {fl['failed_checks']} ocurrencias\n")
            f.write("\n")

        # Resumen por criterio
        docs_ok = [r for r in all_results if r["wcag_resultados"]]
        f.write("=" * 65 + "\nRESUMEN POR CRITERIO WCAG\n" + "=" * 65 + "\n")
        f.write(f"  {'Criterio':<8} {'Nombre':<30} {'Cumple':>7} {'NoCumple':>9}\n")
        f.write("  " + "-" * 58 + "\n")
        for c in CRITERIOS_WCAG:
            cumple   = sum(1 for r in docs_ok if r["wcag_resultados"].get(c["wcag"],{}).get("resultado")=="Cumple")
            nocumple = sum(1 for r in docs_ok if r["wcag_resultados"].get(c["wcag"],{}).get("resultado")=="No cumple")
            f.write(f"  {c['wcag']:<8} {c['nombre_wcag'][:30]:<30} {cumple:>7} {nocumple:>9}\n")

    # ── Resumen consola ───────────────────────────────────────────────────────
    print("=" * 65)
    print("  RESUMEN POR CRITERIO WCAG")
    print("=" * 65)
    print(f"  {'Criterio':<8} {'Nombre':<28} {'Cumple':>7} {'NoCumple':>9}")
    print("  " + "-" * 56)
    docs_ok = [r for r in all_results if r["wcag_resultados"]]
    for c in CRITERIOS_WCAG:
        cumple   = sum(1 for r in docs_ok if r["wcag_resultados"].get(c["wcag"],{}).get("resultado")=="Cumple")
        nocumple = sum(1 for r in docs_ok if r["wcag_resultados"].get(c["wcag"],{}).get("resultado")=="No cumple")
        print(f"  {c['wcag']:<8} {c['nombre_wcag'][:28]:<28} {cumple:>7} {nocumple:>9}")
    print(f"\n  Estado global de documentos:")
    print(f"    ✓ Cumple todos:   {sum(1 for r in all_results if r['estado_global']=='Cumple')}")
    print(f"    ~ Cumple parcial: {sum(1 for r in all_results if r['estado_global']=='Parcial')}")
    print(f"    ✗ No cumple:      {sum(1 for r in all_results if r['estado_global']=='No cumple')}")
    print(f"    — N/A/Error:      {sum(1 for r in all_results if r['estado_global']=='N/A')}")
    print(f"\n  Archivos generados:")
    print(f"    → {csv_path}  (consolidador — 1 fila por documento)")
    print(f"    → {csv_det_path}  (detalle — 1 fila por criterio×documento)")
    print(f"    → {txt_path}")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    main()
