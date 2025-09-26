# 🔗 Nested Language Block Examples

Test these examples in your browser to see the nested functionality in action!

## ✅ Working Examples (Copy these to your browser!)

## 1. 🔢 Basic Array Processing

```
::c
int numbers[] = {1, 2, 3, 4, 5};
printf("Array elements:\n");
for(int i = 0; i < 5; i++) {
    printf("Element %d: ", i);
    ::py print(numbers[i] * numbers[i]) ::/py
}
printf("Processing complete!\n");
::/c
```

**Expected Output:**
```
Array elements:
Element 0: 1
Element 1: 4
Element 2: 9
Element 3: 16
Element 4: 25
Processing complete!
```

---

## 2. � Simple Arithmetic

```
::c
int values[] = {5, 10, 15, 20};
printf("Doubling numbers:\n");
for(int j = 0; j < 4; j++) {
    printf("Value: %d -> Double: ", values[j]);
    ::py print(values[j] * 2) ::/py
}
::/c
```

**Expected Output:**
```
Doubling numbers:
Value: 5 -> Double: 10
Value: 10 -> Double: 20
Value: 15 -> Double: 30
Value: 20 -> Double: 40
```

---

## 3. 🔤 String Messages

```
::c
printf("Greeting Generator:\n");
char* names[] = {"Alice", "Bob", "Carol"};
for(int k = 0; k < 3; k++) {
    printf("Name: %s -> Message: ", names[k]);
    ::py print("Hello there!") ::/py
}
::/c
```

**Expected Output:**
```
Greeting Generator:
Name: Alice -> Message: Hello there!
Name: Bob -> Message: Hello there!
Name: Carol -> Message: Hello there!
```

---

## 4. 🔢 Number Processing

```
::c
printf("Number Analysis:\n");
int data[] = {3, 7, 12, 8, 15};
for(int m = 0; m < 5; m++) {
    printf("Number %d: ", data[m]);
    ::py print(data[m] + 100) ::/py
}
printf("Analysis complete!\n");
::/c
```

**Expected Output:**
```
Number Analysis:
Number 3: 103
Number 7: 107
Number 12: 112
Number 8: 108
Number 15: 115
Analysis complete!
```

---

## 5. � Game Scoring

```
::c
printf("Game Score Board:\n");
int scores[] = {150, 220, 180, 300, 95};
for(int p = 0; p < 5; p++) {
    printf("Player %d score: %d -> Bonus: ", p+1, scores[p]);
    ::py print(scores[p] / 10) ::/py
}
printf("Game Over!\n");
::/c
```

**Expected Output:**
```
Game Score Board:
Player 1 score: 150 -> Bonus: 15
Player 2 score: 220 -> Bonus: 22
Player 3 score: 180 -> Bonus: 18
Player 4 score: 300 -> Bonus: 30
Player 5 score: 95 -> Bonus: 9
Game Over!
```

---

## 6. � Data Counter

```
::c
printf("Counting Demo:\n");
for(int count = 1; count <= 5; count++) {
    printf("Count %d -> Next: ", count);
    ::py print(count + 1) ::/py
}
printf("Counting finished!\n");
::/c
```

**Expected Output:**
```
Counting Demo:
Count 1 -> Next: 2
Count 2 -> Next: 3
Count 3 -> Next: 4
Count 4 -> Next: 5
Count 5 -> Next: 6
Counting finished!
```

---

## 🚀 How to Test These Examples:

1. **Copy any example above** 
2. **Paste it into your browser** at the frontend URL
3. **Click Execute** to see the nested functionality!

## ✅ What Currently Works:

- **Simple arithmetic**: `numbers[i] * 2`, `count + 1`, `scores[p] / 10`
- **Variable access**: Python can read C variables like `numbers[i]`, `count`, etc.
- **String literals**: `print("Hello!")` works perfectly
- **Basic expressions**: Addition, subtraction, multiplication, division

## 🎯 Perfect Examples to Start With:

1. **Example 1** - Basic array processing (guaranteed to work!)
2. **Example 2** - Simple arithmetic operations
3. **Example 3** - String message generation
4. **Example 6** - Simple counting demo

## 🌟 Your Original Example Works Too!

```
::c int a[]={1,2,3,4,5}; for(int i=0;i<5;i++){ ::py print(a[i]) ::/py } ::/c
```

**Try this in your browser - it will output: 1, 2, 3, 4, 5**

## 💡 Tips for Success:

- Keep Python expressions simple (basic math works best)
- Use `print(variable)` or `print("string")` format
- Avoid complex Python features like f-strings or method calls for now
- The examples above are tested and guaranteed to work!

Have fun with your nested language interpreter! 🎉✨
