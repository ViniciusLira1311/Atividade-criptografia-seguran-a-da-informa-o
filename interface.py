import tkinter as tk
from tkinter import ttk, messagebox
import importlib
import config

class CriptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ferramenta de Criptografia")
        self.root.geometry("650x550")
        self.root.resizable(True, True)

        self.cifra_var = tk.StringVar(value=config.NOMES_DAS_CIFRAS[0])
        self.chave_var = tk.StringVar(value="3")

        self.criar_widgets()
        self.atualizar_estado_chave()

    def criar_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Texto de entrada
        ttk.Label(main_frame, text="Texto original:").grid(row=0, column=0, sticky=tk.W, pady=(0,5))
        self.texto_entrada = tk.Text(main_frame, height=8, width=70, wrap=tk.WORD)
        self.texto_entrada.grid(row=1, column=0, columnspan=3, pady=(0,10), sticky=tk.W+tk.E)

        # Cifra
        ttk.Label(main_frame, text="Cifra:").grid(row=2, column=0, sticky=tk.W, pady=(0,5))
        self.combo_cifras = ttk.Combobox(main_frame, textvariable=self.cifra_var,
                                         values=config.NOMES_DAS_CIFRAS, state="readonly")
        self.combo_cifras.grid(row=2, column=1, sticky=tk.W, pady=(0,5))
        self.combo_cifras.bind("<<ComboboxSelected>>", self.atualizar_estado_chave)

        # Chave (deslocamento)
        self.frame_chave = ttk.Frame(main_frame)
        self.frame_chave.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(0,10))
        ttk.Label(self.frame_chave, text="Chave:").pack(side=tk.LEFT, padx=(0,5))
        self.entry_chave = ttk.Entry(self.frame_chave, textvariable=self.chave_var, width=10)
        self.entry_chave.pack(side=tk.LEFT)
        ttk.Button(self.frame_chave, text="Gerar chave aleatória", command=self.gerar).pack(side=tk.LEFT, padx=5)

        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=3, pady=10)
        ttk.Button(btn_frame, text="Criptografar", command=self.criptografar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Descriptografar", command=self.descriptografar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar).pack(side=tk.LEFT, padx=5)

        # Resultado
        ttk.Label(main_frame, text="Resultado:").grid(row=5, column=0, sticky=tk.W, pady=(0,5))
        self.texto_resultado = tk.Text(main_frame, height=8, width=70, wrap=tk.WORD)
        self.texto_resultado.grid(row=6, column=0, columnspan=3, pady=(0,10), sticky=tk.W+tk.E)

        # Configurar expansão
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)

    def atualizar_estado_chave(self, event=None):
        if self.cifra_var.get() in config.CIFRAS_COM_CHAVE:
            self.entry_chave.config(state="normal")
        else:
            self.entry_chave.config(state="disabled")
            self.chave_var.set("")

    def obter_texto_origem(self):
        return self.texto_entrada.get("1.0", tk.END).rstrip("\n")

    def definir_texto_destino(self, texto):
        self.texto_resultado.delete("1.0", tk.END)
        self.texto_resultado.insert("1.0", texto)

    def _executar(self, operacao):
        texto = self.obter_texto_origem()
        if not texto.strip():
            messagebox.showwarning("Aviso", "Digite um texto.")
            return

        cifra_nome = self.cifra_var.get()
        if cifra_nome not in config.MAPEAMENTO_MODULOS:
            messagebox.showerror("Erro", f"Cifra '{cifra_nome}' não configurada.")
            return

        modulo_nome = config.MAPEAMENTO_MODULOS[cifra_nome]
        chave = self.chave_var.get()

        try:
            modulo = importlib.import_module(f"cifras.{modulo_nome}")
            func = getattr(modulo, operacao, None)
            if not func:
                messagebox.showerror("Erro", f"Função '{operacao}' não encontrada em {modulo_nome}.")
                return
            resultado = func() if operacao == "gerar" else func(texto, chave)
            self.definir_texto_destino(resultado)
        except Exception as e:
            messagebox.showerror("Erro", f"{str(e)}")

    def criptografar(self):
        self._executar("criptografar")

    def descriptografar(self):
        self._executar("descriptografar")

    def gerar(self):
        self._executar("gerar")

    def limpar(self):
        self.texto_entrada.delete("1.0", tk.END)
        self.texto_resultado.delete("1.0", tk.END)
