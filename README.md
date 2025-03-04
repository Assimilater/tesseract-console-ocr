# Tesseract Console OCR Training

## What It Is
Tesseract struggles with reading monospaced console text, especially **formatted output like tables**. This project provides **training data and automation scripts** to improve OCR accuracy for **PowerShell, Command Prompt, and other terminal environments**.

If you've ever tried extracting text from terminal screenshots and found Tesseract **unreliable**, this project is for you.

## Why It Exists
I needed to extract structured data from **PowerShell screenshots**, but OCR tools struggled to recognize clear, uniform text. Instead of manually fixing errors or **typing 50 15-digit numbers by hand**, I spent **12+ hours wrestling with Windows Terminal, PyAutoGUI, Pyperclip, and MSS to automate the process** and generate **high-quality training data**.

I'm shocked that nobody else seems to have done this before — so if you're dealing with the same problem, **hopefully my suffering saves you some time.** ❤️

## What You Need to Know for Modifying This Script
Training data was generated using **Windows 11 Terminal (PowerShell)**, but **`generator.py`** can be adapted for other environments.

### **Key Assumptions in the Current Implementation**
 - ✅ **Fullscreen on the left-most monitor** (multi-monitor setups need adjustments).
 - ✅ **Designed for PowerShell output** (modify `wrap_length` and `visible_lines` for other terminals).
 - ✅ **Auto-generates varied console output** via `generation_functions` (extend it to add new cases).

If you're using a different terminal setup, tweak `wrap_length` and `visible_lines` to ensure **the generated text fills the visible area properly**, ensuring you train OCR on accurate data.

### 📥 Download Training Data
The training dataset can be downloaded from **The Internet Archive**:
 - 👉 [training_202503](https://archive.org/details/training_202503)
