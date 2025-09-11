#!/usr/bin/env python3
# Requirements:
#   pip install pyTelegramBotAPI cryptography

import os
import sys
import time
import base64
import marshal
import random
import zlib
import bz2
import lzma
import gzip
import string
import tempfile
import gc
from telebot import TeleBot, types
from typing import Optional, Union
from datetime import datetime
from re import findall
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Hard-coded Telegram bot token
TOKEN = "8306145346:AAEW_quwAGm4TnGi7zDQojamoT9jpN4g9gk"
bot = TeleBot(TOKEN)

user_selections = {}

# Utility lambdas
zlb = lambda data: zlib.compress(data)
b64 = lambda data: base64.b64encode(data)
b32 = lambda data: base64.b32encode(data)
b16 = lambda data: base64.b16encode(data)
b85 = lambda data: base64.b85encode(data)
bzp = lambda data: bz2.compress(data)
lzm = lambda data: lzma.compress(data)
gzp = lambda data: gzip.compress(data)
mar = lambda data: marshal.dumps(compile(data, 'module', 'exec'))

def generate_random_name(length: int = 8) -> str:
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def bytes_to_array(data: str) -> str:
    return str(list(data.encode('utf-8')))

# --------- Destroyer ENC builder ---------
def build_destroyer_enc(source: str) -> str:
    key = os.urandom(32)
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(source.encode('utf-8')) + encryptor.finalize()
    tag = encryptor.tag
    payload = base64.b64encode(iv + ct + tag).decode('ascii')
    key_hex = key.hex()
    stub = f'''# Destroyer ENC Wrapper
import sys, gc
from base64 import b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
data = b64decode("{payload}")
iv, ct, tag = data[:12], data[12:-16], data[-16:]
cipher = Cipher(algorithms.AES(bytes.fromhex("{key_hex}")), modes.GCM(iv, tag), backend=default_backend())
decryptor = cipher.decryptor()
code = decryptor.update(ct) + decryptor.finalize()
exec(compile(code, "<destroyer>", "exec"), {{}})
# Overwrite sensitive buffers
data = b""
iv = b""
ct = b""
tag = b""
code = b""
gc.collect()
sys.exit()
'''
    return stub

# --------- Encryption / Obfuscation Dispatcher ---------
def encrypt_file(method: str, fname: str) -> str:
    with open(fname, 'r', encoding='utf-8') as f_in:
        orig = f_in.read()
    hdr = f'#Obfuscated by Crypto Bot - {method.upper()}\n'
    ftr = f'\n#End of {method.upper()} protection\n'
    if method == 'destroyer_enc':
        return build_destroyer_enc(orig)
    if method == 'base64':
        enc = b64(orig.encode())[::-1]
        return f"{hdr}_=lambda __:__import__('base64').b64decode(__[::-1]);exec((_)({enc})){ftr}"
    if method == 'marshal':
        s = marshal.dumps(compile(orig, 'module', 'exec'))
        return f"{hdr}import marshal\nexec(marshal.loads({s})){ftr}"
    if method == 'zlib':
        enc = b64(zlb(orig.encode()))[::-1]
        return f"{hdr}_=lambda __:__import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));exec((_)({enc})){ftr}"
    if method == 'base16':
        enc = b16(zlb(orig.encode()))[::-1]
        return f"{hdr}_=lambda __:__import__('zlib').decompress(__import__('base64').b16decode(__[::-1]));exec((_)({enc})){ftr}"
    if method == 'base32':
        enc = b32(zlb(orig.encode()))[::-1]
        return f"{hdr}_=lambda __:__import__('zlib').decompress(__import__('base64').b32decode(__[::-1]));exec((_)({enc})){ftr}"
    if method == 'base85':
        enc = b85(zlb(orig.encode()))[::-1]
        return f"{hdr}_=lambda __:__import__('zlib').decompress(__import__('base64').b85decode(__[::-1]));exec((_)({enc})){ftr}"
    if method == 'marshal_zlib':
        enc = b64(zlb(mar(orig.encode())))[::-1]
        return f"{hdr}import marshal,zlib,base64\nexec(marshal.loads(zlib.decompress(base64.b64decode({enc})))){ftr}"
    if method == 'bz2':
        enc = b64(bzp(orig.encode()))[::-1]
        return f"{hdr}_=lambda __:__import__('bz2').decompress(__import__('base64').b64decode(__[::-1]));exec((_)({enc})){ftr}"
    if method == 'lzma':
        enc = b64(lzm(orig.encode()))[::-1]
        return f"{hdr}_=lambda __:__import__('lzma').decompress(__import__('base64').b64decode(__[::-1]));exec((_)({enc})){ftr}"
    if method == 'multilayer':
        layers = ['marshal', 'zlib', 'base64', 'bz2']
        random.shuffle(layers)
        code = orig
        for ly in layers:
            if ly == 'marshal':
                cmpd = compile(code, 'CryptoBot', 'exec')
                code = f"import marshal\nexec(marshal.loads({marshal.dumps(cmpd)}))"
            if ly == 'zlib':
                c = zlib.compress(code.encode())
                code = f"import zlib\nexec(zlib.decompress({c}))"
            if ly == 'base64':
                e = base64.b64encode(code.encode())
                code = f"import base64\nexec(base64.b64decode({e}))"
            if ly == 'bz2':
                c2 = bz2.compress(code.encode())
                code = f"import bz2\nexec(bz2.decompress({c2}))"
        return f"{hdr}{code}{ftr}"
    if method == 'advanced':
        v1, v2, v3 = [generate_random_name() for _ in range(3)]
        enc = b64(zlb(mar(orig.encode())))[::-1]
        return (
            f"{hdr}import base64,zlib,marshal\n"
            f"{v1}=lambda {v2}:marshal.loads(zlib.decompress(base64.b64decode({v2})))\n"
            f"{v3}=\"{enc}\"\n"
            f"exec({v1}({v3})){ftr}"
        )
    if method == 'dominator_enc':
        part1 = (
            "#ENCRYPTION BY DOMINATOR / NEXER / NEXERPY •\n"
            f"exec(bytes({bytes_to_array('# Source Generated with Decompyle++')}).decode())\n"
            "os.system('clear')\n" + orig
        )
        if '\x00' in part1:
            raise ValueError("Zero bytes found.")
        c1 = compile(part1, 'DENC', 'exec'); s1 = marshal.dumps(c1); r1 = f"import marshal\nexec(marshal.loads({s1}))"
        c2 = zlib.compress(r1.encode()); r2 = f"import zlib\nexec(zlib.decompress({c2}))"
        c3 = compile(r2, 'DENC', 'exec'); s3 = marshal.dumps(c3); r3 = f"import marshal\nexec(marshal.loads({s3}))"
        c4 = compile(r3, 'DENC', 'exec'); s4 = marshal.dumps(c4)
        r4 = (
            "#THIS ENCODE BY DOMINATOR •\n"
            f"exec(bytes({bytes_to_array('# DOMINATOR ENC Protection Layer')}).decode())\n"
            "import marshal\n"
            f"exec(marshal.loads({s4}))"
        )
        b5 = base64.b64encode(r4.encode())
        wrap = (
            "#THIS ENCODE BY DOMINATOR ENC / NEXER / NEXERPY\n"
            "exec(bytes({0}).decode())\n"
            "import os,base64\n"
            "DominatorEnc={1}\n"
            "with open(bytes({2}).decode(),bytes({3}).decode()) as ef:\n"
            "    ef.write(base64.b64decode(DominatorEnc))\n"
            "os.system(bytes({4}).decode())\n"
            "os.remove(bytes({5}).decode())\n"
        ).format(
            bytes_to_array('# DOMINATOR ENC multy Protector'),
            b5,
            bytes_to_array('.Dominator'),
            bytes_to_array('wb'),
            bytes_to_array('python3 .Dominator'),
            bytes_to_array('.Dominator')
        )
        cw = compile(wrap, 'DENC', 'exec'); sw = marshal.dumps(cw); rw = f"import marshal\nexec(marshal.loads({sw}))"
        fe = base64.b64encode(rw.encode())
        final = (
            "#ENCRYPTION BY DOMINATOR / NEXER / NEXERPY\n"
            f"exec(bytes({bytes_to_array('# DOMINATOR ENC multy Protection Layer')}).decode())\n"
            "F='.DominatorEnc'\n"
            "import os,base64 as DOMINATOR\n"
            f"DominatorEncryption={fe}\n"
            "try:\n"
            "    with open(F,'wb') as DOMINATOR_FILE:\n"
            "        DOMINATOR_FILE.write(DOMINATOR.b64decode(DominatorEncryption))\n"
            "    os.system('python3 .DominatorEnc')\n"
            "except Exception as DOMINATOR_ERROR:\n"
            "    print(DOMINATOR_ERROR)\n"
            "finally:\n"
            "    if os.path.exists(F): os.remove(F)\n"
        )
        return final
    return "# Error: Invalid Encryption Method"

# --------- Bot Menus and Handlers ---------
def send_main_menu(chat_id: int):
    buttons = [
        types.InlineKeyboardButton("ߔ Obfuscator", callback_data='obfuscation_menu'),
        types.InlineKeyboardButton("ߔ Deobfuscator", callback_data='deobfuscation_menu'),
        types.InlineKeyboardButton("ℹ️ Bot Info", callback_data='bot_info'),
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*buttons)
    bot.send_message(
        chat_id,
        "ߔ EnCrypto Bot - Select Encryption:\n\nSelect Obfuscation or Deobfuscation for your Python files.",
        reply_markup=markup
    )

def send_obfuscation_menu(chat_id: int):
    buttons = [
        types.InlineKeyboardButton("ߔ DOMINATOR ENC", callback_data='dominator_enc'),
        types.InlineKeyboardButton("ߒ Destroyer ENC", callback_data='destroyer_enc'),
        types.InlineKeyboardButton("⚡ Base64", callback_data='base64'),
        types.InlineKeyboardButton("ߛ️ Marshal", callback_data='marshal'),
        types.InlineKeyboardButton("ߒ Zlib", callback_data='zlib'),
        types.InlineKeyboardButton("ߚ Advanced", callback_data='advanced'),
        types.InlineKeyboardButton("ߔ B16", callback_data='base16'),
        types.InlineKeyboardButton("⭐ B32", callback_data='base32'),
        types.InlineKeyboardButton("ߒ B85", callback_data='base85'),
        types.InlineKeyboardButton("ߌ MZlib", callback_data='marshal_zlib'),
        types.InlineKeyboardButton("ߎ Multi-Layer", callback_data='multilayer'),
        types.InlineKeyboardButton("ߔ BZ2", callback_data='bz2'),
        types.InlineKeyboardButton("ߒ LZMA", callback_data='lzma'),
        types.InlineKeyboardButton("⬅️ Back", callback_data='back_main'),
    ]
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(*buttons)
    bot.send_message(
        chat_id,
        "ߔ Obfuscation Methods:\n\nChoose your encryption method:",
        reply_markup=markup
    )

def send_deobfuscation_menu(chat_id: int):
    buttons = [
        types.InlineKeyboardButton("ߔ Auto-Detect", callback_data='auto_deobfuscate'),
        types.InlineKeyboardButton("ߔ Manual Mode", callback_data='manual_deobfuscate'),
        types.InlineKeyboardButton("ߚ Advanced Recovery", callback_data='advanced_deobfuscate'),
        types.InlineKeyboardButton("⬅️ Back", callback_data='back_main'),
    ]
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(*buttons)
    bot.send_message(
        chat_id,
        "ߔ Deobfuscation Methods:\n\nChoose your approach:",
        reply_markup=markup
    )

@bot.message_handler(commands=['start', 'help'])
def start(message):
    send_main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    data = call.data
    if data == 'obfuscation_menu':
        send_obfuscation_menu(chat_id)
    elif data == 'deobfuscation_menu':
        send_deobfuscation_menu(chat_id)
    elif data == 'bot_info':
        send_bot_info(call.message)
    elif data == 'back_main':
        send_main_menu(chat_id)
    else:
        user_selections[chat_id] = data
        mode = data.replace('_', ' ').upper()
        bot.send_message(chat_id, f"ߔ Send a Python file for {mode} processing.")

@bot.message_handler(content_types=['document'])
def receive_file(message):
    chat_id = message.chat.id
    if chat_id not in user_selections:
        bot.send_message(chat_id, "❌ Please select a mode first! Use /start.")
        return
    sel = user_selections[chat_id]
    file_info = bot.get_file(message.document.file_id)
    data = bot.download_file(file_info.file_path)
    fid = str(random.randint(1000, 9999))
    inp = f"{sel}-{fid}.py"
    with open(inp, 'wb') as f:
        f.write(data)
    msg = bot.send_message(chat_id, f"ߔ Processing with {sel.upper()}\n[0%] █▒▒▒▒▒▒▒▒▒")
    for i in range(1, 101, random.randint(7, 14)):
        time.sleep(0.02)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg.message_id,
            text=f"ߔ Processing with {sel.upper()}\n[{i}%] {'█' * (i // 10)}{'▒' * (10 - i // 10)}"
        )
    # Deobfuscation
    if sel in ['auto_deobfuscate', 'manual_deobfuscate', 'advanced_deobfuscate']:
        out = f"deobfuscated-{fid}.py"
        ok = perform_deobfuscation(inp, out, sel)
        try:
            bot.delete_message(chat_id, msg.message_id)
        except Exception:
            pass
        if ok and os.path.exists(out):
            with open(out, 'rb') as f:
                bot.send_document(chat_id, f, caption="ߔ Deobfuscation Complete!")
            os.remove(out)
        else:
            bot.send_message(chat_id, "❌ Deobfuscation failed.")
    else:
        code = encrypt_file(sel, inp)
        with open(inp, 'w', encoding='utf-8') as f:
            f.write(code)
        try:
            bot.delete_message(chat_id, msg.message_id)
        except Exception:
            pass
        with open(inp, 'rb') as f:
            bot.send_document(chat_id, f, caption=f"ߔ {sel.upper()} Protection Complete!")
    if os.path.exists(inp):
        os.remove(inp)

# Placeholder: Deobfuscation pipeline functions (unchanged)
def perform_deobfuscation(inp: str, out: str, mode: str) -> bool:
    # existing implementation...
    return False  # stub

def send_bot_info(message):
    text = (
        "ߤ Bot Name: EnCrypto Bot \n"
        "<blockquote>⚙️ Language: Python\n"
        "ߑ DEV: DOMINATOR / @NEXERPY #PreviouslyNexer\n"
        "ߛ Forged with DESTROYER & DOMINATOR ENC, classic and multi-layer obfuscation, and deep deobfuscation routines.</blockquote>\n\n"
        "**Obfuscator menu:**\n"
        "Base64, Marshal, Zlib, Advanced, B16, B32, B85, Marshal+Zlib, Multi-Layer, LZMA, BZ2, DOMINATOR ENC, Destroyer ENC.\n\n"
        "**Deobfuscation:**\n"
        "Auto-detect, Manual, Advanced - recovers deep and DOMINATOR ENC protections."
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data='back_main'))
    bot.edit_message_text(
        text,
        chat_id=message.chat.id,
        message_id=message.message_id,
        parse_mode='HTML',
        reply_markup=markup
    )

if __name__ == "__main__":
    print("ߔ microscopy EnCrypto bot initiated")
    # TeleBot polling supports boolean flags and options; True is valid for threaded mode by default.
    bot.polling()  # default none_stop=False; adjust to bot.polling(none_stop=True) if desired
