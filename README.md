
# TikTok SessionID Checker

A simple Python script to check the validity of TikTok `sessionid` tokens. It reads session IDs from a file, verifies their status, and categorizes them into valid, invalid, or possibly banned.

## 🔍 Features

- Loads `sessionid`s from file (`email:password:sessionid` format).
- Validates session tokens by simulating a TikTok info.
- Automatically separates results:
  - ✅ `valids.txt`
  - ❌ `bads.txt`
  - 🚫 `might_be_banned.txt`
  - 🔄 `toCheckAgain[Error].txt`
- Proxyless.
- Fast and lightweight – no GUI, pure CLI.

## 📁 Input Format

Each line in `sessionids.txt` should look like:

```
email@example.com:password123:sessionid
```

## ⚙️ Requirements

- Python 3.x
- `httpx`
- `colorama`

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🚀 How to Use

1. Put your combo list in `sessionids.txt`.
2. Run the script:

```bash
python main.py
```

3. Results will be saved to:

```
valids.txt
bads.txt
might_be_banned.txt
toCheckAgain[Error].txt
```

## 📝 License

This project is licensed under the MIT License. Feel free to use and modify it.

---

Made with ❤️ by @oxno1
