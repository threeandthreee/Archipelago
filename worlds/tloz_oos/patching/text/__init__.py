from ..z80asm.Assembler import GameboyAddress

# 🚫 means it's a command character
# ∅ means it's an unknown character
char_table = ("🚫\n🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫"
              "●♣♦♠♥⬆⬇⬅➡×“⌜⌟∅⢄◦"  # 0x1d looks like a dot, but centered? Unused anyway
              " !”#$%&'()*+,-./"
              "0123456789:;<=>?"
              "@ABCDEFGHIJKLMNO"
              "PQRSTUVWXYZ[~]^_"
              "`abcdefghijklmno"
              "pqrstuvwxyz{¥}▲■"
              "ÀÂÄÆÇÈÉÊËÎÏÑÖŒÙÛ"
              "Ü∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅"
              "àâäæçèéêëîïñöœùû"
              "ü∅∅∅∅∅∅∅🚫🚫🚫🚫∅♡")  # ♡ represents a smaller ♥

kanji_table = ("姫村下木東西南北地図出入口水氷池"
               "見門手力知恵勇気火金銀∅♪実上四"
               "季春夏秋冬右左大小本王国男女少年"
               "山人世中々剣花闇将軍真支配者鉄目"
               "詩死心節甲邪悪魔聖川結界生時炎🔒"
               "天空暗黒塔海仙△∅∅∅∅∅∅∅∅"  # This triangle has one more pixel up, and is used to represent the triforce
               "∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅"
               "∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅"
               "➕📖🥚🎎⚗🍲🏺🐟📢🍄🐦🛢📻∅∅∅")

text_colors = set("🟥🟩🟦⬜")

text_table_eng = GameboyAddress(0x1c, 0x5c00)
text_table_eng_address = text_table_eng.address_in_rom()

text_offset_1_table = GameboyAddress(0x3f, 0x4fe2)
text_offset_1_table_address = text_offset_1_table.address_in_rom()
text_offset_2_table = GameboyAddress(0x3f, 0x4ffa)
text_offset_2_table_address = text_offset_2_table.address_in_rom()

text_offset_split_index = 0x2c

text_addresses_limit = GameboyAddress(0x21, 0x4f71).address_in_rom()


def simple_hex(num: int) -> str:
    return hex(num)[2:].rjust(2, "0")


def normalize_text(text: str) -> str:
    normalized_text = ""
    current_line = 0
    words = text.split(" ")
    for word in words:
        word_length = sum(1 for c in word if c not in text_colors)
        if word_length > 16:
            word = f"{word[:15]}.{''.join([c for c in word[15:] if c in text_colors])}"
            pass
        if current_line != 0 and current_line + word_length < 16:
            normalized_text += " "
            current_line += 1
        elif current_line != 0:
            normalized_text += "\n"
            current_line = 0
        normalized_text += word
        current_line += len(word)
    return normalized_text
