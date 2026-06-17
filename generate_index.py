import os
import re
import html

def get_html_title(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            if match:
                return html.unescape(match.group(1).strip())
    except Exception:
        pass
    return os.path.basename(file_path).replace('.html', '').replace('_', ' ')

def build_index():
    base_dir = "materi"
    if not os.path.exists(base_dir):
        print("Folder 'materi' tidak ditemukan.")
        return

    structure = {}

    for root, dirs, files in os.walk(base_dir):
        html_files = [f for f in files if f.endswith('.html')]
        if not html_files:
            continue

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

    # Membuat HTML Konten secara dinamis
    content_html = ""
    for mk, moduls in sorted(structure.items()):
        content_html += f"""
        <!-- Course Card -->
        <div class="course-card bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition duration-200 p-6 flex flex-col justify-between">
            <div>
                <div class="flex items-center space-x-3 mb-4">
                    <div class="bg-blue-50 text-blue-600 p-2.5 rounded-lg">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                        </svg>
                    </div>
                    <h2 class="course-title text-xl font-bold text-gray-800 line-clamp-1">{mk}</h2>
                </div>
                
                <div class="space-y-4">
        """
        for modul, sessions in sorted(moduls.items()):
            content_html += f"""
                    <div class="modul-block border-l-2 border-blue-100 pl-4 py-1">
                        <div class="flex items-center space-x-1 text-gray-500 text-xs font-semibold uppercase tracking-wider mb-2">
                            <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"></path>
                            </svg>
                            <span>{modul}</span>
                        </div>
                        <div class="space-y-1.5">
            """
            for session in sessions:
                content_html += f"""
                            <a href="{session['url']}" target="_blank" class="session-item flex items-center space-x-2 text-sm text-gray-600 hover:text-blue-600 hover:bg-blue-50/50 p-1.5 rounded-lg transition">
                                <svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                                </svg>
                                <span class="session-title truncate">{session['title']}</span>
                            </a>
                """
            content_html += """
                        </div>
                    </div>
            """
        content_html += """
                </div>
            </div>
        </div>
        """

    # Template HTML Utama (menggunakan .replace() agar aman dari kurung kurawal CSS/JS)
    template = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portal Belajar Mandiri UT</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
    </style>
</head>
<body class="bg-slate-50 min-h-screen text-slate-800 flex flex-col justify-between">
    
    <div>
        <!-- Hero Section -->
        <header class="bg-gradient-to-r from-blue-900 to-indigo-950 text-white pt-12 pb-20 shadow-lg relative overflow-hidden">
            <!-- Background Accent -->
            <div class="absolute inset-0 opacity-10">
                <div class="absolute -top-10 -left-10 w-40 h-40 bg-white rounded-full filter blur-3xl"></div>
                <div class="absolute bottom-10 right-10 w-60 h-60 bg-white rounded-full filter blur-3xl"></div>
            </div>
            
            <div class="container mx-auto px-6 max-w-6xl text-center relative z-10">
                <span class="bg-blue-500/20 text-blue-300 text-xs font-semibold px-3 py-1 rounded-full uppercase tracking-wider">Universitas Terbuka</span>
                <h1 class="text-3xl md:text-4xl font-extrabold mt-3 tracking-tight">Portal Belajar Mandiri</h1>
                <p class="text-blue-200 mt-2 text-sm md:text-base max-w-lg mx-auto">Akses berkas HTML sesi perkuliahan Anda kapan saja, di mana saja, secara instan.</p>
            </div>
        </header>

        <!-- Search Bar -->
        <div class="container mx-auto px-6 max-w-xl -mt-7 relative z-20">
            <div class="relative shadow-lg rounded-xl overflow-hidden">
                <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                    </svg>
                </div>
                <input type="text" id="searchInput" placeholder="Cari mata kuliah, modul, atau sesi belajar..." 
                    class="w-full pl-11 pr-4 py-3.5 bg-white text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 border-none rounded-xl transition font-medium">
            </div>
        </div>

        <!-- Main Content Area -->
        <main class="container mx-auto px-6 max-w-6xl py-12">
            <div id="courseGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {{CONTENT}}
            </div>
            
            <!-- Empty State -->
            <div id="emptyState" class="hidden text-center py-12">
                <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <h3 class="text-lg font-semibold text-gray-700">Tidak ada hasil ditemukan</h3>
                <p class="text-gray-400 text-sm mt-1">Coba kata kunci pencarian yang lain.</p>
            </div>
        </main>
    </div>

    <!-- Footer -->
    <footer class="bg-slate-900 text-slate-400 py-6 text-center text-xs border-t border-slate-800">
        <div class="container mx-auto px-6">
            <p>&copy; {{YEAR}} - Diperbarui otomatis menggunakan GitHub Actions</p>
            <p class="text-slate-600 mt-1">Hosting Gratis & Aman lewat GitHub Pages</p>
        </div>
    </footer>

    <!-- Search Script -->
    <script>
        const searchInput = document.getElementById('searchInput');
        const courseCards = document.querySelectorAll('.course-card');
        const emptyState = document.getElementById('emptyState');
        const courseGrid = document.getElementById('courseGrid');

        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase().trim();
            let totalVisibleCards = 0;

            courseCards.forEach(card => {
                const courseTitle = card.querySelector('.course-title').textContent.toLowerCase();
                const sessionItems = card.querySelectorAll('.session-item');
                let cardHasMatchingSession = false;

                sessionItems.forEach(item => {
                    const sessionTitle = item.querySelector('.session-title').textContent.toLowerCase();
                    if (sessionTitle.includes(query)) {
                        item.classList.remove('hidden');
                        item.classList.add('flex');
                        cardHasMatchingSession = true;
                    } else {
                        item.classList.remove('flex');
                        item.classList.add('hidden');
                    }
                });

                // Menampilkan card jika judul MK cocok atau ada sesi di dalamnya yang cocok
                if (courseTitle.includes(query) || cardHasMatchingSession) {
                    card.style.display = 'flex';
                    totalVisibleCards++;
                    
                    // Jika yang dicari adalah judul MK, pastikan sesi di dalamnya tetap tampil semua
                    if (courseTitle.includes(query) && !cardHasMatchingSession) {
                        sessionItems.forEach(item => {
                            item.classList.remove('hidden');
                            item.classList.add('flex');
                        });
                    }
                } else {
                    card.style.display = 'none';
                }
            });

            // Tampilkan empty state jika tidak ada yang cocok
            if (totalVisibleCards === 0) {
                courseGrid.classList.add('hidden');
                emptyState.classList.remove('hidden');
            } else {
                courseGrid.classList.remove('hidden');
                emptyState.classList.add('hidden');
            }
        });
    </script>
</body>
</html>
"""

    # Memasukkan konten ke template secara dinamis
    current_year = os.popen('date +%Y').read().strip()
    if not current_year:
        current_year = "2026"
        
    final_html = template.replace("{{CONTENT}}", content_html).replace("{{YEAR}}", current_year)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_html)
    print("index.html berhasil diperbarui dengan UI baru.")

if __name__ == "__main__":
    build_index()