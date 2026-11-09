"""Build a specification archive; it is deliberately not a platform import ZIP."""
import hashlib,json,pathlib,zipfile
ROOT=pathlib.Path(__file__).parent
STAGE=ROOT/'delivery'
OUT=ROOT/'PAPER_SPECIFICATION_BUNDLE.zip'
files=[p for p in sorted(STAGE.rglob('*')) if p.is_file() and p.name not in {'PAPER_SPECIFICATION_BUNDLE.zip','BUNDLE_VERIFICATION.json','FILE_MANIFEST.json'}]
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files:
        info=zipfile.ZipInfo(p.relative_to(STAGE).as_posix(),date_time=(2026,11,9,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,p.read_bytes())
with zipfile.ZipFile(OUT) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(files)
    assert all(z.read(p.relative_to(STAGE).as_posix())==p.read_bytes() for p in files)
record={'archive':OUT.name,'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'bytes':OUT.stat().st_size,'members_verified':len(files),'archive_type':'research_and_paper_specification','platform_import_package':False}
(ROOT/'BUNDLE_VERIFICATION.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record))
