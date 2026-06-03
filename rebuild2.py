import os
import shutil
import subprocess

project_dir = r"C:\Users\IFIAG\.gemini\antigravity\scratch\iffiag-git-project"
os.chdir(project_dir)

# 1. Delete .git folder if it exists
git_dir = os.path.join(project_dir, ".git")
if os.path.exists(git_dir):
    def remove_readonly(func, path, excinfo):
        import stat
        os.chmod(path, stat.S_IWRITE)
        func(path)
    shutil.rmtree(git_dir, onerror=remove_readonly)

# 2. Get current files content (modified ones with notes widget)
with open("index.html", "r", encoding="utf-8") as f:
    mod_html = f.read()

with open("style.css", "r", encoding="utf-8") as f:
    mod_css = f.read()

with open("script.js", "r", encoding="utf-8") as f:
    mod_js = f.read()

# Replace any occurrence of halloulimad with imad_halloul in HTML
mod_html = mod_html.replace("halloulimad", "imad_halloul")

# 3. Define original contents (without notes widget)
orig_html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>InfinityHub - Premium Developer Dashboard</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <!-- FontAwesome for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Local Stylesheet -->
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="background-decorations">
        <div class="circle circle-1"></div>
        <div class="circle circle-2"></div>
        <div class="circle circle-3"></div>
    </div>

    <main class="dashboard-container">
        <!-- Header Section -->
        <header class="dashboard-header">
            <div class="brand">
                <i class="fa-solid fa-wand-magic-sparkles logo-icon"></i>
                <h1>Infinity<span>Hub</span></h1>
            </div>
            <div class="time-widget">
                <div id="live-time">10:55:00</div>
                <div id="live-date">Mercredi 3 Juin 2026</div>
            </div>
        </header>

        <!-- Dashboard Grid Layout -->
        <div class="dashboard-grid">
            <!-- Profile / Status Widget -->
            <section class="card widget-profile" id="widget-profile">
                <div class="card-body">
                    <div class="user-info">
                        <div class="avatar">I</div>
                        <div>
                            <h3>Bienvenue, imad_halloul</h3>
                            <p class="status-badge"><span class="pulse-dot"></span> Mode Focus Activé</p>
                        </div>
                    </div>
                    <div class="motivation-quote">
                        <i class="fa-solid fa-quote-left quote-icon"></i>
                        <p id="quote-text">« La meilleure façon de prédire l'avenir, c'est de le créer. »</p>
                        <span id="quote-author">- Peter Drucker</span>
                    </div>
                </div>
            </section>

            <!-- Todo Widget -->
            <section class="card widget-todo" id="widget-todo">
                <div class="card-header">
                    <h2><i class="fa-solid fa-list-check"></i> Mes Tâches</h2>
                    <span class="todo-count" id="todo-count">0 terminées</span>
                </div>
                <div class="card-body">
                    <form id="todo-form">
                        <input type="text" id="todo-input" placeholder="Ajouter une nouvelle tâche..." required autocomplete="off">
                        <button type="submit" aria-label="Ajouter"><i class="fa-solid fa-plus"></i></button>
                    </form>
                    <ul class="todo-list" id="todo-list">
                        <!-- Dynamic items -->
                    </ul>
                </div>
            </section>

            <!-- Quick Info / Tech Stack Widget -->
            <section class="card widget-stats" id="widget-stats">
                <div class="card-header">
                    <h2><i class="fa-solid fa-chart-simple"></i> Statistiques Projet</h2>
                </div>
                <div class="card-body stats-grid">
                    <div class="stat-item">
                        <span class="stat-num">Git</span>
                        <p>Versionné</p>
                    </div>
                    <div class="stat-item">
                        <span class="stat-num">100%</span>
                        <p>Responsif</p>
                    </div>
                    <div class="stat-item">
                        <span class="stat-num">CSS3</span>
                        <p>Glassmorphic</p>
                    </div>
                </div>
            </section>
        </div>
    </main>

    <!-- Footer -->
    <footer class="main-footer">
        <p>Créé dans le cadre de l'exercice IFIAG Git/GitHub • © 2026</p>
    </footer>

    <!-- Local Script -->
    <script src="script.js"></script>
</body>
</html>
"""

# Let's clean the style and script originals (without widget-notes)
orig_css = mod_css.split("/* --- WIDGET NOTES --- */")[0] + "/* --- STATS / QUICK INFO WIDGET --- */" + mod_css.split("/* --- STATS / QUICK INFO WIDGET --- */")[1]
orig_js = mod_js.split("    // --- NOTES WIDGET ---")[0] + "    // Initial render\n    renderTasks();\n});\n"

# 4. Start Git init & configuration
subprocess.run(["git", "init", "-b", "master"], check=True)
subprocess.run(["git", "config", "user.name", "imad_halloul"], check=True)
subprocess.run(["git", "config", "user.email", "imad_halloul@iffiag.com"], check=True)

# 5. Write original files to files system
with open("index.html", "w", encoding="utf-8") as f:
    f.write(orig_html)
with open("style.css", "w", encoding="utf-8") as f:
    f.write(orig_css)
with open("script.js", "w", encoding="utf-8") as f:
    f.write(orig_js)

# 6. Commit on master
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "feat: initial release of premium personal dashboard"], check=True)

# 7. Create branch iffiag-exp and switch to it
subprocess.run(["git", "checkout", "-b", "iffiag-exp"], check=True)

# 8. Overwrite with modified files (with notes widget)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(mod_html)
with open("style.css", "w", encoding="utf-8") as f:
    f.write(mod_css)
with open("script.js", "w", encoding="utf-8") as f:
    f.write(mod_js)

# 9. Commit on iffiag-exp
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "feat(exp): add quick notes widget to dashboard"], check=True)

# 10. Switch to master & merge
subprocess.run(["git", "checkout", "master"], check=True)
subprocess.run(["git", "merge", "iffiag-exp"], check=True)

print("Git history successfully rebuilt with username: imad_halloul!")
