# Presser, Clicker

A helper tool that supports holding and rapid clicking of keyboard and mouse keys.

## How to Use

1. Click the button next to `toggle key` to set the activation key for holding or clicking actions.
2. In the `Keys` section, you can add key operations:
    - Keyboard or Mouse:
        - For keyboard keys: select `keyboard` in the first column and set the key in the second column.
        - For mouse buttons: select `mouse` in the first column and set the button in the second column.
    - Hold or Click:
        - To hold: select `hold` in the third column.
        - To click: select `click` in the third column, and set the number of clicks and the interval in the fourth column (minimum value is 0.01).
3. After adding the keys, press `Start Listen` to start monitoring the toggle key. When active, the label next to `Start Listen` will show `toggled`; otherwise, it shows `untoggled`.
    > Once `Start Listen` is pressed, the toggle key and key actions cannot be modified until listening is stopped.

## Notes

- Hold actions are executed in the order they appear on the screen.
- Click actions run independently of each other. Even if their intervals are the same, the execution order is not guaranteed.

> Translated into English with the help of ChatGPT


## 中文版

一個可以長按、連點鍵盤及滑鼠的輔助工具

### 使用方法

1. 點擊 `toggle key` 旁的按鈕設定長按、連點的啟動鍵
2. 在 `Keys` 的區域可以新增按鍵操作
    - 鍵盤或滑鼠：
        - 對於鍵盤按鍵：第一個欄位選擇 `keyboard`，第二個欄位設定按鍵
        - 對於滑鼠按鍵：第一個欄位選擇 `mouse`，第二個欄位設定按鍵
    - 長按或連點：
        - 長按：第三個欄位選擇 `hold` 即可
        - 連點：第三個欄位選擇 `click`，第四個欄位設定點及間隔，最小值為 0.01
3. 新增完後按下 `Start Listen` 開始檢查啟動鍵是否按鍵，當啟動時 `Start Listen` 右邊顯示為 `toggled`，否則為 `untoggled`
    > 按下 Start Listen  後不可修改啟動鍵或新增、刪除按鍵操作，直到結束聆聽

### 注意事項

- 按鍵長按的順序依照畫面顯示的順序
- 按鍵連點皆獨立執行，即使時間間隔一樣也不保證照順序執行
