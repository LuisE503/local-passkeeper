import customtkinter as ctk
import webbrowser
from pathlib import Path
from passkeeper.core.vault import Vault, Credential
import uuid

# Configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
VAULT_FILE = Path.home() / ".local-passkeeper" / "vault.json"

TRANSLATIONS = {
    "English": {
        "title": "🔐 Local Passkeeper", "subtitle": "Secure, local-first password manager",
        "master_pwd": "Master Password", "unlock": "Unlock Vault", "setup_btn": "Create Vault",
        "no_vault": "Welcome to Passkeeper.", "pwd_empty": "Password cannot be empty",
        "err_unlock": "Error unlocking vault: {0}. Did you type your Master Password correctly?", "sidebar_title": "🔐 Passkeeper",
        "btn_all": "📋 All Passwords", "btn_add": "➕ Add New", "btn_inst": "📖 Settings & Info",
        "btn_gh": "⭐ GitHub", "btn_lock": "🔒 Lock Vault", "add_title": "Add New Credential",
        "add_name": "Service Name (e.g. GitHub)", "add_user": "Username / Email",
        "add_pwd": "Password", "save_cred": "Save Credential", "req_fields": "Name and Password are required!",
        "save_ok": "Saved successfully!", "save_err": "Error saving: {0}",
        "vault_title": "Your Vault", "vault_empty": "Your vault is empty.", "btn_show": "Show Pwd",
        "pwd_dialog_title": "Password for {0}\n({1})", "inst_title": "Your Local Vault",
        "setup_title": "🔒 Setup your passkeeper",
        "setup_sub": "1. Create a strong Master Password you will not forget.",
        "phrase_title": "⚠️ YOUR RECOVERY PHRASE",
        "phrase_sub": "2. Write down these 12 words in order on a piece of physical paper.\nIf you forget your password, this is the ONLY way to recover your data!",
        "btn_understood": "I have written them safely. Continue",
        "recover_link": "¿Forgot Password? Use Recovery Phrase", "recover_title": "Rescue Vault",
        "recover_sub": "Type your 12-word exact phrase below (lowercase, separated by spaces)",
        "recover_btn": "Restore Access",
        "inst_text": "Everything is encrypted locally using military-grade encryption (AES-256-GCM).\n\n📂 physical Database Location:\n{0}\n\n🔑 Keys & Recovery\nYour master password is never saved. The encryption key is derived through a combination of\nyour Master Password + your 12-word Recovery Phrase. \n\n💻 Open Source\nThis is a 100% open source project designed as a scalable secure base.\nContributions are welcome!"
    },
    "Español": {
        "title": "🔐 Administrador de Contraseñas", "subtitle": "Gestor de contraseñas seguro y local",
        "master_pwd": "Contraseña Maestra", "unlock": "Desbloquear", "setup_btn": "Crear Bóveda",
        "no_vault": "Bienvenido a Passkeeper.", "pwd_empty": "La contraseña no puede estar vacía",
        "err_unlock": "Error al desbloquear: {0}. ¿Escribió bien la contraseña?", "sidebar_title": "🔐 Passkeeper",
        "btn_all": "📋 Todas las Cuentas", "btn_add": "➕ Agregar Nueva", "btn_inst": "📖 Ajustes e Info",
        "btn_gh": "⭐ GitHub", "btn_lock": "🔒 Bloquear Bóveda", "add_title": "Agregar Nueva Credencial",
        "add_name": "Nombre de Servicio (ej. Facebook)", "add_user": "Usuario / Correo",
        "add_pwd": "Contraseña", "save_cred": "Guardar Credencial", "req_fields": "¡Nombre y Contraseña son obligatorios!",
        "save_ok": "¡Guardado exitosamente!", "save_err": "Error al guardar: {0}",
        "vault_title": "Tu Bóveda", "vault_empty": "Tu bóveda está vacía.", "btn_show": "Mostrar Pwd",
        "pwd_dialog_title": "Contraseña para {0}\n({1})", "inst_title": "Tu Bóveda Local",
        "setup_title": "🔒 Configura tu passkeeper",
        "setup_sub": "1. Crea una Contraseña Maestra fuerte que no vayas a olvidar.",
        "phrase_title": "⚠️ TU FRASE DE RECUPERACIÓN",
        "phrase_sub": "2. Anota estas 12 palabras en el orden exacto en una hoja de papel.\n¡Si olvidas tu clave, es la ÚNICA forma de recuperar tus datos!",
        "btn_understood": "Ya las he guardado. Entrar",
        "recover_link": "¿Olvidaste la clave? Usar Frase", "recover_title": "Rescatar Bóveda",
        "recover_sub": "Escribe tus 12 palabras exactas separadas por espacios",
        "recover_btn": "Restaurar Acceso",
        "inst_text": "Todo está cifrado a nivel militar localmente (AES-256-GCM).\n\n📂 Ubicación de la base de datos física:\n{0}\n\n🔑 Llaves y Recuperación\nLa app nunca guarda tu contraseña. La llave se deriva de combinar\ntu Contraseña Maestra + tu Frase de Rescate de 12 palabras. \n\n💻 Código Abierto\nProyecto 100% abierto diseñado como base escalable. ¡Contribuye!"
    },
    # Simplified fallbacks for brevity in this step, defaulting to EN keys if missing
    "中文": {"title": "🔐 密码管理器", "subtitle": "安全的本地密码管理器", "master_pwd": "主密码", "unlock": "解锁保险库", "init": "初始化保险库", "no_vault": "未找到保险库。将创建一个新的。", "pwd_empty": "密码不能为空", "err_unlock": "解锁错误: {0}", "sidebar_title": "🔐 Passkeeper", "btn_all": "📋 所有密码", "btn_add": "➕ 添加新密码", "btn_inst": "📖 使用说明", "btn_gh": "⭐ GitHub", "btn_lock": "🔒 锁定保险库", "add_title": "添加新凭据", "add_name": "服务名称 (例如 GitHub)", "add_user": "用户名 / 电子邮件", "add_pwd": "密码", "save_cred": "保存凭据", "req_fields": "名称和密码是必填项！", "save_ok": "保存成功！", "save_err": "保存错误: {0}", "vault_title": "你的保险库", "vault_empty": "你的保险库是空的。", "btn_show": "显示密码", "pwd_dialog_title": "{0} 的密码\n({1})", "inst_title": "如何使用", "inst_text": "所有内容都在本地使用军用级加密加密。主密码永远不会保存！"},
    "Português": {"title": "🔐 Gestor de Senhas", "subtitle": "Gestor seguro e local", "master_pwd": "Senha Mestra", "unlock": "Desbloquear cofre", "init": "Inicializar cofre", "no_vault": "Nenhum cofre encontrado. Um novo será criado.", "pwd_empty": "A senha não pode estar vazia", "err_unlock": "Erro ao desbloquear: {0}", "sidebar_title": "🔐 Passkeeper", "btn_all": "📋 Todas as senhas", "btn_add": "➕ Adicionar nova", "btn_inst": "📖 Instruções", "btn_gh": "⭐ GitHub", "btn_lock": "🔒 Bloquear cofre", "add_title": "Adicionar credencial", "add_name": "Serviço (ex: GitHub)", "add_user": "Usuário / E-mail", "add_pwd": "Senha", "save_cred": "Salvar", "req_fields": "Nome e Senha são obrigatórios!", "save_ok": "Salvo com sucesso!", "save_err": "Erro ao salvar: {0}", "vault_title": "Seu Cofre", "vault_empty": "O cofre está vazio.", "btn_show": "Mostrar", "pwd_dialog_title": "Senha para {0}\n({1})", "inst_title": "Como usar", "inst_text": "Tudo é criptografado localmente. Sua senha mestra nunca é salva!"},
    "Français": {"title": "🔐 Gestionnaire de Mots de Passe", "subtitle": "Gestionnaire sûr et local", "master_pwd": "Mot de passe principal", "unlock": "Déverrouiller", "init": "Initialiser", "no_vault": "Aucun coffre existant. Création d'un nouveau.", "pwd_empty": "Mot de passe requis", "err_unlock": "Erreur: {0}", "sidebar_title": "🔐 Passkeeper", "btn_all": "📋 Tous", "btn_add": "➕ Ajouter", "btn_inst": "📖 Instructions", "btn_gh": "⭐ GitHub", "btn_lock": "🔒 Verrouiller", "add_title": "Ajouter un Identifiant", "add_name": "Service (ex: GitHub)", "add_user": "Nom d'utilisateur", "add_pwd": "Mot de passe", "save_cred": "Sauvegarder", "req_fields": "Nom et mot de passe requis!", "save_ok": "Succès!", "save_err": "Erreur: {0}", "vault_title": "Votre Coffre", "vault_empty": "Votre coffre est vide.", "btn_show": "Afficher", "pwd_dialog_title": "Mot de passe {0}\n({1})", "inst_title": "Comment utiliser", "inst_text": "Tout est crypté localement. Le mot de passe principal n'est jamais sauvegardé!"},
    "Deutsch": {"title": "🔐 Passwortmanager", "subtitle": "Sicherer, lokaler Manager", "master_pwd": "Master-Passwort", "unlock": "Tresor entsperren", "init": "Tresor initialisieren", "no_vault": "Kein Tresor gefunden. Erstelle neuen.", "pwd_empty": "Passwort darf nicht leer sein", "err_unlock": "Fehler: {0}", "sidebar_title": "🔐 Passkeeper", "btn_all": "📋 Alle Passwörter", "btn_add": "➕ Neues hinzufügen", "btn_inst": "📖 Anleitung", "btn_gh": "⭐ GitHub", "btn_lock": "🔒 Sperren", "add_title": "Neuen Eintrag", "add_name": "Dienst (z.B. GitHub)", "add_user": "Benutzername", "add_pwd": "Passwort", "save_cred": "Speichern", "req_fields": "Name und Passwort benötigt!", "save_ok": "Erfolgreich gespeichert!", "save_err": "Fehler: {0}", "vault_title": "Dein Tresor", "vault_empty": "Dein Tresor ist leer.", "btn_show": "Anzeigen", "pwd_dialog_title": "Passwort für {0}\n({1})", "inst_title": "Bedienung", "inst_text": "Alles wird lokal verschlüsselt. Das Master-Passwort wird nie gespeichert!"},
    "العربية": {"title": "🔐 مدير كلمات المرور", "subtitle": "آمن ومحلي", "master_pwd": "كلمة المرور الرئيسية", "unlock": "فتح الخزنة", "init": "تهيئة الخزنة", "no_vault": "لم يتم العثور على خزنة. سيتم إنشاء واحدة.", "pwd_empty": "مطلوب كلمة مرور", "err_unlock": "خطأ: {0}", "sidebar_title": "🔐 Passkeeper", "btn_all": "📋 الكل", "btn_add": "➕ إضافة", "btn_inst": "📖 تعليمات", "btn_gh": "⭐ GitHub", "btn_lock": "🔒 قفل", "add_title": "إضافة حساب", "add_name": "الخدمة", "add_user": "اسم المستخدم", "add_pwd": "كلمة المرور", "save_cred": "حفظ", "req_fields": "الاسم وكلمة المرور مطلوبان", "save_ok": "تم الحفظ بنجاح!", "save_err": "خطأ: {0}", "vault_title": "خزنتك", "vault_empty": "الخزنة فارغة", "btn_show": "عرض", "pwd_dialog_title": "كلمة المرور لـ {0}\n({1})", "inst_title": "كيف تستعمل", "inst_text": "يتم تشفير كل شيء محليًا. لا يتم حفظ كلمة المرور الرئيسية أبدًا!"},
    "Русский": {"title": "🔐 Менеджер паролей", "subtitle": "Безопасный локальный менеджер", "master_pwd": "Мастер-пароль", "unlock": "Разблокировать", "init": "Инициализировать", "no_vault": "Хранилище не найдено. Будет создано новое.", "pwd_empty": "Пароль не может быть пустым", "err_unlock": "Ошибка: {0}", "sidebar_title": "🔐 Passkeeper", "btn_all": "📋 Все", "btn_add": "➕ Добавить", "btn_inst": "📖 Инструкции", "btn_gh": "⭐ GitHub", "btn_lock": "🔒 Заблокировать", "add_title": "Добавить аккаунт", "add_name": "Сервис", "add_user": "Имя пользователя", "add_pwd": "Пароль", "save_cred": "Сохранить", "req_fields": "Имя и пароль обязательны!", "save_ok": "Сохранено успешно!", "save_err": "Ошибка: {0}", "vault_title": "Ваше хранилище", "vault_empty": "Ваше хранилище пусто.", "btn_show": "Показать", "pwd_dialog_title": "Пароль для {0}\n({1})", "inst_title": "Как использовать", "inst_text": "Всё зашифровано локально. Мастер-пароль никогда не сохраняется!"},
    "日本語": {"title": "🔐 パスワードマネージャー", "subtitle": "安全なローカル管理", "master_pwd": "マスターパスワード", "unlock": "ロック解除", "init": "初期化", "no_vault": "Vaultがありません。新しく作成します。", "pwd_empty": "パスワードは必須です", "err_unlock": "エラー: {0}", "sidebar_title": "🔐 Passkeeper", "btn_all": "📋 すべて", "btn_add": "➕ 追加", "btn_inst": "📖 使い方", "btn_gh": "⭐ GitHub", "btn_lock": "🔒 ロック", "add_title": "アカウントの追加", "add_name": "サービス", "add_user": "ユーザー名", "add_pwd": "パスワード", "save_cred": "保存", "req_fields": "名前とパスワードは必須です！", "save_ok": "保存しました！", "save_err": "エラー: {0}", "vault_title": "Vault", "vault_empty": "Vaultは空です。", "btn_show": "表示", "pwd_dialog_title": "{0} のパスワード\n({1})", "inst_title": "使用方法", "inst_text": "データは安全にローカルで暗号化されます。マスターパスワードは保存されません！"},
    "한국어": {"title": "🔐 비밀번호 관리자", "subtitle": "안전한 로컬 관리자", "master_pwd": "마스터 비밀번호", "unlock": "잠금 해제", "init": "초기화", "no_vault": "Vault를 찾을 수 없습니다. 새로 만듭니다.", "pwd_empty": "비밀번호를 입력하세요", "err_unlock": "오류: {0}", "sidebar_title": "🔐 Passkeeper", "btn_all": "📋 전체", "btn_add": "➕ 추가", "btn_inst": "📖 설명서", "btn_gh": "⭐ GitHub", "btn_lock": "🔒 잠금", "add_title": "자격 증명 추가", "add_name": "서비스 명", "add_user": "사용자 이름", "add_pwd": "비밀번호", "save_cred": "저장", "req_fields": "이름과 비밀번호가 필요합니다!", "save_ok": "저장 완료!", "save_err": "오류: {0}", "vault_title": "귀하의 Vault", "vault_empty": "Vault가 비어 있습니다.", "btn_show": "표시", "pwd_dialog_title": "{0} 비밀번호\n({1})", "inst_title": "사용법", "inst_text": "모든 데이터는 로컬에서 암호화됩니다. 마스터 비밀번호는 절대 저장되지 않습니다!"}
}

ALL_LANGS = ["Español", "English", "中文", "Português", "Français", "Deutsch", "العربية", "Русский", "日本語", "한국어"]

class PasskeeperApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.language = "Español"
        self.title("Local Passkeeper")
        self.geometry("900x600")
        self.minsize(800, 500)
        
        self.vault = None
        self.master_password = None
        
        self.all_widgets = []
        
        # Start
        self.show_login()

    def t(self, key):
        lang_dict = TRANSLATIONS.get(self.language, TRANSLATIONS["English"])
        return lang_dict.get(key, TRANSLATIONS["English"].get(key, f"[{key}]"))

    def clear_view(self):
        for w in self.winfo_children():
            w.destroy()
        self.all_widgets = []

    def change_language(self, new_lang):
        self.language = new_lang
        # Check current state and redraw
        if self.master_password:
            self.show_dashboard()
        else:
            self.show_login()

    def build_language_selector(self, parent):
        lang_var = ctk.StringVar(value=self.language)
        selector = ctk.CTkOptionMenu(parent, values=ALL_LANGS, variable=lang_var, command=self.change_language, width=120)
        selector.pack(anchor="ne", padx=20, pady=20)

    def show_login(self):
        if VAULT_FILE.exists():
            self.show_unlock()
        else:
            self.show_setup_wizard()

    def show_setup_wizard(self):
        self.master_password = None
        self.vault = None
        self.clear_view()
        
        self.build_language_selector(self)
        
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(expand=True)
        
        title = ctk.CTkLabel(self.login_frame, text=self.t("setup_title"), font=ctk.CTkFont(size=26, weight="bold"))
        title.pack(pady=(30, 10), padx=50)
        
        subtitle = ctk.CTkLabel(self.login_frame, text=self.t("setup_sub"), font=ctk.CTkFont(size=14))
        subtitle.pack(pady=(0, 20))
        
        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text=self.t("master_pwd"), show="*", width=300, height=40)
        self.password_entry.pack(pady=10)
        
        self.btn_gen = ctk.CTkButton(self.login_frame, text=self.t("setup_btn"), command=self.generate_and_show_phrase, width=300, height=40)
        self.btn_gen.pack(pady=20)
        
        self.login_error = ctk.CTkLabel(self.login_frame, text="", text_color="red")
        self.login_error.pack()
        
    def generate_and_show_phrase(self):
        pwd = self.password_entry.get()
        if not pwd:
            self.login_error.configure(text=self.t("pwd_empty"))
            return
            
        self.master_password = pwd
        self.temporary_vault = Vault(pwd, VAULT_FILE)
        self.recovery_phrase = self.temporary_vault.generate_recovery_phrase()
        
        # Hide password entry, show phrase
        self.password_entry.pack_forget()
        self.btn_gen.pack_forget()
        self.login_error.pack_forget()
        
        # Modify titles gracefully
        for w in self.login_frame.winfo_children():
            if isinstance(w, ctk.CTkLabel) and w.cget("text") in [self.t("setup_title"), self.t("setup_sub")]:
                w.destroy()
                
        t1 = ctk.CTkLabel(self.login_frame, text=self.t("phrase_title"), text_color="#d73a49", font=ctk.CTkFont(size=22, weight="bold"))
        t1.pack(pady=(20, 10))
        
        t2 = ctk.CTkLabel(self.login_frame, text=self.t("phrase_sub"), font=ctk.CTkFont(size=12))
        t2.pack(pady=(0, 20))
        
        # Render phrase nicely
        phrase_frame = ctk.CTkFrame(self.login_frame, fg_color="#1e1e1e", border_width=1, border_color="#30363d")
        phrase_frame.pack(pady=10, padx=20, fill="x")
        
        words = self.recovery_phrase.split()
        for i in range(0, len(words), 3):
            row = ctk.CTkFrame(phrase_frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=5)
            for j in range(3):
                if i+j < len(words):
                    lbl = ctk.CTkLabel(row, text=f"{i+j+1}. {words[i+j]}", font=ctk.CTkFont(weight="bold", size=14), width=100, anchor="w")
                    lbl.pack(side="left", padx=10)
                    
        btn_ok = ctk.CTkButton(self.login_frame, text=self.t("btn_understood"), fg_color="#2ea043", hover_color="#238636", command=self.finalize_setup)
        btn_ok.pack(pady=30)
        
    def finalize_setup(self):
        self.temporary_vault.initialize_new(self.recovery_phrase)
        self.vault = self.temporary_vault
        self.show_dashboard()

    def show_unlock(self):
        self.master_password = None
        self.vault = None
        self.clear_view()
        
        self.build_language_selector(self)
        
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(expand=True)
        
        title = ctk.CTkLabel(self.login_frame, text=self.t("title"), font=ctk.CTkFont(size=30, weight="bold"))
        title.pack(pady=(50, 10), padx=50)
        
        subtitle = ctk.CTkLabel(self.login_frame, text=self.t("subtitle"), font=ctk.CTkFont(size=14))
        subtitle.pack(pady=(0, 30))
        
        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text=self.t("master_pwd"), show="*", width=300, height=40)
        self.password_entry.pack(pady=10)
        self.password_entry.bind('<Return>', lambda e: self.attempt_login())
        
        self.btn_login = ctk.CTkButton(self.login_frame, text=self.t("unlock"), command=self.attempt_login, width=300, height=40)
        self.btn_login.pack(pady=10)
        
        self.btn_recover = ctk.CTkButton(self.login_frame, text=self.t("recover_link"), command=self.show_recovery, fg_color="transparent", text_color="#58a6ff", hover_color="#1f2428")
        self.btn_recover.pack(pady=10)
        
        self.login_error = ctk.CTkLabel(self.login_frame, text="", text_color="red")
        self.login_error.pack(pady=10)

    def show_recovery(self):
        self.clear_view()
        self.build_language_selector(self)
        
        frame = ctk.CTkFrame(self)
        frame.pack(expand=True)
        
        t = ctk.CTkLabel(frame, text=self.t("recover_title"), text_color="#d73a49", font=ctk.CTkFont(size=26, weight="bold"))
        t.pack(pady=(30,10), padx=50)
        
        sub = ctk.CTkLabel(frame, text=self.t("recover_sub"))
        sub.pack(pady=(0,20))
        
        self.phrase_entry = ctk.CTkEntry(frame, width=400, height=40)
        self.phrase_entry.pack(pady=10)
        
        self.pwd_new_entry = ctk.CTkEntry(frame, placeholder_text="New Master Password", show="*", width=400, height=40)
        self.pwd_new_entry.pack(pady=10)
        
        btn = ctk.CTkButton(frame, text=self.t("recover_btn"), width=400, height=40, command=self.attempt_recovery)
        btn.pack(pady=20)
        
        self.rec_error = ctk.CTkLabel(frame, text="", text_color="red")
        self.rec_error.pack()
        
    def attempt_recovery(self):
        phrase = self.phrase_entry.get().strip().lower()
        new_pwd = self.pwd_new_entry.get()
        if not phrase or not new_pwd:
             self.rec_error.configure(text=self.t("req_fields"))
             return
             
        try:
             # Attempt to load vault by providing the phrase. If it works, rewrite with the new password
             v = Vault(new_pwd, VAULT_FILE)
             v.load(provided_recovery_phrase=phrase)
             # Resave to re-encrypt with the new password combinations
             v.save()
             self.vault = v
             self.master_password = new_pwd
             self.show_dashboard()
        except Exception as e:
             self.rec_error.configure(text=f"Failed to recover: {str(e)}")

    def attempt_login(self):
        pwd = self.password_entry.get()
        if not pwd:
            self.login_error.configure(text=self.t("pwd_empty"))
            return
            
        try:
            self.vault = Vault(pwd, VAULT_FILE)
            self.vault.load()
            
            self.master_password = pwd
            self.show_dashboard()
        except Exception as e:
            self.login_error.configure(text=self.t("err_unlock").format(str(e)))

    def show_dashboard(self):
        self.clear_view()
        
        self.dashboard_frame = ctk.CTkFrame(self)
        self.dashboard_frame.pack(fill="both", expand=True)
        self.dashboard_frame.grid_columnconfigure(1, weight=1)
        self.dashboard_frame.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self.dashboard_frame, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        logo = ctk.CTkLabel(self.sidebar_frame, text=self.t("sidebar_title"), font=ctk.CTkFont(size=20, weight="bold"))
        logo.pack(pady=20, padx=20)
        
        btn_list = ctk.CTkButton(self.sidebar_frame, text=self.t("btn_all"), command=self.show_list_tab)
        btn_list.pack(pady=10, padx=20)
        
        btn_add = ctk.CTkButton(self.sidebar_frame, text=self.t("btn_add"), command=self.show_add_tab)
        btn_add.pack(pady=10, padx=20)
        
        btn_instructions = ctk.CTkButton(self.sidebar_frame, text=self.t("btn_inst"), command=self.show_instructions_tab, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        btn_instructions.pack(pady=(50, 10), padx=20)
        
        btn_github = ctk.CTkButton(self.sidebar_frame, text=self.t("btn_gh"), command=self.open_github, fg_color="#2ea043", hover_color="#238636")
        btn_github.pack(pady=10, padx=20)
        
        lang_var = ctk.StringVar(value=self.language)
        selector = ctk.CTkOptionMenu(self.sidebar_frame, values=ALL_LANGS, variable=lang_var, command=self.change_language)
        selector.pack(pady=20, padx=20)
        
        btn_lock = ctk.CTkButton(self.sidebar_frame, text=self.t("btn_lock"), command=self.show_login, fg_color="transparent", hover_color="#c53030")
        btn_lock.pack(side="bottom", pady=20, padx=20)
        
        # Main Content Area
        self.main_frame = ctk.CTkFrame(self.dashboard_frame, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.build_add_tab()
        self.build_list_tab()
        self.build_instructions_tab()
        self.show_list_tab()

    def hide_all_tabs(self):
        self.add_tab_frame.pack_forget()
        self.list_tab_frame.pack_forget()
        self.instr_tab_frame.pack_forget()

    def show_add_tab(self):
        self.hide_all_tabs()
        self.add_tab_frame.pack(fill="both", expand=True)
        
    def show_list_tab(self):
        self.hide_all_tabs()
        self.refresh_list()
        self.list_tab_frame.pack(fill="both", expand=True)
        
    def show_instructions_tab(self):
        self.hide_all_tabs()
        self.instr_tab_frame.pack(fill="both", expand=True)

    def build_add_tab(self):
        self.add_tab_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        title = ctk.CTkLabel(self.add_tab_frame, text=self.t("add_title"), font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(anchor="w", pady=(0, 20))
        
        self.add_name = ctk.CTkEntry(self.add_tab_frame, placeholder_text=self.t("add_name"), width=400)
        self.add_name.pack(anchor="w", pady=10)
        
        self.add_user = ctk.CTkEntry(self.add_tab_frame, placeholder_text=self.t("add_user"), width=400)
        self.add_user.pack(anchor="w", pady=10)
        
        self.add_pwd = ctk.CTkEntry(self.add_tab_frame, placeholder_text=self.t("add_pwd"), show="*", width=400)
        self.add_pwd.pack(anchor="w", pady=10)
        
        btn_save = ctk.CTkButton(self.add_tab_frame, text=self.t("save_cred"), command=self.save_credential, width=200)
        btn_save.pack(anchor="w", pady=20)
        
        self.add_msg = ctk.CTkLabel(self.add_tab_frame, text="")
        self.add_msg.pack(anchor="w")

    def save_credential(self):
        name = self.add_name.get()
        user = self.add_user.get()
        pwd = self.add_pwd.get()
        
        if not name or not pwd:
            self.add_msg.configure(text=self.t("req_fields"), text_color="red")
            return
            
        try:
            cipher, nonce = self.vault.encrypt_password(pwd)
            cred = Credential(id=str(uuid.uuid4()), name=name, username=user, password_cipher=cipher, nonce=nonce)
            self.vault.add_credential(cred)
            
            self.add_name.delete(0, 'end')
            self.add_user.delete(0, 'end')
            self.add_pwd.delete(0, 'end')
            self.add_msg.configure(text=self.t("save_ok"), text_color="green")
        except Exception as e:
            self.add_msg.configure(text=self.t("save_err").format(str(e)), text_color="red")

    def build_list_tab(self):
        self.list_tab_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        title = ctk.CTkLabel(self.list_tab_frame, text=self.t("vault_title"), font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(anchor="w", pady=(0, 20))
        
        self.scroll_list = ctk.CTkScrollableFrame(self.list_tab_frame, width=600, height=400)
        self.scroll_list.pack(fill="both", expand=True)

    def refresh_list(self):
        for widget in self.scroll_list.winfo_children():
            widget.destroy()
            
        if not self.vault:
            return
            
        creds = self.vault.list_credentials()
        if not creds:
            lbl = ctk.CTkLabel(self.scroll_list, text=self.t("vault_empty"), text_color="gray")
            lbl.pack(pady=20)
            return
            
        for c in creds:
            row = ctk.CTkFrame(self.scroll_list)
            row.pack(fill="x", pady=5, padx=5)
            
            info = ctk.CTkLabel(row, text=f"{c.name} ({c.username})", font=ctk.CTkFont(weight="bold"), anchor="w", width=300)
            info.pack(side="left", padx=10, pady=10)
            
            btn_show = ctk.CTkButton(row, text=self.t("btn_show"), width=100, command=lambda cred=c: self.show_password(cred))
            btn_show.pack(side="right", padx=10)

    def show_password(self, cred: Credential):
        try:
            pwd = self.vault.decrypt_password(cred.password_cipher, cred.nonce)
            # Create a quick popup dialogue
            dialog = ctk.CTkToplevel(self)
            dialog.title(cred.name)
            dialog.geometry("400x200")
            dialog.attributes('-topmost', True)
            
            lbl = ctk.CTkLabel(dialog, text=self.t("pwd_dialog_title").format(cred.name, cred.username), font=ctk.CTkFont(weight="bold"))
            lbl.pack(pady=20)
            
            entry = ctk.CTkEntry(dialog, width=300, justify="center")
            entry.pack(pady=10)
            entry.insert(0, pwd)
            entry.configure(state="readonly")
            
        except Exception as e:
            print(f"Decryption failed: {e}")

    def build_instructions_tab(self):
        self.instr_tab_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        title = ctk.CTkLabel(self.instr_tab_frame, text=self.t("inst_title"), font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(anchor="w", pady=(0, 20))
        
        lbl_text = ctk.CTkLabel(self.instr_tab_frame, text=self.t("inst_text").format(str(VAULT_FILE)), justify="left", font=ctk.CTkFont(size=14))
        lbl_text.pack(anchor="w")

    def open_github(self):
        webbrowser.open("https://github.com/LuisE503/local-passkeeper")

def main():
    app = PasskeeperApp()
    app.mainloop()

if __name__ == "__main__":
    main()
