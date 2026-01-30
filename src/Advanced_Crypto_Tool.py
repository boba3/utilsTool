import os
import customtkinter as ctk
from tkinter import messagebox, filedialog
import hashlib
import base64
import time
import threading
import multiprocessing
import itertools
import string
from hashids import Hashids
from gmssl import sm3, sm4
from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad, unpad

# --- 全局 MD5 多核工作函数 ---
def md5_worker(target_hash, chars, length, start_index, step, found_event, result_queue, timeout_time):
    it = itertools.islice(itertools.product(chars, repeat=length), start_index, None, step)
    for guess in it:
        if found_event.is_set() or time.time() > timeout_time:
            return
        guess_str = "".join(guess)
        if hashlib.md5(guess_str.encode()).hexdigest() == target_hash:
            result_queue.put(guess_str)
            found_event.set()
            return

class AdvancedCryptoTool(ctk.CTk):
    def __init__(self):
        super().__init__()
        # 路径与字典初始化
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.dict_file = os.path.join(base_dir, "md5dictionary.txt")
        self.ensure_dict_exists()
        
        # 窗口设置
        self.title("安全加解密工作台 v4.0 (国密增强版)")
        self.geometry("1100x820")
        self.current_algo = "MD5"
        ctk.set_appearance_mode("Light") 
        
        self.setup_ui()
        self.update_dict_status()

    def setup_ui(self):
        # --- 顶部：算法与主题 ---
        self.top_frame = ctk.CTkFrame(self, height=70)
        self.top_frame.pack(side="top", fill="x", padx=20, pady=10)
        
        self.algo_segmented = ctk.CTkSegmentedButton(
            self.top_frame, 
            values=["MD5", "SM3", "Base64", "DES", "AES", "SM4", "Hashids"], 
            command=self.on_algo_change,
            selected_color="#409EFF"
        )
        self.algo_segmented.set("MD5")
        self.algo_segmented.pack(side="left", padx=20, pady=15)

        ctk.CTkLabel(self.top_frame, text="主题:").pack(side="left", padx=(20, 5))
        self.theme_menu = ctk.CTkOptionMenu(
            self.top_frame, values=["Light", "Dark", "System"],
            command=ctk.set_appearance_mode, width=90,
            fg_color="#409EFF", button_color="#409EFF"
        )
        self.theme_menu.set("Light")
        self.theme_menu.pack(side="left", padx=10)

        # --- 中间：参数管理 ---
        self.param_frame = ctk.CTkFrame(self)
        self.param_frame.pack(side="top", fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(self.param_frame, text="密钥/盐值:").grid(row=0, column=0, padx=10, pady=10)
        self.key_entry = ctk.CTkEntry(self.param_frame, placeholder_text="Key / Salt (SM4需16位)", width=200)
        self.key_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # 高性能开关 (圆点颜色同步)
        self.high_perf_var = ctk.BooleanVar(value=False)
        self.switch_perf = ctk.CTkSwitch(
            self.param_frame, text="高性能(多核)", 
            variable=self.high_perf_var, command=self.sync_switch_color,
            progress_color="#409EFF", fg_color="#CDD0D6",
            button_color="#CDD0D6", button_hover_color="#CDD0D6"
        )
        self.switch_perf.grid(row=0, column=2, padx=15)

        # 字典统计区
        self.dict_mgr_frame = ctk.CTkFrame(self.param_frame, fg_color="transparent")
        self.dict_mgr_frame.grid(row=0, column=3, padx=10)
        self.lbl_dict_info = ctk.CTkLabel(self.dict_mgr_frame, text="0 条 / 0 KB")
        self.lbl_dict_info.pack(side="left", padx=5)
        
        self.btn_clean = ctk.CTkButton(self.dict_mgr_frame, text="清洗", width=50, height=24, fg_color="#F56C6C", hover_color="#f89898", command=self.clean_dictionary)
        self.btn_clean.pack(side="left", padx=2)
        self.btn_export = ctk.CTkButton(self.dict_mgr_frame, text="导出", width=50, height=24, fg_color="#409EFF", hover_color="#79bbff", command=self.export_dictionary)
        self.btn_export.pack(side="left", padx=2)
        self.btn_refresh = ctk.CTkButton(self.dict_mgr_frame, text="↺", width=30, height=24, command=self.update_dict_status)
        self.btn_refresh.pack(side="left", padx=2)

        self.param_frame.grid_columnconfigure(1, weight=1)

        # --- 底部：主操作区 ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(side="top", fill="both", expand=True, padx=20, pady=10)

        self.text_plain = self.create_text_area(self.main_frame, "明文 (数值/文本)", "left")
        
        self.mid_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.mid_frame.pack(side="left", fill="y", padx=15)
        
        self.btn_encrypt = ctk.CTkButton(self.mid_frame, text="加密 ▶", fg_color="#409EFF", hover_color="#79bbff", command=self.handle_encrypt, width=120, height=45, font=("Arial", 13, "bold"))
        self.btn_encrypt.pack(pady=(220, 10))
        
        self.btn_decrypt = ctk.CTkButton(self.mid_frame, text="◀ 解密/破解", fg_color="#67C23A", hover_color="#95d475", command=self.handle_decrypt_thread, width=120, height=45, font=("Arial", 13, "bold"))
        self.btn_decrypt.pack(pady=10)

        self.text_cipher = self.create_text_area(self.main_frame, "密文 (Hash/Cipher)", "right")

    # --- 辅助与逻辑函数 ---
    def sync_switch_color(self):
        color = "#409EFF" if self.high_perf_var.get() else "#CDD0D6"
        self.switch_perf.configure(button_color=color, button_hover_color=color)

    def create_text_area(self, master, label, side):
        f = ctk.CTkFrame(master)
        f.pack(side=side, fill="both", expand=True, padx=5)
        ctk.CTkLabel(f, text=label, font=("Arial", 14, "bold")).pack(pady=5)
        t = ctk.CTkTextbox(f, font=("Consolas", 12), undo=True)
        t.pack(fill="both", expand=True, padx=10, pady=10)
        return t

    def handle_encrypt(self):
        algo, content, key = self.current_algo, self.text_plain.get("1.0", "end-1c").strip(), self.key_entry.get()
        if not content: return
        try:
            res = ""
            if algo == "MD5":
                res = hashlib.md5(content.encode()).hexdigest()
                self.save_to_dict(content, res)
            elif algo == "SM3":
                res = sm3.sm3_hash(list(content.encode()))
                self.save_to_dict(content, res)
            elif algo == "Base64":
                res = base64.b64encode(content.encode()).decode()
            elif algo in ["DES", "AES"]:
                mode, bs = (DES, 8) if algo == "DES" else (AES, 16)
                cipher = mode.new(key.encode(), mode.MODE_ECB)
                res = base64.b64encode(cipher.encrypt(pad(content.encode(), bs))).decode()
            elif algo == "SM4":
                if len(key) != 16: raise ValueError("SM4密钥须为16位")
                crypt_sm4 = sm4.CryptSM4()
                crypt_sm4.set_key(key.encode(), sm4.SM4_ENCRYPT)
                res = base64.b64encode(crypt_sm4.crypt_ecb(content.encode())).decode()
            elif algo == "Hashids":
                hid = Hashids(salt=key or "salt", min_length=6)
                nums = [int(n.strip()) for n in content.replace("，", ",").split(",") if n.strip().isdigit()]
                if not nums: raise ValueError("请输入数字列表")
                res = hid.encode(*nums)
            
            self.text_cipher.delete("1.0", "end")
            self.text_cipher.insert("1.0", res)
        except Exception as e: messagebox.showerror("错误", str(e))

    def handle_decrypt_thread(self):
        threading.Thread(target=self.handle_decrypt, daemon=True).start()

    def handle_decrypt(self):
        algo, content, key = self.current_algo, self.text_cipher.get("1.0", "end-1c").strip(), self.key_entry.get()
        if not content: return
        self.btn_decrypt.configure(state="disabled", text="处理中...")
        try:
            res = ""
            if algo in ["MD5", "SM3"]:
                pairs = self.get_all_from_dict()
                c_low = content.lower()
                if c_low in pairs: res = f"{pairs[c_low]}"
                elif algo == "MD5":
                    self.show_plain("正在破解...")
                    res = self.multi_core_brute_force(c_low) if self.high_perf_var.get() else self.single_core_brute_force(c_low)
                    if res and res != "TIMEOUT": self.save_to_dict(res, c_low)
                else: res = "[字典未命中]"
            elif algo == "Base64": res = base64.b64decode(content).decode()
            elif algo in ["DES", "AES"]:
                mode, bs = (DES, 8) if algo == "DES" else (AES, 16)
                cipher = mode.new(key.encode(), mode.MODE_ECB)
                res = unpad(cipher.decrypt(base64.b64decode(content)), bs).decode()
            elif algo == "SM4":
                if len(key) != 16: raise ValueError("SM4密钥须为16位")
                crypt_sm4 = sm4.CryptSM4()
                crypt_sm4.set_key(key.encode(), sm4.SM4_DECRYPT)
                res = crypt_sm4.crypt_ecb(base64.b64decode(content)).decode()
            elif algo == "Hashids":
                hid = Hashids(salt=key or "salt", min_length=6)
                res = ", ".join(map(str, hid.decode(content))) or "[解密失败]"
            self.show_plain(res if res else "[操作失败]")
        except: messagebox.showerror("错误", "解密失败，请检查数据或密钥")
        finally: self.btn_decrypt.configure(state="normal", text="◀ 解密/破解")

    def multi_core_brute_force(self, target):
        cpus = max(1, os.cpu_count() - 2)
        chars = string.ascii_lowercase + string.digits
        q, ev, limit = multiprocessing.Queue(), multiprocessing.Event(), time.time() + 60
        procs = []
        for L in range(1, 7):
            for i in range(cpus):
                p = multiprocessing.Process(target=md5_worker, args=(target, chars, L, i, cpus, ev, q, limit))
                p.start(); procs.append(p)
            while any(p.is_alive() for p in procs):
                if ev.is_set() or time.time() > limit: break
                time.sleep(0.1)
            if ev.is_set(): break
        res = q.get() if not q.empty() else ("TIMEOUT" if time.time() > limit else None)
        for p in procs: p.terminate()
        return res

    def single_core_brute_force(self, target):
        start, chars = time.time(), string.ascii_lowercase + string.digits
        for L in range(1, 7):
            for g in itertools.product(chars, repeat=L):
                if time.time() - start > 60: return "TIMEOUT"
                gs = "".join(g)
                if hashlib.md5(gs.encode()).hexdigest() == target: return gs
        return None

    def save_to_dict(self, p, c):
        if c not in self.get_all_from_dict():
            with open(self.dict_file, "a", encoding="utf-8") as f: f.write(f"{c}:{p}\n")
            self.update_dict_status()

    def get_all_from_dict(self):
        pairs = {}
        if os.path.exists(self.dict_file):
            with open(self.dict_file, "r", encoding="utf-8") as f:
                for l in f:
                    if ":" in l:
                        parts = l.strip().split(":", 1)
                        if len(parts) == 2: pairs[parts[0]] = parts[1]
        return pairs

    def clean_dictionary(self):
        if not os.path.exists(self.dict_file): return
        with open(self.dict_file, "r", encoding="utf-8") as f: lines = f.readlines()
        unique = sorted(list(set(l.strip() for l in lines if ":" in l)))
        with open(self.dict_file, "w", encoding="utf-8") as f:
            for l in unique: f.write(l + "\n")
        self.update_dict_status()
        messagebox.showinfo("清洗", "去重及排序完成")

    def update_dict_status(self):
        try:
            size = os.path.getsize(self.dict_file) / 1024
            count = sum(1 for l in open(self.dict_file, 'r', encoding='utf-8') if l.strip())
            self.lbl_dict_info.configure(text=f"{count} 条 / {size:.1f} KB")
        except: pass

    def export_dictionary(self):
        p = filedialog.asksaveasfilename(defaultextension=".txt")
        if p: import shutil; shutil.copy2(self.dict_file, p)

    def show_plain(self, t): 
        self.text_plain.delete("1.0", "end")
        self.text_plain.insert("1.0", t)

    def ensure_dict_exists(self): 
        if not os.path.exists(self.dict_file): open(self.dict_file, "w").close()

    def on_algo_change(self, v): self.current_algo = v

if __name__ == "__main__":
    multiprocessing.freeze_support()
    AdvancedCryptoTool().mainloop()
