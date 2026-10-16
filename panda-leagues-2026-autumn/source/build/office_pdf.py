"""Convert .docx/.pptx to PDF via LibreOffice UNO, refreshing TOC/fields first.
Usage: python3 office_pdf.py file1 [file2 ...]  (PDF written next to each input)"""
import os, sys, time, subprocess, tempfile, uno
from com.sun.star.beans import PropertyValue

sys.path.insert(0, "/root/.claude/skills/synced/945a8792-87ea-440d-aeed-3ca5e5218242_a286977b-5084-471c-b116-73e0d78dbb3b/docx/scripts")
from office.soffice import get_soffice_env


def pv(name, value):
    p = PropertyValue(); p.Name = name; p.Value = value; return p


def main(files):
    prof = tempfile.mkdtemp(prefix="lo_prof_")
    pipe = f"pl{os.getpid()}"
    proc = subprocess.Popen(["soffice", f"-env:UserInstallation=file://{prof}", "--headless", "--invisible", "--nologo",
                             "--norestore", f"--accept=pipe,name={pipe};urp;"], env=get_soffice_env(),
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    local = uno.getComponentContext()
    resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
    for _ in range(60):
        try:
            ctx = resolver.resolve(f"uno:pipe,name={pipe};urp;StarOffice.ComponentContext"); break
        except Exception:
            time.sleep(1)
    desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    try:
        for f in files:
            f = os.path.abspath(f)
            doc = desktop.loadComponentFromURL(uno.systemPathToFileUrl(f), "_blank", 0, (pv("Hidden", True),))
            filt = "impress_pdf_Export" if f.endswith(".pptx") else "writer_pdf_Export"
            if not f.endswith(".pptx"):
                for _ in range(2):  # twice: TOC page numbers settle after first pass
                    idx = doc.getDocumentIndexes()
                    for i in range(idx.getCount()):
                        idx.getByIndex(i).update()
                    doc.getTextFields().refresh()
            fd = uno.Any("[]com.sun.star.beans.PropertyValue", tuple([pv("UseTaggedPDF", True), pv("ExportBookmarks", True), pv("EmbedStandardFonts", True)]))
            out = os.path.splitext(f)[0] + ".pdf"
            doc.storeToURL(uno.systemPathToFileUrl(out), (pv("FilterName", filt), pv("FilterData", fd)))
            doc.close(True)
            print("pdf:", out)
    finally:
        try: desktop.terminate()
        except Exception: pass
        proc.wait(timeout=30)


if __name__ == "__main__":
    main(sys.argv[1:])
