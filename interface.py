# interface.py - Interface com limpeza de chave ao trocar de cifra

import tkinter as tk
from tkinter import ttk, messagebox
import importlib
import config

class CriptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ferramenta de Criptografia - Interface Modular")
        self.root.geometry("700x580")
        self.root.resizable(True, True)

        self.cifra_var = tk.StringVar(value=config.NOMES_DAS_CIFRAS[0] if config.NOMES_DAS_CIFRAS else "")
        self.chave_var = tk.StringVar(value="")

        self.criar_widgets()
        self.atualizar_estado_chave()

    def criar_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Texto de entrada
        ttk.Label(main_frame, text="Texto original:").grid(row=0, column=0, sticky=tk.W, pady=(0,5))
        self.texto_entrada = tk.Text(main_frame, height=8, width=70, wrap=tk.WORD)
        self.texto_entrada.grid(row=1, column=0, columnspan=3, pady=(0,10), sticky=tk.W+tk.E)

        # Seleção da cifra
        ttk.Label(main_frame, text="Cifra:").grid(row=2, column=0, sticky=tk.W, pady=(0,5))
        self.combo_cifras = ttk.Combobox(main_frame, textvariable=self.cifra_var,
                                         values=config.NOMES_DAS_CIFRAS, state="readonly")
        self.combo_cifras.grid(row=2, column=1, sticky=tk.W, pady=(0,5))
        self.combo_cifras.bind("<<ComboboxSelected>>", self.atualizar_estado_chave)

        # Frame da chave
        self.frame_chave = ttk.Frame(main_frame)
        self.frame_chave.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=(0,10))
        
        self.label_chave = ttk.Label(self.frame_chave, text="Chave / Deslocamento:")
        self.label_chave.pack(side=tk.LEFT, padx=(0,5))
        
        self.entry_chave = ttk.Entry(self.frame_chave, textvariable=self.chave_var, width=25)
        self.entry_chave.pack(side=tk.LEFT, padx=(0,5))
        
        # Botão para gerar chave aleatória (inicialmente invisível)
        self.btn_gerar_chave = ttk.Button(self.frame_chave, text="🎲 Gerar Alfabeto Aleatório",
                                          command=self.gerar_chave_aleatoria)

        # Botões de ação
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=3, pady=10)
        ttk.Button(btn_frame, text="Criptografar", command=self.criptografar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Descriptografar", command=self.descriptografar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar tudo", command=self.limpar).pack(side=tk.LEFT, padx=5)

        # Resultado
        ttk.Label(main_frame, text="Resultado:").grid(row=5, column=0, sticky=tk.W, pady=(0,5))
        self.texto_resultado = tk.Text(main_frame, height=8, width=70, wrap=tk.WORD)
        self.texto_resultado.grid(row=6, column=0, columnspan=3, pady=(0,10), sticky=tk.W+tk.E)

        # Redimensionamento
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=0)
        main_frame.columnconfigure(2, weight=0)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)

    def atualizar_estado_chave(self, event=None):
        """Limpa o campo de chave e configura o estado conforme a cifra escolhida."""
        # Sempre limpa a chave ao trocar de cifra
        self.chave_var.set("")
        
        cifra_atual = self.cifra_var.get()
        if cifra_atual in config.CIFRAS_COM_CHAVE:
            if cifra_atual == "Monoalfabética":
                # Campo somente leitura, usuário não pode digitar
                self.entry_chave.config(state="readonly")
                self.btn_gerar_chave.pack(side=tk.LEFT, padx=(5,0))
                # Gera uma chave aleatória automaticamente
                self.gerar_chave_aleatoria()
            else:
                # Cifras como César e Playfair: campo editável
                self.entry_chave.config(state="normal")
                self.btn_gerar_chave.pack_forget()
        else:
            # Cifras sem chave (Atbash, ROT13)
            self.entry_chave.config(state="disabled")
            self.btn_gerar_chave.pack_forget()

    def gerar_chave_aleatoria(self):
        """Gera um alfabeto aleatório e insere no campo de chave."""
        try:
            modulo = importlib.import_module("cifras.monoalfabetica")
            chave_aleatoria = modulo.gerar_alfabeto_aleatorio()
            self.chave_var.set(chave_aleatoria)
            # Opcional: exibir notificação apenas se não for chamado automaticamente
            # messagebox.showinfo("Chave gerada", f"Alfabeto aleatório:\n{chave_aleatoria}")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível gerar chave: {str(e)}")

    def obter_texto_origem(self):
        return self.texto_entrada.get("1.0", tk.END).rstrip("\n")

    def definir_texto_destino(self, texto):
        self.texto_resultado.delete("1.0", tk.END)
        self.texto_resultado.insert("1.0", texto)

    def _executar(self, operacao):
        texto = self.obter_texto_origem()
        if not texto.strip():
            messagebox.showwarning("Aviso", "Digite algum texto.")
            return

        cifra_nome = self.cifra_var.get()
        if cifra_nome not in config.MAPEAMENTO_MODULOS:
            messagebox.showerror("Erro", f"Cifra '{cifra_nome}' não configurada.")
            return

        modulo_nome = config.MAPEAMENTO_MODULOS[cifra_nome]
        chave = self.chave_var.get()

        # Verifica se a cifra exige chave e se ela está vazia
        if cifra_nome in config.CIFRAS_COM_CHAVE and not chave:
            messagebox.showwarning("Aviso", f"A cifra '{cifra_nome}' requer uma chave. Preencha o campo.")
            return

        try:
            modulo = importlib.import_module(f"cifras.{modulo_nome}")
            func = getattr(modulo, operacao, None)
            if not func:
                messagebox.showerror("Erro", f"Função '{operacao}' não encontrada em {modulo_nome}.")
                return
            resultado = func(texto, chave)
            self.definir_texto_destino(resultado)
        except ValueError as e:
            messagebox.showerror("Erro na chave", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"{operacao}: {str(e)}")

    def criptografar(self):
        self._executar("criptografar")

    def descriptografar(self):
        self._executar("descriptografar")

    def limpar(self):
        self.texto_entrada.delete("1.0", tk.END)
        self.texto_resultado.delete("1.0", tk.END)