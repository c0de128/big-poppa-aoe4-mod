"""Dump every file from ALL TOCs of an AoE4 .sga (read-only on the archive).

Layout from AOEMods.Essence SGA/Core/ArchiveReader.cs (same as sga_count.py).
Storage type 0 = stored; otherwise zlib, with a raw-deflate fallback.
Usage: python -I sga_dump_all.py <file.sga> <out_dir>
Writes <out_dir>/<toc>/<folder path>/<name> and prints one line per file.
"""
import pathlib
import struct
import sys
import zlib


def cstr(buf, off):
    end = buf.index(b'\0', off)
    return buf[off:end].decode('utf-8')


def main():
    src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    raw = src.read_bytes()
    blob_off, _blob_len, data_off = struct.unpack_from('<QIQ', raw, 12 + 128)
    toc_off, toc_n, fold_off, fold_n, file_off, file_n, str_off, _str_len = struct.unpack_from('<8I', raw, blob_off)
    strings = raw[blob_off + str_off:]

    tocs = []
    for i in range(toc_n):
        base = blob_off + toc_off + i * 148
        alias = raw[base:base + 64].split(b'\0')[0].decode()
        _fs, _fe, _fis, _fie, root = struct.unpack_from('<5I', raw, base + 128)
        tocs.append((alias, root))

    folders = [struct.unpack_from('<5I', raw, blob_off + fold_off + i * 20) for i in range(fold_n)]
    files = []
    for i in range(file_n):
        name_o, _hash_o, d_off, c_len, u_len = struct.unpack_from('<IIQII', raw, blob_off + file_off + i * 30)
        storage = raw[blob_off + file_off + i * 30 + 25]
        files.append((name_o, d_off, c_len, u_len, storage))

    def walk(fidx, prefix, toc):
        name_o, fs, fe, fis, fie = folders[fidx]
        name = cstr(strings, name_o).replace('\\', '/')
        path = name or prefix  # folder names are stored as full paths
        for j in range(fis, fie):
            name_o, d_off, c_len, u_len, storage = files[j]
            data = raw[data_off + d_off:data_off + d_off + c_len]
            if storage != 0:
                try:
                    data = zlib.decompress(data)
                except zlib.error:
                    data = zlib.decompress(data, -15)
            rel = pathlib.PurePosixPath(toc, path, cstr(strings, name_o).replace('\\', '/'))
            target = out / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            print(f'{rel}\t{len(data)}\t{"ok" if len(data) == u_len else "SIZE MISMATCH"}')
        for k in range(fs, fe):
            if k != fidx:
                walk(k, path, toc)

    for alias, root in tocs:
        walk(root, '', alias)


if __name__ == '__main__':
    main()
