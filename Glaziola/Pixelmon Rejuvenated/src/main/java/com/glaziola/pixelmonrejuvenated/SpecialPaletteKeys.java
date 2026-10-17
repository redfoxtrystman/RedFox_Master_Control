package com.glaziola.pixelmonrejuvenated;

import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

/** Generated from assigned palette feature keys, not from user-visible species names. */
public final class SpecialPaletteKeys {
    private SpecialPaletteKeys() {}
    public static final Set<String> ALL = Collections.unmodifiableSet(
        new HashSet<>(Arrays.asList(("alien|alter|apricot_saucy|apricot_stripes|apricot_tiger|apricot_zebra|archipelago|ashen|autumn|berry_caramel_swirl|berry_lemon_cream|berry_matcha_cream|berry_mint_cream|berry_rainbow_swirl|berry_ruby_cream|berry_ruby_swirl|berry_salted_cream|berry_vanilla_cream|black|black_forehead|black_mask|blocky|blue|blue_raindrops|blue_saucy|blue_stripes|brown|brown_stripes|brown_tiger|brown_zebra|calcium_carbonate|candy|calico_orange_gold|calico_orange_white|calico_orange_white_black|calico_white_orange|christmas|clover_caramel_swirl|clover_lemon_cream|clover_matcha_cream|clover_mint_cream|clover_rainbow_swirl|clover_ruby_cream|clover_ruby_swirl|clover_salted_cream|clover_vanilla_cream|clubs|continental|copper_sulfate|cosmetic|creator|crystal|cupric_chloride|cyan|dark|dark_blue|dark_green|dark_pink|dark_red|diamonds|drowned|duskball|elegant|elf|fancy|flower_caramel_swirl|flower_lemon_cream|flower_matcha_cream|flower_mint_cream|flower_rainbow_swirl|flower_ruby_cream|flower_ruby_swirl|flower_salted_cream|flower_vanilla_cream|forte_green|friendball|garden|gingerbread|golde|goldw|gray|gray_bubbles|gray_diamonds|gray_patches|green|grey|gsball|halloween|heavyball|high_plains|icy_snow|indigo|irish|jungle|karp|light_brown|light_pink|light_yellow|lightblue|lightgray|lime|lithium_chloride|love_caramel_swirl|love_lemon_cream|love_matcha_cream|love_mint_cream|love_rainbow_swirl|love_ruby_cream|love_ruby_swirl|love_salted_cream|love_vanilla_cream|loveball|magenta|magnesium_sulfide|main_circular|manganese_chloride|marine|martian|masterball|meadow|meta|modern|monsoon|moonball|moons|neon|ocean|olive|online|orange|orange_dapples|orange_forehead|orange_mask|orange_orca|orange_twotone|patrick|pink|pink_dapples|pink_orca|pink_twotone|poke_ball|pokeball|polar|potassium_chloride|pr_tangela|premierball|pumpkin|purple|purple_bubbles|purple_diamonds|purple_patches|rainbow|real|red|red_ringed|ribbon_caramel_swirl|ribbon_lemon_cream|ribbon_matcha_cream|ribbon_mint_cream|ribbon_rainbow_swirl|ribbon_ruby_cream|ribbon_ruby_swirl|ribbon_salted_cream|ribbon_vanilla_cream|river|roasted|sandstorm|savanna|secondary_circular|skelly|snow|sodium_carbonate|spirit|spring|star_caramel_swirl|star_lemon_cream|star_matcha_cream|star_mint_cream|star_rainbow_swirl|star_ruby_cream|star_ruby_swirl|star_salted_cream|star_vanilla_cream|starry|strawberry_caramel_swirl|strawberry_lemon_cream|strawberry_matcha_cream|strawberry_mint_cream|strawberry_rainbow_swirl|strawberry_ruby_cream|strawberry_ruby_swirl|strawberry_salted_cream|strawberry_vanilla_cream|strike|summer|sun|tundra|valencian|valentine|violet|violet_raindrops|violet_saucy|white|winter|witch|yellow|yellow_ringed|zombie").split("\\|")))
    );
    public static boolean isSpecial(String aspect) {
        return ALL.contains(aspect);
    }
}
