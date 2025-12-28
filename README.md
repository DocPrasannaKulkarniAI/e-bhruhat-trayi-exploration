# 📜 e-Bhruhat Trayi Exploration by PraKul

**Advanced AI-assisted exploration of the three major classical texts of Āyurveda**

> *"यत्र विद्या तत्र मुक्तिः"* — Where there is knowledge, there is liberation.

---

## 🌟 Overview

**e-Bhruhat Trayi Exploration** is a comprehensive digital tool for exploring, searching, and analyzing the three foundational texts of Āyurveda (Bṛhat Trayī):

- 📕 **Charaka Saṃhitā** — The treatise on internal medicine
- 📗 **Suśruta Saṃhitā** — The treatise on surgery
- 📘 **Aṣṭāṅga Hṛdaya** — The heart of eight branches

This application enables researchers, students, practitioners, and scholars to efficiently navigate thousands of ślokas across these classical texts.

---

## ✨ Features

### 📖 Read Samhita
- Sequential reading with chapter navigation
- Quick jump to any śloka position
- Progress tracking with visual indicators
- Cross-references to similar content in other Samhitas
- 20 ślokas per page for comfortable reading

### 🔍 Search
- Global search across all three Samhitas
- **Total occurrence count** (e.g., "74 occurrences in 29 ślokas")
- Exact match vs. compound match classification
- Multi-column search (Devanagari, IAST, Roman, ASCII)
- Filter by Samhita
- Pagination for large result sets

### ⚖️ Compare Texts
- Side-by-side comparison across Samhitas
- Visual occurrence distribution
- Identify how concepts are discussed differently across texts

### 📑 Chapter Index
- Complete table of contents for all Samhitas
- Browse by Sthāna and Chapter
- Śloka counts per chapter
- One-click navigation

### 📊 Word Frequency Analysis
- Distribution analysis across the corpus
- Visual bar charts by Samhita
- Top chapters by frequency
- Research-oriented insights

### ⚙️ Customization
- 🌓 **Dark/Light mode** toggle
- 🔤 **Font size adjustment** (Small to Extra Large)
- 📱 **Mobile responsive** design

---

## 🚀 Live Demo


🔗 **[Launch Application](https://e-bhruhat-trayi-exploration-by-prakul.streamlit.app/)**



## 📁 Project Structure

```
e-bhruhat-trayi-exploration/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── all3_cleaned.xlsx         # Corpus data (Bṛhat Trayī)
├── README.md                 # This file

```

---

## 📋 Requirements

```
streamlit>=1.28.0
pandas>=2.0.0
openpyxl>=3.1.0
```

---

## 📊 Data Structure

The application expects an Excel file (`all3_cleaned.xlsx`) with the following columns:

| Column | Description |
|--------|-------------|
| `Sloka Text` | Original Sanskrit text in Devanagari |
| `IAST` | International Alphabet of Sanskrit Transliteration |
| `Roman` | Romanized transliteration |
| `ASCII` | ASCII-compatible transliteration |
| `File Name` | Source Samhita name |
| `Sthana` | Section/Sthāna name |
| `Chapter` | Chapter name/number |
| `Sloka_Number_Int` | Śloka number (integer) |

---

## 🔤 Transliteration Support

The application supports multiple transliteration schemes:

- **Devanagari** (Original script)
- **IAST** (International Alphabet of Sanskrit Transliteration)
- **ASCII** (Harvard-Kyoto style)
- **Roman** (Common romanization)

A comprehensive transliteration reference table is available in the Guide tab.

---

## 👨‍🏫 About the Author

**Prof. (Dr.) Prasanna Kulkarni**

Āyurveda Physician | Educator | Clinician | Data Scientist

This application represents a technological contribution to making classical Āyurvedic literature accessible for research, education, and clinical practice.

- 🔗 [LinkedIn](https://linkedin.com/in/drprasannakulkarni)
- 🌐 [Atharva AyurTech](https://atharvaayurtech.com)

---

## 🙏 Acknowledgments

- The ancient sages who compiled these invaluable texts
- The Āyurvedic community for preserving this knowledge
- [Streamlit](https://streamlit.io) for the amazing framework

---


<p align="center">
  <strong>Made with ❤️ for the Āyurvedic Community</strong>
</p>

<p align="center">
  <em>Version 20.1 | © 2025 Prof. (Dr.) Prasanna Kulkarni</em>
</p>
