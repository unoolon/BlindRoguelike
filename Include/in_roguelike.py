import random
import hashlib
import sys
import time

# Настройки мира
WIDTH, HEIGHT = 20, 12
WALL_DENSITY = 0.12
ENEMIES = 5
SEED = None  # Можно поставить число для детерминированности, например 42
LISTEN_RADIUS = 5  # радиус "прислушивания" (манхэттенов)

if SEED is not None:
    random.seed(SEED)

# Локализация (RU/EN)
LANG = 'ru'

TEXT = {
    'ru': {
        'lang_prompt': "Выберите язык / Select language:\n1) Английский\n2) Русский\nВаш выбор [1-2]: ",
        'menu_title': "=== Меню ===",
        'menu_start': "1) Начать игру",
        'menu_set_seed': "2) Установить seed мира (текущий: {shown_seed})",
        'menu_set_size': "3) Установить размер мира (текущий: {w} x {h})",
        'menu_exit': "4) Выход",
        'menu_prompt': "Выберите пункт [1-4]: ",
        'seed_random': "случайный",
        'seed_enter': "Введите seed (пусто — случайный): ",
        'seed_reset': "Seed сброшен: будет случайный мир.\n",
        'seed_set': "Seed установлен: {seed}\n",
        'size_w': "Ширина (минимум 10, максимум 120): ",
        'size_h': "Высота  (минимум 8,  максимум 60): ",
        'size_unchanged': "Размер не изменён.\n",
        'size_set': "Размер мира установлен: {w} x {h}\n",
        'size_invalid': "Некорректное число. Размер не изменён.\n",
        'exit': "Выход.",
        'unknown_menu': "Неизвестный пункт.\n",
        'enter_name': "Введите имя персонажа (пусто — Безымянный): ",
        'default_name': "Безымянный",
        'enter_backstory': "Короткая предыстория героя (можно оставить пустым): ",
        'hero_label': "Герой",
        'backstory_label': "Предыстория",
        'backstory_dash': "—",
        'intro1': "Невидимый рогалик. Двигайтесь WASD (или стрелками). Q — выход.",
        'intro2': "Ничего не отображается, кроме лога. Координаты включатся после находки компаса.",
        'intro3': "На карте можно найти: компас, броню и оружие.",
        'intro4': "Иногда встречаются ямы: наступите, чтобы попасть на другую локацию.",
        'pit_found': "  | Событие: Вы провалились в яму и попали на другую локацию!",
        'level_label': "Локация",
        'char_level': "Уровень героя",
        'xp_label': "опыта",
        'level_up': "  | Событие: {name} повышает уровень до {level}!",
        'intro5': "Герой получает опыт и повышает уровни по ходу игры.",
        'intro6': "На карте могут быть сундуки с лутом.",
        'found_chest': "  | Событие: Вы нашли сундук.",
        'opened_chest': "  | Событие: Вы открыли сундук и нашли: {items}.",
        'floor_transition': "  | Событие: Вы перешли на новый этаж подземелья: {floor}",
        'loot_names': {
            'potion_small': 'малое зелье лечения',
            'potion_large': 'большое зелье лечения',
            'gold_coins': 'золотые монеты',
            'ring_strength': 'кольцо силы',
            'boots_speed': 'сапоги скорости',
            'tree_seed': 'семечко дерева',
        },
        'plant_help': "'P' — посадить семечко рядом (тратит ход).",
        'plant_success': "  | Событие: Вы посадили семечко, выросло дерево.",
        'plant_fail_no_seed': "  | Действие: Нет семечка в инвентаре.",
        'plant_fail_no_space': "  | Действие: Рядом нет свободной клетки для дерева.",
        'extra_action': "Доп.действие: 'K' — прислушаться; 'I' — инвентарь (оба тратят ход).\n",
        'inventory_title': "Инвентарь:",
        'inventory_empty': "(пусто)",
        'inventory_key': "'I' — открыть инвентарь",
        'item_names': {'compass': 'компас', 'armor': 'броня', 'weapon': 'оружие'},
        'inv_added': "  | В инвентарь добавлено: {item}",
        'inv_shown': "Вы открыли инвентарь: ",
        'seed_label': "Seed мира",
        'size_label': "Размер мира",
        'turn_header': "[Ход {turn}]",
        'seed_in_header': " | seed: {seed}",
        'collide_death': "  | Событие: Вас настиг враг. Игра окончена.",
        'press_key_quit': "Вы вышли из игры.",
        'listen_result_prefix': "Вы прислушались: ",
        'listen_silent': "Вы прислушались: вокруг тихо.",
        'dir_n': "на севере",
        'dir_s': "на юге",
        'dir_e': "на востоке",
        'dir_w': "на западе",
        'dir_ne': "на северо-востоке",
        'dir_nw': "на северо-западе",
        'dir_se': "на юго-востоке",
        'dir_sw': "на юго-западе",
        'dir_near': "рядом",
        'nearest_in': ". Ближайший в {dist} кл.",
        'found_compass': "  | Событие: Вы нашли компас! Теперь координаты видны.",
        'found_armor': "  | Событие: Вы нашли броню. Вы чувствуете себя защищённее.",
        'found_weapon': "  | Событие: Вы нашли оружие. Оно внушает уверенность.",
        'moved_with_coords': "  -> Игрок переместился в {x},{y}",
        'moved_no_coords': "  -> Игрок переместился.",
        'bump_wall': "  | Событие: Стена. Движение отменено.",
        'unknown_action': "  | Действие: Пропуск/неизвестная команда.",
        'killed_at': "[Ход {turn}] Событие: {enemy} убил героя {name} на координатах {x},{y}. Игра окончена.",
        'killed': "[Ход {turn}] Событие: {enemy} убил героя {name}. Игра окончена.",
        'kb_exit': "\nВыход.",
        'time_label': "Время",
        'time_format': "{minutes:02d}:{seconds:02d}",
        'enemy_names': {'goblin': 'гоблин', 'slime': 'слизь', 'bat': 'летучая мышь', 'skeleton': 'скелет'},
    },
    'en': {
        'lang_prompt': "Select language / Выберите язык:\n1) English\n2) Русский\nYour choice [1-2]: ",
        'menu_title': "=== Menu ===",
        'menu_start': "1) Start game",
        'menu_set_seed': "2) Set world seed (current: {shown_seed})",
        'menu_set_size': "3) Set world size (current: {w} x {h})",
        'menu_exit': "4) Exit",
        'menu_prompt': "Choose [1-4]: ",
        'seed_random': "random",
        'seed_enter': "Enter seed (empty — random): ",
        'seed_reset': "Seed reset: world will be random.\n",
        'seed_set': "Seed set: {seed}\n",
        'size_w': "Width (min 10, max 120): ",
        'size_h': "Height (min 8, max 60): ",
        'size_unchanged': "Size unchanged.\n",
        'size_set': "World size set: {w} x {h}\n",
        'size_invalid': "Invalid number. Size unchanged.\n",
        'exit': "Exit.",
        'unknown_menu': "Unknown option.\n",
        'enter_name': "Enter character name (empty — Nameless): ",
        'default_name': "Nameless",
        'enter_backstory': "Short backstory (can be empty): ",
        'hero_label': "Hero",
        'backstory_label': "Backstory",
        'backstory_dash': "—",
        'intro1': "Invisible roguelike. Move with WASD (or arrows). Q — quit.",
        'intro2': "Nothing is displayed except the log. Coordinates appear after finding a compass.",
        'intro3': "You can find on the map: compass, armor and weapon.",
        'intro4': "Sometimes there are pits: step onto one to reach another area.",
        'pit_found': "  | Event: You fell into a pit and reached another location!",
        'level_label': "Level",
        'char_level': "Hero level",
        'xp_label': "XP",
        'level_up': "  | Event: {name} levels up to {level}!",
        'intro5': "The hero gains XP and levels up during the game.",
        'intro6': "There may be chests with loot on the map.",
        'found_chest': "  | Event: You found a chest.",
        'opened_chest': "  | Event: You opened the chest and found: {items}.",
        'floor_transition': "  | Event: You moved to a new dungeon floor: {floor}",
        'loot_names': {
            'potion_small': 'small healing potion',
            'potion_large': 'large healing potion',
            'gold_coins': 'gold coins',
            'ring_strength': 'ring of strength',
            'boots_speed': 'boots of speed',
            'tree_seed': 'tree seed',
        },
        'plant_help': "'P' — plant a seed nearby (costs a turn).",
        'plant_success': "  | Event: You planted a seed and a tree grew.",
        'plant_fail_no_seed': "  | Action: No seed in inventory.",
        'plant_fail_no_space': "  | Action: No free adjacent cell to plant a tree.",
        'extra_action': "Extra actions: 'K' — listen; 'I' — inventory (both cost a turn).\n",
        'inventory_title': "Inventory:",
        'inventory_empty': "(empty)",
        'inventory_key': "'I' — open inventory",
        'item_names': {'compass': 'compass', 'armor': 'armor', 'weapon': 'weapon'},
        'inv_added': "  | Added to inventory: {item}",
        'inv_shown': "You opened your inventory: ",
        'seed_label': "World seed",
        'size_label': "World size",
        'turn_header': "[Turn {turn}]",
        'seed_in_header': " | seed: {seed}",
        'collide_death': "  | Event: An enemy caught you. Game over.",
        'press_key_quit': "You quit the game.",
        'listen_result_prefix': "You listened: ",
        'listen_silent': "You listened: it is quiet around.",
        'dir_n': "to the north",
        'dir_s': "to the south",
        'dir_e': "to the east",
        'dir_w': "to the west",
        'dir_ne': "to the northeast",
        'dir_nw': "to the northwest",
        'dir_se': "to the southeast",
        'dir_sw': "to the southwest",
        'dir_near': "nearby",
        'nearest_in': ". Nearest at {dist} tiles.",
        'found_compass': "  | Event: You found a compass! Coordinates are now visible.",
        'found_armor': "  | Event: You found armor. You feel safer.",
        'found_weapon': "  | Event: You found a weapon. It inspires confidence.",
        'moved_with_coords': "  -> Player moved to {x},{y}",
        'moved_no_coords': "  -> Player moved.",
        'bump_wall': "  | Event: Wall. Movement cancelled.",
        'unknown_action': "  | Action: Skip/unknown command.",
        'killed_at': "[Turn {turn}] Event: {enemy} killed the hero {name} at {x},{y}. Game over.",
        'killed': "[Turn {turn}] Event: {enemy} killed the hero {name}. Game over.",
        'kb_exit': "\nExit.",
        'time_label': "Time",
        'time_format': "{minutes:02d}:{seconds:02d}",
        'enemy_names': {'goblin': 'goblin', 'slime': 'slime', 'bat': 'bat', 'skeleton': 'skeleton'},
    }
}

def t(key):
    return TEXT[LANG][key]

def format_game_time(start_time):
    """Форматирует время игры в формат MM:SS"""
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    return t('time_format').format(minutes=minutes, seconds=seconds)

def choose_language():
    global LANG
    try:
        choice = input(TEXT[LANG]['lang_prompt']).strip().lower()
    except EOFError:
        choice = ''
    if choice in ('1', 'en', 'e', 'eng', 'english'):
        LANG = 'en'
    elif choice in ('2', 'ru', 'r', 'rus', 'russian', 'рус', 'русский'):
        LANG = 'ru'
    else:
        # По умолчанию русский
        LANG = 'ru'

# ANSI-раскраска для консоли
ANSI = {'red': '\033[31m', 'reset': '\033[0m'}

def colorize(text, color='red'):
    start = ANSI.get(color, '')
    end = ANSI['reset'] if start else ''
    return f"{start}{text}{end}"

def menu_get_seed():
    current_seed = None
    current_w, current_h = WIDTH, HEIGHT
    while True:
        print(t('menu_title'))
        print(t('menu_start'))
        shown_seed = current_seed if current_seed is not None else t('seed_random')
        print(t('menu_set_seed').format(shown_seed=shown_seed))
        print(t('menu_set_size').format(w=current_w, h=current_h))
        print(t('menu_exit'))
        choice = input(t('menu_prompt')).strip()
        if choice == '1':
            return current_seed, current_w, current_h
        elif choice == '2':
            s = input(t('seed_enter')).strip()
            current_seed = None if s == '' else s
            if current_seed is None:
                print(t('seed_reset'))
            else:
                print(t('seed_set').format(seed=current_seed))
        elif choice == '3':
            try:
                w = input(t('size_w')).strip()
                h = input(t('size_h')).strip()
                if w == '' or h == '':
                    print(t('size_unchanged'))
                    continue
                w = int(w)
                h = int(h)
                w = max(10, min(120, w))
                h = max(8, min(60, h))
                current_w, current_h = w, h
                print(t('size_set').format(w=current_w, h=current_h))
            except ValueError:
                print(t('size_invalid'))
        elif choice == '4':
            print(t('exit'))
            sys.exit(0)
        else:
            print(t('unknown_menu'))

# Попытка использовать модули для чтения клавиш без Enter на Windows
USE_MSVCRT = False
USE_READLINE = False
try:
    import msvcrt
    USE_MSVCRT = True
except Exception:
    try:
        import termios, tty, select  # noqa
        USE_READLINE = True
    except Exception:
        pass

def get_key():
    if USE_MSVCRT:
        while True:
            ch = msvcrt.getch()
            if ch in (b'\xe0', b'\x00'):  # спец-клавиши (стрелки)
                ch2 = msvcrt.getch()
                arrows = {b'H': 'w', b'P': 's', b'K': 'a', b'M': 'd'}
                return arrows.get(ch2, '')
            try:
                c = ch.decode('utf-8').lower()
            except Exception:
                c = ''
            return c
    elif USE_READLINE:
        import sys, termios, tty, select  # noqa
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            r, _, _ = select.select([sys.stdin], [], [], None)
            if r:
                c = sys.stdin.read(1).lower()
                return c
            return ''
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    else:
        try:
            return input().strip().lower()[:1]
        except EOFError:
            return 'q'

# Генерация стен
def gen_walls(rng):
    walls = set()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if rng.random() < WALL_DENSITY:
                walls.add((x, y))
    # Делаем границу непроходимой
    for x in range(WIDTH):
        walls.add((x, 0))
        walls.add((x, HEIGHT - 1))
    for y in range(HEIGHT):
        walls.add((0, y))
        walls.add((WIDTH - 1, y))
    # Гарантируем проходимую рамку входа/старта
    for x in range(3):
        walls.discard((x, 0))
        walls.discard((x, 1))
    return walls

# Поиск свободной клетки
def random_free_cell(walls, forbidden=set(), rng=None):
    if rng is None:
        rng = random
    while True:
        p = (rng.randrange(WIDTH), rng.randrange(HEIGHT))
        if p not in walls and p not in forbidden:
            return p

def derive_seed(base_seed_str, tag):
    """Создаёт детерминированное целочисленное зерно из строки seed и тега."""
    s = f"{base_seed_str}::{tag}".encode('utf-8')
    h = hashlib.sha256(s).digest()
    return int.from_bytes(h[:8], 'big', signed=False)

def main():
    # Выбор языка в начале каждой игры
    choose_language()
    
    # Меню перед стартом игры
    seed_value, chosen_w, chosen_h = menu_get_seed()
    # Устанавливаем выбранный размер до генерации
    global WIDTH, HEIGHT
    WIDTH, HEIGHT = chosen_w, chosen_h
    # Если seed не выбран, генерируем случайный, чтобы можно было повторить мир
    if seed_value is None:
        seed_value = str(random.randrange(1<<63))

    # Инициализируем независимые ГСЧ для разных подсистем
    rng_world   = random.Random(derive_seed(seed_value, 'world'))
    rng_walls   = random.Random(derive_seed(seed_value, 'walls'))
    rng_items   = random.Random(derive_seed(seed_value, 'items'))
    rng_enemies = random.Random(derive_seed(seed_value, 'enemies'))
    rng_moves   = random.Random(derive_seed(seed_value, 'moves'))
    rng_pits    = random.Random(derive_seed(seed_value, 'pits'))

    # Ввод имени персонажа и его предыстории
    print(t('enter_name'), end='')
    player_name = input().strip()
    if player_name == '':
        player_name = t('default_name')
    print(t('enter_backstory'), end='')
    player_backstory = input().strip()
    
    # Засекаем время начала игры
    game_start_time = time.time()

    level_index = 1
    walls = gen_walls(rng_walls)
    player = random_free_cell(walls, rng=rng_world)
    # Инициализация монстров разных типов
    MONSTER_KINDS = ['goblin', 'slime', 'bat', 'skeleton']
    enemies = []  # список словарей: { 'kind': str, 'pos': (x,y), 'state': dict }
    enemy_positions = set()
    for _ in range(ENEMIES):
        pos = random_free_cell(walls, forbidden=enemy_positions | {player}, rng=rng_enemies)
        kind = MONSTER_KINDS[rng_enemies.randrange(len(MONSTER_KINDS))]
        state = {'skip': False} if kind in ['slime', 'skeleton'] else {}
        enemies.append({'kind': kind, 'pos': pos, 'state': state})
        enemy_positions.add(pos)

    # Компас появляется в случайной свободной клетке (не у игрока и не у врагов)
    compass = random_free_cell(walls, forbidden=enemy_positions | {player}, rng=rng_items)
    compass_found = False

    # Снаряжение: броня и оружие на разных свободных клетках
    armor = random_free_cell(walls, forbidden=enemy_positions | {player, compass}, rng=rng_items)
    weapon = random_free_cell(walls, forbidden=enemy_positions | {player, compass, armor}, rng=rng_items)
    armor_found = False
    weapon_found = False

    # Инвентарь
    inventory = []

    # Уровень персонажа и опыт
    player_level = 1
    player_xp = 0

    def xp_needed_for_next_level(level):
        # Простая шкала: 10, 20, 30, ...
        return level * 10

    def grant_xp(amount):
        nonlocal player_xp, player_level
        player_xp += amount
        # Повышение уровня при накоплении
        while player_xp >= xp_needed_for_next_level(player_level):
            player_xp -= xp_needed_for_next_level(player_level)
            player_level += 1
            print(t('level_up').format(name=player_name, level=player_level))

    # Яма (переход на новую локацию)
    pit = random_free_cell(walls, forbidden=enemy_positions | {player, compass, armor, weapon}, rng=rng_pits)

    # Сундуки с лутом
    LOOT_TABLE = ['potion_small', 'potion_large', 'gold_coins', 'ring_strength', 'boots_speed', 'tree_seed']
    rng_chests = random.Random(derive_seed(seed_value, 'chests'))
    chest_positions = []
    chests = {}
    # 1-3 сундука на локацию
    num_chests = rng_chests.randrange(1, 4)
    forbidden_for_chests = enemy_positions | {player, compass, armor, weapon, pit}
    for _ in range(num_chests):
        pos = random_free_cell(walls, forbidden=forbidden_for_chests, rng=rng_chests)
        forbidden_for_chests.add(pos)
        # 1-2 предмета в сундуке
        loot_count = 1 + rng_chests.randrange(2)
        loot = [LOOT_TABLE[rng_chests.randrange(len(LOOT_TABLE))] for __ in range(loot_count)]
        chests[pos] = loot

    deltas = {
        'w': (0, -1),
        's': (0, 1),
        'a': (-1, 0),
        'd': (1, 0),
        # альтернативные
        'ц': (0, -1), 'ы': (0, 1), 'ф': (-1, 0), 'в': (1, 0),  # если раскладка RU
    }

    turn = 0
    print(f"{t('hero_label')}: {player_name}")
    if player_backstory:
        print(f"{t('backstory_label')}: {player_backstory}")
    else:
        print(f"{t('backstory_label')}: {t('backstory_dash')}")
    print("")
    print(t('intro1'))
    print(t('intro2'))
    print(t('intro3'))
    print(t('intro4'))
    print(t('intro5'))
    print(t('intro6'))
    print(t('extra_action'))
    print(t('plant_help'))
    print(f"{t('seed_label')}: {seed_value}")
    print(f"{t('size_label')}: {WIDTH} x {HEIGHT}\n")

    while True:
        turn += 1
        header = t('turn_header').format(turn=turn)
        if compass_found:
            header = f"{header} Координаты игрока: {player[0]},{player[1]}"
        header = f"{header} | {t('level_label')}: {level_index}"
        header = f"{header} | {t('char_level')}: {player_level} ({player_xp} {t('xp_label')})"
        header = f"{header} | {t('time_label')}: {format_game_time(game_start_time)}"
        # На первом ходу показываем использованный seed, если он задан
        if turn == 1 and seed_value is not None:
            header = f"{header}{t('seed_in_header').format(seed=seed_value)}"
        print(header, end='')

        # Проверка столкновения (вдруг враг уже тут)
        if any(e['pos'] == player for e in enemies):
            print(colorize(t('collide_death')))
            return

        print("")  # перенос строки после координат/заголовка

        # Ввод команды
        key = get_key()
        if key == 'q':
            print(t('press_key_quit'))
            sys.exit(0)

        # Действие/движение игрока
        moved = False
        bump_wall = False
        listened = False
        listen_msg = None

        # Прислушаться (тратит ход)
        if key in ('k', 'л'):
            listened = True

            def dir_name(dx, dy):
                if dx == 0 and dy < 0: return t('dir_n')
                if dx == 0 and dy > 0: return t('dir_s')
                if dy == 0 and dx > 0: return t('dir_e')
                if dy == 0 and dx < 0: return t('dir_w')
                if dx > 0 and dy < 0: return t('dir_ne')
                if dx < 0 and dy < 0: return t('dir_nw')
                if dx > 0 and dy > 0: return t('dir_se')
                if dx < 0 and dy > 0: return t('dir_sw')
                return t('dir_near')

            counts = {}
            nearest = None
            for e in enemies:
                ex, ey = e['pos']
                dx = ex - player[0]
                dy = ey - player[1]
                dist = abs(dx) + abs(dy)  # манхэттен
                if dist <= LISTEN_RADIUS and dist > 0:
                    # нормализуем в 8 направлений по знакам
                    sx = 0 if dx == 0 else (1 if dx > 0 else -1)
                    sy = 0 if dy == 0 else (1 if dy > 0 else -1)
                    dkey = dir_name(sx, sy)
                    counts[dkey] = counts.get(dkey, 0) + 1
                    if nearest is None or dist < nearest:
                        nearest = dist

            if counts:
                parts = [f"{n} {d}" for d, n in counts.items()]
                info = "; ".join(parts)
                if nearest is not None:
                    info += t('nearest_in').format(dist=nearest)
                listen_msg = f"{t('listen_result_prefix')}{info}"
            else:
                listen_msg = t('listen_silent')

        # Движение
        elif key in deltas:
            dx, dy = deltas[key]
            nx, ny = player[0] + dx, player[1] + dy
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                if (nx, ny) not in walls:
                    player = (nx, ny)
                    moved = True
                else:
                    bump_wall = True
        # Открыть инвентарь (тратит ход)
        elif key in ('i', 'ш'):
            listened = True  # используем общий вывод лога для действий без движения
            items_to_show = inventory[:]
            if not items_to_show:
                listen_msg = f"{t('inventory_title')} {t('inventory_empty')}"
            else:
                display_names = [TEXT[LANG]['item_names'].get(it, it) for it in items_to_show]
                listen_msg = f"{t('inventory_title')} " + ", ".join(display_names)
        # Посадить семечко (тратит ход)
        elif key in ('p', 'з'):
            listened = True
            # Ищем семечко в инвентаре
            if 'tree_seed' not in inventory:
                listen_msg = t('plant_fail_no_seed')
            else:
                # пытаемся посадить в одну из соседних свободных клеток (4 направления)
                planted = False
                for dx, dy in [(0,-1),(0,1),(-1,0),(1,0)]:
                    tx, ty = player[0] + dx, player[1] + dy
                    if 0 <= tx < WIDTH and 0 <= ty < HEIGHT and (tx, ty) not in walls:
                        # сажаем дерево: превращаем клетку в стену
                        walls.add((tx, ty))
                        inventory.remove('tree_seed')
                        listen_msg = t('plant_success')
                        grant_xp(6)
                        planted = True
                        break
                if not planted:
                    listen_msg = t('plant_fail_no_space')

        # Подбор предметов (после действия/перемещения)
        if not compass_found and player == compass:
            compass_found = True
            compass = None
            print(t('found_compass'))
            inventory.append('compass')
            print(t('inv_added').format(item=TEXT[LANG]['item_names']['compass']))
            grant_xp(3)

        if not armor_found and player == armor:
            armor_found = True
            armor = None
            print(t('found_armor'))
            inventory.append('armor')
            print(t('inv_added').format(item=TEXT[LANG]['item_names']['armor']))
            grant_xp(5)

        if not weapon_found and player == weapon:
            weapon_found = True
            weapon = None
            print(t('found_weapon'))
            inventory.append('weapon')
            print(t('inv_added').format(item=TEXT[LANG]['item_names']['weapon']))
            grant_xp(7)

        # Открытие сундука
        if player in chests:
            loot_keys = chests.pop(player)
            print(t('found_chest'))
            # Добавляем лут в инвентарь и формируем строку для вывода
            display_names = []
            for lk in loot_keys:
                inventory.append(lk)
                display_names.append(TEXT[LANG]['loot_names'].get(lk, lk))
                grant_xp(4)
            print(t('opened_chest').format(items=", ".join(display_names)))

        # Провал в яму и переход на новую локацию
        if player == pit:
            print(t('pit_found'))
            level_index += 1
            # Обновляем время начала для нового уровня (время продолжает идти)
            # game_start_time остается тем же, чтобы время накапливалось
            # Перегенерация ресурсов уровня с новым тегом уровня
            level_tag = f"{level_index}"
            rng_walls.seed(derive_seed(seed_value, 'walls'+level_tag))
            rng_items.seed(derive_seed(seed_value, 'items'+level_tag))
            rng_enemies.seed(derive_seed(seed_value, 'enemies'+level_tag))
            rng_world.seed(derive_seed(seed_value, 'world'+level_tag))
            rng_moves.seed(derive_seed(seed_value, 'moves'+level_tag))
            rng_pits.seed(derive_seed(seed_value, 'pits'+level_tag))
            rng_chests.seed(derive_seed(seed_value, 'chests'+level_tag))

            walls = gen_walls(rng_walls)
            player = random_free_cell(walls, rng=rng_world)
            enemies = []
            enemy_positions = set()
            for _ in range(ENEMIES):
                pos = random_free_cell(walls, forbidden=enemy_positions | {player}, rng=rng_enemies)
                kind = MONSTER_KINDS[rng_enemies.randrange(len(MONSTER_KINDS))]
                state = {'skip': False} if kind in ['slime', 'skeleton'] else {}
                enemies.append({'kind': kind, 'pos': pos, 'state': state})
                enemy_positions.add(pos)

            # На новых уровнях предметы появляются снова, но найденные флаги сохраняем как находки инвентаря
            compass = random_free_cell(walls, forbidden=enemy_positions | {player}, rng=rng_items)
            armor = random_free_cell(walls, forbidden=enemy_positions | {player, compass}, rng=rng_items)
            weapon = random_free_cell(walls, forbidden=enemy_positions | {player, compass, armor}, rng=rng_items)
            # Сбросить флаги найденности только если предмета ещё нет в инвентаре
            compass_found = 'compass' in inventory
            armor_found = 'armor' in inventory
            weapon_found = 'weapon' in inventory

            pit = random_free_cell(walls, forbidden=enemy_positions | {player, compass, armor, weapon}, rng=rng_pits)

            # Сгенерировать сундуки на новой локации
            chest_positions = []
            chests = {}
            num_chests = rng_chests.randrange(1, 4)
            forbidden_for_chests = enemy_positions | {player, compass, armor, weapon, pit}
            for _ in range(num_chests):
                pos = random_free_cell(walls, forbidden=forbidden_for_chests, rng=rng_chests)
                forbidden_for_chests.add(pos)
                loot_count = 1 + rng_chests.randrange(2)
                loot = [LOOT_TABLE[rng_chests.randrange(len(LOOT_TABLE))] for __ in range(loot_count)]
                chests[pos] = loot

            # Сообщение о переходе на новый этаж и повышение уровня героя через опыт
            print(t('floor_transition').format(floor=level_index))
            needed_xp = xp_needed_for_next_level(player_level) - player_xp
            if needed_xp < 0:
                needed_xp = 0
            grant_xp(needed_xp)

        # Логи хода
        if listened:
            print(f"  | {listen_msg}")
        elif moved:
            if compass_found:
                print(t('moved_with_coords').format(x=player[0], y=player[1]))
            else:
                print(t('moved_no_coords'))
        elif bump_wall:
            print(t('bump_wall'))
        else:
            print(t('unknown_action'))

        # Ход врагов: разные типы поведения
        def step_enemy(enemy):
            kind = enemy['kind']
            x, y = enemy['pos']
            options = [(0,0), (1,0),(-1,0),(0,1),(0,-1)]
            if kind == 'goblin':
                # Жадно приближается по манхэттену
                best = (x, y)
                best_dist = abs(x - player[0]) + abs(y - player[1])
                rng_moves.shuffle(options)
                for dx, dy in options:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and (nx, ny) not in walls:
                        d = abs(nx - player[0]) + abs(ny - player[1])
                        if d < best_dist:
                            best_dist = d
                            best = (nx, ny)
                return best
            elif kind == 'slime':
                # Двигается через ход
                skip = enemy['state'].get('skip', False)
                enemy['state']['skip'] = not skip
                if skip:
                    return (x, y)
                rng_moves.shuffle(options)
                for dx, dy in options:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and (nx, ny) not in walls:
                        return (nx, ny)
                return (x, y)
            elif kind == 'skeleton':
                # Скелет движется медленно, но целенаправленно к игроку
                # Двигается только через ход, как слизь, но более предсказуемо
                skip = enemy['state'].get('skip', False)
                enemy['state']['skip'] = not skip
                if skip:
                    return (x, y)
                
                # Скелет движется к игроку, но не так агрессивно как гоблин
                px, py = player[0], player[1]
                dx_to_player = px - x
                dy_to_player = py - y
                
                # Выбираем направление к игроку (приоритет горизонтальному движению)
                if abs(dx_to_player) > abs(dy_to_player):
                    # Движемся по горизонтали
                    if dx_to_player > 0:
                        move_options = [(1, 0), (0, 1), (0, -1), (0, 0)]
                    else:
                        move_options = [(-1, 0), (0, 1), (0, -1), (0, 0)]
                else:
                    # Движемся по вертикали
                    if dy_to_player > 0:
                        move_options = [(0, 1), (1, 0), (-1, 0), (0, 0)]
                    else:
                        move_options = [(0, -1), (1, 0), (-1, 0), (0, 0)]
                
                for dx, dy in move_options:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and (nx, ny) not in walls:
                        return (nx, ny)
                return (x, y)
            else:  # bat
                rng_moves.shuffle(options)
                for dx, dy in options:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and (nx, ny) not in walls:
                        return (nx, ny)
                return (x, y)

        new_enemies = []
        enemy_positions = set()
        for enemy in enemies:
            enemy['pos'] = step_enemy(enemy)
            new_enemies.append(enemy)
            enemy_positions.add(enemy['pos'])
        enemies = new_enemies

        # Проверка после хода врагов
        if any(e['pos'] == player for e in enemies):
            killer = next(e for e in enemies if e['pos'] == player)
            kind_name = TEXT[LANG]['enemy_names'].get(killer['kind'], killer['kind'])
            if compass_found:
                print(colorize(t('killed_at').format(turn=turn, enemy=kind_name, name=player_name, x=player[0], y=player[1])))
            else:
                print(colorize(t('killed').format(turn=turn, enemy=kind_name, name=player_name)))
            return

if __name__ == "__main__":
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print(TEXT[LANG]['kb_exit'])