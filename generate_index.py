import os
import re
import html

def get_html_title(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Mencari tag <title> di dalam file HTML
            match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            if match:
                return html.unescape(match.group(1).strip())
    except Exception:
        pass
    # Jika tidak ada title, gunakan nama file tanpa ekstensi
    return os.path.basename(file_path).replace('.html', '').replace('_', ' ')

def build_index():
    base_dir = "materi"
    if not os.path.exists(base_dir):
        print("Folder 'materi' tidak ditemukan.")
        return

    structure = {}

    # Membaca direktori secara rekursif
    for root, dirs, files in os.walk(base_dir):
        # Filter hanya file .html
        html_files = [f for f in files if f.endswith('.html')]
        if not html_files:
            continue

        # Dapatkan path relatif dari folder 'materi'
        rel_path = os.path.relpath(root, base_dir)
        parts = rel_path.split(os.sep)

        if len(parts) >= 2:
            mata_kuliah = parts[0].replace('_', ' ')
            modul = parts[1].replace('_', ' ')
            
            if mata_kuliah not in structure:
                structure[mata_kuliah] = {}
            if modul not in structure[mata_kuliah]:
                structure[mata_kuliah][modul] = []

            for file in sorted(html_files):
                full_path = os.path.join(root, file)
                web_path = os.path.join(base_dir, rel_path, file).replace(os.sep, '/')
                title = get_html_title(full_path)
                structure[mata_kuliah][modul].append({
                    "title": title,
                    "url": web_path
                })

    # Membuat HTML Konten
    content_html = ""
    for mk, moduls in sorted(structure.items()):
        content_html += f"""
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 class="text-2xl font-bold text-blue-800 mb-4 border-b pb-2">{mk}</h2>
            <div class="space-y-4">
        """
        for modul, sessions in sorted(moduls.items()):
            content_html += f"""
                <div>
                    <h3 class="text-lg font-semibold text-gray-700 mb-2">{modul}</h3>
                    <ul class="list-disc list-inside space-y-1 pl-4">
            """
            for session in sessions:
                content_html += f"""
                        <li>
                            <a href="{session['url']}" target="_blank" class="text-blue-600 hover:text-blue-800 hover:underline transition">
                                {session['title']}
                            </a>
                        </li>
                """
            content_html += """
                    </ul>
                </div>
            """
        content_html += """
            </div>
        </div>
        """

    # Template HTML Utama
    template = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portal Belajar Universitas Terbuka</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 min-h-screen text-gray-800">
    <header class="bg-blue-900 text-white py-6 shadow-md mb-8">
        <div class="container mx-auto px-4">
            <h1 class="text-3xl font-bold">Portal Belajar Mandiri</h1>
            <p class="text-blue-200 mt-1">Arsip Materi Sesi Kuliah Universitas Terbuka</p>
        </div>
    </header>

    <main class="container mx-auto px-4 max-w-4xl pb-12">
        {content_html if content_html else '<p class="text-center text-gray-500">Belum ada materi yang diunggah di folder <b>materi/</b>.</p>'}
    </main>

    <footer class="bg-gray-800 text-gray-400 py-6 text-center text-sm border-t border-gray-700">
        <p>&copy; {os.popen('date +%Y').read().strip()} - Diperbarui secara otomatis via GitHub Actions</p>
    </footer>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(template)
    print("index.html berhasil diperbarui.")

if __name__ == "__main__":
    build_index()