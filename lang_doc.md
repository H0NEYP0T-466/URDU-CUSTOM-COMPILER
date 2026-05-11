# Urdu Custom Programming Language (Documentation)

Assalam o Alaikum! Urdu Custom Programming Language ek simple, Roman-Urdu based language hai jo beginners aur Urdu speakers ke liye programming seekhna asaan banati hai. Yeh language ek complete pipeline (Lexer, Parser, Semantic Analyzer, IR, Optimizer, CodeGen, aur Interpreter) par mushtamil hai.

---

## 1. Keywords (Zaruri Alfaz)

Language mein mandarja zail keywords use hote hain:

| Keyword | Matlab (Urdu) | Description |
| :--- | :--- | :--- |
| `rakho` | رکھو | Variable declare ya assign karne ke liye. |
| `dikhao` | دکھاؤ | Screen par output dikhane (Print) ke liye. |
| `agar` | اگر | Condition check karne ke liye (If). |
| `warna` | ورنہ | Agar condition ghalat ho toh (Else). |
| `jabtak` | جب تک | Loop chalane ke liye (While Loop). |
| `khatam` | ختم | Block (if/while/function) ko end karne ke liye. |
| `functionbnao` | فنکشن بناؤ | Naya function define karne ke liye. |
| `wapisbejo` | واپس بھیجو | Function se value return karne ke liye. |
| `sahi` | صحیح | Boolean True value. |
| `ghalat` | غلط | Boolean False value. |
| `aur` | اور | Logical AND operator. |
| `ya` | یا | Logical OR operator. |

---

## 2. Variables aur Data Types

Variables banane ke liye `rakho` keyword istemal hota hai.

### Data Types:
1. **Numbers**: Integers (e.g., `10`) aur Floats (e.g., `10.5`).
2. **Strings**: Double quotes mein text (e.g., `"Assalam o Alaikum"`).
3. **Booleans**: `sahi` ya `ghalat`.
4. **Arrays (Lists)**: Square brackets mein multiple values (e.g., `[1, 2, 3]`).

### Misaal (Example):
```urdu
rakho umer = 25
rakho naam = "Fezan"
rakho student_hai = sahi
rakho marks = [80, 90, 85]
```

---

## 3. Operators

### Arithmetic Operators:
- `+` (Jama), `-` (Nafi), `*` (Zarab), `/` (Taqseem)

### Comparison Operators:
- `>` (Bara hai), `<` (Chota hai), `>=` (Bara ya barabar), `<=` (Chota ya barabar), `==` (Barabar hai), `!=` (Barabar nahi hai)

### Logical Operators:
- `aur` (AND), `ya` (OR)

---

## 4. Control Flow (Conditions aur Loops)

### If-Else (agar-warna):
```urdu
rakho x = 10
agar x > 5
    dikhao "X bara hai 5 se"
warna
    dikhao "X chota ya barabar hai 5 se"
khatam
```

### While Loop (jabtak):
```urdu
rakho ginti = 1
jabtak ginti <= 5
    dikhao ginti
    rakho ginti = ginti + 1
khatam
```

---

## 5. Functions

Functions ko `functionbnao` se define kiya jata hai aur call karne ke liye sirf naam istemal hota hai.

### Baghair Parameters ke:
```urdu
functionbnao salam()
    dikhao "Assalam o Alaikum!"
khatam

salam() # Call
```

### Parameters aur Return ke saath:
```urdu
functionbnao jama_karo(a, b)
    wapisbejo a + b
khatam

rakho result = jama_karo(10, 20)
dikhao result
```

---

## 6. Arrays (Lists)

Arrays banane aur unka data access karne ka tarika:

```urdu
rakho fruits = ["Aam", "Kela", "Seb"]

# Access karna
dikhao fruits[0] # Aam

# Value change karna
rakho fruits[1] = "Angoor"
dikhao fruits[1] # Angoor
```

---

## 7. Commments

Code mein comments dene ke liye `#` ka istemal karein.
```urdu
# Yeh ek comment hai
rakho x = 5 # Yeh bhi comment hai
```

---

## 8. Mukammal Program ki Misaal (Full Example)

Yeh program ek list ke numbers ka total karta hai:

```urdu
functionbnao total_karo(list, size)
    rakho sum = 0
    rakho i = 0
    jabtak i < size
        rakho sum = sum + list[i]
        rakho i = i + 1
    khatam
    wapisbejo sum
khatam

rakho numbers = [10, 20, 30, 40]
rakho result = total_karo(numbers, 4)

dikhao "List ka total hai: "
dikhao result
```

---
*Developed for Urdu Custom Compiler Project.*
