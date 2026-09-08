#!/usr/bin/env python3
# =============================================================================
# evaluar_wcag_ceguera_v2.py
# Evaluación automatizada WCAG 2.1 Nivel A y AA — Ceguera total
# 13 criterios definitivos — Boletín Oficial UNMdP
# Tesina LGU — Algamiz & Emiliano 2025/2026
#
# CRITERIOS (13):
#   1.1.1  Contenido no textual          (A)  Auto
#   1.3.1  Información y relaciones      (A)  Auto
#   1.3.2  Secuencia significativa       (A)  Manual → NVDA
#   1.4.5  Imágenes de texto             (AA) Auto
#   2.4.1  Saltar bloques                (A)  Auto
#   2.4.2  Título de página              (A)  Auto
#   2.4.3  Orden de foco                 (A)  Manual → NVDA Tab
#   2.4.4  Propósito de los enlaces      (A)  Auto+Manual
#   2.4.6  Encabezados y etiquetas       (AA) Auto
#   3.1.1  Idioma de la página           (A)  Auto
#   3.1.2  Idioma de las partes          (AA) Manual
#   4.1.1  Procesamiento                 (A)  Auto
#   4.1.2  Nombre, función, valor        (A)  Auto
#
# USO: python evaluar_wcag_ceguera_v2.py
# REQUISITOS: Python 3.7+ — solo biblioteca estándar, sin pip.
# =============================================================================

import urllib.request, urllib.error, csv, re, time
from html.parser import HTMLParser
from datetime import datetime

URLS = [
    "https://digesto.mdp.edu.ar/vista/ver_norma.php?id_norma=92309",
    "https://digesto.mdp.edu.ar/vista/ver_norma.php?id_norma=92383",
    "https://digesto.mdp.edu.ar/vista/ver_norma.php?id_norma=94838",
    "https://digesto.mdp.edu.ar/vista/ver_norma.php?id_norma=94881",
    "https://digesto.mdp.edu.ar/vista/ver_norma.php?id_norma=95518",
    "https://digesto.mdp.edu.ar/vista/ver_norma.php?id_norma=95638",
    "https://digesto.mdp.edu.ar/vista/ver_norma.php?id_norma=96549",
    "https://digesto.mdp.edu.ar/vista/ver_norma.php?id_norma=96731",
    "https://digesto.mdp.edu.ar/vista/ver_norma.php?id_norma=97706",
    "https://digesto.mdp.edu.ar/vista/ver_norma.php?id_norma=97815",
    "https://digesto.mdp.edu.ar/vista/ver_norma.php?id_norma=98047",
    "https://digesto.mdp.edu.ar/vista/ver_norma.php?id_norma=98353",
    "https://digesto.mdp.edu.ar/vista/ver_norma.php?id_norma=99132",
    "https://digesto.mdp.edu.ar/vista/ver_norma.php?id_norma=99216",
    "https://digesto.mdp.edu.ar/vista/ver_norma.php?id_norma=100361",
    "https://digesto.mdp.edu.ar/vista/ver_norma.php?id_norma=100631",
    "https://digesto.mdp.edu.ar/vista/ver_norma.php?id_norma=102085",
    "https://digesto.mdp.edu.ar/vista/ver_norma.php?id_norma=102148",
    "https://digesto.mdp.edu.ar/vista/ver_norma.php?id_norma=102161",
    "https://digesto.mdp.edu.ar/vista/ver_norma.php?id_norma=102522",
    "https://digesto.mdp.edu.ar/vista/ver_norma.php?id_norma=102797",
    "https://digesto.mdp.edu.ar/vista/ver_norma.php?id_norma=103295",
]

CRITERIA = [
    ("1.1.1",  "Contenido no textual",      "A",  "auto"),
    ("1.3.1",  "Información y relaciones",  "A",  "auto"),
    ("1.3.2",  "Secuencia significativa",   "A",  "manual"),
    ("1.4.5",  "Imágenes de texto",         "AA", "auto"),
    ("2.4.1",  "Saltar bloques",            "A",  "auto"),
    ("2.4.2",  "Título de página",          "A",  "auto"),
    ("2.4.3",  "Orden de foco",             "A",  "manual"),
    ("2.4.4",  "Propósito de los enlaces",  "A",  "auto"),
    ("2.4.6",  "Encabezados y etiquetas",   "AA", "auto"),
    ("3.1.1",  "Idioma de la página",       "A",  "auto"),
    ("3.1.2",  "Idioma de las partes",      "AA", "manual"),
    ("4.1.1",  "Procesamiento",             "A",  "auto"),
    ("4.1.2",  "Nombre, función, valor",    "A",  "auto"),
]

TEXTOS_GENERICOS = {"clic aquí","haga clic aquí","click here","aquí","acá","here",
                    "ver más","ver más","leer más","más info","más información",
                    "link","enlace","ir","continuar","siguiente","anterior","descargar"}


class WCAGParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title=""; self._in_title=False
        self.lang=""
        self.images=[]
        self.headings=[]
        self.links=[]
        self.inputs=[]
        self.label_fors=set()
        self._all_ids=[]
        self.has_main=False; self.has_nav=False
        self.has_header=False; self.has_footer=False
        self.skip_links=[]
        self._in_heading=False; self._cur_hl=0; self._cur_ht=""
        self._in_link=False; self._cur_link={}; self._link_count=0
        self.lang_parts=[]
        self.focusable=[]  # elementos que reciben foco

    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=="html": self.lang=a.get("lang","")
        if tag=="title": self._in_title=True
        role=a.get("role","")
        if tag=="main" or role=="main": self.has_main=True
        if tag=="nav"  or role=="navigation": self.has_nav=True
        if tag=="header": self.has_header=True
        if tag=="footer": self.has_footer=True
        el_lang=a.get("lang","")
        if el_lang and el_lang!=self.lang and tag not in ("html","meta"):
            self.lang_parts.append({"tag":tag,"lang":el_lang})
        el_id=a.get("id","")
        if el_id: self._all_ids.append(el_id)
        if tag=="img":
            self.images.append({
                "src":a.get("src",""),"alt":a.get("alt",""),
                "has_alt":"alt" in a,
                "is_decorative":"alt" in a and a.get("alt","")=="",
                "aria_hidden":a.get("aria-hidden","")=="true",
            })
        if tag in ("h1","h2","h3","h4","h5","h6"):
            self._in_heading=True; self._cur_hl=int(tag[1]); self._cur_ht=""
        if tag=="a":
            self._in_link=True; self._link_count+=1
            href=a.get("href","")
            self._cur_link={"href":href,"aria_label":a.get("aria-label",""),"text":"","index":self._link_count}
            if href.startswith("#") and self._link_count<=5:
                self.skip_links.append(href)
        if tag in ("input","select","textarea","button"):
            self.inputs.append({"tag":tag,"type":a.get("type","text"),"id":a.get("id",""),
                "aria_label":a.get("aria-label","")+a.get("aria-labelledby",""),"title":a.get("title","")})
            tabindex=a.get("tabindex","")
            self.focusable.append({"tag":tag,"tabindex":tabindex,"id":a.get("id","")})
        if tag=="label":
            lf=a.get("for","")
            if lf: self.label_fors.add(lf)

    def handle_endtag(self, tag):
        if tag=="title": self._in_title=False
        if tag in ("h1","h2","h3","h4","h5","h6"):
            if self._in_heading: self.headings.append((self._cur_hl,self._cur_ht.strip()))
            self._in_heading=False
        if tag=="a":
            if self._in_link: self.links.append(self._cur_link)
            self._in_link=False

    def handle_data(self, data):
        if self._in_title: self.title+=data
        if self._in_heading: self._cur_ht+=data
        if self._in_link: self._cur_link["text"]=self._cur_link.get("text","")+data

    def dup_ids(self):
        seen=set(); dups=[]
        for i in self._all_ids:
            if i in seen: dups.append(i)
            seen.add(i)
        return dups


def evaluar(html, url):
    p=WCAGParser()
    try: p.feed(html)
    except: pass
    R={}; O={}

    # 1.1.1 Contenido no textual
    imgs=p.images
    sig=[i for i in imgs if not i["is_decorative"] and not i["aria_hidden"]]
    sin_alt=[i for i in sig if not i["has_alt"]]
    gen=[i for i in sig if i["has_alt"] and i["alt"].strip().lower() in
         ("image","imagen","foto","photo","img","logo","icon","icono","figura")]
    if not imgs:
        R["1.1.1"]="N/A"; O["1.1.1"]="No se encontraron imágenes."
    elif sin_alt:
        R["1.1.1"]="No cumple"; O["1.1.1"]=f"{len(sin_alt)} imagen(es) sin atributo alt. Src: {'; '.join(i['src'][:50] for i in sin_alt[:3])}"
    elif gen:
        R["1.1.1"]="Parcial"; O["1.1.1"]=f"{len(gen)} imagen(es) con alt genérico ('{gen[0]['alt']}'). Verificar descripción."
    else:
        R["1.1.1"]="Cumple"; O["1.1.1"]=f"{len(imgs)} imagen(es) con alt presente."

    # 1.3.1 Información y relaciones
    sem=p.has_main or p.has_nav or p.has_header or p.has_footer
    obs=[]
    if not sem: obs.append("Sin landmarks semánticos (main/nav/header/footer o roles ARIA).")
    if not p.headings: obs.append("Sin encabezados HTML (H1-H6).")
    if obs:
        R["1.3.1"]="No cumple" if (not sem and not p.headings) else "Parcial"; O["1.3.1"]=" | ".join(obs)
    else:
        R["1.3.1"]="Cumple"; O["1.3.1"]="Landmarks y encabezados presentes."

    # 1.3.2 Secuencia significativa — manual
    R["1.3.2"]="— sin evaluar —"
    O["1.3.2"]="NVDA: navegar con flecha abajo y verificar que el orden de lectura sea lógico."

    # 1.4.5 Imágenes de texto
    imgs_txt=[i for i in imgs if any(kw in i["src"].lower() for kw in
        ["titulo","title","texto","text","heading","banner","firma","encabezado","resolucion","ordenanza"])]
    if not imgs:
        R["1.4.5"]="N/A"; O["1.4.5"]="No hay imágenes."
    elif imgs_txt:
        R["1.4.5"]="Parcial"; O["1.4.5"]=f"Posibles imágenes de texto: {len(imgs_txt)}. Verificar visualmente."
    else:
        R["1.4.5"]="Cumple"; O["1.4.5"]="No se detectaron imágenes con texto informativo."

    # 2.4.1 Saltar bloques
    has_skip=len(p.skip_links)>0
    has_main_lm=p.has_main
    if has_skip or has_main_lm:
        mec=[]
        if has_skip: mec.append(f"skip link(s): {', '.join(p.skip_links[:3])}")
        if has_main_lm: mec.append("landmark <main> presente")
        R["2.4.1"]="Cumple"; O["2.4.1"]="Mecanismo para saltar bloques: "+"; ".join(mec)+"."
    else:
        R["2.4.1"]="No cumple"; O["2.4.1"]="Sin skip links ni landmark <main>. El lector de pantalla debe recorrer todo el contenido repetido."

    # 2.4.2 Título de página
    title=p.title.strip()
    GENERICOS={"visualizar norma","untitled","sin título","página","inicio","home","norma","document"}
    if not title:
        R["2.4.2"]="No cumple"; O["2.4.2"]="Elemento <title> ausente o vacío."
    elif title.lower() in GENERICOS:
        R["2.4.2"]="Parcial"; O["2.4.2"]=f"Título genérico: '{title}'. No identifica el documento específico."
    else:
        R["2.4.2"]="Cumple"; O["2.4.2"]=f"Título: '{title}'"

    # 2.4.3 Orden de foco — manual
    neg_tab=[f for f in p.focusable if f["tabindex"]=="-1"]
    R["2.4.3"]="— sin evaluar —"
    obs_243="NVDA: navegar con Tab y verificar que el orden de foco sea lógico."
    if neg_tab: obs_243+=f" Atención: {len(neg_tab)} elemento(s) con tabindex=-1 (excluidos del foco)."
    O["2.4.3"]=obs_243

    # 2.4.4 Propósito de los enlaces
    links=p.links
    sin_texto=[l for l in links if not l["text"].strip() and not l["aria_label"].strip()]
    genericos=[l for l in links if l["text"].strip().lower() in TEXTOS_GENERICOS and not l["aria_label"].strip()]
    if sin_texto:
        R["2.4.4"]="No cumple"; O["2.4.4"]=f"{len(sin_texto)} enlace(s) sin texto ni aria-label (opacos para el lector de pantalla)."
    elif genericos:
        R["2.4.4"]="Parcial"; O["2.4.4"]=f"{len(genericos)} enlace(s) con texto genérico ('{genericos[0]['text']}'). Verificar contexto."
    elif not links:
        R["2.4.4"]="N/A"; O["2.4.4"]="No se encontraron enlaces en la página."
    else:
        R["2.4.4"]="Cumple"; O["2.4.4"]=f"{len(links)} enlace(s) con texto descriptivo."

    # 2.4.6 Encabezados y etiquetas
    if not p.headings:
        R["2.4.6"]="No cumple"; O["2.4.6"]="Sin encabezados (H1-H6). El lector de pantalla no puede navegar por secciones."
    else:
        niv=[h[0] for h in p.headings]
        saltos=[f"H{niv[i-1]}→H{niv[i]}" for i in range(1,len(niv)) if niv[i]>niv[i-1]+1]
        vacios=[h for h in p.headings if not h[1]]
        if saltos:
            R["2.4.6"]="Parcial"; O["2.4.6"]=f"{len(p.headings)} encabezado(s). Saltos de nivel: {', '.join(saltos)}."
        elif vacios:
            R["2.4.6"]="Parcial"; O["2.4.6"]=f"{len(p.headings)} encabezado(s). {len(vacios)} vacío(s)."
        else:
            ej=", ".join(f"H{h[0]}:'{h[1][:25]}'" for h in p.headings[:3])
            R["2.4.6"]="Cumple"; O["2.4.6"]=f"{len(p.headings)} encabezado(s) en orden. Ej: {ej}"

    # 3.1.1 Idioma de la página
    lang=p.lang.strip()
    if not lang:
        R["3.1.1"]="No cumple"; O["3.1.1"]="Atributo lang ausente en <html>."
    elif lang.lower().startswith("es"):
        R["3.1.1"]="Cumple"; O["3.1.1"]=f"lang='{lang}' declarado correctamente."
    else:
        R["3.1.1"]="Parcial"; O["3.1.1"]=f"lang='{lang}' — verificar si corresponde al idioma del contenido."

    # 3.1.2 Idioma de las partes — manual
    R["3.1.2"]="— sin evaluar —"
    O["3.1.2"]="Verificar manualmente si hay fragmentos en otro idioma sin atributo lang."

    # 4.1.1 Procesamiento
    dups=p.dup_ids(); obs=[]
    if dups: obs.append(f"IDs duplicados: {', '.join(dups[:5])}")
    ab=len(re.findall(r'<(?!/)(?!!)[a-z][^>]*(?<!/)>',html,re.I))
    ci=len(re.findall(r'</[a-z][^>]*>',html,re.I))
    vo=len(re.findall(r'<(?:img|br|hr|input|meta|link|area|base|col|embed|param|source|track|wbr)[^>]*>',html,re.I))
    if abs((ab-vo)-ci)>5: obs.append(f"Posible desequilibrio de etiquetas (abiertas≈{ab-vo}, cerradas≈{ci}).")
    if obs:
        R["4.1.1"]="No cumple" if dups else "Parcial"; O["4.1.1"]=" | ".join(obs)
    else:
        R["4.1.1"]="Cumple"; O["4.1.1"]="Sin IDs duplicados. Estructura de etiquetas aparentemente correcta."

    # 4.1.2 Nombre, función, valor
    sin_txt_link=[l for l in p.links if not l["text"].strip() and not l["aria_label"].strip()]
    sin_label=[i for i in p.inputs if not (i["id"] in p.label_fors or i["aria_label"] or i["title"])
               and i["type"] not in ("hidden","submit","reset","button","image")]
    obs=[]
    if sin_txt_link: obs.append(f"{len(sin_txt_link)} enlace(s) sin texto ni aria-label.")
    if sin_label: obs.append(f"{len(sin_label)} campo(s) sin etiqueta accesible.")
    if obs:
        R["4.1.2"]="No cumple" if (sin_txt_link and sin_label) else "Parcial"; O["4.1.2"]=" | ".join(obs)
    else:
        R["4.1.2"]="Cumple"; O["4.1.2"]=f"{len(p.links)} enlace(s) con texto o aria-label. Campos correctamente etiquetados."

    return R, O


def fetch(url, timeout=15):
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
        "Accept-Language":"es-AR,es;q=0.9",
    }
    req=urllib.request.Request(url,headers=headers)
    with urllib.request.urlopen(req,timeout=timeout) as r:
        cs=r.headers.get_content_charset() or "utf-8"
        return r.read().decode(cs,errors="replace")

def doc_id(url):
    m=re.search(r'id_norma=(\d+)',url)
    return f"id_norma={m.group(1)}" if m else url

def main():
    print("="*65)
    print("  EVALUACIÓN WCAG 2.1 A/AA — CEGUERA TOTAL — BO UNMdP v2")
    print(f"  {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"  Documentos: {len(URLS)}  |  Criterios: {len(CRITERIA)}")
    print("="*65)

    results=[]
    for i,url in enumerate(URLS,1):
        did=doc_id(url)
        print(f"\n[{i:02d}/{len(URLS)}] {did} ...",end=" ",flush=True)
        try:
            html=fetch(url)
            R,O=evaluar(html,url)
            results.append({"url":url,"doc_id":did,"R":R,"O":O,"error":None})
            c=sum(1 for v in R.values() if v=="Cumple")
            n=sum(1 for v in R.values() if v=="No cumple")
            pa=sum(1 for v in R.values() if v=="Parcial")
            ma=sum(1 for v in R.values() if v=="— sin evaluar —")
            print(f"OK  Cumple:{c}  NoCumple:{n}  Parcial:{pa}  Manual:{ma}")
        except Exception as e:
            print(f"ERROR: {e}")
            results.append({"url":url,"doc_id":did,
                "R":{c[0]:"N/A" for c in CRITERIA},"O":{c[0]:f"Error: {e}" for c in CRITERIA},"error":str(e)})
        time.sleep(0.5)

    csv_path="resultados_wcag_ceguera_v2.csv"
    with open(csv_path,"w",newline="",encoding="utf-8-sig") as f:
        w=csv.writer(f)
        w.writerow(["Documento","Criterio","Nombre","Nivel","Método","Resultado","Observaciones"])
        for doc in results:
            for code,name,nivel,metodo in CRITERIA:
                res=doc["R"].get(code,"N/A")
                obs=doc["O"].get(code,"")
                w.writerow([doc["doc_id"],code,name,nivel,"Auto" if metodo=="auto" else "Manual",res,obs])

    txt_path="resultados_wcag_ceguera_v2.txt"
    with open(txt_path,"w",encoding="utf-8") as f:
        f.write("EVALUACIÓN WCAG 2.1 A/AA — CEGUERA TOTAL — BO UNMdP\n")
        f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write(f"Documentos: {len(results)}  |  Criterios: {len(CRITERIA)}\n")
        f.write("="*65+"\n\n")
        for doc in results:
            f.write(f"DOCUMENTO: {doc['doc_id']}\nURL: {doc['url']}\n")
            if doc["error"]:
                f.write(f"  ⚠ Error: {doc['error']}\n\n"); continue
            f.write("-"*50+"\n")
            for code,name,nivel,_ in CRITERIA:
                res=doc["R"].get(code,"N/A")
                obs=doc["O"].get(code,"")
                marca={"Cumple":"✓","No cumple":"✗","Parcial":"~","N/A":"—","— sin evaluar —":"⚙"}.get(res,"?")
                f.write(f"  {marca} [{nivel}] {code} {name}\n     → {res}")
                if obs: f.write(f": {obs}")
                f.write("\n")
            f.write("\n")
        f.write("="*65+"\nRESUMEN POR CRITERIO\n"+"="*65+"\n")
        f.write(f"{'Criterio':<10} {'Nombre':<32} {'Cumple':>7} {'NoCumple':>9} {'Parcial':>8} {'Manual':>7}\n")
        f.write("-"*65+"\n")
        for code,name,nivel,_ in CRITERIA:
            c=sum(1 for d in results if d["R"].get(code)=="Cumple")
            n=sum(1 for d in results if d["R"].get(code)=="No cumple")
            pa=sum(1 for d in results if d["R"].get(code)=="Parcial")
            ma=sum(1 for d in results if d["R"].get(code)=="— sin evaluar —")
            f.write(f"{code:<10} {name[:32]:<32} {c:>7} {n:>9} {pa:>8} {ma:>7}\n")

    print("\n"+"="*65)
    print("  RESUMEN POR CRITERIO")
    print("="*65)
    print(f"  {'Criterio':<10} {'Cumple':>7} {'NoCumple':>9} {'Parcial':>8} {'Manual':>7}")
    print("  "+"-"*45)
    for code,name,nivel,_ in CRITERIA:
        c=sum(1 for d in results if d["R"].get(code)=="Cumple")
        n=sum(1 for d in results if d["R"].get(code)=="No cumple")
        pa=sum(1 for d in results if d["R"].get(code)=="Parcial")
        ma=sum(1 for d in results if d["R"].get(code)=="— sin evaluar —")
        print(f"  {code:<10} {c:>7} {n:>9} {pa:>8} {ma:>7}")
    print("\n"+"="*65)
    print(f"  Archivos generados:")
    print(f"    → {csv_path}")
    print(f"    → {txt_path}")
    print("="*65)
    print("\n  PRÓXIMOS PASOS:")
    print("  1. Abrir consolidador_wcag_ceguera_v3.html")
    print("  2. Cargar resultados_wcag_ceguera_v2.csv (pestaña 'Cargar CSV')")
    print("  3. Completar con NVDA: 1.3.2, 2.4.3, 3.1.2 (pestaña 'Ingreso manual')")
    print("="*65+"\n")

if __name__ == "__main__":
    main()
