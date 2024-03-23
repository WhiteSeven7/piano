import pygame
import sys
import os
from dataclasses import dataclass

@dataclass
class Block:
    rect: pygame.Rect
    name: pygame.Surface
    key: pygame.Surface
    black: bool
    colorful: bool = False
    time: int = 0

    def draw(self):
        surf = pygame.display.get_surface()
        name_rect = self.name.get_rect(midbottom=(self.rect.centerx, self.rect.bottom - 20))
        key_rect = self.key.get_rect(midbottom=(name_rect.centerx, name_rect.bottom - 40))
        if self.colorful:
            color = pygame.color.Color('#000000' if self.black else '#FFFFFF')
            color = color.lerp(
                '#00A2E8',
                (self.time - pygame.time.get_ticks()) / 5500
            )
        elif self.black:
            color = '#000000'
        else:
            color = '#FFFFFF'
        pygame.draw.rect(surf, color, self.rect)
        surf.blit(self.name, name_rect)
        surf.blit(self.key, key_rect)

    def set_colorful(self):
        self.colorful = True
        self.time = pygame.time.get_ticks() + 5500

    def update(self):
        tick = pygame.time.get_ticks()
        if self.time < tick:
            self.colorful = False


# 音符
class SoundSys:
    width = 38
    heiht = 300
    @staticmethod
    def get_sound(directory) -> dict[str, pygame.mixer.Sound]:
        sounds_dict = {}
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if not os.path.isfile(file_path):
                continue
            filename, _ = os.path.splitext(file)
            try:
                py_sound = pygame.mixer.Sound(file_path)
            except pygame.error:
                continue
            sounds_dict[filename] = py_sound
        return sounds_dict
    
    @staticmethod
    def get_sharp(sound_name) -> str:
        a, b = sound_name
        return a + '#' + b
    
    @staticmethod
    def remove_sharp(sound_name) -> str:
        a, _ , b = sound_name
        return a + b
    
    def __init__(self) -> None:
        self.font = pygame.font.Font(None, 25)
        self.sounds = self.get_sound('sound')
        self.key_map = {
            pygame.K_1: 'C2',
            pygame.K_2: 'D2',
            pygame.K_3: 'E2',
            pygame.K_4: 'F2',
            pygame.K_5: 'G2',
            pygame.K_6: 'A2',
            pygame.K_7: 'B2',
            pygame.K_8: 'C3',
            pygame.K_9: 'D3',
            pygame.K_0: 'E3',
            pygame.K_q: 'F3',
            pygame.K_w: 'G3',
            pygame.K_e: 'A3',
            pygame.K_r: 'B3',
            pygame.K_t: 'C4',
            pygame.K_y: 'D4',
            pygame.K_u: 'E4',
            pygame.K_i: 'F4',
            pygame.K_o: 'G4',
            pygame.K_p: 'A4',
            pygame.K_a: 'B4',
            pygame.K_s: 'C5',
            pygame.K_d: 'D5',
            pygame.K_f: 'E5',
            pygame.K_g: 'F5',
            pygame.K_h: 'G5',
            pygame.K_j: 'A5',
            pygame.K_k: 'B5',
            pygame.K_l: 'C6',
            pygame.K_z: 'D6',
            pygame.K_x: 'E6',
            pygame.K_c: 'F6',
            pygame.K_v: 'G6',
            pygame.K_b: 'A6',
            pygame.K_n: 'B6',
            pygame.K_m: 'C7'
        }

        self._get_blocks()

    def play_by_name(self, sound_name: str):
        if sound_name not in self.sounds:
            sound_name = self.remove_sharp(sound_name)
        print(sound_name)
        self.sounds[sound_name].play()
        self.name_blocks[sound_name].set_colorful()

    def play(self, key, shift):
        if key not in self.key_map:
            return
        if shift:
            self.play_by_name(self.get_sharp(self.key_map[key]))
        else:
            self.play_by_name(self.key_map[key])

    def draw(self):
        for block in self.name_blocks.values():
            block.draw()

    def get_size(self):
        return self.width * len(self.key_map), self.heiht
    
    def _get_blocks(self):
        # name_map = {v: k for k, v in self.key_map.items()}
        name_c = {
            'C2': '1',
            'D2': '2',
            'E2': '3',
            'F2': '4',
            'G2': '5',
            'A2': '6',
            'B2': '7',
            'C3': '8',
            'D3': '9',
            'E3': '0',
            'F3': 'q',
            'G3': 'w',
            'A3': 'e',
            'B3': 'r',
            'C4': 't',
            'D4': 'y',
            'E4': 'u',
            'F4': 'i',
            'G4': 'o',
            'A4': 'p',
            'B4': 'a',
            'C5': 's',
            'D5': 'd',
            'E5': 'f',
            'F5': 'g',
            'G5': 'h',
            'A5': 'j',
            'B5': 'k',
            'C6': 'l',
            'D6': 'z',
            'E6': 'x',
            'F6': 'c',
            'G6': 'v',
            'A6': 'b',
            'B6': 'n',
            'C7': 'm',
            'C#2': '!',
            'D#2': '@',
            'F#2': '$',
            'G#2': '%',
            'A#2': '^',
            'C#3': '*',
            'D#3': '(',
            'F#3': 'Q',
            'G#3': 'W',
            'A#3': 'E',
            'C#4': 'T',
            'D#4': 'Y',
            'F#4': 'I',
            'G#4': 'O',
            'A#4': 'P',
            'C#5': 'S',
            'D#5': 'D',
            'F#5': 'G',
            'G#5': 'H',
            'A#5': 'J',
            'C#6': 'L',
            'D#6': 'Z',
            'F#6': 'C',
            'G#6': 'V',
            'A#6': 'B',
        }
        sorted_sound_names = sorted(
            self.key_map.values(),
            key=lambda x: x[-1] + x[1]
        )
        self.name_blocks = {
            name: Block(
                pygame.rect.Rect(i * self.width, 0, self.width ,self.heiht),
                self.font.render(name, True, '#000000'),
                self.font.render(name_c[name], True, '#000000'),
                False
            )   
            for i, name in enumerate(sorted_sound_names)
        }

        black_blocks = {}
        for name in self.name_blocks:
            n_name = self.get_sharp(name)
            if n_name in self.sounds:
                rect = self.name_blocks[name].rect.move(self.width / 2, 0)
                rect.height = rect.height * 2 / 3
                black_blocks[n_name] = Block(
                    rect,
                    self.font.render(n_name, True, '#DDDDDD'),
                    self.font.render(name_c[n_name], True, '#DDDDDD'),
                    True
                )
        self.name_blocks.update(black_blocks)

    def update(self):
        for block in self.name_blocks.values():
            block.update()

# 游戏
class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        self.sound_sys = SoundSys()
        self.surface = pygame.display.set_mode(self.sound_sys.get_size())
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("电子钢琴")

    def control(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get(pygame.KEYDOWN):
            self.sound_sys.play(
                event.key,
                keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
            )


    def update(self):
        self.control()
        self.sound_sys.update()
        self.sound_sys.draw()
    

    def run(self):
        while True:
            if pygame.event.get(pygame.QUIT):
                pygame.quit()
                sys.exit()
            self.surface.fill('#333333')
            self.update()
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game()
    game.run()
