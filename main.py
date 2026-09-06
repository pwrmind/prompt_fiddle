# /// script
# dependencies = [
#   "pyyaml",
#   "requests",
#   "colorama",
# ]
# ///

import os
import sys
import json
import yaml
import requests
import difflib
from colorama import init, Fore, Style

init(autoreset=True)

DEFAULT_OPTIONS = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "num_ctx": 2048,
    "repeat_penalty": 1.1,
}

CACHE_FILE = ".prompt_cache.txt"

def load_config(config_path):
    if not os.path.exists(config_path):
        print(f"{Fore.RED}❌ Ошибка: Файл конфигурации {config_path} не найден.")
        sys.exit(1)
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f) or {}
    user_options = config.get('options', {})
    merged_options = {**DEFAULT_OPTIONS, **{k: v for k, v in user_options.items() if v is not None}}
    config['options'] = merged_options
    return config

def load_input(input_path):
    if not os.path.exists(input_path):
        print(f"{Fore.RED}❌ Ошибка: Входной файл {input_path} не найден.")
        sys.exit(1)
    with open(input_path, 'r', encoding='utf-8') as f:
        return f.read()

def show_diff(old_text, new_text):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ ОТВЕТОМ:")
    print(f"{Fore.GREEN}+ Добавлено{Fore.RESET}  {Fore.RED}- Удалено{Fore.RESET}\n" + "-" * 50)
    old_lines = old_text.splitlines()
    new_lines = new_text.splitlines()
    diff = difflib.ndiff(old_lines, new_lines)
    has_changes = False
    for line in diff:
        if line.startswith('+ '):
            print(f"{Fore.GREEN}{line}")
            has_changes = True
        elif line.startswith('- '):
            print(f"{Fore.RED}{line}")
            has_changes = True
        elif line.startswith('? '):
            print(f"{Fore.BLUE}{line}")
        else:
            print(f"{Style.DIM}{line}")
    if not has_changes:
        print(f"{Fore.YELLOW}Текст ответа абсолютно идентичен предыдущему.")
    print("-" * 50)

def run_prompt(config_path, input_path):
    config = load_config(config_path)
    raw_text = load_input(input_path)
    model = config.get('model')
    if not model:
        print(f"{Fore.RED}❌ Ошибка: В конфигурации не указана модель.")
        sys.exit(1)
    api_url = f"{config.get('api_base', 'http://localhost:11434')}/api/generate"
    payload = {
        "model": model,
        "prompt": raw_text,
        "system": config.get('system_prompt', ''),
        "stream": True,
        "options": config.get('options', {})
    }
    print(f"{Fore.BLUE}🚀 Запуск модели '{model}'...")
    print(f"⚙️ Параметры: {json.dumps(payload['options'], ensure_ascii=False)}")
    print("-" * 50)
    current_response = []
    try:
        response = requests.post(api_url, json=payload, stream=True)
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line.decode('utf-8'))
                text_chunk = chunk.get('response', '')
                current_response.append(text_chunk)
                sys.stdout.write(text_chunk)
                sys.stdout.flush()
                if chunk.get('done', False):
                    print("\n" + "-" * 50)
                    print(f"{Fore.GREEN}✅ Генерация завершена.")
        full_new_text = "".join(current_response).strip()
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                old_text = f.read().strip()
            show_diff(old_text, full_new_text)
        else:
            print(f"{Fore.YELLOW}\nℹ️ Это первый запуск. Ответ сохранен в кэш для будущих сравнений.")
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            f.write(full_new_text)
    except requests.exceptions.RequestException as e:
        print(f"\n{Fore.RED}❌ Ошибка сети: {e}")

if __name__ == "__main__":
    run_prompt("config.yaml", "input.txt")

