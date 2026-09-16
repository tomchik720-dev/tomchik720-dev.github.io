import tkinter as tk
import random
import math

# ============================================================
# ОКНО
# ============================================================

root = tk.Tk()
root.title("LOVE YOU")
root.attributes("-fullscreen", True)
root.configure(bg="#020002")

W = root.winfo_screenwidth()
H = root.winfo_screenheight()

canvas = tk.Canvas(
    root,
    width=W,
    height=H,
    bg="#020002",
    highlightthickness=0
)

canvas.pack(fill="both", expand=True)

# ESC — выход
root.bind("<Escape>", lambda e: root.destroy())


# ============================================================
# НАСТРОЙКИ
# ============================================================

CX = W / 2
CY = H / 2

# Размер сердца
# /28 — большое сердце, но полностью помещается на экране
SCALE = min(W, H) / 32

# Количество LOVE YOU
COUNT = 300


# ============================================================
# ЦВЕТА
# ============================================================

PINK = "#ff1493"
PINK_LIGHT = "#ff4fa3"
PINK_SOFT = "#ff75b8"


# ============================================================
# ФОРМА СЕРДЦА
# ============================================================

def heart_point(t):

    x = 16 * math.sin(t) ** 3

    y = (
        13 * math.cos(t)
        - 5 * math.cos(2 * t)
        - 2 * math.cos(3 * t)
        - math.cos(4 * t)
    )

    return (
        CX + x * SCALE,
        CY - y * SCALE
    )


# ============================================================
# СОЗДАЁМ ЦЕЛЕВЫЕ ТОЧКИ
# ============================================================

targets = []

for i in range(COUNT):

    t = (i / COUNT) * math.pi * 2

    x, y = heart_point(t)

    # Небольшой разброс
    x += random.uniform(-5, 5)
    y += random.uniform(-5, 5)

    targets.append((x, y))


# ============================================================
# ЧАСТИЦЫ
# ============================================================

particles = []

for i in range(COUNT):

    tx, ty = targets[i]

    # Начальная позиция далеко от сердца
    side = random.randint(0, 3)

    if side == 0:
        sx = random.randint(0, W)
        sy = random.randint(-H, 0)

    elif side == 1:
        sx = random.randint(W, W + 300)
        sy = random.randint(0, H)

    elif side == 2:
        sx = random.randint(0, W)
        sy = random.randint(H, H + 300)

    else:
        sx = random.randint(-300, 0)
        sy = random.randint(0, H)

    # Размер текста
    size = random.randint(10, 17)

    # Оттенок
    color = random.choice([
        PINK,
        PINK,
        PINK_LIGHT,
        PINK_SOFT
    ])

    particles.append({
        "sx": sx,
        "sy": sy,

        "tx": tx,
        "ty": ty,

        "size": size,
        "color": color,

        "delay": i * 0.018,

        "id": None
    })


# ============================================================
# ПЛАВНОЕ ДВИЖЕНИЕ
# ============================================================

def ease(t):

    return t * t * (3 - 2 * t)


# ============================================================
# ВРЕМЯ
# ============================================================

frame = 0


# ============================================================
# АНИМАЦИЯ
# ============================================================

def animate():

    global frame

    frame += 1

    current_time = frame / 60

    for p in particles:

        # ----------------------------------------------------
        # СЛОВО ЕЩЁ НЕ ПОЯВИЛОСЬ
        # ----------------------------------------------------

        if current_time < p["delay"]:
            continue

        # ----------------------------------------------------
        # СОЗДАЁМ LOVE YOU
        # ----------------------------------------------------

        if p["id"] is None:

            p["id"] = canvas.create_text(
                p["sx"],
                p["sy"],
                text="LOVE YOU",
                fill=p["color"],
                font=("Arial", p["size"], "bold"),
                anchor="center"
            )

        # ----------------------------------------------------
        # ПРОГРЕСС
        # ----------------------------------------------------

        progress = (
            current_time - p["delay"]
        ) / 2.5

        if progress < 0:
            progress = 0

        if progress > 1:
            progress = 1

        smooth = ease(progress)

        # ----------------------------------------------------
        # ПОЛЁТ К СЕРДЦУ
        # ----------------------------------------------------

        x = p["sx"] + (
            p["tx"] - p["sx"]
        ) * smooth

        y = p["sy"] + (
            p["ty"] - p["sy"]
        ) * smooth

        # ----------------------------------------------------
        # ЛЁГКОЕ КОЛЕБАНИЕ
        # ----------------------------------------------------

        if progress < 1:

            wave = math.sin(
                current_time * 5 +
                p["delay"] * 8
            ) * 4 * (1 - smooth)

            x += wave

        canvas.coords(
            p["id"],
            x,
            y
        )

    # Продолжаем анимацию
    root.after(16, animate)


# ============================================================
# ЗАПУСК
# ============================================================

animate()

root.mainloop()