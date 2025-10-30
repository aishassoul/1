
import os, sys
from pathlib import Path


if sys.platform == "darwin":
    os.environ.setdefault("SDL_AUDIODRIVER", "coreaudio")

import pygame
from mutagen.mp3 import MP3


pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()


BASE_DIR = Path(__file__).resolve().parent
IMG_PLAY  = BASE_DIR / "play.png"
IMG_PAUSE = BASE_DIR / "pause.png"
IMG_NEXT  = BASE_DIR / "next.png"
IMG_PREV  = BASE_DIR / "back.png"
BG_IMAGE  = BASE_DIR / "rose.jpg"   


SONG_PATHS = sorted(
    list(BASE_DIR.rglob("*.mp3")) + list(BASE_DIR.rglob("*.MP3")),
    key=lambda p: p.name.lower()
)

if not SONG_PATHS:
    raise FileNotFoundError(
        "Не нашёл ни одного .mp3 в папке проекта. "
        "Положи хотя бы один mp3 рядом с player.py или в любую подпапку."
    )

current_idx = 0          
is_playing = False       
track_len = 0.0          

def current_path() -> Path:
    return SONG_PATHS[current_idx]

def _mp3_length(path: Path) -> float:
    try:
        return float(MP3(str(path)).info.length)
    except Exception:
        return 0.0

def play_song(start_sec: float = 0.0):
    """Загрузить и воспроизвести текущий трек с позиции start_sec."""
    global track_len, is_playing
    fpath = current_path()
    pygame.mixer.music.load(str(fpath))
    pygame.mixer.music.play(start=max(0.0, float(start_sec)))
    track_len = _mp3_length(fpath)
    is_playing = True

def stop_song():
    global is_playing
    pygame.mixer.music.stop()
    is_playing = False

def toggle_pause():
    global is_playing
    if is_playing:
        pygame.mixer.music.pause()
        is_playing = False
    else:
        pygame.mixer.music.unpause()
        is_playing = True

def next_song():
    global current_idx
    current_idx = (current_idx + 1) % len(SONG_PATHS)
    play_song(0.0)

def prev_song():
    global current_idx
    current_idx = (current_idx - 1) % len(SONG_PATHS)
    play_song(0.0)


WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player 🎵  (Space=Play/Pause, S=Stop, N/→, B/←)")
font = pygame.font.Font(None, 26)

def _load_image(path: Path, size):
    if path.exists():
        img = pygame.image.load(str(path))
        return pygame.transform.scale(img, size)
    return None

btn_play_img  = _load_image(IMG_PLAY,  (80, 80))
btn_pause_img = _load_image(IMG_PAUSE, (80, 80))
btn_next_img  = _load_image(IMG_NEXT,  (80, 80))
btn_prev_img  = _load_image(IMG_PREV,  (80, 80))

background = None
if BG_IMAGE.exists():
    background = pygame.image.load(str(BG_IMAGE))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

button_positions = {"prev": (100, 350), "play_pause": (210, 350), "next": (320, 350)}
BTN_W, BTN_H = 80, 80


PB_X, PB_Y, PB_W, PB_H = 50, 300, 400, 10
KNOB_R = 8
is_dragging = False
drag_x = PB_X


play_song(0.0)
clock = pygame.time.Clock()
running = True


while running:
    
    if not is_dragging and not pygame.mixer.music.get_busy() and is_playing:
        next_song()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:         
                toggle_pause()
            elif event.key in (pygame.K_n, pygame.K_RIGHT): 
                next_song()
            elif event.key in (pygame.K_b, pygame.K_LEFT):   
                prev_song()
            elif event.key == pygame.K_s:             
                stop_song()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            
            for name, (bx, by) in button_positions.items():
                if bx <= x <= bx + BTN_W and by <= y <= by + BTN_H:
                    if name == "play_pause":
                        toggle_pause()
                    elif name == "next":
                        next_song()
                    elif name == "prev":
                        prev_song()
          
            if PB_X <= x <= PB_X + PB_W and PB_Y - 10 <= y <= PB_Y + PB_H + 10:
                is_dragging = True
                drag_x = x

        elif event.type == pygame.MOUSEMOTION and is_dragging:
            drag_x = max(PB_X, min(PB_X + PB_W, event.pos[0]))

        elif event.type == pygame.MOUSEBUTTONUP:
            if is_dragging:
                frac = (drag_x - PB_X) / PB_W
                new_t = max(0.0, min(track_len - 0.01, frac * track_len)) if track_len > 0 else 0.0
                pygame.mixer.music.play(start=float(new_t))
                is_playing = True
            is_dragging = False

   
    screen.fill((30, 30, 30))
    if background:
        screen.blit(background, (0, 0))

    def _blit_btn(img, pos, label):
        if img is not None:
            screen.blit(img, pos)
        else:
            
            pygame.draw.rect(screen, (50, 50, 50), (*pos, BTN_W, BTN_H), border_radius=12)
            t = font.render(label, True, (255, 255, 255))
            screen.blit(t, (pos[0] + (BTN_W - t.get_width()) // 2, pos[1] + (BTN_H - t.get_height()) // 2))

    _blit_btn(btn_prev_img,  button_positions["prev"],  "Prev")
    _blit_btn(btn_next_img,  button_positions["next"],  "Next")
    _blit_btn(btn_pause_img if is_playing else btn_play_img, button_positions["play_pause"], "Play")

    raw_ms = pygame.mixer.music.get_pos()
    cur_t = 0.0 if raw_ms < 0 else raw_ms / 1000.0
    if not is_dragging:
        frac = 0.0 if track_len <= 0 else min(cur_t / track_len, 1.0)
        knob_x = PB_X + int(frac * PB_W)
    else:
        knob_x = drag_x

    pygame.draw.rect(screen, (180, 180, 180), (PB_X, PB_Y, PB_W, PB_H))
    pygame.draw.circle(screen, (255, 255, 255), (knob_x, PB_Y + PB_H // 2), KNOB_R)

    def _fmt(t):
        t = max(0, int(t))
        return f"{t//60}:{t%60:02d}"

    screen.blit(font.render(f"{_fmt(cur_t)} / {_fmt(track_len)}", True, (255, 255, 255)),
                (WIDTH // 2 - 40, PB_Y - 25))

    name_surf = font.render(current_path().stem, True, (255, 255, 255))
    screen.blit(name_surf, (WIDTH // 2 - name_surf.get_width() // 2, 450))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
