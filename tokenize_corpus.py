import tiktoken
import numpy as np
import time
import threading

def print_with_time(message, start_time, stop_event):
    while not stop_event.is_set():
        elapsed_time = time.time() - start_time
        print(f"\r{message} (Elapsed time: {elapsed_time:.2f} seconds)", end="")
        time.sleep(0.1)
    elapsed_time = time.time() - start_time
    print(f"\r{message} (Elapsed time: {elapsed_time:.2f} seconds) Done")

def run_task(task_func, message):
    start_time = time.time()
    stop_event = threading.Event()
    timer_thread = threading.Thread(target=print_with_time, args=(message, start_time, stop_event))
    timer_thread.start()
    task_func()
    stop_event.set()
    timer_thread.join()

def load_tokenizer():
    global tokenizer
    tokenizer = tiktoken.get_encoding("gpt2")

def read_corpus_file():
    global text
    with open("/media/razgarize/Western Digital SATA 2TB/codeparrot-clean/Extracted files/merged_dataset.txt", "r") as file:
        text = file.read()

def tokenize_text():
    global tokens
    tokens = tokenizer.encode(text, allowed_special="all")

def save_tokens():
    np.save("tokens.npy", tokens)

def split_tokens():
    global train_tokens, val_tokens
    train_tokens = tokens[: int(len(tokens) * 0.9)]
    val_tokens = tokens[int(len(tokens) * 0.9) :]

def save_train_tokens():
    np.save("train_tokens.npy", train_tokens)

def save_val_tokens():
    np.save("val_tokens.npy", val_tokens)

run_task(load_tokenizer, "Loading tokenizer...")
run_task(read_corpus_file, "Reading corpus file...")
run_task(tokenize_text, "Tokenizing text...")
run_task(save_tokens, "Saving tokens to 'tokens.npy'...")
run_task(split_tokens, "Splitting tokens into training and validation sets...")
run_task(save_train_tokens, "Saving training tokens to 'train_tokens.npy'...")
run_task(save_val_tokens, "Saving validation tokens to 'val_tokens.npy'...")

print("All tasks completed successfully.")
