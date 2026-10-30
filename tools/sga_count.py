"""Count files in an AoE4 .sga across ALL TOCs (header-only, read-only).
Layout from AOEMods.Essence SGA/Core/ArchiveReader.cs. Usage: python -I sga_count.py <file.sga> ..."""
import struct, sys, collections
for path in sys.argv[1:]:
    with open(path, 'rb') as f:
        magic = f.read(8); ver, prod = struct.unpack('<HH', f.read(4)); f.read(128)
        blob_off, blob_len, data_off, data_len, _u = struct.unpack('<QIQQI', f.read(32)); f.read(256)
        f.seek(blob_off)
        toc_off, toc_n, fold_off, fold_n, file_off, file_n = struct.unpack('<6I', f.read(24))
        f.seek(blob_off + toc_off)
        tocs = []
        for _ in range(toc_n):
            alias = f.read(64).split(b'\0')[0].decode(); name = f.read(64).split(b'\0')[0].decode()
            fs, fe, fis, fie, root = struct.unpack('<5I', f.read(20)); tocs.append((alias, name, fis, fie))
        f.seek(blob_off + file_off); storage = collections.Counter()
        for _ in range(file_n):
            rec = f.read(30); storage[rec[25]] += 1
    print(f'{path}\n  magic={magic!r} v{ver} tocs={toc_n} files(total)={file_n} storage_types={dict(storage)}')
    for a, n, s, e in tocs: print(f'    toc alias={a!r} name={n!r} files={e - s}')
