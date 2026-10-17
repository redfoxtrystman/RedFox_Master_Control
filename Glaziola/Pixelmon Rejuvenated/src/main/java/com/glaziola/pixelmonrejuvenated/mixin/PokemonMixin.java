package com.glaziola.pixelmonrejuvenated.mixin;

import com.glaziola.pixelmonrejuvenated.SpecialPaletteKeys;

import com.cobblemon.mod.common.api.pokemon.feature.FlagSpeciesFeature;
import com.cobblemon.mod.common.api.pokemon.feature.SpeciesFeature;
import com.cobblemon.mod.common.pokemon.Pokemon;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Cobblemon 1.8.1 / NeoForge 1.21.1.
 * Special palettes win over shiny, including cases where shiny was assigned
 * BEFORE a palette was applied, such as commands, saved data and eggs.
 */
@Mixin(value = Pokemon.class, remap = false)
public abstract class PokemonMixin {

    @Inject(method = "setShiny", at = @At("HEAD"), cancellable = true, remap = false)
    private void pixelmonrejuvenated$rejectShinyOnSpecial(boolean shiny, CallbackInfo ci) {
        if (!shiny) return;
        Pokemon pokemon = (Pokemon)(Object)this;
        if (pokemon.isClient$common()) return;
        if (pixelmonrejuvenated$hasSpecial(pokemon)) ci.cancel();
    }

    @Inject(method = "updateAspects", at = @At("TAIL"), remap = false)
    private void pixelmonrejuvenated$clearShinyAfterFeatureChanges(CallbackInfo ci) {
        Pokemon pokemon = (Pokemon)(Object)this;
        if (pokemon.isClient$common()) return;
        if (pokemon.getShiny() && pixelmonrejuvenated$hasSpecial(pokemon)) {
            // setShiny(false) runs updateAspects again, but stops here on second pass.
            pokemon.setShiny(false);
        }
    }

    private static boolean pixelmonrejuvenated$hasSpecial(Pokemon pokemon) {
        // Computed aspects cover forced appearances and already-applied flags.
        if (pokemon.getAspects() != null) {
            for (String aspect : pokemon.getAspects()) {
                if (SpecialPaletteKeys.isSpecial(aspect)) return true;
            }
        }
        // Aspects may not yet be recalculated when setShiny is first called.
        if (pokemon.getForcedAspects() != null) {
            for (String aspect : pokemon.getForcedAspects()) {
                if (SpecialPaletteKeys.isSpecial(aspect)) return true;
            }
        }
        if (pokemon.getFeatures() != null) {
            for (SpeciesFeature feature : pokemon.getFeatures()) {
                if (feature instanceof FlagSpeciesFeature flag
                        && flag.getEnabled()
                        && SpecialPaletteKeys.isSpecial(flag.getName())) {
                    return true;
                }
            }
        }
        return false;
    }
}
