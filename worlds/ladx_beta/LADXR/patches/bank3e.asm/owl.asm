HandleOverworldOwlStatue:
    ; overworld owls we
    call GetRoomStatusAddressInHL
    ld   a, [hl]
    and  $20
    ret  nz
    ld   a, [hl]
    or   $20
    ld   [hl], a

    ldh  a, [$FFF6]
    add  $02
    ldh  [$FFF6], a
    call GiveItemAndMessageForRoomMultiworld
    ldh  a, [$FFF6]
    sub  $02
    ldh  [$FFF6], a


HandleOwlStatue:
    call GetRoomStatusAddressInHL
    ld   a, [hl]
    and  $20
    ret  nz
    ld   a, [hl]
    or   $20
    ld   [hl], a

    ; manipulate room address on dungeon owls to fit into table
    ; sub 0x100 and then flip bits 0 and 6 of the low byte
    ld   hl, $7700 ; sub 0x100
    call OffsetPointerByRoomNumber
    ; flip bits 0 and 6
    ld   a, l
    xor  $41
    ld   l, a
    ld   a, [hl]
    ldh  [$FFF1], a
    call ItemMessageMultiworldOwl
    call GiveItemFromChestMultiworldOwl
    ret



GetRoomStatusAddressInHL:
    ld   a, [$DBA5] ; isIndoor
    ld   d, a
    ld   hl, $D800
    ldh  a, [$FFF6]   ; room nr
    ld   e, a
    ldh  a, [$FFF7]   ; map nr
    cp   $FF
    jr   nz, .notColorDungeon

    ld   d, $00
    ld   hl, $DDE0
    jr   .notIndoorB

.notColorDungeon:
    cp   $1A
    jr   nc, .notIndoorB

    cp   $06
    jr   c, .notIndoorB

    inc  d

.notIndoorB:
    add  hl, de
    ret


RenderOwlStatueItem:
    ldh  a, [$FFF6] ; map room
    cp $B2
    jr nz, .NotYipYip
    ; Add 2 to room to set room pointer to an empty room for trade items
    add a, 2
    ldh [$FFF6], a
    call RenderItemForRoom
    ldh  a, [$FFF6] ; map room
    ; ...and undo it
    sub a, 2
    ldh [$FFF6], a
    ret
.NotYipYip:
    call RenderItemForRoom
    ret
